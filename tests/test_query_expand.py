"""
Unit tests for copilot/query_expand.py and its wiring into retriever.retrieve().

All tests are deterministic and require no Ollama / network / filesystem.
"""

from __future__ import annotations

import dataclasses
import hashlib
from unittest.mock import patch, call

import numpy as np
import pytest

from copilot.query_expand import expand_query
from copilot.models import Chunk, RetrievalResult


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _unit_vec(seed_text: str) -> np.ndarray:
    seed = int(hashlib.sha256(seed_text.encode()).hexdigest()[:8], 16) % (2**31)
    rng = np.random.default_rng(seed)
    v = rng.standard_normal(1024).astype(np.float32)
    v /= np.linalg.norm(v)
    return v


def _make_chunk(chunk_id: str = "aabb1122ccdd3344", score: float = 0.90) -> Chunk:
    return Chunk(
        chunk_id=chunk_id,
        text="Some factual ED content.",
        kb_path="kb/test.md",
        heading_path="Test > Section",
        source_url=None,
        source_tier=1,
        source_count=1,
        verified=True,
        availability="live",
        changed_note=None,
        score=score,
    )


# ---------------------------------------------------------------------------
# expand_query — basic expansion behaviour
# ---------------------------------------------------------------------------

class TestExpandQuery:

    def test_fsd_abbrev_expands_to_full_form(self):
        result = expand_query("How do I increase my FSD range?")
        assert "Frame Shift Drive" in result

    def test_full_form_expands_to_abbrev(self):
        result = expand_query("How does the Frame Shift Drive work?")
        assert "FSD" in result

    def test_ax_abbrev_expands(self):
        result = expand_query("What is the best AX ship build?")
        assert "anti-xeno" in result or "Thargoid" in result

    def test_sco_expands(self):
        result = expand_query("How does SCO work?")
        assert "Supercruise Overcharge" in result

    def test_pp2_expands(self):
        result = expand_query("What changed in PP2?")
        assert "Powerplay" in result

    def test_g5_grade_expands(self):
        result = expand_query("I want G5 FSD engineering")
        assert "grade 5" in result

    def test_mats_expands(self):
        result = expand_query("Where do I farm G5 mats?")
        assert "materials" in result

    def test_trailblazers_expands(self):
        result = expand_query("How does Trailblazers work?")
        assert "colonisation" in result

    def test_colonisation_expands_to_trailblazers(self):
        result = expand_query("Tell me about colonisation")
        assert "Trailblazers" in result

    def test_farseer_expands(self):
        result = expand_query("How do I unlock Farseer?")
        assert "Felicity Farseer" in result

    def test_cmdr_expands(self):
        result = expand_query("Is this good for a CMDR like me?")
        assert "Commander" in result

    def test_unknown_query_unchanged(self):
        q = "What is the meaning of life?"
        result = expand_query(q)
        assert result == q

    def test_empty_query_unchanged(self):
        assert expand_query("") == ""
        assert expand_query("   ") == "   "

    def test_original_query_preserved_as_prefix(self):
        q = "What is an FSD?"
        result = expand_query(q)
        assert result.startswith(q)

    def test_case_insensitive_abbrev(self):
        """fsd, FSD, Fsd all expand."""
        assert "Frame Shift Drive" in expand_query("fsd engineering")
        assert "Frame Shift Drive" in expand_query("FSD engineering")
        assert "Frame Shift Drive" in expand_query("Fsd engineering")

    def test_no_duplicate_expansions(self):
        """Calling expand_query twice should not accumulate duplicates in output.

        The second call operates on already-expanded text; expansions already
        present in the string must be skipped to avoid repetition.
        """
        once = expand_query("FSD range")
        twice = expand_query(once)
        # Count occurrences of "Frame Shift Drive" in twice — should be 1
        assert twice.count("Frame Shift Drive") == 1

    def test_multiword_phrase_detected(self):
        """Multi-word entries like 'frame shift drive' → 'FSD' are matched."""
        result = expand_query("Explain the Frame Shift Drive module")
        assert "FSD" in result

    def test_fdl_expands(self):
        result = expand_query("What hardpoints does the FDL have?")
        assert "Fer-de-Lance" in result

    def test_cutter_expands(self):
        result = expand_query("Is the Cutter good for trading?")
        assert "Imperial Cutter" in result


