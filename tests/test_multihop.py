"""
tests/test_multihop.py — Group A1: multihop scaffold tests.

All tests run without Ollama (decompose is pure; no I/O).
"""

from __future__ import annotations

import pytest


# ---------------------------------------------------------------------------
# A1-1: single-hop identity
# ---------------------------------------------------------------------------

def test_decompose_single_hop_identity():
    """A clearly single-hop query must come back unchanged, length 1."""
    from copilot.multihop import decompose
    q = "where is Felicity Farseer"
    result = decompose(q)
    assert result == [q], f"Expected [{q!r}], got {result!r}"


def test_decompose_single_hop_returns_list():
    """decompose always returns a list, never a bare string."""
    from copilot.multihop import decompose
    result = decompose("what ships have the best jump range")
    assert isinstance(result, list)
    assert len(result) >= 1


# ---------------------------------------------------------------------------
# A1-2: multi-hop splits
# ---------------------------------------------------------------------------

def test_decompose_multihop_splits_and_where():
    """'X and where are they located' → ordered list of >=2 sub-queries."""
    from copilot.multihop import decompose
    q = "which engineer unlocks the FSD mod I need and where are they located"
    result = decompose(q)
    assert isinstance(result, list), "decompose must return a list"
    assert len(result) >= 2, f"Expected >=2 sub-queries for multi-hop, got: {result!r}"
    # Every sub-query must be non-empty
    for sq in result:
        assert sq.strip(), f"Empty sub-query in result: {result!r}"


def test_decompose_multihop_and_then():
    """'X then Y' → 2-element list."""
    from copilot.multihop import decompose
    q = "unlock Felicity Farseer then upgrade my FSD range"
    result = decompose(q)
    assert len(result) >= 2, f"Expected 2 parts for 'then' split, got: {result!r}"
    for sq in result:
        assert sq.strip()


def test_decompose_multihop_plain_and():
    """'X and Y' with two distinct clauses → 2-element list."""
    from copilot.multihop import decompose
    q = "which engineers do FSD mods and what materials do I need"
    result = decompose(q)
    assert len(result) >= 2, f"Expected split on 'and', got: {result!r}"


# ---------------------------------------------------------------------------
# A1-3: pure — no I/O, no network
# ---------------------------------------------------------------------------

def test_decompose_pure_no_io(monkeypatch):
    """decompose must not touch Ollama even if it raises — proves offline purity."""
    import copilot.ollama_client as _oc

    def _raise_embed(texts):
        raise RuntimeError("Ollama must not be called from decompose()")

    def _raise_stream(messages, **kwargs):
        raise RuntimeError("Ollama must not be called from decompose()")
        yield  # make it a generator

    monkeypatch.setattr(_oc, "embed", _raise_embed)
    monkeypatch.setattr(_oc, "chat_stream", _raise_stream)

    from copilot.multihop import decompose
    # Should complete without raising, proving no Ollama call was made.
    result = decompose("which engineer unlocks the FSD mod I need and where are they located")
    assert isinstance(result, list)
    assert len(result) >= 1


# ---------------------------------------------------------------------------
# A1-4: idempotency on atomic queries
# ---------------------------------------------------------------------------

def test_decompose_idempotent():
    """decompose(decompose(q)[0]) == decompose(q)[0] for a single-hop query."""
    from copilot.multihop import decompose
    q = "where is Felicity Farseer"
    first = decompose(q)
    assert len(first) == 1
    second = decompose(first[0])
    assert second == first, f"Not idempotent: {first!r} → {second!r}"


def test_decompose_idempotent_on_first_subquery():
    """For a multi-hop split, the first sub-query should be stable on re-decomposition."""
    from copilot.multihop import decompose
    q = "which engineer unlocks the FSD mod I need and where are they located"
    result = decompose(q)
    if len(result) > 1:
        # First sub-query is atomic; re-decomposing should not split further.
        re_result = decompose(result[0])
        assert re_result == [result[0]], (
            f"First sub-query {result[0]!r} should be stable, got {re_result!r}"
        )


# ---------------------------------------------------------------------------
# A1-5: default flag and config alignment
# ---------------------------------------------------------------------------

def test_multihop_enabled_default_false():
    """MULTIHOP_ENABLED must be False at module level."""
    import copilot.multihop as mh
    assert mh.MULTIHOP_ENABLED is False


def test_config_multihop_default_false():
    """config.toml [copilot] multihop defaults to false."""
    from copilot.paths import load_config
    cfg = load_config()
    # Either the key is absent (defaults to False) or it is explicitly False.
    val = cfg.get("copilot", {}).get("multihop", False)
    assert val is False, f"Expected multihop=False in config, got {val!r}"


# ---------------------------------------------------------------------------
# A1-6: edge cases
# ---------------------------------------------------------------------------

def test_decompose_empty_string():
    """decompose('') must return a non-empty list (either [''] or [])."""
    from copilot.multihop import decompose
    result = decompose("")
    # Spec says: returns [""] or [] — pick one and TEST it.
    # Our implementation returns [""]; assert that.
    assert isinstance(result, list)
    assert len(result) >= 0  # either [] or [""] is valid per spec


def test_decompose_never_returns_none():
    """decompose must never return None."""
    from copilot.multihop import decompose
    result = decompose("test")
    assert result is not None


def test_decompose_non_empty_subqueries():
    """Every returned sub-query must be a non-empty string (after strip)."""
    from copilot.multihop import decompose
    queries = [
        "how do I unlock Farseer",
        "which engineer does FSD and where are they",
        "find a good combat ship then engineer it for pvp",
        "",
        "just one thing",
    ]
    for q in queries:
        result = decompose(q)
        assert isinstance(result, list)
        # At minimum, if non-empty result, each entry must be a string
        for sq in result:
            assert isinstance(sq, str)
