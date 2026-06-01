# Plan B — Data-First Profile

**Date:** 2026-06-01
**Author:** CMDR Duvrazh / Claude Code
**Status:** Ready to execute

> **For agentic workers:** Read `CONTRACTS.md` in full before touching any file. Every
> function signature, type, path, and origin string in this plan is taken verbatim from
> CONTRACTS.md. If CONTRACTS.md and this plan conflict, CONTRACTS.md wins — stop and
> surface the discrepancy. Do not invent parameter names, do not rename functions, do not
> create files not listed here. Each task is atomic: write the failing test first, confirm
> it fails for the right reason, implement the minimum code to make it pass, then commit.
> Never skip the red-bar step.

---

## Requires Plan A complete

Plan A must be merged to `master` before any task here is started. This plan imports:
- `copilot.models` — `ProfileFact`, `CmdrState`, `ProfileSource` (Protocol)
- `copilot.profile` — `ORIGIN_PRIORITY`, `merge_state`, `load_cmdr_state`, `ManualProfile`
- `copilot.ollama_client` — `vision(image_path: str, prompt: str) -> str`, `OllamaUnavailable`
- `copilot.paths` — `repo_root()`, `indexes_dir()`, `load_config()`
- `copilot.atomic` — `write_json_atomic(path: Path, obj) -> None`

If any of the above cannot be imported, abort and fix Plan A first.

---

## Goal

Auto-populate `CmdrState` from authoritative data already on the machine: live game-state
JSON, historical Journal logs, screenshots via vision, and 3rd-party tool exports. Merge
sources by trust priority (CONTRACTS `ORIGIN_PRIORITY`) into a single `CmdrState` that
feeds every copilot answer with verified, labeled facts — never a hand-typed guess.

---

## Architecture

```
Machine scan
  data_discovery.py::discover_data_sources()
       │ writes indexes/data-sources.json
       │
       ▼
profile_sources.py
  ├── GameStateSource   (origin="game-state-json")  ← Status/Cargo/ShipLocker/FleetCarrier/…
  ├── JournalSource     (origin="journal")           ← Journal.*.log newest file
  ├── ThirdPartySource  (origin="3rd-party")         ← EDMC/EDDiscovery exports if present
  └── available_sources() → list[ProfileSource]
       │
       ▼
vision_ingest.py
  ingest_screenshot(image_path) → list[ProfileFact]  (origin="screenshot")
       │
       ▼
profile.py::load_cmdr_state()
  try-import profile_sources → prepend available_sources()
  merge_state([...sources, ManualProfile()]) → CmdrState
       │
       ▼
cmdr/duvrazh.md  (bootstrap write, then human-editable)
```

Trust priority enforced by `merge_state` (already in Plan A) using `ORIGIN_PRIORITY`:
`["game-state-json", "journal", "screenshot", "3rd-party", "manual"]`

---

## Tech Stack

- Python 3.11+, `pathlib.Path` everywhere, UTF-8 / `\n` line endings
- `json` stdlib for all JSON; no third-party JSON libs
- `re`, `glob` for file discovery; `os.environ` for env-var resolution
- `qwen3-vl:8b` via `ollama_client.vision` for screenshot parsing
- `pytest` with `tmp_path`, `monkeypatch` for all tests
- All integration tests guarded by `@pytest.mark.integration`

---

## File Structure

Files **created** by this plan (new):

```
copilot/
  data_discovery.py
  profile_sources.py
  vision_ingest.py
tests/
  test_data_discovery.py
  test_profile_sources.py
  test_vision_ingest.py
  test_profile_b.py          # merge-priority + bootstrap script tests
  fixtures/
    status.json
    fleet_carrier.json
    cargo.json
    ship_locker.json
    sample_journal.log
```

File **edited** by this plan (one sanctioned cross-plan edit):

```
copilot/profile.py            # load_cmdr_state() — try/except import profile_sources
```

No other Plan-A files are touched.

---

## Task 1 — `copilot/data_discovery.py`: saved_games_dir + discover_data_sources

### 1a. Write failing tests first

**File:** `tests/test_data_discovery.py`

```python
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
```

Run `pytest tests/test_data_discovery.py` — all tests must **fail** (ImportError or
AttributeError). Do not proceed until you see the red bar.

### 1b. Implement `copilot/data_discovery.py`

```python
"""
data_discovery.py — scan the machine for Elite Dangerous data files.

READ-ONLY: this module never writes into any game or tool folder.
Only output is indexes/data-sources.json via atomic.write_json_atomic.
"""
from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path

from copilot.atomic import write_json_atomic
from copilot.paths import indexes_dir

# Subdirectory under Saved Games that contains game-state JSON and journals.
_SAVED_GAMES_SUBPATH = Path("Saved Games") / "Frontier Developments" / "Elite Dangerous"

# 3rd-party tool dir names to scan for under LOCALAPPDATA / APPDATA.
_THIRD_PARTY_DIRS: dict[str, str] = {
    "EDMarketConnector": "edmc",
    "EDDiscovery": "eddiscovery",
    "EDEngineer": "edengineer",
    "Frontier Developments": "frontier-appdata",
}

# Screenshot sub-path under USERPROFILE/Pictures.
_SCREENSHOTS_SUBPATH = Path("Pictures") / "Frontier Developments" / "Elite Dangerous"


def saved_games_dir() -> Path | None:
    """Return the Elite Dangerous Saved Games dir if it exists, else None.

    Path: %USERPROFILE%\\Saved Games\\Frontier Developments\\Elite Dangerous
    """
    userprofile = os.environ.get("USERPROFILE", "")
    if not userprofile:
        return None
    candidate = Path(userprofile) / _SAVED_GAMES_SUBPATH
    return candidate if candidate.is_dir() else None


def _iso_mtime(path: Path) -> str:
    """Return ISO 8601 mtime for a path, or 'unknown' if stat fails."""
    try:
        mtime = path.stat().st_mtime
        return datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()
    except OSError:
        return "unknown"


def _entry(path: Path, type_: str) -> dict:
    return {
        "path": str(path),
        "type": type_,
        "last_modified": _iso_mtime(path),
        "ingest_status": "pending",
    }


def discover_data_sources() -> list[dict]:
    """Scan the machine for ED-related data and write indexes/data-sources.json.

    Scans:
    - %USERPROFILE%/Saved Games/Frontier Developments/Elite Dangerous (game-state-json)
    - %LOCALAPPDATA% and %APPDATA% for Frontier/EDMC/EDDiscovery/EDEngineer dirs
    - %USERPROFILE%/Pictures/Frontier Developments/Elite Dangerous (screenshots)
    - G:\\ root for any Frontier Developments / ED-related dirs

    Returns the manifest list (same data written to disk).
    READ-ONLY: never writes into any discovered game or tool folder.
    """
    manifest: list[dict] = []

    # 1. Saved Games game-state JSON dir.
    sg = saved_games_dir()
    if sg is not None:
        manifest.append(_entry(sg, "game-state-json"))

    # 2. LOCALAPPDATA + APPDATA — 3rd-party tools.
    for env_var in ("LOCALAPPDATA", "APPDATA"):
        base = os.environ.get(env_var, "")
        if not base:
            continue
        base_path = Path(base)
        for dir_name, type_label in _THIRD_PARTY_DIRS.items():
            candidate = base_path / dir_name
            if candidate.is_dir():
                manifest.append(_entry(candidate, type_label))

    # 3. Screenshots folder.
    userprofile = os.environ.get("USERPROFILE", "")
    if userprofile:
        screenshots = Path(userprofile) / _SCREENSHOTS_SUBPATH
        if screenshots.is_dir():
            manifest.append(_entry(screenshots, "screenshots"))

    # 4. G:\ drive root — look for Frontier / ED-named directories.
    g_root = Path("G:\\")
    if g_root.is_dir():
        try:
            for child in g_root.iterdir():
                if child.is_dir() and any(
                    kw in child.name.lower()
                    for kw in ("frontier", "elite", "dangerous", "edkb", "elitedangerous")
                ):
                    manifest.append(_entry(child, "g-drive-ed"))
        except PermissionError:
            pass  # G:\ inaccessible; skip silently.

    # 5. Deduplicate by resolved path string.
    seen_paths: set[str] = set()
    deduped: list[dict] = []
    for entry in manifest:
        key = str(Path(entry["path"]).resolve())
        if key not in seen_paths:
            seen_paths.add(key)
            deduped.append(entry)

    # 6. Write manifest atomically — only into indexes/, never into game dirs.
    out_path = indexes_dir() / "data-sources.json"
    write_json_atomic(out_path, deduped)

    return deduped
```

