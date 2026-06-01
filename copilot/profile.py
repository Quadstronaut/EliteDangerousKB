"""
CMDR profile management.

Defines the ProfileSource protocol, ManualProfile (reads cmdr/duvrazh.md),
ORIGIN_PRIORITY list, merge_state(), and load_cmdr_state().

Plan B adds copilot/profile_sources.py with GameStateSource, JournalSource,
ThirdPartySource; load_cmdr_state() already calls it if importable.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Protocol

from copilot import paths
from copilot.models import CmdrState, ProfileFact

# ---------------------------------------------------------------------------
# Priority (highest trust first — index 0 = best)
# ---------------------------------------------------------------------------

ORIGIN_PRIORITY: list[str] = [
    "game-state-json",
    "journal",
    "screenshot",
    "3rd-party",
    "manual",
]


# ---------------------------------------------------------------------------
# Protocol
# ---------------------------------------------------------------------------

class ProfileSource(Protocol):
    @property
    def origin(self) -> str: ...

    def get_facts(self) -> list[ProfileFact]: ...


# ---------------------------------------------------------------------------
# ManualProfile — reads cmdr/duvrazh.md YAML frontmatter + body bullets
# ---------------------------------------------------------------------------

class ManualProfile:
    origin = "manual"

    def get_facts(self) -> list[ProfileFact]:
        # Resolve the profile-relative path from config; fall back to the
        # canonical default when config can't be loaded (e.g. tests pointing
        # repo_root at a temp dir with no config.toml).
        profile_rel = "cmdr/duvrazh.md"
        try:
            cfg = paths.load_config()
            profile_rel = cfg.get("paths", {}).get("cmdr_profile", profile_rel)
        except Exception:
            pass

        profile_path = paths.repo_root() / profile_rel

        if not profile_path.exists():
            return []

        raw = profile_path.read_text(encoding="utf-8")
        frontmatter, body = _split_frontmatter(raw)
        facts: list[ProfileFact] = []

        # Parse frontmatter key: value pairs (simple subset — no nested YAML)
        for line in frontmatter.splitlines():
            m = re.match(r"^(\w+):\s*(.+)$", line.strip())
            if not m:
                continue
            key, value = m.group(1), m.group(2).strip()
            fact_key = _map_frontmatter_key(key)
            if fact_key:
                facts.append(
                    ProfileFact(
                        key=fact_key,
                        value=value,
                        origin="manual",
                        freshness="unknown",
                        verified=False,
                    )
                )

        # Parse body bullet lines (- text)
        bullet_num = 0
        for line in body.splitlines():
            stripped = line.strip()
            if stripped.startswith("- "):
                content = stripped[2:].strip()
                bullet_num += 1
                facts.append(
                    ProfileFact(
                        key=f"note.{bullet_num}",
                        value=content,
                        origin="manual",
                        freshness="unknown",
                        verified=False,
                    )
                )

        return facts


def _split_frontmatter(raw: str) -> tuple[str, str]:
    """Return (frontmatter_text, body_text). Frontmatter is between --- delimiters."""
    if not raw.startswith("---"):
        return "", raw
    parts = raw.split("---", 2)
    if len(parts) < 3:
        return "", raw
    return parts[1], parts[2]


def _map_frontmatter_key(key: str) -> str | None:
    """Map frontmatter keys to canonical ProfileFact keys."""
    mapping = {
        "rank_combat": "rank.combat",
        "rank_trade": "rank.trade",
        "rank_explorer": "rank.explorer",
        "rank_exobiologist": "rank.exobiologist",
        "rank_mercenary": "rank.mercenary",
        "rank_cqc": "rank.cqc",
        "balance_cr": "balance_cr",
        "name": "name",
    }
    return mapping.get(key)


# ---------------------------------------------------------------------------
# merge_state
# ---------------------------------------------------------------------------

def merge_state(sources: list) -> CmdrState:
    """
    Collect facts from all sources; per fact key, keep the one whose origin has
    the lowest ORIGIN_PRIORITY index (highest trust). Assemble CmdrState.
    """
    best: dict[str, ProfileFact] = {}

    for source in sources:
        for fact in source.get_facts():
            existing = best.get(fact.key)
            if existing is None:
                best[fact.key] = fact
            else:
                try:
                    new_pri = ORIGIN_PRIORITY.index(fact.origin)
                    old_pri = ORIGIN_PRIORITY.index(existing.origin)
                    if new_pri < old_pri:
                        best[fact.key] = fact
                except ValueError:
                    # Unknown origin — keep existing.
                    pass

    all_facts = list(best.values())

    # Populate CmdrState fields from recognised keys.
    name = best["name"].value if "name" in best else "Commander"

    ranks: dict[str, str] = {}
    for k, v in best.items():
        if k.startswith("rank."):
            ranks[k[5:]] = v.value  # e.g. "combat" → "Expert"

    balance_cr: int | None = None
    if "balance_cr" in best:
        try:
            balance_cr = int(best["balance_cr"].value)
        except ValueError:
            pass

    # Assets: carriers mentioned in note bullets.
    assets: dict = {}
    goals: list[str] = []

    return CmdrState(
        name=name,
        ranks=ranks,
        balance_cr=balance_cr,
        assets=assets,
        goals=goals,
        facts=all_facts,
    )


# ---------------------------------------------------------------------------
# load_cmdr_state
# ---------------------------------------------------------------------------

def load_cmdr_state() -> CmdrState:
    """
    Discover available ProfileSources and merge them into a CmdrState.

    Tries to import copilot.profile_sources (added in Plan B); if absent,
    falls back to ManualProfile only.
    """
    sources: list = []

    try:
        from copilot import profile_sources  # type: ignore[import]
        sources.extend(profile_sources.available_sources())
    except (ImportError, TypeError, AttributeError):
        # profile_sources not yet installed or set to None in tests.
        pass

    sources.append(ManualProfile())
    return merge_state(sources)
