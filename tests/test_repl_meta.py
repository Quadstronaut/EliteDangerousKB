"""
tests/test_repl_meta.py — Stage 1: meta-commands (help / topics / sources).

meta_command() intercepts tool-about questions BEFORE answer() so they don't
hit the RAG gate and spuriously REFUSE. These tests pin the closed grammar,
the manifest-derived topics rendering, the source roster, PURITY (zero
network / Ollama / retrieve), state=None safety, exit non-shadowing, and the
greeting. Everything runs OFFLINE — no live Ollama is started or patched.
"""

from __future__ import annotations

import io
import json
from unittest.mock import MagicMock

import pytest

from copilot import paths
from copilot.assemble import REFUSAL
from copilot.acquire_sources import ED_SOURCES
from copilot.models import CmdrState
from copilot.repl import meta_command

STATE = CmdrState(name="Duvrazh")


# ---------------------------------------------------------------------------
# Manifest fixtures via monkeypatched paths.indexes_dir -> tmp dir
# ---------------------------------------------------------------------------

def _write_manifest(tmp_path, manifest: dict) -> None:
    """Write a manifest.json into tmp and point indexes_dir() at it.

    meta_command must read THROUGH index.load_manifest() (which reads
    paths.indexes_dir()/manifest.json), so patching this is the only hook
    needed — no hardcoded paths allowed in the implementation.
    """
    (tmp_path / "manifest.json").write_text(
        json.dumps(manifest), encoding="utf-8"
    )


@pytest.fixture
def indexes_tmp(tmp_path, monkeypatch):
    """Redirect paths.indexes_dir() to a fresh tmp dir for the test."""
    monkeypatch.setattr(paths, "indexes_dir", lambda: tmp_path)
    return tmp_path


def _manifest_two_pages() -> dict:
    """>=2 chunks spanning >=2 distinct kb_path values."""
    return {
        "aabbccdd11223344": {
            "content_hash": "h1",
            "kb_path": "kb/engineers/felicity-farseer.md",
            "heading_path": "Felicity Farseer > Unlock",
            "payload": {},
        },
        "eeff00112233aabb": {
            "content_hash": "h2",
            "kb_path": "kb/engineers/felicity-farseer.md",
            "heading_path": "Felicity Farseer > Location",
            "payload": {},
        },
        "1122334455667788": {
            "content_hash": "h3",
            "kb_path": "kb/systems/deciat.md",
            "heading_path": "Deciat > Overview",
            "payload": {},
        },
    }


# ---------------------------------------------------------------------------
# AC1: function exists, signature, returns str | None
# ---------------------------------------------------------------------------

def test_ac1_signature(indexes_tmp):
    assert callable(meta_command)
    assert isinstance(meta_command("help", STATE), str)
    assert meta_command("definitely not a command", STATE) is None


# ---------------------------------------------------------------------------
# AC2: help / ? / commands / menu
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("q", ["help", "?", "commands", "menu"])
def test_ac2_help_tokens(q):
    out = meta_command(q, STATE)
    assert out is not None
    for substr in ("help", "topics", "sources", "exit"):
        assert substr in out, f"help text missing {substr!r}"
    # grounding contract in plain English
    low = out.lower()
    assert "verified knowledge base" in low or "verified source" in low
    assert "refuse" in low or "refus" in low
    # identity line
    assert "covas" in low
    assert "elite dangerous" in low
    # must NOT leak the refusal string
    assert REFUSAL not in out


# ---------------------------------------------------------------------------
# AC3: help natural phrasings (case-insensitive, optional '?')
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("q", [
    "what can you do",
    "What Can You Do?",
    "what commands can you accept",
    "what commands do you accept?",
    "what can i type",
    "  what can i ask  ",
    "how do i use this?",
])
def test_ac3_help_phrasings(q):
    out = meta_command(q, STATE)
    assert out is not None
    assert "topics" in out and "sources" in out


# ---------------------------------------------------------------------------
# AC4: topics non-empty — true counts + every kb_path verbatim
# ---------------------------------------------------------------------------