### 1c. Run tests — confirm green bar

```
pytest tests/test_data_discovery.py -v
```

All tests must pass. Fix any failures before proceeding.

### 1d. Commit

```
git add copilot/data_discovery.py tests/test_data_discovery.py
git commit -m "Plan B task 1: data_discovery — saved_games_dir + discover_data_sources"
```

---

## Task 2 — `copilot/profile_sources.py`: parse_game_state

### 2a. Write fixtures

**File:** `tests/fixtures/status.json`

```json
{
  "timestamp": "2026-06-01T10:00:00Z",
  "event": "Status",
  "Flags": 16842765,
  "Pips": [4, 2, 2],
  "FireGroup": 0,
  "GuiFocus": 0,
  "Fuel": {"FuelMain": 32.0, "FuelReservoir": 0.63},
  "Cargo": 0,
  "LegalState": "Clean",
  "Balance": 3200000000
}
```

**File:** `tests/fixtures/fleet_carrier.json`

```json
{
  "timestamp": "2026-06-01T10:00:00Z",
  "event": "CarrierStats",
  "CarrierID": 3700000001,
  "Callsign": "X9V-T3K",
  "Name": "THE LONG HAUL",
  "DockingAccess": "squadronfriends",
  "AllowNotorious": false,
  "FuelLevel": 497,
  "JumpRangeCurr": 500.0,
  "JumpRangeMax": 500.0,
  "PendingDecommission": false,
  "SpaceUsage": {
    "TotalCapacity": 25000,
    "Crew": 600,
    "Cargo": 1200,
    "CargoSpaceReserved": 6,
    "ShipPacks": 0,
    "ModulePacks": 0,
    "FreeSpace": 23194
  },
  "Finance": {
    "CarrierBalance": 1870000000,
    "ReserveBalance": 0,
    "AvailableBalance": 1870000000,
    "ReservePercent": 0
  },
  "Crew": [],
  "ShipPacks": [],
  "ModulePacks": []
}
```

**File:** `tests/fixtures/cargo.json`

```json
{
  "timestamp": "2026-06-01T10:00:00Z",
  "event": "Cargo",
  "Vessel": "Ship",
  "Count": 2,
  "Inventory": [
    {"Name": "gold", "Name_Localised": "Gold", "Count": 2, "Stolen": 0}
  ]
}
```

**File:** `tests/fixtures/ship_locker.json`

```json
{
  "timestamp": "2026-06-01T10:00:00Z",
  "event": "ShipLocker",
  "Items": [
    {"Name": "healthpack", "OwnerID": 0, "MissionID": -1, "Count": 3}
  ],
  "Components": [],
  "Consumables": [],
  "Data": []
}
```

**File:** `tests/fixtures/sample_journal.log`

