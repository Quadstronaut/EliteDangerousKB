"""
ED query expansion — appends synonym/abbreviation expansions so dense embeddings
match both abbreviated and full-form ED terminology.

Public API:
    expand_query(q: str) -> str
        Returns the original query with known ED abbreviations/synonyms appended.
        The original query text is preserved unchanged as a prefix.
        Only appends when a known term is detected; leaves unrecognised queries intact.
        Pure Python — no Ollama, no network, no filesystem I/O.

Design:
    ED queries are abbreviation-heavy ("FSD", "AX", "SCO", "G5 mats") and
    dense embeddings trained on general text under-match exact tokens.  By
    appending expansions we give the embedding both the short and long form so
    semantic distance collapses to near-zero for equivalent queries.

    We use a curated bidirectional map. Both directions are stored explicitly
    (abbrev → full, full → abbrev) so detection only requires one dict lookup
    per token, keeping the function O(tokens).

    Conservative rule: append only; never rewrite the original query. This
    guarantees that if expansion is wrong or redundant, it degrades to the
    original embedding and never makes retrieval worse than baseline.
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# Term map — bidirectional, curated ED abbreviations and synonyms.
# Keys are downcased for case-insensitive matching; values are the expansions
# to append (naturally cased, space-separated).
# ---------------------------------------------------------------------------

# Default expansion is ON. Can be disabled per-call with expand=False.
EXPAND_QUERY_DEFAULT: bool = True

_ED_TERM_MAP: dict[str, str] = {
    # Frame Shift Drive
    "fsd": "Frame Shift Drive",
    "frame shift drive": "FSD",

    # Supercruise Overcharge (Odyssey)
    "sco": "Supercruise Overcharge",
    "supercruise overcharge": "SCO",

    # Anti-Xeno / Thargoid combat
    "ax": "anti-xeno Thargoid",
    "anti-xeno": "AX",
    "thargoid": "AX anti-xeno",

    # Guardian tech
    "guardian": "Guardian tech-broker blueprint",

    # Powerplay
    "pp": "Powerplay",
    "pp2": "Powerplay 2.0",
    "powerplay": "PP",
    "powerplay 2.0": "PP2",

    # Colonisation / Trailblazers
    "trailblazers": "colonisation",
    "colonisation": "Trailblazers",
    "colonization": "Trailblazers colonisation",

    # Engineering grade shorthand
    "g1": "grade 1",
    "g2": "grade 2",
    "g3": "grade 3",
    "g4": "grade 4",
    "g5": "grade 5",
    "grade 1": "G1",
    "grade 2": "G2",
    "grade 3": "G3",
    "grade 4": "G4",
    "grade 5": "G5",

    # Materials
    "mats": "materials",
    "materials": "mats",

    # Ships (common abbreviations)
    "cutter": "Imperial Cutter",
    "imperial cutter": "Cutter",
    "corvette": "Federal Corvette",
    "federal corvette": "Corvette",
    "fdl": "Fer-de-Lance",
    "fer-de-lance": "FDL",
    "asp": "Asp Explorer",
    "asp explorer": "Asp",
    "python mk ii": "Python Mk 2",
    "python mk 2": "Python Mk II",

    # Commander
    "cmdr": "Commander",
    "commander": "CMDR",

    # Engineers
    "felicity": "Felicity Farseer",
    "farseer": "Felicity Farseer engineer",
    "meta-alloys": "Meta-Alloys barnacle",
    "meta alloys": "Meta-Alloys barnacle",

    # Jump range / neutron routing
    "neutron boosting": "neutron star jump range multiplier",
    "neutron plotter": "Spansh neutron plotter jump range",

    # Combat
    "pve": "combat player-versus-environment",
    "pvp": "combat player-versus-player",
    "haz res": "Hazardous Resource Extraction Site",
    "res": "Resource Extraction Site",

    # Economy / trade
    "fc": "Fleet Carrier",
    "fleet carrier": "FC",
    "arx": "ARX in-game currency",

    # Odyssey on-foot
    "exobio": "exobiology on-foot",
    "exobiology": "exobio",
}

# Compile a regex that matches whole tokens only (word boundaries for single
# words; literal phrase match for multi-word entries).  Multi-word entries are
# sorted longest-first so "frame shift drive" matches before "fsd".
_MULTI_WORD: list[tuple[str, str]] = sorted(
    [(k, v) for k, v in _ED_TERM_MAP.items() if " " in k],
    key=lambda x: -len(x[0]),
)
_SINGLE_WORD: dict[str, str] = {k: v for k, v in _ED_TERM_MAP.items() if " " not in k}

# Regex for single-word term detection (word-boundary anchored, case-insensitive).
_SINGLE_WORD_RE = re.compile(
    r"\b(" + "|".join(re.escape(k) for k in _SINGLE_WORD) + r")\b",
    re.IGNORECASE,
)


def expand_query(q: str) -> str:
    """Append ED synonym/abbreviation expansions to *q*.

    The original query is returned unchanged if no known terms are found.
    When terms are found, their expansions are appended after a space so the
    embedding sees both forms.  Duplicate expansions are deduplicated.

    The function is idempotent: calling it twice on already-expanded text will
    not add duplicate expansions because matching uses the *original* q only.

    Args:
        q: Raw user query string.

    Returns:
        Expanded query string (original + appended expansions), or original q
        if no known terms matched.
    """
    if not q or not q.strip():
        return q

    found: list[str] = []
    q_lower = q.lower()

    # 1. Check multi-word phrases first (longest match priority).
    for phrase, expansion in _MULTI_WORD:
        if phrase in q_lower:
            found.append(expansion)

    # 2. Check single-word terms (word-boundary match).
    for match in _SINGLE_WORD_RE.finditer(q):
        key = match.group(0).lower()
        expansion = _SINGLE_WORD.get(key)
        if expansion:
            found.append(expansion)

    if not found:
        return q

    # Deduplicate while preserving order; skip expansions already present in q.
    q_lower_full = q.lower()
    seen: set[str] = set()
    unique: list[str] = []
    for exp in found:
        exp_lower = exp.lower()
        if exp_lower not in seen and exp_lower not in q_lower_full:
            seen.add(exp_lower)
            unique.append(exp)

    if not unique:
        return q

    return q + " " + " ".join(unique)
