"""Tests for copilot/index.py — full rebuild, upsert, search, manifest."""
import json
import textwrap
import hashlib
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fake_embed(texts: list[str]) -> np.ndarray:
    """Deterministic fake embeddings: hash each text to a seeded unit vector."""
    vecs = []
    for t in texts:
        seed = int(hashlib.sha256(t.encode()).hexdigest()[:8], 16) % (2**31)
        rng = np.random.default_rng(seed)
        v = rng.standard_normal(1024).astype(np.float32)
        v /= np.linalg.norm(v)
        vecs.append(v)
    return np.array(vecs, dtype=np.float32)


def _make_md(title: str, heading: str, body: str) -> str:
    return textwrap.dedent(f"""\
        ---
        source_url: https://example.com
        source_tier: 2
        source_count: 1
        verified: true
        availability: live
        ---
        # {title}

        ## {heading}

        {body}
    """)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def kb(tmp_path):
    """Two-file KB in a temp directory."""
    kb_dir = tmp_path / "kb"
    kb_dir.mkdir()

    (kb_dir / "ships").mkdir()
    (kb_dir / "ships" / "python-mk-ii.md").write_text(
        _make_md("Python Mk II", "Overview", "The Python Mk II is a medium multirole ship."),
        encoding="utf-8",
    )
    (kb_dir / "engineers").mkdir()
    (kb_dir / "engineers" / "felicity-farseer.md").write_text(
        _make_md(
            "Felicity Farseer",
            "Unlock",
            "Invite: provide an exploration rank of Scout or higher and 1 unit of Meta-Alloys.",
        ),
        encoding="utf-8",
    )
    return kb_dir


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_build_index_returns_chunk_count(kb, tmp_path, monkeypatch):
    monkeypatch.setenv("EDKB_ROOT", str(tmp_path))
    _patch_dirs(monkeypatch, tmp_path)

    with patch("copilot.ollama_client.embed", side_effect=_fake_embed):
        from copilot import index
        count = index.build_index(kb)

    assert count >= 2  # at least one chunk per file


def test_build_index_writes_artifacts(kb, tmp_path, monkeypatch):
    monkeypatch.setenv("EDKB_ROOT", str(tmp_path))
    _patch_dirs(monkeypatch, tmp_path)

    with patch("copilot.ollama_client.embed", side_effect=_fake_embed):
        from copilot import index
        count = index.build_index(kb)

    emb_dir = tmp_path / "embeddings"
    idx_dir = tmp_path / "indexes"

    vectors = np.load(emb_dir / "vectors.npy")
    chunk_ids = json.loads((emb_dir / "chunk_ids.json").read_text(encoding="utf-8"))
    manifest = json.loads((idx_dir / "manifest.json").read_text(encoding="utf-8"))

    assert vectors.shape == (count, 1024)
    assert vectors.dtype == np.float32
    assert len(chunk_ids) == count
    assert set(chunk_ids) == set(manifest.keys())

    # payload should NOT contain 'text' or 'score'
    for entry in manifest.values():
        assert "text" not in entry["payload"]
        assert "score" not in entry["payload"]
        assert "content_hash" in entry
        assert "kb_path" in entry
        assert "heading_path" in entry


def test_search_ordering(kb, tmp_path, monkeypatch):
    """Search returns results sorted descending by cosine score."""
    monkeypatch.setenv("EDKB_ROOT", str(tmp_path))
    _patch_dirs(monkeypatch, tmp_path)

    with patch("copilot.ollama_client.embed", side_effect=_fake_embed):
        from copilot import index
        index.build_index(kb)

    # Use one of the actual chunk vectors as the query — it should score 1.0 first.
    emb_dir = tmp_path / "embeddings"
    vectors = np.load(emb_dir / "vectors.npy")
    query_vec = vectors[0]

    results = index.search(query_vec, top_k=5)
    assert results, "search returned empty list"
    scores = [s for _, s in results]
    assert scores == sorted(scores, reverse=True), "results not sorted descending"
    assert abs(scores[0] - 1.0) < 1e-4, "exact query vector should score ~1.0"


def test_upsert_unchanged(kb, tmp_path, monkeypatch):
    """No-op upsert on unmodified KB reports all unchanged."""
    monkeypatch.setenv("EDKB_ROOT", str(tmp_path))
    _patch_dirs(monkeypatch, tmp_path)

    with patch("copilot.ollama_client.embed", side_effect=_fake_embed):
        from copilot import index
        index.build_index(kb)
        result = index.upsert_changed(kb)

    assert result["added"] == 0
    assert result["removed"] == 0
    assert result["unchanged"] >= 2