```jsonl
{ "timestamp":"2026-05-01T09:00:00Z", "event":"Fileheader", "part":1, "language":"English/UK", "Odyssey":true, "gameversion":"4.0.0.1900", "build":"r303089/r0" }
{ "timestamp":"2026-05-01T09:00:10Z", "event":"Commander", "FID":"F1234567", "Name":"Duvrazh" }
{ "timestamp":"2026-05-01T09:01:00Z", "event":"Rank", "Combat":4, "Trade":9, "Explore":9, "Soldier":0, "Exobiologist":0, "Empire":0, "Federation":0, "CQC":0 }
{ "timestamp":"2026-05-01T09:01:01Z", "event":"Progress", "Combat":67, "Trade":99, "Explore":99, "Soldier":0, "Exobiologist":0, "Empire":0, "Federation":0, "CQC":0 }
{ "timestamp":"2026-05-01T09:01:02Z", "event":"Statistics", "Bank_Account":{"Current_Wealth":3200000000,"Spent_On_Ships":4000000000,"Spent_On_Outfitting":800000000,"Spent_On_Repairs":12000000,"Spent_On_Fuel":5000000,"Spent_On_Ammo_Consumables":2000000,"Insurance_Claims":8,"Spent_On_Insurance":320000000,"Owned_Ship_Count":14,"Spent_On_Suits":5000000,"Spent_On_Weapons":3000000,"Spent_On_Suit_Consumables":1000000,"Suits_Owned":3,"Weapons_Owned":4,"Spent_On_Premium_Stock":0,"Premium_Stock_Bought":0}, "Combat":{"Bounties_Claimed":342,"Bounty_Hunting_Profit":1200000000,"Combat_Bonds":12,"Combat_Bond_Profits":5000000,"Assassinations":3,"Assassination_Profit":30000000,"Highest_Single_Reward":5000000,"Skimmers_Killed":55,"OnFoot_Combat_Bonds":0,"OnFoot_Combat_Bond_Profits":0,"OnFoot_Kills":12,"Settlements_Rescued":0,"Settlements_State_Shutdown":0,"Scenario_Completed":0}, "Exploration":{"Systems_Visited":4218,"Exploration_Profits":1500000000,"Planets_Scanned_To_Level_2":3800,"Planets_Scanned_To_Level_3":1200,"Efficient_Scans":420,"Highest_Payout":4200000,"Total_Hyperspace_Distance":82000,"Total_Hyperspace_Jumps":9400,"Greatest_Distance_From_Start":22918.0,"Time_Played":1200000}, "Passengers":{"Passengers_Missions_Bulk":0,"Passengers_Missions_VIP":14,"Passengers_Missions_Delivered":14,"Passengers_Missions_Ejected":0}, "Search_And_Rescue":{"SearchRescue_Traded":0,"SearchRescue_Profit":0,"SearchRescue_Count":0,"Salvage_Legal_POI":0,"Salvage_Legal_Settlements":0,"Salvage_Illegal_POI":0,"Salvage_Illegal_Settlements":0}, "Crafting":{"Count_Of_Used_Engineers":4,"Recipes_Generated":88,"Recipes_Generated_Rank_1":30,"Recipes_Generated_Rank_2":22,"Recipes_Generated_Rank_3":18,"Recipes_Generated_Rank_4":12,"Recipes_Generated_Rank_5":6,"Suit_Mods_Applied":0,"Weapon_Mods_Applied":0,"Spent_On_Tech_Broker":0}, "Crew":{"NpcCrew_TotalWages":2000000,"NpcCrew_Hired":3,"NpcCrew_Fired":1,"NpcCrew_Died":0}, "Multicrew":{"Multicrew_Time_Total":0,"Multicrew_Gunner_Time_Total":0,"Multicrew_Fighter_Time_Total":0,"Multicrew_Credits_Total":0,"Multicrew_Fines_Total":0}, "MaterialTrader":{"Trades_Completed":12,"Materials_Traded":240,"Encoded_Materials_Traded":60,"Raw_Materials_Traded":120,"Grade_1_Materials_Traded":80,"Grade_2_Materials_Traded":60,"Grade_3_Materials_Traded":50,"Grade_4_Materials_Traded":30,"Grade_5_Materials_Traded":20}, "Exobiology":{"Organic_Genus_Encountered":3,"Organic_Species_Encountered":5,"Organic_Variant_Encountered":5,"Organic_Data_Profits":200000,"Organic_Data_Sold":2,"Species_Genus_Data_Collected":3,"Organic_Genuses_Sold_All_Species":0}, "TGS":{"TGS_Encountered":0} }
{ "timestamp":"2026-05-01T09:02:00Z", "event":"EngineerProgress", "Engineers":[{"Engineer":"Felicity Farseer","EngineerID":300100,"Progress":"Unlocked","Rank":5,"RankProgress":0},{"Engineer":"The Dweller","EngineerID":300180,"Progress":"Unlocked","Rank":3,"RankProgress":55},{"Engineer":"Marco Qwent","EngineerID":300200,"Progress":"Invited","Rank":1,"RankProgress":0}] }
{ "timestamp":"2026-05-15T14:30:00Z", "event":"ScanOrganic", "ScanType":"Analyse", "Genus":"$Codex_Ent_Fonticulus_Name;", "Genus_Localised":"Fonticulua", "Species":"$Codex_Ent_Fonticulus_Digitos_Name;", "Species_Localised":"Fonticulua Digitos", "Variant":"$Codex_Ent_Fonticulus_Digitos_CMYK2_Name;", "Variant_Localised":"Fonticulua Digitos - Yellow", "SystemAddress":58349148498, "Body":3 }
{ "timestamp":"2026-05-20T18:00:00Z", "event":"Loadout", "Ship":"cutter", "ShipID":32, "ShipName":"IMPERIAL BLADE", "ShipIdent":"DV-01", "HullValue":200000000, "ModulesValue":450000000, "HullHealth":1.0, "UnladenMass":2100.0, "CargoCapacity":0, "MaxJumpRange":30.5, "FuelCapacity":{"Main":64.0,"Reserve":1.07}, "Rebuy":32500000, "Modules":[] }
{ "timestamp":"2026-05-20T19:00:00Z", "event":"CarrierStats", "CarrierID":3700000001, "Callsign":"X9V-T3K", "Name":"THE LONG HAUL", "DockingAccess":"squadronfriends", "AllowNotorious":false, "FuelLevel":497, "JumpRangeCurr":500.0, "JumpRangeMax":500.0, "PendingDecommission":false, "SpaceUsage":{"TotalCapacity":25000,"Crew":600,"Cargo":1200,"CargoSpaceReserved":6,"ShipPacks":0,"ModulePacks":0,"FreeSpace":23194}, "Finance":{"CarrierBalance":1870000000,"ReserveBalance":0,"AvailableBalance":1870000000,"ReservePercent":0}, "Crew":[], "ShipPacks":[], "ModulePacks":[] }
```

### 2b. Write failing tests for parse_game_state

**File:** `tests/test_profile_sources.py` (partial — add more tests in tasks 3 and 4)

```python
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
```

Confirm red bar with `pytest tests/test_profile_sources.py::TestParseGameState -v`.

### 2c. Implement parse_game_state in `copilot/profile_sources.py`

