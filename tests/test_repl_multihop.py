"""
tests/test_repl_multihop.py — Group A2: repl wiring & gate preservation.

All Ollama calls are mocked. Tests run offline with no live Ollama.
"""

from __future__ import annotations

import dataclasses
from unittest.mock import MagicMock, patch, call

import pytest

from copilot.models import Chunk, CmdrState, RetrievalResult


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

def _make_chunk(
    chunk_id: str = "aabbccdd11223344",
    text: str = "Felicity Farseer requires Meta-Alloys to unlock engineering.",
    score: float = 0.87,
) -> Chunk:
    return Chunk(
        chunk_id=chunk_id,
        text=text,
        kb_path="kb/engineers/felicity-farseer.md",
        heading_path="Felicity Farseer > Unlock",
        source_url="https://inara.cz/elite/engineer/1/",
        source_tier=1,
        source_count=3,
        verified=True,
        availability="live",
        changed_note=None,
        score=score,
    )


def _grounded_result(query: str = "test", chunk_id: str = "aabbccdd11223344") -> RetrievalResult:
    chunk = _make_chunk(chunk_id=chunk_id)
    return RetrievalResult(
        query=query,
        chunks=[chunk],
        max_score=0.87,
        grounded=True,
    )


def _empty_result(query: str = "test") -> RetrievalResult:
    return RetrievalResult(query=query, chunks=[], max_score=0.0, grounded=False)


STATE = CmdrState(name="TestCmdr")
TAU = 0.55  # must match config.toml [retrieval].tau


# ---------------------------------------------------------------------------
# A2-1: default (multihop=false) path calls retrieve exactly once
# ---------------------------------------------------------------------------

def test_answer_default_path_unchanged(monkeypatch):
    """With multihop=false, answer() calls retriever.retrieve exactly ONCE."""
    import copilot.retriever as _retriever
    import copilot.ollama_client as _oc

    cited_answer = "Farseer needs Meta-Alloys [aabbccdd11223344]."

    retrieve_mock = MagicMock(return_value=_grounded_result())
    monkeypatch.setattr(_retriever, "retrieve", retrieve_mock)

    def _mock_stream(messages, model=None):
        yield cited_answer

    monkeypatch.setattr(_oc, "chat_stream", _mock_stream)

    # Ensure multihop is off in config
    original_load_config = None
    import copilot.paths as _paths
    original_load_config = _paths.load_config

    def _cfg_with_multihop_off():
        cfg = original_load_config()
        cfg.setdefault("copilot", {})["multihop"] = False
        return cfg

    monkeypatch.setattr(_paths, "load_config", _cfg_with_multihop_off)
    # Also patch repl's load_config since it imports it directly
    import copilot.repl as _repl
    monkeypatch.setattr(_repl, "load_config", _cfg_with_multihop_off)

    from copilot.repl import answer
    result = answer("How do I unlock Farseer?", STATE)

    # retrieve called exactly once — proves default path is intact
    assert retrieve_mock.call_count == 1, (
        f"Expected retrieve called 1 time, got {retrieve_mock.call_count}"
    )
    assert result == cited_answer


# ---------------------------------------------------------------------------
# A2-2: _union_results dedup by chunk_id
# ---------------------------------------------------------------------------

def test_union_dedups_by_chunk_id():
    """Union of two results sharing a chunk_id keeps the higher-scored copy."""
    from copilot.repl import _union_results

    chunk_low = _make_chunk(chunk_id="aabbccdd11223344", score=0.60)
    chunk_high = _make_chunk(chunk_id="aabbccdd11223344", score=0.85)
    chunk_other = _make_chunk(chunk_id="zz11223344556677", score=0.70)

    r1 = RetrievalResult(query="q1", chunks=[chunk_low], max_score=0.60, grounded=True)
    r2 = RetrievalResult(query="q2", chunks=[chunk_high, chunk_other], max_score=0.85, grounded=True)

    union = _union_results([r1, r2], tau=TAU)

    # Exactly 2 unique chunks (the shared id appears once; the other once)
    ids = [c.chunk_id for c in union.chunks]
    assert len(ids) == 2, f"Expected 2 unique chunks, got {len(ids)}: {ids}"
    assert len(set(ids)) == 2, f"Duplicate chunk_ids in union: {ids}"

    # The shared chunk keeps the higher score
    shared = next(c for c in union.chunks if c.chunk_id == "aabbccdd11223344")
    assert shared.score == 0.85, f"Expected max score 0.85, got {shared.score}"

    # max_score reflects union max
    assert union.max_score == 0.85


# ---------------------------------------------------------------------------
# A2-3: _union_results grounded threshold
# ---------------------------------------------------------------------------

def test_union_grounded_threshold_above_tau():
    """Union whose max_score >= tau must be grounded=True."""
    from copilot.repl import _union_results

    chunk = _make_chunk(score=0.80)
    r = RetrievalResult(query="q", chunks=[chunk], max_score=0.80, grounded=True)
    union = _union_results([r], tau=TAU)
    assert union.grounded is True


def test_union_grounded_threshold_below_tau():
    """Union whose max_score < tau must be grounded=False."""
    from copilot.repl import _union_results

    chunk = _make_chunk(score=0.40)
    r = RetrievalResult(query="q", chunks=[chunk], max_score=0.40, grounded=False)
    union = _union_results([r], tau=TAU)
    assert union.grounded is False


def test_union_empty_results_list():
    """_union_results([]) returns an ungrounded empty result without crashing."""
    from copilot.repl import _union_results
    union = _union_results([], tau=TAU)
    assert union.grounded is False
    assert union.chunks == []


