# tests/test_models.py
"""Tests for copilot/models.py — dataclass field names, types, and invariants."""

import dataclasses
import pytest


# ---------------------------------------------------------------------------
# Chunk
# ---------------------------------------------------------------------------

def make_chunk(**overrides):
    from copilot.models import Chunk
    defaults = dict(
        chunk_id="abc123def456789a",
        text="Felicity Farseer > Unlock: Need an Asp Explorer",
        kb_path="kb/engineers/felicity-farseer.md",
        heading_path="Felicity Farseer > Unlock",
        source_url="https://inara.cz/engineers",
        source_tier=1,
        source_count=2,
        verified=True,
        availability="live",
        changed_note=None,
        score=0.0,
    )
    defaults.update(overrides)
    return Chunk(**defaults)


def test_chunk_is_frozen():
    chunk = make_chunk()
    with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
        chunk.score = 0.99  # type: ignore


def test_chunk_default_score_zero():
    chunk = make_chunk()
    assert chunk.score == 0.0


def test_chunk_replace_score():
    """Scores are injected at retrieval time via dataclasses.replace (not mutation)."""
    chunk = make_chunk()
    scored = dataclasses.replace(chunk, score=0.87)
    assert scored.score == 0.87
    assert chunk.score == 0.0  # original unmodified


def test_chunk_fields_present():
    from copilot.models import Chunk
    field_names = {f.name for f in dataclasses.fields(Chunk)}
    required = {
        "chunk_id", "text", "kb_path", "heading_path",
        "source_url", "source_tier", "source_count",
        "verified", "availability", "changed_note", "score",
    }
    assert required <= field_names, f"Missing fields: {required - field_names}"


def test_chunk_source_url_nullable():
    chunk = make_chunk(source_url=None)
    assert chunk.source_url is None


def test_chunk_changed_note_nullable():
    chunk = make_chunk(changed_note="PP1 -> PP2 in 2024")
    assert chunk.changed_note == "PP1 -> PP2 in 2024"


# ---------------------------------------------------------------------------
# RetrievalResult
# ---------------------------------------------------------------------------

def test_retrieval_result_fields():
    from copilot.models import RetrievalResult
    field_names = {f.name for f in dataclasses.fields(RetrievalResult)}
    assert {"query", "chunks", "max_score", "grounded"} <= field_names


def test_retrieval_result_grounded_flag():
    from copilot.models import RetrievalResult
    result = RetrievalResult(
        query="unlock farseer",
        chunks=[make_chunk(score=0.72)],
        max_score=0.72,
        grounded=True,
    )
    assert result.grounded is True


def test_retrieval_result_not_grounded():
    from copilot.models import RetrievalResult
    result = RetrievalResult(
        query="unlock farseer",
        chunks=[make_chunk(score=0.30)],
        max_score=0.30,
        grounded=False,
    )
    assert result.grounded is False


# ---------------------------------------------------------------------------
# ProfileFact
# ---------------------------------------------------------------------------

def test_profile_fact_fields():
    from copilot.models import ProfileFact
    field_names = {f.name for f in dataclasses.fields(ProfileFact)}
    assert {"key", "value", "origin", "freshness", "verified"} <= field_names


def test_profile_fact_construction():
    from copilot.models import ProfileFact
    fact = ProfileFact(
        key="rank.combat",
        value="Expert",
        origin="journal",
        freshness="2026-05-15",
        verified=True,
    )
    assert fact.key == "rank.combat"
    assert fact.origin == "journal"


# ---------------------------------------------------------------------------
# CmdrState
# ---------------------------------------------------------------------------

def test_cmdr_state_default_factories():
    from copilot.models import CmdrState
    state = CmdrState(name="Duvrazh")
    assert state.ranks == {}
    assert state.balance_cr is None
    assert state.assets == {}
    assert state.goals == []
    assert state.facts == []


def test_cmdr_state_independence():
    """Two CmdrState instances must not share default mutable containers."""
    from copilot.models import CmdrState
    a = CmdrState(name="Alpha")
    b = CmdrState(name="Beta")
    a.ranks["combat"] = "Elite"
    assert "combat" not in b.ranks


def test_cmdr_state_with_profile_facts():
    from copilot.models import CmdrState, ProfileFact
    fact = ProfileFact(
        key="balance_cr", value="3000000000",
        origin="manual", freshness="unknown", verified=False,
    )
    state = CmdrState(name="Duvrazh", facts=[fact])
    assert len(state.facts) == 1
    assert state.facts[0].key == "balance_cr"