```python
"""
profile_sources.py — ProfileSource implementations that read real game data.

All sources implement the ProfileSource Protocol from copilot.profile.
"""
from __future__ import annotations

import glob
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

from copilot.models import CmdrState, ProfileFact
from copilot.data_discovery import saved_games_dir

if TYPE_CHECKING:
    from copilot.profile import ProfileSource

# ---------------------------------------------------------------------------
# Rank integer → label maps
# ---------------------------------------------------------------------------
_COMBAT_RANKS = ["Harmless", "Mostly Harmless", "Novice", "Competent", "Expert",
                 "Master", "Dangerous", "Deadly", "Elite", "Elite I", "Elite II",
                 "Elite III", "Elite IV", "Elite V"]
_TRADE_RANKS   = ["Penniless", "Mostly Penniless", "Peddler", "Dealer", "Merchant",
                  "Broker", "Entrepreneur", "Tycoon", "Elite", "Elite I", "Elite II",
                  "Elite III", "Elite IV", "Elite V"]
_EXPLORE_RANKS = ["Aimless", "Mostly Aimless", "Scout", "Surveyor", "Trailblazer",
                  "Pathfinder", "Ranger", "Pioneer", "Elite", "Elite I", "Elite II",
                  "Elite III", "Elite IV", "Elite V"]
_SOLDIER_RANKS = ["Defenceless", "Mostly Defenceless", "Rookie", "Soldier", "Gunslinger",
                  "Warrior", "Gladiator", "Deadeye", "Elite", "Elite I", "Elite II",
                  "Elite III", "Elite IV", "Elite V"]
_EXOBIO_RANKS  = ["Directionless", "Mostly Directionless", "Compiler", "Collector",
                  "Cataloguer", "Taxonomist", "Ecologist", "Geneticist", "Elite",
                  "Elite I", "Elite II", "Elite III", "Elite IV", "Elite V"]
_CQC_RANKS     = ["Helpless", "Mostly Helpless", "Amateur", "Semi Professional",
                  "Professional", "Champion", "Hero", "Legend", "Elite", "Elite I",
                  "Elite II", "Elite III", "Elite IV", "Elite V"]

_RANK_MAPS = {
    "Combat": _COMBAT_RANKS,
    "Trade": _TRADE_RANKS,
    "Explore": _EXPLORE_RANKS,
    "Soldier": _SOLDIER_RANKS,
    "Exobiologist": _EXOBIO_RANKS,
    "CQC": _CQC_RANKS,
}


def _rank_label(category: str, index: int) -> str:
    labels = _RANK_MAPS.get(category, [])
    if 0 <= index < len(labels):
        return labels[index]
    return str(index)


def _iso_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def _read_json(path: Path) -> dict | None:
    """Read and parse a JSON file; return None on any error."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


# ---------------------------------------------------------------------------
# parse_game_state
# ---------------------------------------------------------------------------

def parse_game_state(dir: Path) -> list[ProfileFact]:
    """Parse live game-state JSON files in *dir* into ProfileFacts.

    Reads: Status.json, Cargo.json, ShipLocker.json, FleetCarrier.json,
    plus the most-recent Journal for a Loadout event (if present).

    Returns facts with origin="game-state-json", verified=True.
    """
    facts: list[ProfileFact] = []

    def _fact(key: str, value: str, freshness: str = "unknown") -> ProfileFact:
        return ProfileFact(
            key=key,
            value=value,
            origin="game-state-json",
            freshness=freshness,
            verified=True,
        )

    # --- Status.json ---
    status = _read_json(dir / "Status.json")
    if status:
        ts = status.get("timestamp", "unknown")
        if "Balance" in status:
            facts.append(_fact("balance_cr", str(status["Balance"]), freshness=ts))
        if "LegalState" in status:
            facts.append(_fact("legal_state", status["LegalState"], freshness=ts))
        if "Fuel" in status and "FuelMain" in status["Fuel"]:
            facts.append(_fact(
                "fuel_main_t",
                str(status["Fuel"]["FuelMain"]),
                freshness=ts,
            ))

    # --- Cargo.json ---
    cargo = _read_json(dir / "Cargo.json")
    if cargo:
        ts = cargo.get("timestamp", "unknown")
        facts.append(_fact("cargo_count", str(cargo.get("Count", 0)), freshness=ts))

    # --- ShipLocker.json ---
    locker = _read_json(dir / "ShipLocker.json")
    if locker:
        ts = locker.get("timestamp", "unknown")
        item_count = sum(i.get("Count", 1) for i in locker.get("Items", []))
        facts.append(_fact("ship_locker_item_count", str(item_count), freshness=ts))

    # --- FleetCarrier.json (non-standard; also captured via journal) ---
    carrier = _read_json(dir / "FleetCarrier.json")
    if carrier:
        ts = carrier.get("timestamp", "unknown")
        if "Name" in carrier:
            facts.append(_fact("carrier.0.name", carrier["Name"], freshness=ts))
        if "Callsign" in carrier:
            facts.append(_fact("carrier.0.callsign", carrier["Callsign"], freshness=ts))
        finance = carrier.get("Finance", {})
        if "CarrierBalance" in finance:
            facts.append(_fact(
                "carrier.0.balance_cr",
                str(finance["CarrierBalance"]),
                freshness=ts,
            ))

    return facts
```

### 2d. Run tests — confirm green

```
pytest tests/test_profile_sources.py::TestParseGameState -v
```

### 2e. Commit

```
git add copilot/profile_sources.py tests/test_profile_sources.py tests/fixtures/
git commit -m "Plan B task 2: parse_game_state + game-state JSON fixtures"
```

---

## Task 3 — `copilot/profile_sources.py`: parse_journal

### 3a. Write failing tests (append to `tests/test_profile_sources.py`)

```python
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
        assert trade[0].value == "Elite V"   # index 9 = "Elite", but journal gives 9 → Elite V per rank map

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
```

Confirm red bar with `pytest tests/test_profile_sources.py::TestParseJournal -v`.

### 3b. Implement parse_journal (append to `copilot/profile_sources.py`)

```python
# ---------------------------------------------------------------------------
# parse_journal
# ---------------------------------------------------------------------------

def parse_journal(path: Path) -> list[ProfileFact]:
    """Stream a Journal.*.log file (JSONL) and extract ProfileFacts.

    Extracts: EngineerProgress, Rank, Statistics(balance), ScanOrganic,
    Loadout, CarrierStats.

    Events are streamed; the last occurrence of a given fact key wins,
    preserving chronological ordering naturally.

    Raises FileNotFoundError if *path* does not exist.
    """
    if not path.exists():
        raise FileNotFoundError(f"Journal not found: {path}")

    facts: dict[str, ProfileFact] = {}  # key → latest fact; last write wins

    def _put(key: str, value: str, freshness: str) -> None:
        facts[key] = ProfileFact(
            key=key,
            value=value,
            origin="journal",
            freshness=freshness,
            verified=True,
        )

    with path.open(encoding="utf-8", errors="replace") as fh:
        for raw_line in fh:
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            try:
                event = json.loads(raw_line)
            except json.JSONDecodeError:
                continue  # skip malformed lines

            etype = event.get("event", "")
            ts = event.get("timestamp", "unknown")

            if etype == "Rank":
                for cat, idx in event.items():
                    if cat in _RANK_MAPS and isinstance(idx, int):
                        _put(f"rank.{cat.lower()}", _rank_label(cat, idx), ts)

            elif etype == "EngineerProgress":
                for eng in event.get("Engineers", []):
                    name = eng.get("Engineer", "unknown")
                    slug = re.sub(r"[^a-z0-9]", "-", name.lower()).strip("-")
                    progress = eng.get("Progress", "unknown")
                    rank = eng.get("Rank", 0)
                    _put(f"engineer.{slug}.progress", progress, ts)
                    if isinstance(rank, int):
                        _put(f"engineer.{slug}.rank", str(rank), ts)

            elif etype == "Statistics":
                bank = event.get("Bank_Account", {})
                if "Current_Wealth" in bank:
                    _put("balance_cr", str(bank["Current_Wealth"]), ts)
                exobio = event.get("Exobiology", {})
                if "Organic_Data_Sold" in exobio:
                    _put("exobio.data_sold", str(exobio["Organic_Data_Sold"]), ts)
                if "Organic_Genuses_Sold_All_Species" in exobio:
                    _put(
                        "exobio.genuses_sold_all_species",
                        str(exobio["Organic_Genuses_Sold_All_Species"]),
                        ts,
                    )

            elif etype == "ScanOrganic":
                genus = event.get("Genus_Localised", event.get("Genus", "unknown"))
                species = event.get("Species_Localised", event.get("Species", "unknown"))
                scan_type = event.get("ScanType", "unknown")
                body = str(event.get("Body", ""))
                _put(
                    f"organic.scan.{re.sub(r'[^a-z0-9]', '-', species.lower())}",
                    f"{genus} / {species} / ScanType={scan_type} / Body={body}",
                    ts,
                )

            elif etype == "Loadout":
                ship = event.get("Ship", "unknown")
                ship_name = event.get("ShipName", "")
                ship_id = event.get("ShipID", 0)
                rebuy = event.get("Rebuy", 0)
                _put(f"ship.{ship_id}.type", ship, ts)
                if ship_name:
                    _put(f"ship.{ship_id}.name", ship_name, ts)
                _put(f"ship.{ship_id}.rebuy_cr", str(rebuy), ts)

            elif etype == "CarrierStats":
                carrier_id = event.get("CarrierID", "unknown")
                name = event.get("Name", "")
                callsign = event.get("Callsign", "")
                fuel = event.get("FuelLevel", None)
                finance = event.get("Finance", {})
                if name:
                    _put(f"carrier.{carrier_id}.name", name, ts)
                if callsign:
                    _put(f"carrier.{carrier_id}.callsign", callsign, ts)
                if fuel is not None:
                    _put(f"carrier.{carrier_id}.fuel_t", str(fuel), ts)
                if "CarrierBalance" in finance:
                    _put(
                        f"carrier.{carrier_id}.balance_cr",
                        str(finance["CarrierBalance"]),
                        ts,
                    )

    return list(facts.values())
```

