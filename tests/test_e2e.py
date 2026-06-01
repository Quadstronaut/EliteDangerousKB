"""
End-to-end integration test.

Mocks: ollama_client.embed, ollama_client.chat_stream.
Real:  index.build_index (writes to tmp dirs), retriever.retrieve, repl.answer.

Scenarios:
  1. build_index on seed kb/ succeeds and returns >0 chunks.
  2. retrieve("How do I unlock Felicity Farseer?") returns grounded=True
     with at least one chunk whose kb_path contains "felicity-farseer".
     (xfail under fake embeddings — see note below; passes with real bge-m3.)
  3. repl.answer("best pizza topping", state) returns REFUSAL (off-topic, below tau).
"""
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest

from copilot.models import CmdrState


# ---------------------------------------------------------------------------
# Deterministic fake embed (same helper as test_index.py)
# ---------------------------------------------------------------------------

def _fake_embed(texts: list[str]) -> np.ndarray:
    vecs = []
    for t in texts:
        seed = int(hashlib.sha256(t.encode()).hexdigest()[:8], 16) % (2**31)
        rng = np.random.default_rng(seed)
        v = rng.standard_normal(1024).astype(np.float32)
        v /= np.linalg.norm(v)
        vecs.append(v)
    return np.array(vecs, dtype=np.float32)


STATE = CmdrState(name="Duvrazh")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def built_index(tmp_path_factory):
    """Build index from the real seed kb/ directory into a temp location."""
    tmp = tmp_path_factory.mktemp("e2e")
    emb_dir = tmp / "embeddings"
    idx_dir = tmp / "indexes"
    emb_dir.mkdir()
    idx_dir.mkdir()

    import copilot.paths as _paths
    # Patch path functions to point at tmp dirs.
    original_emb = _paths.embeddings_dir
    original_idx = _paths.indexes_dir
    _paths.embeddings_dir = lambda: emb_dir
    _paths.indexes_dir = lambda: idx_dir

    with patch("copilot.ollama_client.embed", side_effect=_fake_embed):
        from copilot import index
        from copilot.paths import kb_dir
        count = index.build_index(kb_dir())

    # Restore
    _paths.embeddings_dir = original_emb
    _paths.indexes_dir = original_idx

    return {"count": count, "emb_dir": emb_dir, "idx_dir": idx_dir, "tmp": tmp}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_e2e_build_index_nonzero(built_index):
    assert built_index["count"] > 0, "build_index returned 0 chunks for seed KB"


@pytest.mark.xfail(
    reason="Fake hash-seeded embeddings cannot produce an on-topic grounded "
           "result; passes with real bge-m3 during manual integration verification.",
    strict=False,
)
def test_e2e_retrieve_farseer_grounded(built_index, monkeypatch):
    monkeypatch.setattr("copilot.paths.embeddings_dir", lambda: built_index["emb_dir"])
    monkeypatch.setattr("copilot.paths.indexes_dir", lambda: built_index["idx_dir"])
    monkeypatch.setattr("copilot.ollama_client.embed", _fake_embed)

    from copilot import retriever
    result = retriever.retrieve("How do I unlock Felicity Farseer?")

    assert result.grounded, (
        f"Expected grounded=True but got max_score={result.max_score:.3f}. "
        "Fake embed is deterministic but the query vector must match chunk vectors "
        "closely enough — check tau setting or embedding mock."
    )
    farseer_chunks = [c for c in result.chunks if "felicity-farseer" in c.kb_path]
    assert farseer_chunks, (
        "No felicity-farseer chunk in retrieval result. "
        f"Top chunk: {result.chunks[0].kb_path if result.chunks else 'none'}"
    )


def test_e2e_off_topic_refusal(built_index, monkeypatch):
    """An unrelated query must be refused regardless of index content."""
    monkeypatch.setattr("copilot.paths.embeddings_dir", lambda: built_index["emb_dir"])
    monkeypatch.setattr("copilot.paths.indexes_dir", lambda: built_index["idx_dir"])
    monkeypatch.setattr("copilot.ollama_client.embed", _fake_embed)

    from copilot.repl import answer, REFUSAL

    # Mock chat_stream to ensure it is never reached (refusal fires at retrieval gate).
    with patch("copilot.ollama_client.chat_stream") as mock_stream:
        result = answer("best pizza topping", STATE)

    assert result == REFUSAL
    mock_stream.assert_not_called()
