"""Tests for copilot.profile_sources."""
from __future__ import annotations

import json
from pathlib import Path
import pytest

from copilot.models import ProfileFact

# Fixtures dir relative to this test file.
FIXTURES = Path(__file__).parent / "fixtures"


# ---------------------------------------------------------------------------
# Task 2: parse_game_state
# ---------------------------------------------------------------------------

def _write_game_state_files(dir_: Path) -> None:
    """Copy fixture JSON files into a tmp dir to simulate Saved Games."""
    for fname in ("status.json", "cargo.json", "ship_locker.json", "fleet_carrier.json"):
        src = FIXTURES / fname
        if src.exists():
            (dir_ / fname.replace("_", "").lower()).write_text(
                src.read_text(encoding="utf-8"), encoding="utf-8"
            )
            # Also write with canonical capitalisation the game uses.
            canonical = {
                "status.json": "Status.json",
                "cargo.json": "Cargo.json",
                "ship_locker.json": "ShipLocker.json",
                "fleet_carrier.json": "FleetCarrier.json",  # not written by the game; handled via journal
            }
            (dir_ / canonical[fname]).write_text(
                src.read_text(encoding="utf-8"), encoding="utf-8"
            )


class TestParseGameState:
    def test_returns_list_of_profile_facts(self, tmp_path):
        from copilot.profile_sources import parse_game_state
        _write_game_state_files(tmp_path)
        facts = parse_game_state(tmp_path)
        assert isinstance(facts, list)
        assert all(isinstance(f, ProfileFact) for f in facts)

    def test_origin_is_game_state_json(self, tmp_path):
        from copilot.profile_sources import parse_game_state
        _write_game_state_files(tmp_path)
        facts = parse_game_state(tmp_path)
        assert len(facts) > 0
        assert all(f.origin == "game-state-json" for f in facts)

    def test_verified_is_true(self, tmp_path):
        from copilot.profile_sources import parse_game_state
        _write_game_state_files(tmp_path)
        facts = parse_game_state(tmp_path)
        assert all(f.verified is True for f in facts)

    def test_balance_extracted_from_status(self, tmp_path):
        from copilot.profile_sources import parse_game_state
        _write_game_state_files(tmp_path)
        facts = parse_game_state(tmp_path)
        balance_facts = [f for f in facts if f.key == "balance_cr"]
        assert len(balance_facts) == 1
        assert balance_facts[0].value == "3200000000"

    def test_carrier_name_extracted_from_fleet_carrier(self, tmp_path):
        from copilot.profile_sources import parse_game_state
        _write_game_state_files(tmp_path)
        facts = parse_game_state(tmp_path)
        carrier_facts = [f for f in facts if "carrier" in f.key and "name" in f.key]
        assert len(carrier_facts) >= 1
        assert any("THE LONG HAUL" in f.value for f in carrier_facts)

    def test_empty_dir_returns_empty_list(self, tmp_path):
        from copilot.profile_sources import parse_game_state
        facts = parse_game_state(tmp_path)
        assert facts == []

    def test_malformed_json_skipped_gracefully(self, tmp_path):
        from copilot.profile_sources import parse_game_state
        (tmp_path / "Status.json").write_text("{bad json", encoding="utf-8")
        # Should not raise; returns whatever valid files it can parse.
        facts = parse_game_state(tmp_path)
        assert isinstance(facts, list)


# ---------------------------------------------------------------------------
# Task 3: parse_journal
# ---------------------------------------------------------------------------