def test_upsert_detects_added_and_removed(kb, tmp_path, monkeypatch):
    monkeypatch.setenv("EDKB_ROOT", str(tmp_path))
    _patch_dirs(monkeypatch, tmp_path)

    with patch("copilot.ollama_client.embed", side_effect=_fake_embed):
        from copilot import index
        index.build_index(kb)

        # Edit one file and add a new one.
        (kb / "ships" / "python-mk-ii.md").write_text(
            _make_md("Python Mk II", "Overview", "Updated text for Python Mk II."),
            encoding="utf-8",
        )
        (kb / "new-page.md").write_text(
            _make_md("New Page", "Section", "Brand new page content."),
            encoding="utf-8",
        )
        # Delete a file.
        (kb / "engineers" / "felicity-farseer.md").unlink()

        result = index.upsert_changed(kb)

    assert result["added"] >= 1    # new page + edited page produce new chunks
    assert result["removed"] >= 1  # felicity chunks tombstoned
    # manifest must not contain tombstoned chunk_ids
    manifest = index.load_manifest()
    for entry in manifest.values():
        assert entry["kb_path"] != "kb/engineers/felicity-farseer.md"


def test_chunk_by_id_roundtrip(kb, tmp_path, monkeypatch):
    """chunk_by_id returns a Chunk whose chunk_id matches the requested id."""
    monkeypatch.setenv("EDKB_ROOT", str(tmp_path))
    _patch_dirs(monkeypatch, tmp_path)

    with patch("copilot.ollama_client.embed", side_effect=_fake_embed):
        from copilot import index
        index.build_index(kb)

    emb_dir = tmp_path / "embeddings"
    chunk_ids = json.loads((emb_dir / "chunk_ids.json").read_text(encoding="utf-8"))
    cid = chunk_ids[0]

    chunk = index.chunk_by_id(cid)
    assert chunk is not None
    assert chunk.chunk_id == cid


# ---------------------------------------------------------------------------
# Internal helper for monkeypatching path functions
# ---------------------------------------------------------------------------

def _patch_dirs(monkeypatch, tmp_path: Path):
    monkeypatch.setattr("copilot.paths.embeddings_dir", lambda: tmp_path / "embeddings")
    monkeypatch.setattr("copilot.paths.indexes_dir", lambda: tmp_path / "indexes")
    (tmp_path / "embeddings").mkdir(exist_ok=True)
    (tmp_path / "indexes").mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Corrupt vectors.npy recovery (council round-2 fix)
# ---------------------------------------------------------------------------

def test_search_corrupt_vectors_returns_empty_with_warning(kb, tmp_path, monkeypatch, capsys):
    """search() on a corrupt vectors.npy emits a WARNING and returns [] (no traceback)."""
    monkeypatch.setenv("EDKB_ROOT", str(tmp_path))
    _patch_dirs(monkeypatch, tmp_path)

    with patch("copilot.ollama_client.embed", side_effect=_fake_embed):
        from copilot import index
        index.build_index(kb)

    # Overwrite vectors.npy with garbage bytes (simulates hardware corruption).
    (tmp_path / "embeddings" / "vectors.npy").write_bytes(b"CORRUPT")

    q = _fake_embed(["query"])[0]
    result = index.search(q, top_k=5)

    assert result == [], "Expected [] on corrupt vectors.npy, got non-empty result"
    stderr = capsys.readouterr().err
    assert "WARNING" in stderr and "vectors.npy" in stderr


def test_upsert_corrupt_vectors_triggers_full_reembed(kb, tmp_path, monkeypatch, capsys):
    """upsert_changed() on a corrupt vectors.npy emits WARNING and re-embeds all chunks."""
    monkeypatch.setenv("EDKB_ROOT", str(tmp_path))
    _patch_dirs(monkeypatch, tmp_path)

    with patch("copilot.ollama_client.embed", side_effect=_fake_embed):
        from copilot import index
        index.build_index(kb)

    # Corrupt vectors.npy but leave manifest intact (the dangerous scenario:
    # manifest says "unchanged", but we have no valid vectors to stack).
    (tmp_path / "embeddings" / "vectors.npy").write_bytes(b"CORRUPT")

    with patch("copilot.ollama_client.embed", side_effect=_fake_embed):
        result = index.upsert_changed(kb)

    assert result["added"] >= 2, f"Expected full re-embed, got added={result['added']}"
    stderr = capsys.readouterr().err
    assert "WARNING" in stderr and "vectors.npy" in stderr
