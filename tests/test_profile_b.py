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


# ---------------------------------------------------------------------------
# Task 7: bootstrap CLI / merge+write logic
# ---------------------------------------------------------------------------

class TestBootstrap:
    def test_bootstrap_writes_duvrazh_md(self, tmp_path, monkeypatch):
        """Bootstrap should update cmdr/duvrazh.md with merged facts."""
        import copilot.profile_sources as ps_mod
        from copilot import paths as paths_mod

        # Point repo_root to tmp_path so we don't touch real files.
        monkeypatch.setattr(paths_mod, "repo_root", lambda: tmp_path)
        cmdr_dir = tmp_path / "cmdr"
        cmdr_dir.mkdir()
        (cmdr_dir / "duvrazh.md").write_text(
            "---\nname: Duvrazh\n---\n# CMDR Duvrazh\n", encoding="utf-8"
        )

        mock_fact = ProfileFact(
            key="rank.combat",
            value="Expert",
            origin="game-state-json",
            freshness="2026-06-01T10:00:00+00:00",
            verified=True,
        )

        class _FakeSrc:
            origin = "game-state-json"
            def get_facts(self):
                return [mock_fact]

        monkeypatch.setattr(ps_mod, "available_sources", lambda: [_FakeSrc()])

        # Patch vision ingest to return known facts.
        screenshot_fact = ProfileFact(
            key="rank.trade",
            value="Elite V",
            origin="screenshot",
            freshness="2026-06-01T00:00:00+00:00",
            verified=False,
        )

        with patch("copilot.profile_sources.ingest_screenshot", return_value=[screenshot_fact]):
            from copilot.profile_sources import bootstrap
            bootstrap(screenshot_path=None)  # None → skip vision ingest in test

        profile_text = (cmdr_dir / "duvrazh.md").read_text(encoding="utf-8")
        assert "rank.combat" in profile_text or "Expert" in profile_text

    def test_bootstrap_skips_vision_when_no_screenshot(self, tmp_path, monkeypatch):
        """If screenshot_path is None or missing, bootstrap must not crash."""
        import copilot.profile_sources as ps_mod
        from copilot import paths as paths_mod

        monkeypatch.setattr(paths_mod, "repo_root", lambda: tmp_path)
        cmdr_dir = tmp_path / "cmdr"
        cmdr_dir.mkdir()
        (cmdr_dir / "duvrazh.md").write_text("---\nname: Duvrazh\n---\n", encoding="utf-8")
        monkeypatch.setattr(ps_mod, "available_sources", lambda: [])

        from copilot.profile_sources import bootstrap
        bootstrap(screenshot_path=None)  # Should complete without error.

    def test_bootstrap_merges_vision_facts_at_screenshot_priority(self, tmp_path, monkeypatch):
        """Vision facts (screenshot) must lose to journal facts for the same key."""
        import copilot.profile_sources as ps_mod
        from copilot import paths as paths_mod

        monkeypatch.setattr(paths_mod, "repo_root", lambda: tmp_path)
        cmdr_dir = tmp_path / "cmdr"
        cmdr_dir.mkdir()
        (cmdr_dir / "duvrazh.md").write_text("---\nname: Duvrazh\n---\n", encoding="utf-8")

        journal_fact = ProfileFact(
            key="rank.combat",
            value="Expert",
            origin="journal",
            freshness="2026-05-01T09:01:00+00:00",
            verified=True,
        )
        vision_fact = ProfileFact(
            key="rank.combat",
            value="Master",  # lower-trust; should lose.
            origin="screenshot",
            freshness="2026-01-01T00:00:00+00:00",
            verified=False,
        )

        class _JournalSrc:
            origin = "journal"
            def get_facts(self):
                return [journal_fact]

        monkeypatch.setattr(ps_mod, "available_sources", lambda: [_JournalSrc()])

        fake_screenshot = tmp_path / "fake.png"
        fake_screenshot.write_bytes(b"\x89PNG\r\n")

        with patch("copilot.profile_sources.ingest_screenshot", return_value=[vision_fact]):
            from copilot.profile_sources import bootstrap
            bootstrap(screenshot_path=str(fake_screenshot))

        profile_text = (cmdr_dir / "duvrazh.md").read_text(encoding="utf-8")
        assert "Expert" in profile_text
        assert "Master" not in profile_text