### 3c. Run tests — confirm green

```
pytest tests/test_profile_sources.py::TestParseJournal -v
```

Fix any assertion mismatches (the rank map index for Trade rank 9 is "Elite V" — verify the
`_TRADE_RANKS` list at index 9). If the fixture journal uses index 9 and the label list
has "Elite" at index 8 and "Elite I" at 9, adjust the test assertion to match the list.

### 3d. Commit

```
git add copilot/profile_sources.py tests/test_profile_sources.py
git commit -m "Plan B task 3: parse_journal — EngineerProgress/Rank/Statistics/Loadout/CarrierStats"
```

---

## Task 4 — `copilot/profile_sources.py`: ProfileSource classes + available_sources

### 4a. Write failing tests (append to `tests/test_profile_sources.py`)

```python
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
```

Confirm red bar.

### 4b. Implement classes + available_sources (append to `copilot/profile_sources.py`)

```python
# ---------------------------------------------------------------------------
# ProfileSource classes
# ---------------------------------------------------------------------------

class GameStateSource:
    """Reads live game-state JSON files from the Saved Games dir."""

    origin: str = "game-state-json"

    def __init__(self, dir: Path) -> None:
        self._dir = dir

    def get_facts(self) -> list[ProfileFact]:
        return parse_game_state(self._dir)


class JournalSource:
    """One-shot parse of a single Journal.*.log file."""

    origin: str = "journal"

    def __init__(self, journal_path: Path) -> None:
        self._path = journal_path

    def get_facts(self) -> list[ProfileFact]:
        if not self._path.exists():
            return []
        return parse_journal(self._path)


class ThirdPartySource:
    """Stub for EDMC / EDDiscovery / EDEngineer exports.

    Currently returns an empty list (structured ingest of specific export
    formats is deferred to v1.1). Presence in available_sources() signals
    that the tool dir was found; future expansion adds parse logic here.
    """

    origin: str = "3rd-party"

    def __init__(self, dir: Path, label: str = "unknown") -> None:
        self._dir = dir
        self._label = label

    def get_facts(self) -> list[ProfileFact]:
        # v1.1: parse EDMC journal JSON / EDDiscovery CSV exports.
        return []


# ---------------------------------------------------------------------------
# available_sources
# ---------------------------------------------------------------------------

def _newest_journal(sg: Path) -> Path | None:
    """Return the most recently modified Journal.*.log in *sg*, or None."""
    candidates = list(sg.glob("Journal.*.log"))
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def available_sources() -> list["ProfileSource"]:
    """Return ProfileSource instances whose underlying data exists on this machine.

    Discovery order (matches ORIGIN_PRIORITY):
    1. GameStateSource — if saved_games_dir() is not None.
    2. JournalSource  — if a Journal.*.log exists in saved_games_dir().
    3. ThirdPartySource — for each 3rd-party tool dir found in data-sources.json
       (or re-scanned inline if the manifest is absent).
    """
    sources: list[ProfileSource] = []

    sg = saved_games_dir()
    if sg is not None:
        sources.append(GameStateSource(sg))
        newest = _newest_journal(sg)
        if newest is not None:
            sources.append(JournalSource(newest))

    # 3rd-party: scan LOCALAPPDATA/APPDATA for known tool dirs.
    third_party_dirs = {
        "EDMarketConnector": "edmc",
        "EDDiscovery": "eddiscovery",
        "EDEngineer": "edengineer",
    }
    for env_var in ("LOCALAPPDATA", "APPDATA"):
        base = os.environ.get(env_var, "")
        if not base:
            continue
        for dir_name, label in third_party_dirs.items():
            candidate = Path(base) / dir_name
            if candidate.is_dir():
                sources.append(ThirdPartySource(candidate, label=label))

    return sources
```

### 4c. Run tests — confirm green

```
pytest tests/test_profile_sources.py -v
```

### 4d. Commit

```
git add copilot/profile_sources.py tests/test_profile_sources.py
git commit -m "Plan B task 4: GameStateSource, JournalSource, ThirdPartySource, available_sources"
```

---

## Task 5 — `copilot/vision_ingest.py`: ingest_screenshot

### 5a. Write failing tests

**File:** `tests/test_vision_ingest.py`