# ---------------------------------------------------------------------------
# retrieve() wiring — expanded text embedded, original query in result
# ---------------------------------------------------------------------------

class TestRetrieveQueryExpand:
    """Verify that retriever.retrieve embeds the EXPANDED text but keeps
    RetrievalResult.query equal to the ORIGINAL query string."""

    def _patch_config(self, monkeypatch):
        cfg = {"retrieval": {"top_k": 5, "tau": 0.55}, "copilot": {}}
        monkeypatch.setattr("copilot.retriever._config", lambda: cfg)

    def test_expanded_text_is_embedded_not_original(self, monkeypatch):
        """retrieve('FSD range') must embed the expanded text, not the literal query."""
        embedded_texts: list[str] = []

        def _mock_embed(texts):
            embedded_texts.extend(texts)
            return np.stack([_unit_vec(t) for t in texts])

        monkeypatch.setattr("copilot.ollama_client.embed", _mock_embed)
        monkeypatch.setattr("copilot.index.search", lambda qv, top_k: [])
        self._patch_config(monkeypatch)

        from copilot import retriever
        retriever.retrieve("FSD range")

        assert embedded_texts, "embed() was never called"
        embedded = embedded_texts[0]
        # The expansion adds "Frame Shift Drive"; it must appear in what was embedded.
        assert "Frame Shift Drive" in embedded, (
            f"Expected 'Frame Shift Drive' in embedded text, got: {embedded!r}"
        )

    def test_result_query_is_original_not_expanded(self, monkeypatch):
        """RetrievalResult.query must be the original query, not the expanded one."""
        original_query = "FSD range tips"

        monkeypatch.setattr(
            "copilot.ollama_client.embed",
            lambda texts: np.stack([_unit_vec(t) for t in texts]),
        )
        monkeypatch.setattr("copilot.index.search", lambda qv, top_k: [])
        self._patch_config(monkeypatch)

        from copilot import retriever
        result = retriever.retrieve(original_query)

        assert result.query == original_query, (
            f"Expected result.query={original_query!r}, got {result.query!r}"
        )

    def test_unknown_query_still_works(self, monkeypatch):
        """A query with no ED terms embeds the original text unchanged."""
        query = "What is the meaning of life?"
        embedded_texts: list[str] = []

        def _mock_embed(texts):
            embedded_texts.extend(texts)
            return np.stack([_unit_vec(t) for t in texts])

        monkeypatch.setattr("copilot.ollama_client.embed", _mock_embed)
        monkeypatch.setattr("copilot.index.search", lambda qv, top_k: [])
        self._patch_config(monkeypatch)

        from copilot import retriever
        result = retriever.retrieve(query)

        assert embedded_texts[0] == query
        assert result.query == query

    def test_result_query_unchanged_with_expansion(self, monkeypatch):
        """Expanded text is used for embedding but result.query is always original."""
        chunk = _make_chunk()

        monkeypatch.setattr(
            "copilot.ollama_client.embed",
            lambda texts: np.stack([_unit_vec(t) for t in texts]),
        )
        monkeypatch.setattr(
            "copilot.index.search",
            lambda qv, top_k: [(chunk.chunk_id, 0.88)],
        )
        monkeypatch.setattr("copilot.index.chunk_by_id", lambda cid: chunk)
        self._patch_config(monkeypatch)

        original = "How does SCO work?"
        from copilot import retriever
        result = retriever.retrieve(original)

        assert result.query == original
        assert result.grounded is True