class TestParseJournal:
    def test_returns_list_of_profile_facts(self):
        from copilot.profile_sources import parse_journal
        facts = parse_journal(FIXTURES / "sample_journal.log")
        assert isinstance(facts, list)
        assert len(facts) > 0

    def test_origin_is_journal(self):
        from copilot.profile_sources import parse_journal
        facts = parse_journal(FIXTURES / "sample_journal.log")
        assert all(f.origin == "journal" for f in facts)

    def test_verified_is_true(self):
        from copilot.profile_sources import parse_journal
        facts = parse_journal(FIXTURES / "sample_journal.log")
        assert all(f.verified is True for f in facts)

    def test_rank_combat_extracted(self):
        from copilot.profile_sources import parse_journal
        facts = parse_journal(FIXTURES / "sample_journal.log")
        combat = [f for f in facts if f.key == "rank.combat"]
        assert len(combat) == 1
        assert combat[0].value == "Expert"   # index 4 in _COMBAT_RANKS

    def test_rank_trade_extracted(self):
        from copilot.profile_sources import parse_journal
        facts = parse_journal(FIXTURES / "sample_journal.log")
        trade = [f for f in facts if f.key == "rank.trade"]
        assert len(trade) == 1
        assert trade[0].value == "Elite I"   # journal Trade index 9 → _TRADE_RANKS[9] == "Elite I"

    def test_balance_extracted_from_statistics(self):
        from copilot.profile_sources import parse_journal
        facts = parse_journal(FIXTURES / "sample_journal.log")
        balance = [f for f in facts if f.key == "balance_cr"]
        assert len(balance) >= 1
        assert balance[0].value == "3200000000"

    def test_engineer_progress_extracted(self):
        from copilot.profile_sources import parse_journal
        facts = parse_journal(FIXTURES / "sample_journal.log")
        farseer = [f for f in facts if "farseer" in f.key.lower() or
                   ("engineer" in f.key and "felicity" in f.value.lower())]
        # At minimum expect an engineer rank fact for Felicity Farseer
        eng_facts = [f for f in facts if f.key.startswith("engineer.")]
        assert len(eng_facts) >= 1

    def test_carrier_stats_extracted(self):
        from copilot.profile_sources import parse_journal
        facts = parse_journal(FIXTURES / "sample_journal.log")
        carrier = [f for f in facts if "carrier" in f.key]
        assert len(carrier) >= 1

    def test_loadout_ship_extracted(self):
        from copilot.profile_sources import parse_journal
        facts = parse_journal(FIXTURES / "sample_journal.log")
        ship = [f for f in facts if f.key.startswith("ship.") and "name" in f.key]
        assert len(ship) >= 1
        assert any("IMPERIAL BLADE" in f.value for f in ship)

    def test_organic_scan_extracted(self):
        from copilot.profile_sources import parse_journal
        facts = parse_journal(FIXTURES / "sample_journal.log")
        organic = [f for f in facts if "organic" in f.key or "exobio" in f.key]
        assert len(organic) >= 1

    def test_nonexistent_file_raises_file_not_found(self):
        from copilot.profile_sources import parse_journal
        with pytest.raises(FileNotFoundError):
            parse_journal(Path("/no/such/journal.log"))


# ---------------------------------------------------------------------------
# Task 4: ProfileSource classes + available_sources
# ---------------------------------------------------------------------------

class TestProfileSourceClasses:
    def test_game_state_source_origin(self, tmp_path):
        from copilot.profile_sources import GameStateSource
        src = GameStateSource(tmp_path)
        assert src.origin == "game-state-json"

    def test_game_state_source_get_facts_empty_dir(self, tmp_path):
        from copilot.profile_sources import GameStateSource
        src = GameStateSource(tmp_path)
        assert src.get_facts() == []

    def test_game_state_source_get_facts_with_files(self, tmp_path):
        from copilot.profile_sources import GameStateSource
        _write_game_state_files(tmp_path)
        src = GameStateSource(tmp_path)
        facts = src.get_facts()
        assert len(facts) > 0

    def test_journal_source_origin(self):
        from copilot.profile_sources import JournalSource
        src = JournalSource(FIXTURES / "sample_journal.log")
        assert src.origin == "journal"

    def test_journal_source_get_facts(self):
        from copilot.profile_sources import JournalSource
        src = JournalSource(FIXTURES / "sample_journal.log")
        facts = src.get_facts()
        assert len(facts) > 0
        assert all(f.origin == "journal" for f in facts)

    def test_third_party_source_origin(self, tmp_path):
        from copilot.profile_sources import ThirdPartySource
        src = ThirdPartySource(tmp_path, label="edmc")
        assert src.origin == "3rd-party"

    def test_third_party_source_empty_returns_empty(self, tmp_path):
        from copilot.profile_sources import ThirdPartySource
        src = ThirdPartySource(tmp_path, label="edmc")
        assert src.get_facts() == []

    def test_available_sources_returns_list(self, tmp_path, monkeypatch):
        from copilot import profile_sources
        monkeypatch.setattr(profile_sources, "saved_games_dir", lambda: tmp_path)
        _write_game_state_files(tmp_path)
        sources = profile_sources.available_sources()
        assert isinstance(sources, list)
        assert len(sources) >= 1

    def test_available_sources_none_when_no_saved_games(self, monkeypatch):
        from copilot import profile_sources
        monkeypatch.setattr(profile_sources, "saved_games_dir", lambda: None)
        sources = profile_sources.available_sources()
        # Should return only third-party or empty — never crash.
        assert isinstance(sources, list)

    def test_available_sources_implements_protocol(self, tmp_path, monkeypatch):
        """Each returned source must have .origin (str) and .get_facts() callable."""
        from copilot import profile_sources
        monkeypatch.setattr(profile_sources, "saved_games_dir", lambda: tmp_path)
        _write_game_state_files(tmp_path)
        for src in profile_sources.available_sources():
            assert hasattr(src, "origin")
            assert callable(getattr(src, "get_facts"))
