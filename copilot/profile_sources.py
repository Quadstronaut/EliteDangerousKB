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


# ---------------------------------------------------------------------------
# Bootstrap function + CLI entry point
# ---------------------------------------------------------------------------

# Module-level import so tests can patch copilot.profile_sources.ingest_screenshot.
# Guarded so importing profile_sources never hard-fails on the optional dep.
try:
    from copilot.vision_ingest import ingest_screenshot
except ImportError:  # pragma: no cover
    def ingest_screenshot(image_path: str) -> list[ProfileFact]:  # type: ignore[misc]
        return []


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
