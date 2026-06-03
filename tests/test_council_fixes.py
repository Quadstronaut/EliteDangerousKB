"""
Regression tests for the 2026-06-03 council review fixes.

Each test pins a specific bug the 3-agent review found and we fixed, so it
cannot silently regress. Grouped by the module it guards.
"""
import json
import textwrap
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest
import requests


# ===========================================================================
# ollama_client — broadened exception handling
# ===========================================================================

class _Resp:
    """Minimal fake requests.Response."""
    def __init__(self, payload=None, raise_status=None, lines=None):
        self._payload = payload or {}
        self._raise_status = raise_status
        self._lines = lines or []

    def raise_for_status(self):
        if self._raise_status:
            raise self._raise_status

    def json(self):
        return self._payload

    def iter_lines(self):
        yield from self._lines


def test_embed_read_timeout_becomes_unavailable():
    from copilot import ollama_client
    with patch("requests.post", side_effect=requests.exceptions.ReadTimeout("slow")):
        with pytest.raises(ollama_client.OllamaUnavailable):
            ollama_client.embed(["x"])


def test_embed_http_error_becomes_unavailable():
    from copilot import ollama_client
    resp = _Resp(raise_status=requests.exceptions.HTTPError("503"))
    with patch("requests.post", return_value=resp):
        with pytest.raises(ollama_client.OllamaUnavailable):
            ollama_client.embed(["x"])


def test_embed_missing_embeddings_key_becomes_unavailable():
    from copilot import ollama_client
    resp = _Resp(payload={"models": []})  # no "embeddings"
    with patch("requests.post", return_value=resp):
        with pytest.raises(ollama_client.OllamaUnavailable):
            ollama_client.embed(["x"])


def test_chat_stream_midstream_drop_becomes_unavailable():
    from copilot import ollama_client

    def _lines():
        yield json.dumps({"message": {"content": "Hello "}}).encode()
        raise requests.exceptions.ChunkedEncodingError("connection broken")

    resp = _Resp(lines=_lines())
    with patch("requests.post", return_value=resp):
        with pytest.raises(ollama_client.OllamaUnavailable):
            list(ollama_client.chat_stream([{"role": "user", "content": "hi"}]))


def test_vision_missing_file_raises_filenotfound():
    from copilot import ollama_client
    with pytest.raises(FileNotFoundError):
        ollama_client.vision("G:/definitely-not-here-12345.png", "describe")


# ===========================================================================
# repl — verified_only filter + crash-proof loop
# ===========================================================================

def test_retrieval_filters_verified_only():
    from copilot import repl
    assert repl._retrieval_filters({"copilot": {"mode": "verified_only"}}) == {"verified": True}


def test_retrieval_filters_include_unverified():
    from copilot import repl
    assert repl._retrieval_filters({"copilot": {"mode": "include_unverified"}}) is None


def test_retrieval_filters_defaults_to_verified_only():
    from copilot import repl
    assert repl._retrieval_filters({}) == {"verified": True}


def test_answer_passes_verified_filter_to_retrieve():
    """answer() must forward the verified_only filter into retrieve()."""
    from copilot import repl
    captured = {}

    class _Result:
        grounded = False
        chunks = []

    def _fake_retrieve(query, *, top_k=None, filters=None):
        captured["filters"] = filters
        return _Result()

    with patch("copilot.repl.load_config", return_value={"copilot": {"mode": "verified_only"}}):
        with patch("copilot.retriever.retrieve", side_effect=_fake_retrieve):
            repl.answer("how to unlock farseer", None)

    assert captured["filters"] == {"verified": True}