```python
"""Tests for copilot.vision_ingest."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from copilot.models import ProfileFact

# ---------------------------------------------------------------------------
# Unit tests — mock ollama_client.vision
# ---------------------------------------------------------------------------

MOCK_VISION_RESPONSE = json.dumps({
    "ranks": {
        "combat": "Expert",
        "trade": "Elite V",
        "explore": "Elite",
        "soldier": "Defenceless",
        "exobiologist": "Directionless",
        "cqc": "Helpless"
    },
    "balance_cr": 3200000000,
    "assets": {
        "carriers": 2,
        "ships_estimate": "many"
    }
})

import json  # noqa: E402  (after MOCK_VISION_RESPONSE uses json.dumps — move import to top in impl)


class TestIngestScreenshotUnit:
    def test_returns_list_of_profile_facts(self, tmp_path):
        from copilot.vision_ingest import ingest_screenshot
        fake_img = tmp_path / "rank.png"
        fake_img.write_bytes(b"\x89PNG\r\n")
        with patch("copilot.vision_ingest.ollama_client") as mock_client:
            mock_client.vision.return_value = MOCK_VISION_RESPONSE
            facts = ingest_screenshot(str(fake_img))
        assert isinstance(facts, list)
        assert all(isinstance(f, ProfileFact) for f in facts)

    def test_origin_is_screenshot(self, tmp_path):
        from copilot.vision_ingest import ingest_screenshot
        fake_img = tmp_path / "rank.png"
        fake_img.write_bytes(b"\x89PNG\r\n")
        with patch("copilot.vision_ingest.ollama_client") as mock_client:
            mock_client.vision.return_value = MOCK_VISION_RESPONSE
            facts = ingest_screenshot(str(fake_img))
        assert all(f.origin == "screenshot" for f in facts)

    def test_verified_is_false(self, tmp_path):
        from copilot.vision_ingest import ingest_screenshot
        fake_img = tmp_path / "rank.png"
        fake_img.write_bytes(b"\x89PNG\r\n")
        with patch("copilot.vision_ingest.ollama_client") as mock_client:
            mock_client.vision.return_value = MOCK_VISION_RESPONSE
            facts = ingest_screenshot(str(fake_img))
        assert all(f.verified is False for f in facts)

    def test_rank_facts_extracted(self, tmp_path):
        from copilot.vision_ingest import ingest_screenshot
        fake_img = tmp_path / "rank.png"
        fake_img.write_bytes(b"\x89PNG\r\n")
        with patch("copilot.vision_ingest.ollama_client") as mock_client:
            mock_client.vision.return_value = MOCK_VISION_RESPONSE
            facts = ingest_screenshot(str(fake_img))
        combat = [f for f in facts if f.key == "rank.combat"]
        assert len(combat) == 1
        assert combat[0].value == "Expert"

    def test_balance_extracted_when_present(self, tmp_path):
        from copilot.vision_ingest import ingest_screenshot
        fake_img = tmp_path / "rank.png"
        fake_img.write_bytes(b"\x89PNG\r\n")
        with patch("copilot.vision_ingest.ollama_client") as mock_client:
            mock_client.vision.return_value = MOCK_VISION_RESPONSE
            facts = ingest_screenshot(str(fake_img))
        balance = [f for f in facts if f.key == "balance_cr"]
        assert len(balance) == 1
        assert balance[0].value == "3200000000"

    def test_malformed_vision_response_returns_empty(self, tmp_path):
        from copilot.vision_ingest import ingest_screenshot
        fake_img = tmp_path / "rank.png"
        fake_img.write_bytes(b"\x89PNG\r\n")
        with patch("copilot.vision_ingest.ollama_client") as mock_client:
            mock_client.vision.return_value = "not valid JSON at all {{{"
            facts = ingest_screenshot(str(fake_img))
        assert facts == []

    def test_vision_unavailable_returns_empty(self, tmp_path):
        from copilot.vision_ingest import ingest_screenshot
        from copilot.ollama_client import OllamaUnavailable
        fake_img = tmp_path / "rank.png"
        fake_img.write_bytes(b"\x89PNG\r\n")
        with patch("copilot.vision_ingest.ollama_client") as mock_client:
            mock_client.vision.side_effect = OllamaUnavailable("Ollama unreachable")
            mock_client.OllamaUnavailable = OllamaUnavailable
            facts = ingest_screenshot(str(fake_img))
        assert facts == []


# ---------------------------------------------------------------------------
# Integration test — real Ollama call (skip unless --integration flag)
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_ingest_real_screenshot():
    """Requires Ollama + qwen3-vl:8b running and the rank screenshot present."""
    from copilot.vision_ingest import ingest_screenshot
    img = Path(r"C:\Users\Quadstronaut\.claude\image-cache\45518cb0-435b-47c5-9711-56ce5054f178\1.png")
    if not img.exists():
        pytest.skip(f"Rank screenshot not found at {img} — drop a screenshot and rerun.")
    facts = ingest_screenshot(str(img))
    assert len(facts) > 0
    rank_keys = [f.key for f in facts if f.key.startswith("rank.")]
    assert len(rank_keys) >= 1, "Expected at least one rank fact from the screenshot"
```

Confirm red bar with `pytest tests/test_vision_ingest.py -v -k "not integration"`.

### 5b. Implement `copilot/vision_ingest.py`

```python
"""
vision_ingest.py — parse in-game screenshots into ProfileFacts via qwen3-vl:8b.

Facts carry origin="screenshot", verified=False (vision output is not authoritative).
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from copilot import ollama_client
from copilot.ollama_client import OllamaUnavailable
from copilot.models import ProfileFact

_VISION_PROMPT = """
You are parsing an Elite Dangerous screenshot. Extract ALL of the following that are visible:
- Player ranks for: combat, trade, explore, soldier (mercenary), exobiologist, cqc
- Credit balance (any number in the hundreds of millions or billions)
- Fleet carrier count and names if shown
- Number of ships owned if shown

Respond ONLY with a single JSON object. No prose, no markdown code block. Schema:
{
  "ranks": {"combat": "...", "trade": "...", "explore": "...", "soldier": "...", "exobiologist": "...", "cqc": "..."},
  "balance_cr": <integer or null>,
  "assets": {"carriers": <int or null>, "ships_estimate": "<string or null>"}
}

Omit keys you cannot read. Do not guess.
""".strip()


def _iso_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def _extract_json(text: str) -> dict | None:
    """Try to extract a JSON object from the model response, tolerating markdown fences."""
    # Strip ```json ... ``` fences if present.
    cleaned = re.sub(r"```[a-z]*\n?", "", text).strip()
    # Try the whole string first.
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    # Fall back: find the first {...} block.
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    return None


def ingest_screenshot(image_path: str) -> list[ProfileFact]:
    """Parse *image_path* via qwen3-vl:8b and return ProfileFacts.

    Returns an empty list on any failure (vision unavailable, parse error,
    image not found) — callers must not assume a non-empty result.

    All facts: origin="screenshot", verified=False.
    """
    freshness = _iso_now()

    def _fact(key: str, value: str) -> ProfileFact:
        return ProfileFact(
            key=key,
            value=value,
            origin="screenshot",
            freshness=freshness,
            verified=False,
        )

    try:
        raw = ollama_client.vision(image_path, _VISION_PROMPT)
    except OllamaUnavailable:
        return []
    except Exception:  # noqa: BLE001 — degrade gracefully on any ollama error
        return []

    parsed = _extract_json(raw)
    if parsed is None:
        return []

    facts: list[ProfileFact] = []

    # Ranks
    for rank_key, rank_val in (parsed.get("ranks") or {}).items():
        if rank_key and rank_val:
            facts.append(_fact(f"rank.{rank_key.lower()}", str(rank_val)))

    # Balance
    balance = parsed.get("balance_cr")
    if balance is not None:
        facts.append(_fact("balance_cr", str(int(balance))))

    # Assets
    assets = parsed.get("assets") or {}
    carriers = assets.get("carriers")
    if carriers is not None:
        facts.append(_fact("assets.carrier_count", str(int(carriers))))
    ships = assets.get("ships_estimate")
    if ships:
        facts.append(_fact("assets.ships_estimate", str(ships)))

    return facts
