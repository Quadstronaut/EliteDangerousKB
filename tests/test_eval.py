"""
Unit tests for copilot/eval.py — deterministic, no Ollama required.

Tests feed synthetic RetrievalResult objects to the metric functions and
assert recall@k / MRR / refusal rates are computed correctly.
"""

from __future__ import annotations

import dataclasses
from unittest.mock import patch

import pytest

from copilot.models import Chunk, RetrievalResult
from copilot.eval import retrieval_metrics, refusal_calibration, load_golden


# ---------------------------------------------------------------------------
# Fixtures and helpers
# ---------------------------------------------------------------------------

def _make_chunk(
    chunk_id: str = "aabbccdd11223344",
    kb_path: str = "kb/engineers/felicity-farseer.md",
    text: str = "Meta-Alloys unlock Felicity Farseer.",
    score: float = 0.90,
) -> Chunk:
    return Chunk(
        chunk_id=chunk_id,
        text=text,
        kb_path=kb_path,
        heading_path="Felicity Farseer > Unlock",
        source_url=None,
        source_tier=1,
        source_count=1,
        verified=True,
        availability="live",
        changed_note=None,
        score=score,
    )


def _grounded_result(question: str, chunks: list[Chunk]) -> RetrievalResult:
    return RetrievalResult(
        query=question,
        chunks=chunks,
        max_score=max(c.score for c in chunks) if chunks else 0.0,
        grounded=bool(chunks),
    )


def _empty_result(question: str) -> RetrievalResult:
    return RetrievalResult(query=question, chunks=[], max_score=0.0, grounded=False)


# Minimal golden question records for testing.
_GOLDEN_ON_TOPIC = [
    {
        "question": "How do I unlock Farseer?",
        "expect_kb_paths": ["kb/engineers/felicity-farseer.md"],
        "expect_chunk_substrings": ["Meta-Alloys"],
        "off_topic": False,
    }
]

_GOLDEN_OFF_TOPIC = [
    {
        "question": "What is the best pizza topping?",
        "expect_kb_paths": [],
        "expect_chunk_substrings": [],
        "off_topic": True,
    }
]

_GOLDEN_MIXED = _GOLDEN_ON_TOPIC + _GOLDEN_OFF_TOPIC


# ---------------------------------------------------------------------------
# retrieval_metrics — recall@k and MRR
# ---------------------------------------------------------------------------

class TestRetrievalMetrics:

    def test_perfect_retrieval_rank1(self):
        """Hit at rank 1 → recall@k=1.0, MRR=1.0."""
        chunk = _make_chunk()
        result = _grounded_result("How do I unlock Farseer?", [chunk])

        with patch("copilot.retriever.retrieve", return_value=result):
            metrics = retrieval_metrics(_GOLDEN_ON_TOPIC, top_k=5)

        assert metrics["recall_at_k"] == 1.0
        assert metrics["mrr"] == 1.0
        assert metrics["n_questions"] == 1
        assert metrics["n_hits"] == 1
        assert metrics["top_k"] == 5

    def test_complete_miss(self):
        """No chunks at all → recall@k=0.0, MRR=0.0."""
        result = _empty_result("How do I unlock Farseer?")

        with patch("copilot.retriever.retrieve", return_value=result):
            metrics = retrieval_metrics(_GOLDEN_ON_TOPIC, top_k=5)

        assert metrics["recall_at_k"] == 0.0
        assert metrics["mrr"] == 0.0
        assert metrics["n_hits"] == 0

    def test_hit_at_rank2_gives_mrr_half(self):
        """Hit at rank 2 → MRR = 0.5."""
        noise_chunk = _make_chunk(
            chunk_id="noise00000000000",
            kb_path="kb/other.md",
            text="Unrelated content here.",
            score=0.95,
        )
        hit_chunk = _make_chunk(score=0.85)  # rank 2

        result = _grounded_result("How do I unlock Farseer?", [noise_chunk, hit_chunk])

        with patch("copilot.retriever.retrieve", return_value=result):
            metrics = retrieval_metrics(_GOLDEN_ON_TOPIC, top_k=5)

        assert metrics["recall_at_k"] == 1.0
        assert abs(metrics["mrr"] - 0.5) < 1e-9

    def test_hit_via_chunk_substring(self):
        """Hit is detected via expect_chunk_substrings even if kb_path doesn't match."""
        golden = [
            {
                "question": "Unlock Farseer",
                "expect_kb_paths": ["kb/NONEXISTENT.md"],
                "expect_chunk_substrings": ["Meta-Alloys"],  # text match
                "off_topic": False,
            }
        ]
        chunk = _make_chunk(kb_path="kb/some/other.md", text="Meta-Alloys unlock Farseer.")
        result = _grounded_result("Unlock Farseer", [chunk])

        with patch("copilot.retriever.retrieve", return_value=result):
            metrics = retrieval_metrics(golden, top_k=5)

        assert metrics["recall_at_k"] == 1.0

    def test_empty_golden_returns_zeroes(self):
        """No on-topic questions → zeroes without calling retrieve."""
        with patch("copilot.retriever.retrieve", side_effect=AssertionError("should not call")):
            metrics = retrieval_metrics([], top_k=5)

        assert metrics["recall_at_k"] == 0.0
        assert metrics["mrr"] == 0.0
        assert metrics["n_questions"] == 0

    def test_off_topic_records_excluded_from_metrics(self):
        """Off-topic records must NOT be evaluated by retrieval_metrics."""
        # Only off-topic records; retrieve should never be called.
        with patch("copilot.retriever.retrieve", side_effect=AssertionError("should not call")):
            metrics = retrieval_metrics(_GOLDEN_OFF_TOPIC, top_k=5)

        assert metrics["n_questions"] == 0

    def test_multiple_questions_partial_hit(self):
        """3 questions, 2 hits at rank 1, 1 miss → recall=2/3, MRR=2/3."""
        golden = [
            {
                "question": f"question {i}",
                "expect_kb_paths": ["kb/engineers/felicity-farseer.md"],
                "expect_chunk_substrings": [],
                "off_topic": False,
            }
            for i in range(3)
        ]

        call_count = {"n": 0}

        def _mock_retrieve(question, *, top_k=5):
            i = call_count["n"]
            call_count["n"] += 1
            if i < 2:
                return _grounded_result(question, [_make_chunk()])
            return _empty_result(question)

        with patch("copilot.retriever.retrieve", side_effect=_mock_retrieve):
            metrics = retrieval_metrics(golden, top_k=5)

        assert metrics["n_questions"] == 3
        assert metrics["n_hits"] == 2
        assert abs(metrics["recall_at_k"] - 2 / 3) < 1e-9
        assert abs(metrics["mrr"] - 2 / 3) < 1e-9


