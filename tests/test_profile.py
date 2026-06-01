"""Tests for copilot/profile.py — ManualProfile, merge_state, priority override."""
import textwrap
from pathlib import Path

import pytest

from copilot.models import CmdrState, ProfileFact


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

SAMPLE_DUVRAZH_MD = textwrap.dedent("""\
    ---
    name: Duvrazh
    rank_combat: Expert
    rank_trade: Elite V
    rank_explorer: Elite
    rank_exobiologist: Directionless
    rank_mercenary: Defenceless
    rank_cqc: Helpless
    balance_cr: 3000000000
    ---

    # CMDR Duvrazh

    - 2 fleet carriers
    - Goals: engineering, AX combat, exobiology, colonisation, Odyssey on-foot
""")


def _write_profile(tmp_path: Path, content: str = SAMPLE_DUVRAZH_MD) -> Path:
    p = tmp_path / "cmdr" / "duvrazh.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# ManualProfile
# ---------------------------------------------------------------------------

def test_manual_profile_parses_ranks(tmp_path, monkeypatch):
    profile_path = _write_profile(tmp_path)
    monkeypatch.setattr("copilot.paths.repo_root", lambda: tmp_path)

    from copilot.profile import ManualProfile
    mp = ManualProfile()
    facts = mp.get_facts()

    keys = {f.key for f in facts}
    assert "rank.combat" in keys
    assert "rank.trade" in keys

    combat_fact = next(f for f in facts if f.key == "rank.combat")
    assert combat_fact.value == "Expert"
    assert combat_fact.origin == "manual"
    assert combat_fact.verified is False


def test_manual_profile_parses_balance(tmp_path, monkeypatch):
    _write_profile(tmp_path)
    monkeypatch.setattr("copilot.paths.repo_root", lambda: tmp_path)

    from copilot.profile import ManualProfile
    mp = ManualProfile()
    facts = mp.get_facts()

    balance_fact = next((f for f in facts if f.key == "balance_cr"), None)
    assert balance_fact is not None
    assert balance_fact.value == "3000000000"


def test_manual_profile_parses_body_bullets(tmp_path, monkeypatch):
    _write_profile(tmp_path)
    monkeypatch.setattr("copilot.paths.repo_root", lambda: tmp_path)

    from copilot.profile import ManualProfile
    mp = ManualProfile()
    facts = mp.get_facts()

    body_keys = {f.key for f in facts if f.key.startswith("note.")}
    assert len(body_keys) >= 1  # at least one body-bullet fact


# ---------------------------------------------------------------------------
# merge_state priority
# ---------------------------------------------------------------------------

def test_higher_priority_source_wins(tmp_path, monkeypatch):
    """A 'journal' origin fact overrides a 'manual' origin fact for the same key."""
    _write_profile(tmp_path)
    monkeypatch.setattr("copilot.paths.repo_root", lambda: tmp_path)

    from copilot.profile import ManualProfile, merge_state, ORIGIN_PRIORITY

    assert ORIGIN_PRIORITY.index("journal") < ORIGIN_PRIORITY.index("manual")

    class FakeJournalSource:
        origin = "journal"

        def get_facts(self) -> list[ProfileFact]:
            return [
                ProfileFact(
                    key="rank.combat",
                    value="Elite",           # higher than Expert from manual
                    origin="journal",
                    freshness="2026-05-01",
                    verified=True,
                )
            ]

    state = merge_state([FakeJournalSource(), ManualProfile()])
    assert state.ranks.get("combat") == "Elite"  # journal wins


def test_merge_state_populates_cmdr_state(tmp_path, monkeypatch):
    _write_profile(tmp_path)
    monkeypatch.setattr("copilot.paths.repo_root", lambda: tmp_path)

    from copilot.profile import ManualProfile, merge_state
    state = merge_state([ManualProfile()])

    assert isinstance(state, CmdrState)
    assert state.name == "Duvrazh"
    assert "combat" in state.ranks
    assert state.balance_cr == 3_000_000_000


def test_load_cmdr_state_no_profile_sources(tmp_path, monkeypatch):
    """load_cmdr_state works when copilot.profile_sources is absent (ImportError path)."""
    _write_profile(tmp_path)
    monkeypatch.setattr("copilot.paths.repo_root", lambda: tmp_path)

    import sys
    # Ensure profile_sources is NOT importable.
    sys.modules.pop("copilot.profile_sources", None)
    monkeypatch.setitem(sys.modules, "copilot.profile_sources", None)  # type: ignore[arg-type]

    from copilot.profile import load_cmdr_state
    state = load_cmdr_state()
    assert state.name == "Duvrazh"