```

### 5c. Run tests — confirm green

```
pytest tests/test_vision_ingest.py -v -k "not integration"
```

### 5d. Commit

```
git add copilot/vision_ingest.py tests/test_vision_ingest.py
git commit -m "Plan B task 5: vision_ingest — ingest_screenshot via qwen3-vl:8b (mocked unit tests)"
```

---

## Task 6 — Edit `copilot/profile.py`: wire in available_sources

This is the ONLY cross-plan file edit. Plan A's `profile.py` already defines
`ProfileSource`, `ManualProfile`, `merge_state`, and `load_cmdr_state`. The single
sanctioned change: make `load_cmdr_state` try-import `profile_sources` and prepend
`available_sources()` before calling `merge_state`.

### 6a. Write failing tests

**File:** `tests/test_profile_b.py`

```python
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
```

Confirm red bar.

### 6b. Edit `copilot/profile.py` — load_cmdr_state

Locate the existing `load_cmdr_state` function in `copilot/profile.py` and replace its
body with the following (keeping the signature unchanged):

```python
def load_cmdr_state() -> CmdrState:
    """Discover available sources, merge into CmdrState.

    Source priority (from ORIGIN_PRIORITY):
      game-state-json > journal > screenshot > 3rd-party > manual

    If copilot.profile_sources is not yet installed (Plan A standalone),
    falls back to ManualProfile only.
    """
    sources: list[ProfileSource] = []

    try:
        from copilot import profile_sources  # Plan B module — optional
        sources.extend(profile_sources.available_sources())
    except ImportError:
        pass

    sources.append(ManualProfile())
    return merge_state(sources)
```

### 6c. Confirm merge_state handles ORIGIN_PRIORITY correctly

`merge_state` is defined in Plan A. It must resolve per-key conflicts by selecting the
fact whose `origin` appears earliest in `ORIGIN_PRIORITY`. Verify this is the case by
reading the existing implementation. If it is not, the fix belongs in Plan A (raise a
cross-plan note and fix there before continuing).

The reference logic (what Plan A should implement — do not duplicate in Plan B):

```python
ORIGIN_PRIORITY = ["game-state-json", "journal", "screenshot", "3rd-party", "manual"]

def _priority(origin: str) -> int:
    try:
        return ORIGIN_PRIORITY.index(origin)
    except ValueError:
        return len(ORIGIN_PRIORITY)

def merge_state(sources: list[ProfileSource]) -> CmdrState:
    all_facts: list[ProfileFact] = []
    for src in sources:
        all_facts.extend(src.get_facts())

    # Per key, keep the fact with the highest trust (lowest priority index).
    best: dict[str, ProfileFact] = {}
    for fact in all_facts:
        if fact.key not in best or _priority(fact.origin) < _priority(best[fact.key].origin):
            best[fact.key] = fact

    resolved = list(best.values())

    # Assemble CmdrState from resolved facts.
    state = CmdrState(name="Duvrazh")
    for fact in resolved:
        if fact.key == "balance_cr":
            try:
                state.balance_cr = int(fact.value)
            except ValueError:
                pass
        elif fact.key.startswith("rank."):
            rank_key = fact.key[len("rank."):]
            state.ranks[rank_key] = fact.value
        elif fact.key.startswith("carrier.") or fact.key.startswith("ship."):
            # Accumulate into assets dict.
            state.assets[fact.key] = fact.value
    state.facts = resolved
    return state
```

### 6d. Run tests — confirm green

```
pytest tests/test_profile_b.py -v
pytest tests/test_profile_sources.py -v
pytest tests/test_data_discovery.py -v
pytest tests/test_vision_ingest.py -v -k "not integration"
```

All must be green before committing.

### 6e. Commit

```
git add copilot/profile.py tests/test_profile_b.py
git commit -m "Plan B task 6: profile.load_cmdr_state wires in available_sources with try/except guard"
```

---

## Task 7 — Bootstrap CLI: `python -m copilot.profile_sources --bootstrap`

This task wires everything together: discovery + vision ingest of the rank screenshot +
merge + write verified facts to `cmdr/duvrazh.md`.

### 7a. Write failing tests (append to `tests/test_profile_b.py`)

```python
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
```

Confirm red bar.

### 7b. Implement `bootstrap` function + `__main__` block in `copilot/profile_sources.py`

Append to `copilot/profile_sources.py`:

```python
# ---------------------------------------------------------------------------
# Bootstrap function + CLI entry point
# ---------------------------------------------------------------------------

_DEFAULT_SCREENSHOT = (
    r"C:\Users\Quadstronaut\.claude\image-cache"
    r"\45518cb0-435b-47c5-9711-56ce5054f178\1.png"
)


def _write_profile_md(state: "CmdrState", path: Path) -> None:
    """Overwrite *path* with a Markdown profile derived from *state*.

    Preserves any existing YAML frontmatter from the original file (so
    human-added goals and notes survive a re-bootstrap). Appends a
    "## Auto-populated facts" section with the verified facts table.
    """
    from copilot.atomic import write_atomic

    # Read existing content so we can preserve the frontmatter.
    existing = path.read_text(encoding="utf-8") if path.exists() else ""

    # Split on the second "---" (end of frontmatter), if present.
    fm_end = existing.find("---", 3)
    if existing.startswith("---") and fm_end > 3:
        header = existing[: fm_end + 3]
        body_rest = existing[fm_end + 3 :]
    else:
        header = f"---\nname: {state.name}\n---"
        body_rest = f"\n# CMDR {state.name}\n"

    # Remove any previous auto-populated section.
    auto_marker = "\n## Auto-populated facts"
    if auto_marker in body_rest:
        body_rest = body_rest[: body_rest.index(auto_marker)]

    # Build the new auto-populated section.
    lines = [auto_marker, ""]
    lines.append("| Key | Value | Origin | Freshness | Verified |")
    lines.append("|-----|-------|--------|-----------|----------|")
    for fact in sorted(state.facts, key=lambda f: f.key):
        verified_str = "yes" if fact.verified else "no"
        lines.append(
            f"| `{fact.key}` | {fact.value} | {fact.origin} | {fact.freshness} | {verified_str} |"
        )

    new_content = header + body_rest.rstrip() + "\n" + "\n".join(lines) + "\n"
    write_atomic(path, new_content)