def test_main_survives_ollama_unavailable(monkeypatch, capsys):
    """A mid-session Ollama outage must print a friendly message, not crash."""
    from copilot import repl
    from copilot.ollama_client import OllamaUnavailable

    inputs = iter(["any question", "exit"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(inputs))
    monkeypatch.setattr(repl, "answer", lambda *a, **k: (_ for _ in ()).throw(OllamaUnavailable("down")))
    monkeypatch.setattr("copilot.profile.load_cmdr_state", lambda: None)

    repl.main()  # must return cleanly
    out = capsys.readouterr().out
    assert "unavailable" in out.lower()


# ===========================================================================
# index — integrity guard, missing-vectors upsert, non-utf8 resilience
# ===========================================================================

def _fake_embed(texts):
    import hashlib
    vecs = []
    for t in texts:
        seed = int(hashlib.sha256(t.encode()).hexdigest()[:8], 16) % (2**31)
        rng = np.random.default_rng(seed)
        v = rng.standard_normal(1024).astype(np.float32)
        v /= np.linalg.norm(v)
        vecs.append(v)
    return np.array(vecs, dtype=np.float32)


def _patch_dirs(monkeypatch, tmp_path):
    monkeypatch.setattr("copilot.paths.embeddings_dir", lambda: tmp_path / "embeddings")
    monkeypatch.setattr("copilot.paths.indexes_dir", lambda: tmp_path / "indexes")
    (tmp_path / "embeddings").mkdir(exist_ok=True)
    (tmp_path / "indexes").mkdir(exist_ok=True)


def _seed_kb(tmp_path):
    kb = tmp_path / "kb"
    kb.mkdir()
    (kb / "a.md").write_text(
        "---\nsource_tier: 1\nverified: true\n---\n# A\n## S\n\nAlpha content.\n",
        encoding="utf-8",
    )
    (kb / "b.md").write_text(
        "---\nsource_tier: 1\nverified: true\n---\n# B\n## S\n\nBeta content.\n",
        encoding="utf-8",
    )
    return kb


def test_search_refuses_on_length_skew(tmp_path, monkeypatch):
    monkeypatch.setenv("EDKB_ROOT", str(tmp_path))
    _patch_dirs(monkeypatch, tmp_path)
    from copilot import index

    with patch("copilot.ollama_client.embed", side_effect=_fake_embed):
        index.build_index(_seed_kb(tmp_path))

    # Corrupt the pairing: drop one id (simulate interrupted write).
    ids_path = tmp_path / "embeddings" / "chunk_ids.json"
    ids = json.loads(ids_path.read_text(encoding="utf-8"))
    ids_path.write_text(json.dumps(ids[:-1]), encoding="utf-8")

    q = _fake_embed(["query"])[0]
    assert index.search(q, top_k=5) == []  # refuses, no IndexError, no mis-cite


def test_upsert_survives_missing_vectors(tmp_path, monkeypatch):
    monkeypatch.setenv("EDKB_ROOT", str(tmp_path))
    _patch_dirs(monkeypatch, tmp_path)
    from copilot import index

    kb = _seed_kb(tmp_path)
    with patch("copilot.ollama_client.embed", side_effect=_fake_embed):
        index.build_index(kb)
        # Vectors lost but manifest survives (crash window).
        (tmp_path / "embeddings" / "vectors.npy").unlink()
        result = index.upsert_changed(kb)  # must not KeyError

    assert result["added"] >= 2  # everything re-embedded


def test_build_index_skips_non_utf8_file(tmp_path, monkeypatch):
    monkeypatch.setenv("EDKB_ROOT", str(tmp_path))
    _patch_dirs(monkeypatch, tmp_path)
    from copilot import index

    kb = _seed_kb(tmp_path)
    # Latin-1 byte that is invalid UTF-8.
    (kb / "bad.md").write_bytes(b"---\nverified: true\n---\n# Bad\n## S\n\ncaf\xe9\n")

    with patch("copilot.ollama_client.embed", side_effect=_fake_embed):
        count = index.build_index(kb)  # must not raise

    assert count >= 2  # the two good files still indexed


# ===========================================================================
# retriever — empty-text chunks never served
# ===========================================================================

def test_retriever_drops_empty_text_chunks(monkeypatch):
    from copilot import retriever
    from copilot.models import Chunk

    empty = Chunk(
        chunk_id="dead0001", text="", kb_path="kb/x.md", heading_path="X",
        source_url=None, source_tier=1, source_count=1, verified=True,
        availability="live", changed_note=None, score=0.0,
    )
    monkeypatch.setattr("copilot.retriever._config", lambda: {"retrieval": {"tau": 0.5, "top_k": 8}})
    monkeypatch.setattr("copilot.ollama_client.embed", lambda t: np.ones((1, 1024), dtype=np.float32))
    monkeypatch.setattr("copilot.index.search", lambda v, k: [("dead0001", 0.99)])
    monkeypatch.setattr("copilot.index.chunk_by_id", lambda cid: empty)

    result = retriever.retrieve("q")
    assert result.chunks == []
    assert result.grounded is False  # nothing real to ground on


# ===========================================================================
# chunker — same-named H3 under different H2 stays distinct
# ===========================================================================

def test_h3_collision_resolved(tmp_path):
    from copilot.chunker import chunk_page

    md = textwrap.dedent("""\
        ---
        verified: true
        ---
        # Guide

        ## Engineering

        ### Requirements

        Engineering needs materials.

        ## Outfitting

        ### Requirements

        Outfitting needs credits.
    """)
    p = tmp_path / "guide.md"
    p.write_text(md, encoding="utf-8")

    chunks = chunk_page(p)
    req = [c for c in chunks if c.heading_path.endswith("Requirements")]
    assert len(req) == 2, f"expected 2 Requirements chunks, got {[c.heading_path for c in chunks]}"
    assert req[0].chunk_id != req[1].chunk_id, "H3 collision — chunk_ids must differ"
    # Both parents represented.
    paths = {c.heading_path for c in req}
    assert any("Engineering" in p for p in paths)
    assert any("Outfitting" in p for p in paths)


# ===========================================================================
# profile_sources — journal rank keys canonicalized (no dupes)
# ===========================================================================

def test_journal_rank_keys_canonical(tmp_path):
    from copilot.profile_sources import parse_journal

    j = tmp_path / "Journal.test.log"
    j.write_text(
        json.dumps({"event": "Rank", "Combat": 4, "Explore": 8, "Soldier": 0,
                    "timestamp": "2026-06-01T00:00:00Z"}) + "\n",
        encoding="utf-8",
    )
    facts = {f.key: f.value for f in parse_journal(j)}

    # Canonical keys present...
    assert "rank.explorer" in facts
    assert "rank.mercenary" in facts
    assert "rank.combat" in facts
    # ...and the journal-native aliases are gone (would duplicate manual keys).
    assert "rank.explore" not in facts
    assert "rank.soldier" not in facts


# ===========================================================================
# mcp_server — citations are the ids ACTUALLY cited, not every retrieved id
# ===========================================================================

def test_ed_kb_answer_citations_are_actually_cited():
    from copilot.models import Chunk, RetrievalResult

    def _c(cid):
        return Chunk(
            chunk_id=cid, text="t", kb_path="kb/x.md", heading_path="X",
            source_url=None, source_tier=1, source_count=1, verified=True,
            availability="live", changed_note=None, score=0.8,
        )

    # Three chunks retrieved; the answer cites only the first.
    result = RetrievalResult(
        query="q",
        chunks=[_c("aaaa1111bbbb2222"), _c("cccc3333dddd4444"), _c("eeee5555ffff6666")],
        max_score=0.8,
        grounded=True,
    )
    fake = "Farseer wants Meta-Alloys [aaaa1111bbbb2222]."

    with (
        patch("copilot.mcp_server.retriever") as mr,
        patch("copilot.mcp_server.assemble") as ma,
        patch("copilot.mcp_server.ollama_client") as mo,
    ):
        mr.retrieve.return_value = result
        ma.build_messages.return_value = [{"role": "user", "content": "q"}]
        ma.validate_answer.return_value = (True, "ok")
        mo.chat_stream.return_value = iter([fake])

        from copilot.mcp_server import ed_kb_answer
        out = ed_kb_answer("q")

    # Only the cited id — NOT all three retrieved ids.
    assert out["citations"] == ["aaaa1111bbbb2222"]