# ---------------------------------------------------------------------------
# A2-4: gate runs over union (multihop=true path)
# ---------------------------------------------------------------------------

def test_multihop_gate_runs_over_union(monkeypatch):
    """With multihop=true, validate_answer runs over the UNION result.

    A fabricated citation in the answer is still rejected — gate is not weakened.
    """
    import copilot.retriever as _retriever
    import copilot.ollama_client as _oc
    import copilot.repl as _repl
    import copilot.multihop as _mh

    # Two sub-queries, each returning a real chunk with different IDs.
    chunk_a = _make_chunk(chunk_id="aabbccdd11223344", score=0.87)
    chunk_b = _make_chunk(
        chunk_id="eeff00112233aabb",
        text="Deciat is the system where Felicity Farseer operates.",
        score=0.82,
    )
    result_a = RetrievalResult(query="q1", chunks=[chunk_a], max_score=0.87, grounded=True)
    result_b = RetrievalResult(query="q2", chunks=[chunk_b], max_score=0.82, grounded=True)

    # retrieve returns alternating results for the two sub-queries
    retrieve_results = [result_a, result_b]
    retrieve_call_count = {"n": 0}

    def _mock_retrieve(query, *, top_k=None, filters=None):
        idx = retrieve_call_count["n"] % len(retrieve_results)
        retrieve_call_count["n"] += 1
        return retrieve_results[idx]

    monkeypatch.setattr(_retriever, "retrieve", _mock_retrieve)

    # Decompose into exactly 2 sub-queries
    monkeypatch.setattr(_mh, "decompose", lambda q: ["part 1 of query", "part 2 of query"])

    # The model fabricates a citation NOT in the union result
    fabricated_answer = "Farseer unlocks FSDs [deadbeef12345678]."

    def _mock_stream(messages, model=None):
        yield fabricated_answer

    monkeypatch.setattr(_oc, "chat_stream", _mock_stream)

    # Force multihop=true via config patch
    import copilot.paths as _paths
    original_load_config = _paths.load_config

    def _cfg_with_multihop_on():
        cfg = original_load_config()
        cfg.setdefault("copilot", {})["multihop"] = True
        cfg["copilot"]["max_regen"] = 0  # skip regen to simplify test
        return cfg

    monkeypatch.setattr(_paths, "load_config", _cfg_with_multihop_on)
    monkeypatch.setattr(_repl, "load_config", _cfg_with_multihop_on)

    from copilot.repl import answer
    from copilot.assemble import REFUSAL

    result = answer("which engineer unlocks FSD and where are they", STATE)
    # Fabricated citation must be rejected → REFUSAL
    assert result == REFUSAL, f"Expected REFUSAL for fabricated citation, got: {result!r}"


# ---------------------------------------------------------------------------
# A2-5: empty context refusal on multihop path
# ---------------------------------------------------------------------------

def test_multihop_empty_context_refuses(monkeypatch):
    """With multihop=true, if every sub-query retrieval is empty/ungrounded,
    answer() returns REFUSAL (empty-context refusal invariant holds on union path)."""
    import copilot.retriever as _retriever
    import copilot.repl as _repl
    import copilot.multihop as _mh
    import copilot.paths as _paths

    # Every sub-query returns empty/ungrounded
    empty = _empty_result()
    monkeypatch.setattr(_retriever, "retrieve", lambda *a, **kw: empty)
    monkeypatch.setattr(_mh, "decompose", lambda q: ["part1", "part2"])

    original_load_config = _paths.load_config

    def _cfg_with_multihop_on():
        cfg = original_load_config()
        cfg.setdefault("copilot", {})["multihop"] = True
        return cfg

    monkeypatch.setattr(_paths, "load_config", _cfg_with_multihop_on)
    monkeypatch.setattr(_repl, "load_config", _cfg_with_multihop_on)

    from copilot.repl import answer
    from copilot.assemble import REFUSAL

    result = answer("multi-hop query that finds nothing", STATE)
    assert result == REFUSAL, f"Expected REFUSAL on empty union, got: {result!r}"


# ---------------------------------------------------------------------------
# A2-6: multihop=true with valid cited answer passes gate
# ---------------------------------------------------------------------------

def test_multihop_valid_answer_passes_gate(monkeypatch):
    """With multihop=true and a properly cited answer, answer() returns the answer."""
    import copilot.retriever as _retriever
    import copilot.ollama_client as _oc
    import copilot.repl as _repl
    import copilot.multihop as _mh
    import copilot.paths as _paths

    chunk_a = _make_chunk(chunk_id="aabbccdd11223344", score=0.87)
    result_a = RetrievalResult(query="q1", chunks=[chunk_a], max_score=0.87, grounded=True)
    monkeypatch.setattr(_retriever, "retrieve", lambda *a, **kw: result_a)
    monkeypatch.setattr(_mh, "decompose", lambda q: ["part1", "part2"])

    cited_answer = "Farseer needs Meta-Alloys to unlock [aabbccdd11223344]."

    def _mock_stream(messages, model=None):
        yield cited_answer

    monkeypatch.setattr(_oc, "chat_stream", _mock_stream)

    original_load_config = _paths.load_config

    def _cfg_with_multihop_on():
        cfg = original_load_config()
        cfg.setdefault("copilot", {})["multihop"] = True
        return cfg

    monkeypatch.setattr(_paths, "load_config", _cfg_with_multihop_on)
    monkeypatch.setattr(_repl, "load_config", _cfg_with_multihop_on)

    from copilot.repl import answer
    result = answer("test query", STATE)
    assert result == cited_answer