def test_ac4_topics_nonempty(indexes_tmp):
    manifest = _manifest_two_pages()
    _write_manifest(indexes_tmp, manifest)

    out = meta_command("topics", STATE)
    assert out is not None

    distinct_pages = sorted({e["kb_path"] for e in manifest.values()})
    assert len(distinct_pages) == 2
    chunks = len(manifest)  # 3

    # true page count and chunk count present as substrings
    assert str(len(distinct_pages)) in out
    assert str(chunks) in out
    # every distinct kb_path rendered verbatim
    for kb_path in distinct_pages:
        assert kb_path in out, f"missing kb_path {kb_path!r}"
    assert REFUSAL not in out


# ---------------------------------------------------------------------------
# AC5: topics empty — guidance, no raise
# ---------------------------------------------------------------------------

def test_ac5_topics_empty_missing_manifest(indexes_tmp):
    # No manifest.json written -> load_manifest() returns {}.
    out = meta_command("topics", STATE)
    assert out is not None
    assert "knowledge base is empty" in out
    assert "research loop" in out
    assert REFUSAL not in out


def test_ac5_topics_empty_explicit_empty_dict(indexes_tmp):
    _write_manifest(indexes_tmp, {})
    out = meta_command("topics", STATE)
    assert "knowledge base is empty" in out
    assert "research loop" in out


# ---------------------------------------------------------------------------
# AC6: topics natural phrasings (case / ? / whitespace tolerant)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("q", [
    "what's in your database",
    "Whats In Your Database?",
    "what do you know",
    "  what do you know?  ",
    "what is in your database",
    "what pages do you have",
    "what's in your knowledge base",
    "whats in your knowledge base",
])
def test_ac6_topics_phrasings(indexes_tmp, q):
    _write_manifest(indexes_tmp, _manifest_two_pages())
    out = meta_command(q, STATE)
    assert out is not None
    assert "kb/systems/deciat.md" in out


# ---------------------------------------------------------------------------
# AC7: sources — every key + tier conveyed, no network
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("q", [
    "sources", "source",
    "where do you get your data",
    "what are your sources?",
])
def test_ac7_sources(q):
    out = meta_command(q, STATE)
    assert out is not None
    for src in ED_SOURCES:
        assert src.key in out, f"missing source key {src.key!r}"
    assert "tier" in out.lower()
    # every source's integer tier rendered
    for tier in sorted({s.tier for s in ED_SOURCES}):
        assert str(tier) in out
    assert REFUSAL not in out


# ---------------------------------------------------------------------------
# AC8 / AC15: PURITY — zero retrieve, zero ollama, zero network, offline-safe
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("q", [
    "help", "?", "commands", "menu",
    "topics", "topic", "coverage",
    "sources", "source",
    "what's in your database", "what are your sources",
])
def test_ac8_purity_no_retrieve_no_ollama(indexes_tmp, monkeypatch, q):
    _write_manifest(indexes_tmp, _manifest_two_pages())

    import copilot.retriever as _retriever
    import copilot.ollama_client as _oc

    retrieve_mock = MagicMock(side_effect=AssertionError("retrieve must not be called"))
    chat_mock = MagicMock(side_effect=AssertionError("chat_stream must not be called"))
    embed_mock = MagicMock(side_effect=AssertionError("embed must not be called"))
    monkeypatch.setattr(_retriever, "retrieve", retrieve_mock)
    monkeypatch.setattr(_oc, "chat_stream", chat_mock)
    monkeypatch.setattr(_oc, "embed", embed_mock)

    out = meta_command(q, STATE)
    assert out is not None
    assert retrieve_mock.call_count == 0
    assert chat_mock.call_count == 0
    assert embed_mock.call_count == 0


# ---------------------------------------------------------------------------
# AC9: real questions fall through to answer() (return None)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("q", [
    "sol",
    "how do I unlock Felicity Farseer",
    "where can I buy meta-alloys",
    "what do you know about sol",        # subject appended -> NOT meta
    "jameson crash site",
    "thargoid sensor",
    "what topics does sol have",
    "sources of meta-alloys",            # 'sources' as a substring, not whole-string
    "help me find deciat",               # 'help' as a prefix, not whole-string
])
def test_ac9_real_questions_fall_through(indexes_tmp, q):
    _write_manifest(indexes_tmp, _manifest_two_pages())
    assert meta_command(q, STATE) is None


# ---------------------------------------------------------------------------
# AC11: state=None safe
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("q", ["help", "topics", "sources"])
def test_ac11_state_none_safe(indexes_tmp, q):
    _write_manifest(indexes_tmp, _manifest_two_pages())
    out = meta_command(q, None)
    assert isinstance(out, str)


