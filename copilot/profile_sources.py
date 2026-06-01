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