# ---------------------------------------------------------------------------
# refusal_calibration — false_refusal_rate, false_answer_rate
# ---------------------------------------------------------------------------

class TestRefusalCalibration:

    def test_perfect_calibration(self):
        """On-topic grounded + off-topic not grounded → both rates 0.0."""
        on_result = _grounded_result("How do I unlock Farseer?", [_make_chunk()])
        off_result = _empty_result("Best pizza topping?")

        def _mock_retrieve(question, **kwargs):
            if "pizza" in question:
                return off_result
            return on_result

        with patch("copilot.retriever.retrieve", side_effect=_mock_retrieve):
            cal = refusal_calibration(_GOLDEN_MIXED)

        assert cal["false_refusal_rate"] == 0.0
        assert cal["false_answer_rate"] == 0.0
        assert cal["n_on_topic"] == 1
        assert cal["n_off_topic"] == 1
        assert cal["n_false_refusals"] == 0
        assert cal["n_false_answers"] == 0

    def test_false_refusal_on_topic_grounded_false(self):
        """On-topic query returns grounded=False → false_refusal_rate=1.0."""
        on_result = _empty_result("How do I unlock Farseer?")  # grounded=False

        with patch("copilot.retriever.retrieve", return_value=on_result):
            cal = refusal_calibration(_GOLDEN_ON_TOPIC)

        assert cal["false_refusal_rate"] == 1.0
        assert cal["n_false_refusals"] == 1

    def test_false_answer_off_topic_grounded_true(self):
        """Off-topic query returns grounded=True → false_answer_rate=1.0."""
        off_result = _grounded_result("Best pizza topping?", [_make_chunk()])

        with patch("copilot.retriever.retrieve", return_value=off_result):
            cal = refusal_calibration(_GOLDEN_OFF_TOPIC)

        assert cal["false_answer_rate"] == 1.0
        assert cal["n_false_answers"] == 1

    def test_empty_lists_return_zero_rates(self):
        """No on-topic or off-topic records → both rates 0.0."""
        with patch("copilot.retriever.retrieve", side_effect=AssertionError("should not call")):
            cal = refusal_calibration([])

        assert cal["false_refusal_rate"] == 0.0
        assert cal["false_answer_rate"] == 0.0

    def test_off_topic_grounded_counted_as_false_answer(self):
        """Explicit: off-topic grounded=True is counted in n_false_answers."""
        golden = [
            {
                "question": "off-topic question",
                "expect_kb_paths": [],
                "expect_chunk_substrings": [],
                "off_topic": True,
            }
        ]
        # grounded=True even though off-topic — this is a false answer
        result = _grounded_result("off-topic question", [_make_chunk()])

        with patch("copilot.retriever.retrieve", return_value=result):
            cal = refusal_calibration(golden)

        assert cal["n_false_answers"] == 1
        assert cal["false_answer_rate"] == 1.0


# ---------------------------------------------------------------------------
# load_golden
# ---------------------------------------------------------------------------

class TestLoadGolden:

    def test_load_golden_default_path(self):
        """load_golden() without args should load from eval/golden_questions.json."""
        records = load_golden()
        assert isinstance(records, list)
        assert len(records) > 0
        # Check required fields
        for rec in records:
            assert "question" in rec
            assert "expect_kb_paths" in rec
            assert "expect_chunk_substrings" in rec

    def test_load_golden_has_on_and_off_topic(self):
        """Golden set must contain both on-topic and off-topic records."""
        records = load_golden()
        on_topic = [r for r in records if not r.get("off_topic", False)]
        off_topic = [r for r in records if r.get("off_topic", False)]
        assert len(on_topic) >= 5, "Need at least 5 on-topic questions"
        assert len(off_topic) >= 3, "Need at least 3 off-topic questions for refusal calibration"

    def test_load_golden_explicit_path(self, tmp_path):
        """load_golden(path) loads from the given path."""
        data = [{"question": "test", "expect_kb_paths": [], "expect_chunk_substrings": [], "off_topic": False}]
        p = tmp_path / "test_golden.json"
        p.write_text(__import__("json").dumps(data), encoding="utf-8")
        records = load_golden(p)
        assert records == data
