"""
copilot/multihop.py — Multi-hop query decomposition scaffold.

DECISION A (Stage-0 spec): DEFER — ship a tested, importable scaffold now.
Full multi-hop (LLM-driven decomposition + iterative retrieve) is deferred
until the eval signal below justifies the extra round-trip and gate surface.

EVAL SIGNAL THAT FLIPS THIS TO ON:
  Build multi-hop for real (LLM-driven decomposition) when
  copilot.eval.retrieval_metrics shows recall_at_k on a multi-hop golden
  subset (records tagged "multihop": true in eval/golden_questions.json)
  materially below the single-hop recall_at_k at the same top_k.

  Concretely: if union-of-top-k provably misses cross-chunk facts on the
  tagged subset — i.e. the gap closes when we decompose and retrieve
  per-sub-query — then the extra round-trip is justified and
  MULTIHOP_ENABLED should be flipped to True and connected to an
  LLM-based decomposer.

  At ~5 pages / 27 chunks with top_k=8 the single dense retrieval already
  pulls a large fraction of the entire KB into context, so the multi-hop
  queries ("which engineer unlocks X and where are they") are in practice
  answerable from top-8 because co-occurring facts share the same retrieval
  window. The deferral is falsifiable, not vibes.

PUBLIC INTERFACE:
  MULTIHOP_ENABLED: bool        — module-level flag, default False.
  decompose(query) -> list[str] — pure, no I/O, no network, no Ollama.
"""

from __future__ import annotations

import re

# Module-level flag consumed by repl.answer() to gate the multi-hop path.
# Default OFF — the default config (config.toml [copilot] multihop = false)
# must produce byte-identical behaviour to the single-hop path.
MULTIHOP_ENABLED: bool = False

# ---------------------------------------------------------------------------
# Conjunction markers that signal explicit multi-hop shapes.
# Order matters: more specific patterns first.
# ---------------------------------------------------------------------------

# "X and where are they located" / "X and where is she"
_WHERE_CONJ_RE = re.compile(
    r"\s+and\s+(where\s+(?:are|is|can|do|does)\b.+)",
    re.IGNORECASE,
)

# "X then Y" — sequential steps
_THEN_RE = re.compile(
    r"^(.+?)\s+then\s+(.+)$",
    re.IGNORECASE,
)

# "X and Y" — parallel sub-questions (generic; lowest priority)
_AND_RE = re.compile(
    r"^(.+?)\s+and\s+(.+)$",
    re.IGNORECASE,
)


def decompose(query: str) -> list[str]:
    """Split a query into ordered sub-queries for recognised multi-hop shapes.

    Pure: no I/O, no network, no Ollama.  Always returns a non-empty list.
    Single-hop / unrecognised shapes return [query] unchanged.

    Recognised patterns (applied in order, first match wins):
      1. "... and where are/is/can they/she ..." → [prefix, "where are ..."]
      2. "... then ..."                           → [part1, part2]
      3. "... and ..."                            → [part1, part2]

    Args:
        query: The raw user query string.

    Returns:
        An ordered list of >=1 non-empty sub-query strings.
        decompose("") → [""].
    """
    # Always return at least one element; never return empty list.
    if not query:
        return [""]

    stripped = query.strip()

    # Pattern 1: "...and where are/is/can/do/does..."
    m = _WHERE_CONJ_RE.search(stripped)
    if m:
        prefix = stripped[: m.start()].strip()
        suffix = m.group(1).strip()
        if prefix and suffix:
            return [prefix, suffix]

    # Pattern 2: "X then Y"
    m = _THEN_RE.match(stripped)
    if m:
        part1 = m.group(1).strip()
        part2 = m.group(2).strip()
        if part1 and part2:
            return [part1, part2]

    # Pattern 3: "X and Y" — generic conjunction
    m = _AND_RE.match(stripped)
    if m:
        part1 = m.group(1).strip()
        part2 = m.group(2).strip()
        if part1 and part2:
            return [part1, part2]

    # Single-hop: return unchanged.
    return [stripped]
