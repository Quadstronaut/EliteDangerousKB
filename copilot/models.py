# copilot/models.py
"""Shared dataclasses for the ED Knowledge Engine + COVAS Copilot.

These are the canonical types imported by all plans (A/B/C/D).
CONTRACTS.md is the single source of truth — do not add fields here without
updating CONTRACTS.md first.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Chunk:
    chunk_id: str            # = sha256((kb_path + "::" + heading_path).encode()).hexdigest()[:16]
    text: str                # clean embeddable text: breadcrumb prepended; frontmatter/wikilinks/URLs stripped
    kb_path: str             # e.g. "kb/engineers/felicity-farseer.md"
    heading_path: str        # e.g. "Felicity Farseer > Unlock"
    source_url: str | None
    source_tier: int         # 0..3
    source_count: int
    verified: bool
    availability: str        # "live" | "seasonal" | "changed"
    changed_note: str | None
    score: float = 0.0       # cosine similarity; set at retrieval time (copy via dataclasses.replace)


@dataclass
class RetrievalResult:
    query: str
    chunks: list[Chunk]
    max_score: float
    grounded: bool           # max_score >= config.retrieval.tau


@dataclass
class ProfileFact:
    key: str                 # e.g. "rank.combat", "ship.cutter.owned", "balance_cr"
    value: str
    origin: str              # "game-state-json"|"journal"|"screenshot"|"3rd-party"|"manual"
    freshness: str           # ISO date or "unknown"
    verified: bool           # True from logs/game-state; False from manual/vision


@dataclass
class CmdrState:
    name: str
    ranks: dict[str, str] = field(default_factory=dict)   # {"combat":"Expert",...}
    balance_cr: int | None = None
    assets: dict = field(default_factory=dict)            # {"carriers":[...], "ships":[...]}
    goals: list[str] = field(default_factory=list)
    facts: list[ProfileFact] = field(default_factory=list)
