"""M3 — non-dict manifest robustness.

manifest.json containing valid-but-wrong JSON (`null` -> None, or a list)
parses cleanly but is NOT a dict. upsert_changed()'s try/except caught
(ValueError, OSError) but NOT the downstream TypeError from `cid in None` /
`None[cid]`. Fix: load_manifest() coerces ANY non-dict parse result to {} (full
rebuild), symmetric with the corrupt-JSON case; the upsert path emits an
observable WARNING for the non-dict case too.
"""
import json
import textwrap
import hashlib
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest


def _fake_embed(texts: list[str]) -> np.ndarray:
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


@pytest.fixture()
def kb(tmp_path):
    kb_dir = tmp_path / "kb"
    kb_dir.mkdir()
    (kb_dir / "ships").mkdir()
    (kb_dir / "ships" / "python-mk-ii.md").write_text(
        _make_md("Python Mk II", "Overview", "The Python Mk II is a medium multirole ship."),
        encoding="utf-8",
    )
    (kb_dir / "engineers").mkdir()
    (kb_dir / "engineers" / "felicity-farseer.md").write_text(
        _make_md("Felicity Farseer", "Unlock", "Provide 1 unit of Meta-Alloys."),
        encoding="utf-8",
    )
    return kb_dir


def _patch_dirs(monkeypatch, tmp_path: Path):
    monkeypatch.setattr("copilot.paths.embeddings_dir", lambda: tmp_path / "embeddings")
    monkeypatch.setattr("copilot.paths.indexes_dir", lambda: tmp_path / "indexes")
    (tmp_path / "embeddings").mkdir(exist_ok=True)
    (tmp_path / "indexes").mkdir(exist_ok=True)


# ---- AC-M3a: literal null manifest -> {} + degrade-to-full-rebuild + WARN ---

def test_null_manifest_load_returns_empty_dict(kb, tmp_path, monkeypatch):
    monkeypatch.setenv("EDKB_ROOT", str(tmp_path))
    _patch_dirs(monkeypatch, tmp_path)
    from copilot import index
    (tmp_path / "indexes" / "manifest.json").write_text("null", encoding="utf-8")
    loaded = index.load_manifest()
    assert loaded == {}          # NOT None
    assert isinstance(loaded, dict)


def test_null_manifest_upsert_degrades_to_full_rebuild(kb, tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("EDKB_ROOT", str(tmp_path))
    _patch_dirs(monkeypatch, tmp_path)

    with patch("copilot.ollama_client.embed", side_effect=_fake_embed):
        from copilot import index
        index.build_index(kb)

    # Replace the good manifest with literal `null` (valid JSON, parses to None).
    (tmp_path / "indexes" / "manifest.json").write_text("null", encoding="utf-8")

    with patch("copilot.ollama_client.embed", side_effect=_fake_embed):
        result = index.upsert_changed(kb)  # must NOT raise TypeError

    assert result["added"] >= 2, f"expected full re-embed, got added={result['added']}"
    stderr = capsys.readouterr().err
    assert "WARNING" in stderr and "manifest.json" in stderr


# ---- AC-M3b: list manifest -> {} + degrade-to-full-rebuild + WARN ----------

def test_list_manifest_load_returns_empty_dict(kb, tmp_path, monkeypatch):
    monkeypatch.setenv("EDKB_ROOT", str(tmp_path))
    _patch_dirs(monkeypatch, tmp_path)
    from copilot import index
    (tmp_path / "indexes" / "manifest.json").write_text("[1, 2, 3]", encoding="utf-8")
    loaded = index.load_manifest()
    assert loaded == {}
    assert isinstance(loaded, dict)


def test_list_manifest_upsert_degrades_to_full_rebuild(kb, tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("EDKB_ROOT", str(tmp_path))
    _patch_dirs(monkeypatch, tmp_path)

    with patch("copilot.ollama_client.embed", side_effect=_fake_embed):
        from copilot import index
        index.build_index(kb)

    (tmp_path / "indexes" / "manifest.json").write_text("[1, 2, 3]", encoding="utf-8")

    with patch("copilot.ollama_client.embed", side_effect=_fake_embed):
        result = index.upsert_changed(kb)  # must NOT raise TypeError

    assert result["added"] >= 2, f"expected full re-embed, got added={result['added']}"
    stderr = capsys.readouterr().err
    assert "WARNING" in stderr and "manifest.json" in stderr


# ---- AC-M3c: valid dict manifest unchanged (happy path) -------------------

def test_valid_dict_manifest_load_returns_verbatim(kb, tmp_path, monkeypatch):
    monkeypatch.setenv("EDKB_ROOT", str(tmp_path))
    _patch_dirs(monkeypatch, tmp_path)
    from copilot import index
    payload = {"abc123": {"content_hash": "deadbeef", "kb_path": "kb/x.md",
                          "heading_path": "X", "payload": {}}}
    (tmp_path / "indexes" / "manifest.json").write_text(json.dumps(payload), encoding="utf-8")
    assert index.load_manifest() == payload  # verbatim


def test_valid_dict_manifest_upsert_unchanged_classification(kb, tmp_path, monkeypatch, capsys):
    """A no-op upsert on a valid dict manifest reports all unchanged and emits
    NO manifest WARNING (happy path wholly unchanged)."""
    monkeypatch.setenv("EDKB_ROOT", str(tmp_path))
    _patch_dirs(monkeypatch, tmp_path)

    with patch("copilot.ollama_client.embed", side_effect=_fake_embed):
        from copilot import index
        index.build_index(kb)
        capsys.readouterr()  # drop build noise
        result = index.upsert_changed(kb)

    assert result["added"] == 0
    assert result["removed"] == 0
    assert result["unchanged"] >= 2
    stderr = capsys.readouterr().err
    assert "manifest.json" not in stderr  # no degrade warning on the happy path


def test_chunk_by_id_on_null_manifest_returns_none(kb, tmp_path, monkeypatch):
    """chunk_by_id() over a null manifest must NOT TypeError — it sees {} and
    returns None (the id is absent)."""
    monkeypatch.setenv("EDKB_ROOT", str(tmp_path))
    _patch_dirs(monkeypatch, tmp_path)
    from copilot import index
    (tmp_path / "indexes" / "manifest.json").write_text("null", encoding="utf-8")
    assert index.chunk_by_id("anything") is None
