"""Tests for copilot.data_discovery — all FS interaction via tmp_path + monkeypatch."""
import json
import os
from pathlib import Path
import pytest

from copilot.data_discovery import saved_games_dir, discover_data_sources


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def fake_home(tmp_path, monkeypatch):
    """Minimal fake %USERPROFILE% tree with the Saved Games journal dir."""
    home = tmp_path / "Users" / "CMDR"
    sg = home / "Saved Games" / "Frontier Developments" / "Elite Dangerous"
    sg.mkdir(parents=True)
    # A few fake game-state JSON files
    (sg / "Status.json").write_text('{"timestamp":"2026-06-01T00:00:00Z","event":"Status"}', encoding="utf-8")
    (sg / "Cargo.json").write_text('{"timestamp":"2026-06-01T00:00:00Z","event":"Cargo","Inventory":[]}', encoding="utf-8")
    # EDMC app data
    edmc_appdata = home / "AppData" / "Local" / "EDMarketConnector"
    edmc_appdata.mkdir(parents=True)
    (edmc_appdata / "netLog.txt").write_text("net log stub", encoding="utf-8")
    # Screenshots folder
    screenshots = home / "Pictures" / "Frontier Developments" / "Elite Dangerous"
    screenshots.mkdir(parents=True)
    (screenshots / "rank-screen.png").write_bytes(b"\x89PNG\r\n")

    monkeypatch.setenv("USERPROFILE", str(home))
    monkeypatch.setenv("LOCALAPPDATA", str(home / "AppData" / "Local"))
    monkeypatch.setenv("APPDATA", str(home / "AppData" / "Roaming"))
    return home


@pytest.fixture()
def no_saved_games(tmp_path, monkeypatch):
    """Home dir without Saved Games — saved_games_dir() must return None."""
    home = tmp_path / "Users" / "NoGame"
    home.mkdir(parents=True)
    monkeypatch.setenv("USERPROFILE", str(home))
    return home


# ---------------------------------------------------------------------------
# saved_games_dir
# ---------------------------------------------------------------------------

def test_saved_games_dir_returns_path_when_present(fake_home):
    result = saved_games_dir()
    assert result is not None
    assert result.is_dir()
    assert (result / "Status.json").exists()


def test_saved_games_dir_returns_none_when_absent(no_saved_games):
    result = saved_games_dir()
    assert result is None


# ---------------------------------------------------------------------------
# discover_data_sources
# ---------------------------------------------------------------------------

def test_discover_finds_saved_games_dir(fake_home, tmp_path, monkeypatch):
    # Route indexes/ into tmp_path so we don't touch the real repo
    indexes = tmp_path / "indexes"
    indexes.mkdir()
    monkeypatch.setattr("copilot.paths.indexes_dir", lambda: indexes)

    manifest = discover_data_sources()

    paths_found = [e["path"] for e in manifest]
    sg_path = str(fake_home / "Saved Games" / "Frontier Developments" / "Elite Dangerous")
    assert any(sg_path in p for p in paths_found), "Saved Games dir not in manifest"


def test_discover_includes_edmc(fake_home, tmp_path, monkeypatch):
    indexes = tmp_path / "indexes"
    indexes.mkdir()
    monkeypatch.setattr("copilot.paths.indexes_dir", lambda: indexes)

    manifest = discover_data_sources()

    types = [e["type"] for e in manifest]
    assert "edmc" in types


def test_discover_includes_screenshots(fake_home, tmp_path, monkeypatch):
    indexes = tmp_path / "indexes"
    indexes.mkdir()
    monkeypatch.setattr("copilot.paths.indexes_dir", lambda: indexes)

    manifest = discover_data_sources()

    types = [e["type"] for e in manifest]
    assert "screenshots" in types


def test_discover_writes_json_manifest(fake_home, tmp_path, monkeypatch):
    indexes = tmp_path / "indexes"
    indexes.mkdir()
    monkeypatch.setattr("copilot.paths.indexes_dir", lambda: indexes)

    discover_data_sources()

    manifest_path = indexes / "data-sources.json"
    assert manifest_path.exists()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert isinstance(data, list)
    assert len(data) > 0
    required_keys = {"path", "type", "last_modified", "ingest_status"}
    for entry in data:
        assert required_keys <= entry.keys(), f"Entry missing keys: {entry}"


def test_discover_never_writes_outside_indexes(fake_home, tmp_path, monkeypatch):
    """Guard: discover_data_sources() must not write into the scanned dirs."""
    indexes = tmp_path / "indexes"
    indexes.mkdir()
    monkeypatch.setattr("copilot.paths.indexes_dir", lambda: indexes)

    sg = fake_home / "Saved Games" / "Frontier Developments" / "Elite Dangerous"
    files_before = set(sg.iterdir())

    discover_data_sources()

    files_after = set(sg.iterdir())
    assert files_before == files_after, "discover_data_sources() wrote into Saved Games dir"


def test_discover_manifest_entries_have_valid_ingest_status(fake_home, tmp_path, monkeypatch):
    indexes = tmp_path / "indexes"
    indexes.mkdir()
    monkeypatch.setattr("copilot.paths.indexes_dir", lambda: indexes)

    manifest = discover_data_sources()

    valid_statuses = {"pending", "ingested", "skipped"}
    for entry in manifest:
        assert entry["ingest_status"] in valid_statuses, f"Bad ingest_status: {entry}"