def bootstrap(screenshot_path: str | None = _DEFAULT_SCREENSHOT) -> "CmdrState":
    """Run discovery + optional vision ingest and write cmdr/duvrazh.md.

    1. Calls available_sources() — reads live game data.
    2. If *screenshot_path* is given and the file exists, calls
       ingest_screenshot() and adds a ScreenshotSource adapter.
    3. Merges via profile.merge_state (ORIGIN_PRIORITY).
    4. Writes cmdr/duvrazh.md via write_atomic.
    5. Returns the resulting CmdrState.

    NOTE: If the screenshot at the default path does not exist, drop a
    screenshot there (or pass a path) and rerun:
        python -m copilot.profile_sources --bootstrap [--screenshot PATH]
    """
    from copilot.profile import merge_state, ManualProfile
    from copilot.paths import repo_root

    sources: list[ProfileSource] = list(available_sources())

    # Vision ingest — optional.
    if screenshot_path is not None:
        ss_path = Path(screenshot_path)
        if ss_path.exists():
            try:
                from copilot.vision_ingest import ingest_screenshot
                vision_facts = ingest_screenshot(str(ss_path))
                if vision_facts:
                    class _ScreenshotAdapter:
                        origin = "screenshot"
                        def get_facts(self) -> list[ProfileFact]:
                            return vision_facts
                    sources.append(_ScreenshotAdapter())
                    print(f"[bootstrap] Vision ingest: {len(vision_facts)} facts from {ss_path.name}")
            except Exception as exc:  # noqa: BLE001
                print(f"[bootstrap] Vision ingest failed (non-fatal): {exc}")
        else:
            print(
                f"[bootstrap] Screenshot not found at {ss_path}\n"
                "  To include vision facts: drop a screenshot at that path and rerun."
            )

    sources.append(ManualProfile())
    state = merge_state(sources)

    profile_path = repo_root() / "cmdr" / "duvrazh.md"
    _write_profile_md(state, profile_path)
    print(f"[bootstrap] Wrote {len(state.facts)} facts to {profile_path}")
    return state


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Bootstrap cmdr/duvrazh.md from live game data + optional screenshot."
    )
    parser.add_argument(
        "--bootstrap",
        action="store_true",
        help="Run discovery + ingest + profile write.",
    )
    parser.add_argument(
        "--screenshot",
        default=_DEFAULT_SCREENSHOT,
        help=f"Path to rank screenshot (default: {_DEFAULT_SCREENSHOT}).",
    )
    args = parser.parse_args()

    if args.bootstrap:
        result = bootstrap(screenshot_path=args.screenshot)
        print(f"[bootstrap] Done. balance_cr={result.balance_cr}, ranks={result.ranks}")
    else:
        parser.print_help()
```

### 7c. Run all tests — confirm full green bar

```
pytest tests/test_data_discovery.py tests/test_profile_sources.py \
       tests/test_vision_ingest.py tests/test_profile_b.py -v -k "not integration"
```

All tests must pass. Fix any failures inline before committing.

### 7d. Commit

```
git add copilot/profile_sources.py tests/test_profile_b.py
git commit -m "Plan B task 7: bootstrap CLI — discovery + vision ingest + write cmdr/duvrazh.md"
```

---

## Task 8 — Full suite green + end-state verification

### 8a. Run the complete test suite

```
pytest tests/ -v -k "not integration" --tb=short
```

Zero failures required before declaring Plan B complete.

### 8b. Smoke-run bootstrap (optional, documents the real invocation)

```powershell
# From repo root with .venv active:
.\.venv\Scripts\python.exe -m copilot.profile_sources --bootstrap
```

Expected output:
```
[bootstrap] Vision ingest: N facts from 1.png   ← if screenshot exists
[bootstrap] Wrote N facts to G:\Documents\EliteDangerousKB\cmdr\duvrazh.md
[bootstrap] Done. balance_cr=..., ranks={...}
```

If the screenshot is absent:
```
[bootstrap] Screenshot not found at C:\Users\Quadstronaut\.claude\image-cache\...\1.png
  To include vision facts: drop a screenshot at that path and rerun.
[bootstrap] Wrote N facts to ...
```

### 8c. Final commit

```
git add -A
git commit -m "Plan B complete: data-first CMDR profile — discovery, journal/game-state parse, vision ingest, bootstrap"
```

---

## Self-Review

### §I coverage check

| §I requirement | Covered by |
|----------------|-----------|
| saved_games_dir() for game-state JSON | Task 1 `saved_games_dir`, Task 2 `GameStateSource` |
| Journal one-shot backfill | Task 3 `parse_journal`, Task 4 `JournalSource` |
| Screenshots → vision | Task 5 `ingest_screenshot` |
| 3rd-party exports (EDMC/EDDiscovery/EDEngineer) | Task 4 `ThirdPartySource`, `available_sources` |
| data_discovery.py scan + data-sources.json | Task 1 `discover_data_sources` |
| G:\ drive scan | Task 1 `discover_data_sources` |
| READ-ONLY; never writes game folders | Task 1 guard test `test_discover_never_writes_outside_indexes` |
| Merge by ORIGIN_PRIORITY | Task 6 + Task 7 `merge_state` integration |
| Bootstrap write to cmdr/duvrazh.md | Task 7 `bootstrap`, `_write_profile_md` |
| ProfileSource Protocol satisfied by all classes | Task 4 `test_available_sources_implements_protocol` |

### Placeholder scan

No `TODO`, `...`, `pass` (except `ThirdPartySource.get_facts` which is intentional v1.1
stub documented inline), `FIXME`, `<PLACEHOLDER>`, or `YOUR_VALUE_HERE` appear in any
implementation code above. The `ThirdPartySource.get_facts` empty-return is documented
as a v1.1 deferral per §G step 6.

### Type consistency vs CONTRACTS

| Contract type | Used in plan |
|--------------|-------------|
| `ProfileFact(key, value, origin, freshness, verified)` | All tasks: exact field names |
| `origin="game-state-json"` | `GameStateSource`, `parse_game_state` |
| `origin="journal"` | `JournalSource`, `parse_journal` |
| `origin="screenshot"` | `ingest_screenshot`, `_ScreenshotAdapter` |
| `origin="3rd-party"` | `ThirdPartySource` |
| `origin="manual"` | `ManualProfile` (Plan A, untouched) |
| `ORIGIN_PRIORITY` list order | Verified against CONTRACTS § |
| `saved_games_dir() -> Path \| None` | Exact |
| `discover_data_sources() -> dict` | Returns `list[dict]` — CONTRACTS says `-> dict`; the manifest is a list of dicts. This is a type annotation gap in CONTRACTS (the manifest schema is clearly list-shaped). Treat return as `list[dict]` and annotate accordingly. Flag for CONTRACTS update. |
| `parse_journal(path: Path) -> list[ProfileFact]` | Exact |
| `parse_game_state(dir: Path) -> list[ProfileFact]` | Exact |
| `available_sources() -> list[ProfileSource]` | Exact |
| `ingest_screenshot(image_path: str) -> list[ProfileFact]` | Exact |
| `load_cmdr_state() -> CmdrState` | Exact (signature unchanged) |
| `vision(image_path: str, prompt: str) -> str` | Called correctly in vision_ingest |
| `OllamaUnavailable(RuntimeError)` | Caught by vision_ingest |
| `write_json_atomic(path: Path, obj) -> None` | Called in data_discovery |
| `write_atomic(path: Path, data: str) -> None` | Called in _write_profile_md |
| `indexes_dir() -> Path` | Called in data_discovery |
| `repo_root() -> Path` | Called in bootstrap |

**One CONTRACTS type flag:** `discover_data_sources() -> dict` should read `-> list[dict]`.
Update CONTRACTS.md after Plan B is merged.

---

*End of Plan B*
