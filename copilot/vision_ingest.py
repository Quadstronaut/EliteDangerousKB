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
