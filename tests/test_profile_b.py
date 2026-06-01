"""Plan B integration tests for copilot.profile — merge priority and source wiring."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from copilot.models import ProfileFact, CmdrState


# ---------------------------------------------------------------------------
# Task 6: merge priority — game-state-json beats manual for same key
# ---------------------------------------------------------------------------

class TestMergePriority:
    def test_game_state_beats_manual_for_balance(self):
        from copilot.profile import merge_state, ORIGIN_PRIORITY

        class _GameSrc:
            origin = "game-state-json"
            def get_facts(self):
                return [ProfileFact(
                    key="balance_cr",
                    value="3200000000",
                    origin="game-state-json",
                    freshness="2026-06-01T10:00:00+00:00",
                    verified=True,
                )]

        class _ManualSrc:
            origin = "manual"
            def get_facts(self):
                return [ProfileFact(
                    key="balance_cr",
                    value="1000",
                    origin="manual",
                    freshness="unknown",
                    verified=False,
                )]

        state = merge_state([_GameSrc(), _ManualSrc()])
        assert state.balance_cr == 3200000000

    def test_manual_wins_when_only_source(self):
        from copilot.profile import merge_state

        class _ManualSrc:
            origin = "manual"
            def get_facts(self):
                return [ProfileFact(
                    key="balance_cr",
                    value="42000000",
                    origin="manual",
                    freshness="unknown",
                    verified=False,
                )]

        state = merge_state([_ManualSrc()])
        assert state.balance_cr == 42000000

    def test_journal_beats_screenshot_for_rank(self):
        from copilot.profile import merge_state

        class _JournalSrc:
            origin = "journal"
            def get_facts(self):
                return [ProfileFact(
                    key="rank.combat",
                    value="Expert",
                    origin="journal",
                    freshness="2026-05-01T09:01:00+00:00",
                    verified=True,
                )]

        class _ScreenshotSrc:
            origin = "screenshot"
            def get_facts(self):
                return [ProfileFact(
                    key="rank.combat",
                    value="Master",
                    origin="screenshot",
                    freshness="2026-01-01T00:00:00+00:00",
                    verified=False,
                )]

        state = merge_state([_JournalSrc(), _ScreenshotSrc()])
        rank_fact = next((f for f in state.facts if f.key == "rank.combat"), None)
        assert rank_fact is not None
        assert rank_fact.value == "Expert"
        assert rank_fact.origin == "journal"

    def test_load_cmdr_state_prepends_available_sources(self, monkeypatch):
        """load_cmdr_state() must use available_sources() when profile_sources is importable."""
        import copilot.profile as profile_mod

        mock_fact = ProfileFact(
            key="balance_cr",
            value="9999999999",
            origin="game-state-json",
            freshness="2026-06-01T10:00:00+00:00",
            verified=True,
        )

        class _FakeSrc:
            origin = "game-state-json"
            def get_facts(self):
                return [mock_fact]

        with patch.dict("sys.modules", {}):
            import copilot.profile_sources as ps_mod
            original_available = ps_mod.available_sources
            ps_mod.available_sources = lambda: [_FakeSrc()]
            try:
                state = profile_mod.load_cmdr_state()
                assert state.balance_cr == 9999999999
            finally:
                ps_mod.available_sources = original_available

    def test_load_cmdr_state_survives_import_error(self, monkeypatch):
        """load_cmdr_state() must not crash if profile_sources is unavailable."""
        import sys
        import copilot.profile as profile_mod

        # Temporarily hide profile_sources.
        saved = sys.modules.pop("copilot.profile_sources", None)
        try:
            # Should fall back to ManualProfile only — no exception.
            state = profile_mod.load_cmdr_state()
            assert isinstance(state, CmdrState)
        finally:
            if saved is not None:
                sys.modules["copilot.profile_sources"] = saved