# ---------------------------------------------------------------------------
# AC12: exit / quit / q are NOT shadowed (return None)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("q", ["exit", "quit", "q", "EXIT", " quit ", "q?"])
def test_ac12_exit_not_shadowed(q):
    assert meta_command(q, STATE) is None


# ---------------------------------------------------------------------------
# Whole-string discipline: bare "what do you know about" IS topics,
# but with a subject it is NOT.
# ---------------------------------------------------------------------------

def test_bare_what_do_you_know_about_is_topics(indexes_tmp):
    _write_manifest(indexes_tmp, _manifest_two_pages())
    assert meta_command("what do you know about", STATE) is not None
    assert meta_command("what do you know about?", STATE) is not None
    assert meta_command("what do you know about sol", STATE) is None


# ---------------------------------------------------------------------------
# Malformed manifest entry (missing kb_path) is skipped, not raised
# ---------------------------------------------------------------------------

def test_topics_skips_malformed_entry(indexes_tmp):
    manifest = {
        "good1111": {"content_hash": "h", "kb_path": "kb/a.md", "payload": {}},
        "bad22222": {"content_hash": "h", "payload": {}},  # missing kb_path
    }
    _write_manifest(indexes_tmp, manifest)
    out = meta_command("topics", STATE)
    assert out is not None
    assert "kb/a.md" in out
    # 1 distinct page, but 2 chunks total
    assert str(2) in out  # chunk count


# ---------------------------------------------------------------------------
# Determinism: same manifest + query -> identical output
# ---------------------------------------------------------------------------

def test_topics_deterministic(indexes_tmp):
    _write_manifest(indexes_tmp, _manifest_two_pages())
    a = meta_command("topics", STATE)
    b = meta_command("topics", STATE)
    assert a == b


# ---------------------------------------------------------------------------
# AC13: greeting mentions 'help' and retains 'exit' affordance
# ---------------------------------------------------------------------------

def test_ac13_greeting_mentions_help(monkeypatch, capsys):
    """Run main() with immediate EOF stdin; assert greeting only.

    answer() is never reached (EOF on first input -> Goodbye + break), and we
    hard-fail if retrieve/chat are touched, proving the greeting path is clean.
    """
    import copilot.repl as _repl
    import copilot.retriever as _retriever
    import copilot.ollama_client as _oc

    monkeypatch.setattr(_repl, "load_cmdr_state", lambda: STATE, raising=False)
    # If load_cmdr_state is imported lazily inside main(), patch the source too.
    import copilot.profile as _profile
    monkeypatch.setattr(_profile, "load_cmdr_state", lambda: STATE)

    monkeypatch.setattr(
        _retriever, "retrieve",
        MagicMock(side_effect=AssertionError("retrieve must not run in greeting test")),
    )
    monkeypatch.setattr(
        _oc, "chat_stream",
        MagicMock(side_effect=AssertionError("chat must not run in greeting test")),
    )

    # Empty stdin -> input() raises EOFError on first read -> Goodbye + break.
    monkeypatch.setattr("sys.stdin", io.StringIO(""))

    _repl.main()
    captured = capsys.readouterr()
    out = captured.out
    assert "help" in out
    assert "exit" in out.lower()


# ---------------------------------------------------------------------------
# AC10: gate unchanged — an ungrounded answer() still returns exactly REFUSAL.
# ---------------------------------------------------------------------------

def test_ac10_gate_unchanged_ungrounded_refuses(monkeypatch):
    import copilot.retriever as _retriever
    from copilot.models import RetrievalResult
    from copilot.repl import answer

    ungrounded = RetrievalResult(query="sol", chunks=[], max_score=0.0, grounded=False)
    monkeypatch.setattr(_retriever, "retrieve", lambda *a, **kw: ungrounded)

    # Ensure single-hop path (multihop off) so retrieve result is used directly.
    import copilot.paths as _paths
    import copilot.repl as _repl_mod
    orig = _paths.load_config

    def _cfg_off():
        cfg = orig()
        cfg.setdefault("copilot", {})["multihop"] = False
        return cfg

    monkeypatch.setattr(_paths, "load_config", _cfg_off)
    monkeypatch.setattr(_repl_mod, "load_config", _cfg_off)

    assert answer("sol", STATE) == REFUSAL
