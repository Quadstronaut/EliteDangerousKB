"""Tests for copilot/retriever.py — grounded vs. refused, filters, top_k."""
import hashlib
from pathlib import Path
from unittest.mock import MagicMock, patch

import dataclasses
import numpy as np
import pytest

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


def _make_chunk(chunk_id: str, verified: bool = True, score: float = 0.0) -> Chunk:
    return Chunk(
        chunk_id=chunk_id,
        text="Some factual ED content.",
        kb_path="kb/test.md",
        heading_path="Test > Section",
        source_url="https://example.com",
        source_tier=1,
        source_count=2,
        verified=verified,
        availability="live",
        changed_note=None,
        score=score,
    )


TAU = 0.55  # must match config.toml default


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_retrieve_grounded_above_tau(tmp_path, monkeypatch):
    """High-similarity result → grounded=True, chunks populated."""
    _setup_index_mocks(monkeypatch, tmp_path, top_scores=[0.85, 0.80])

    from copilot import retriever
    result = retriever.retrieve("How do I unlock Felicity Farseer?")

    assert result.grounded is True
    assert result.max_score >= TAU
    assert len(result.chunks) == 2
    for c in result.chunks:
        assert c.score > 0.0


def test_retrieve_not_grounded_below_tau(tmp_path, monkeypatch):
    """Low-similarity results → grounded=False even with non-empty chunks."""
    _setup_index_mocks(monkeypatch, tmp_path, top_scores=[0.30, 0.25])

    from copilot import retriever
    result = retriever.retrieve("best pizza topping")

    assert result.grounded is False
    assert result.max_score < TAU


def test_retrieve_empty_index(tmp_path, monkeypatch):
    """No index at all → grounded=False, max_score=0.0, chunks=[]."""
    monkeypatch.setattr("copilot.index.search", lambda qv, top_k: [])
    monkeypatch.setattr(
        "copilot.ollama_client.embed",
        lambda texts: np.stack([_unit_vec(t) for t in texts]),
    )
    _patch_config(monkeypatch)

    from copilot import retriever
    result = retriever.retrieve("anything")

    assert result.grounded is False
    assert result.max_score == 0.0
    assert result.chunks == []


def test_retrieve_filters_verified(tmp_path, monkeypatch):
    """filters={"verified": True} removes unverified chunks."""
    chunk_a = _make_chunk("aaaa1111", verified=True)
    chunk_b = _make_chunk("bbbb2222", verified=False)

    monkeypatch.setattr(
        "copilot.ollama_client.embed",
        lambda texts: np.stack([_unit_vec(t) for t in texts]),
    )
    monkeypatch.setattr(
        "copilot.index.search",
        lambda qv, top_k: [("aaaa1111", 0.80), ("bbbb2222", 0.75)],
    )
    monkeypatch.setattr(
        "copilot.index.chunk_by_id",
        lambda cid: chunk_a if cid == "aaaa1111" else chunk_b,
    )
    _patch_config(monkeypatch)

    from copilot import retriever
    result = retriever.retrieve("query", filters={"verified": True})

    assert all(c.verified for c in result.chunks)
    assert len(result.chunks) == 1


def test_retrieve_sets_score_via_replace(tmp_path, monkeypatch):
    """Each returned Chunk has .score set to the cosine value from search."""
    chunk_a = _make_chunk("cccc3333")  # score=0.0 initially

    monkeypatch.setattr(
        "copilot.ollama_client.embed",
        lambda texts: np.stack([_unit_vec(t) for t in texts]),
    )
    monkeypatch.setattr(
        "copilot.index.search",
        lambda qv, top_k: [("cccc3333", 0.91)],
    )
    monkeypatch.setattr("copilot.index.chunk_by_id", lambda cid: chunk_a)
    _patch_config(monkeypatch)

    from copilot import retriever
    result = retriever.retrieve("query")

    assert abs(result.chunks[0].score - 0.91) < 1e-6


# ---------------------------------------------------------------------------
# Internal test helpers
# ---------------------------------------------------------------------------

def _setup_index_mocks(monkeypatch, tmp_path: Path, top_scores: list[float]):
    n = len(top_scores)
    ids = [f"chunk{i:04d}" for i in range(n)]
    chunks = [_make_chunk(cid) for cid in ids]

    monkeypatch.setattr(
        "copilot.ollama_client.embed",
        lambda texts: np.stack([_unit_vec(t) for t in texts]),
    )
    monkeypatch.setattr(
        "copilot.index.search",
        lambda qv, top_k: list(zip(ids, top_scores))[:top_k],
    )
    monkeypatch.setattr(
        "copilot.index.chunk_by_id",
        lambda cid: next((c for c in chunks if c.chunk_id == cid), None),
    )
    _patch_config(monkeypatch)


def _patch_config(monkeypatch):
    cfg = {
        "retrieval": {"top_k": 8, "tau": TAU},
    }
    monkeypatch.setattr("copilot.retriever._config", lambda: cfg)
