"""
Prompt assembly and answer validation for the COVAS copilot.

Keeps retrieval, profiling, and generation concerns separated:
  - build_messages(): assembles the messages list for chat_stream
  - validate_answer(): post-hoc citation-completeness check
  - SYSTEM_PROMPT: module constant; imported by tests
"""

from __future__ import annotations

import re

from copilot.models import CmdrState, ProfileFact, RetrievalResult

# Refusal string re-exported here so callers/tests can reference assemble.REFUSAL
# without importing repl (and to keep validate_answer free of a hard repl dep).
REFUSAL: str = "I don't have a verified source for that."

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are COVAS, an Elite Dangerous knowledge assistant for CMDR {cmdr_name}.

RULES (non-negotiable):
1. Answer ONLY from the CONTEXT block below. Do not use prior knowledge.
2. Every factual claim MUST end with its source in brackets: [chunk_id].
   Example: "You need Meta-Alloys to invite Felicity Farseer [a3f1c9b2]."
3. If the CONTEXT does not contain sufficient information to answer,
   reply with EXACTLY: "I don't have a verified source for that."
   Do not guess, estimate, or extrapolate.
4. If a chunk has a CHANGED NOTE, surface it clearly alongside the fact.
5. Be concise and practical. CMDR {cmdr_name} is an experienced commander.
""".strip()

# ---------------------------------------------------------------------------
# build_messages
# ---------------------------------------------------------------------------

def build_messages(
    query: str,
    result: RetrievalResult,
    state: CmdrState | None,
) -> list[dict]:
    """
    Build the messages list for ollama_client.chat_stream.

    Structure:
      [0] system  — SYSTEM_PROMPT + CMDR PROFILE block
      [1] user    — CONTEXT block + the query
    """
    cmdr_name = state.name if state else "Commander"

    # --- System message ---
    system_content = SYSTEM_PROMPT.format(cmdr_name=cmdr_name)
    if state:
        system_content += "\n\n" + _build_profile_block(state)

    # --- User message: context + query ---
    context_block = _build_context_block(result)
    user_content = f"{context_block}\n\nQUESTION: {query}"

    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content},
    ]


def _build_profile_block(state: CmdrState) -> str:
    lines = ["CMDR PROFILE:"]
    lines.append(f"  Name: {state.name}")

    for rank_key, rank_val in (state.ranks or {}).items():
        lines.append(f"  Rank[{rank_key}]: {rank_val}")

    if state.balance_cr is not None:
        lines.append(f"  Balance: {state.balance_cr:,} CR")

    for asset_key, asset_val in (state.assets or {}).items():
        lines.append(f"  Asset[{asset_key}]: {asset_val}")

    for goal in (state.goals or []):
        lines.append(f"  Goal: {goal}")

    # All ProfileFact entries — label manual ones.
    for fact in (state.facts or []):
        label = " (manual, unverified)" if fact.origin == "manual" else ""
        lines.append(f"  {fact.key}: {fact.value}{label}")

    return "\n".join(lines)


def _build_context_block(result: RetrievalResult) -> str:
    if not result.chunks:
        return "CONTEXT: (empty)"

    lines = ["CONTEXT:"]
    for chunk in result.chunks:
        entry = f"[{chunk.chunk_id}] {chunk.text}"
        if chunk.changed_note:
            entry += f"\n  CHANGED NOTE: {chunk.changed_note}"
        lines.append(entry)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# validate_answer
# ---------------------------------------------------------------------------

# Matches any [chunk_id] citation in the text. chunk_ids are lowercase hex of
# 8..16 chars (sha256[:16] in production; shorter ids appear in tests/fixtures).
_CITATION_RE = re.compile(r"\[([a-f0-9]{6,16})\]")

# Words too common to signal a claim is "about" a source. Kept small and
# generic so the grounding check stays permissive (we want to catch fabrication,
# not punish paraphrase).
_STOPWORDS = frozenset("""
a an the to of in on at for and or but with from by as is are was were be been
being you your yours i we our he she it they them their this that these those
will would can could should shall may might must do does did has have had not no
nor yes if then else than into out up down over under above below more most less
some any all each every both either neither one two three about which who whom what
when where how why use used using need needs needed get gets got make makes made
provide provides provided also just only very much many such per via near
""".split())

_WORD_RE = re.compile(r"[a-z0-9]+")


def _content_words(text: str) -> set[str]:
    """Lowercase content tokens: alnum runs ≥3 chars, minus stopwords.

    Splits on non-alphanumerics so "meta-alloys" → {"meta", "alloys"}, giving
    paraphrases a fair chance to overlap their source.
    """
    return {w for w in _WORD_RE.findall(text.lower()) if len(w) >= 3 and w not in _STOPWORDS}


def _claim_grounding_enabled() -> bool:
    """config[copilot][claim_grounding_check], default True (fail-safe to strict)."""
    try:
        from copilot.paths import load_config
        return bool(load_config().get("copilot", {}).get("claim_grounding_check", True))
    except Exception:
        return True


def _check_claim_grounding(answer: str, result: RetrievalResult) -> tuple[bool, str]:
    """Reject a citation whose preceding claim shares NO content word with the
    chunk it cites — the laundering case (a wrong claim with a real [id] glued on).

    Span attribution: the text from the previous citation up to each ``[id]`` is
    that id's claim. We require ≥1 shared content word with the cited chunk's
    text. Spans with <2 content words are too short to judge and pass (avoids
    false-rejecting "She is in Deciat [id]"-style fragments). This is lexical,
    not semantic — it catches gross fabrication, not subtle wrongness.
    """
    by_id = {c.chunk_id: c for c in result.chunks}
    prev = 0
    for m in _CITATION_RE.finditer(answer):
        cid = m.group(1)
        span = answer[prev:m.start()]
        prev = m.end()
        claim_words = _content_words(span)
        if len(claim_words) < 2:
            continue  # too little to judge — don't false-reject
        chunk = by_id.get(cid)
        if chunk is None:
            continue  # fabricated id is caught by the citation check below
        if claim_words & _content_words(chunk.text):
            continue  # anchored to its source
        return (
            False,
            f"Cited claim not supported by source [{cid}]: ...{span.strip()[-70:]!r}",
        )
    return True, "ok"


def validate_answer(
    answer: str,
    result: RetrievalResult,
    *,
    claim_grounding: bool | None = None,
) -> tuple[bool, str]:
    """
    Verify the answer is traceable to retrieved sources (the anti-BS gate).

    Layers, in order:

    1. The REFUSAL constant always passes.
    2. NO FABRICATED CITATIONS: every ``[id]`` cited must exist in result.chunks.
       A made-up source is the dangerous failure and is rejected outright.
    3. GROUNDED: the answer must carry at least one valid ``[id]`` citation.
    4. CLAIM GROUNDING (when enabled — config[copilot][claim_grounding_check],
       default ON): each cited claim must share content with the chunk it cites,
       so a confident WRONG claim with a real [id] glued on is rejected rather
       than laundered into a trusted answer. See _check_claim_grounding.

    Layer 4 is deliberately lexical and conservative (catch fabrication, pass
    paraphrase). It can be disabled per-call (claim_grounding=False) or via
    config when a stricter/looser posture is wanted.

    Returns (True, "ok") or (False, reason_string).
    """
    # Rule 1: refusal is always valid.
    if answer.strip() == REFUSAL.strip():
        return True, "ok"

    valid_ids = {c.chunk_id for c in result.chunks}
    cited = _CITATION_RE.findall(answer)

    # Rule 2: no fabricated citations.
    for cited_id in cited:
        if cited_id not in valid_ids:
            return False, f"Cited chunk_id [{cited_id}] not found in retrieval result."

    # Rule 3: must be grounded in at least one real source.
    if not cited:
        return False, "Answer contains no citation; not grounded in any source."

    # Rule 4: claims must be anchored to the source they cite.
    enabled = _claim_grounding_enabled() if claim_grounding is None else claim_grounding
    if enabled:
        return _check_claim_grounding(answer, result)

    return True, "ok"
