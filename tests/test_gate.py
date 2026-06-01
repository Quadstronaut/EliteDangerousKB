"""
Refusal-calibration tests — the anti-hallucination gate (spec §B).

Four scenarios:
  (a) empty retrieval result             → REFUSAL
  (b) non-empty but grounded=False       → REFUSAL
  (c) grounded + properly cited answer   → returns the answer
  (d) grounded + uncited answer × 2      → REFUSAL after one regen attempt
"""
import dataclasses
from unittest.mock import MagicMock, call, patch

import pytest

from copilot.models import Chunk, CmdrState, RetrievalResult


def _make_chunk(chunk_id: str = "abc12345ff0011aa") -> Chunk:
    return Chunk(
        chunk_id=chunk_id,
        text="Felicity Farseer requires Meta-Alloys.",
        kb_path="kb/engineers/felicity-farseer.md",
        heading_path="Felicity Farseer > Unlock",
        source_url="https://inara.cz/elite/engineer/1/",
        source_tier=1,
        source_count=3,
        verified=True,
        availability="live",
        changed_note=None,
        score=0.87,
    )


def _empty_result(query: str = "test") -> RetrievalResult:
    return RetrievalResult(query=query, chunks=[], max_score=0.0, grounded=False)


def _low_score_result(query: str = "test") -> RetrievalResult:
    chunk = _make_chunk()
    return RetrievalResult(
        query=query,
        chunks=[dataclasses.replace(chunk, score=0.30)],
        max_score=0.30,
        grounded=False,
    )


def _grounded_result(query: str = "test") -> RetrievalResult:
    chunk = _make_chunk()
    return RetrievalResult(
        query=query,
        chunks=[chunk],
        max_score=0.87,
        grounded=True,
    )


CITED_ANSWER = "You need Meta-Alloys to invite Farseer [abc12345ff0011aa]."
UNCITED_ANSWER = "You need Meta-Alloys to invite Farseer."

STATE = CmdrState(name="Duvrazh")


# ---------------------------------------------------------------------------
# (a) Empty retrieval → REFUSAL
# ---------------------------------------------------------------------------

def test_gate_empty_retrieval():
    with patch("copilot.retriever.retrieve", return_value=_empty_result()):
        from copilot.repl import answer, REFUSAL
        result = answer("How do I unlock Farseer?", STATE)
    assert result == REFUSAL


# ---------------------------------------------------------------------------
# (b) Non-empty but grounded=False → REFUSAL
# ---------------------------------------------------------------------------

def test_gate_below_tau():
    with patch("copilot.retriever.retrieve", return_value=_low_score_result()):
        from copilot.repl import answer, REFUSAL
        result = answer("best pizza topping", STATE)
    assert result == REFUSAL


# ---------------------------------------------------------------------------
# (c) Grounded + properly cited → returns the answer
# ---------------------------------------------------------------------------

def test_gate_grounded_cited_answer():
    def _mock_stream(messages, model=None):
        yield CITED_ANSWER

    with (
        patch("copilot.retriever.retrieve", return_value=_grounded_result()),
        patch("copilot.ollama_client.chat_stream", side_effect=_mock_stream),
    ):
        from copilot.repl import answer
        result = answer("How do I unlock Farseer?", STATE)

    assert result == CITED_ANSWER


# ---------------------------------------------------------------------------
# (d) Grounded + uncited answer twice → REFUSAL after one regen
# ---------------------------------------------------------------------------

def test_gate_regen_then_refusal():
    call_count = {"n": 0}

    def _mock_stream(messages, model=None):
        call_count["n"] += 1
        yield UNCITED_ANSWER  # never cited; always fails validation

    with (
        patch("copilot.retriever.retrieve", return_value=_grounded_result()),
        patch("copilot.ollama_client.chat_stream", side_effect=_mock_stream),
    ):
        from copilot.repl import answer, REFUSAL
        result = answer("How do I unlock Farseer?", STATE)

    assert result == REFUSAL
    # Must have called chat_stream exactly twice (original + one regen).
    assert call_count["n"] == 2
