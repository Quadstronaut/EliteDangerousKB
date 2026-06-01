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

# Sentence tokeniser: split on period/exclamation/question + whitespace.
_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")

# Short words that typically are not factual claims.
_NON_CLAIM_PATTERNS = re.compile(
    r"^(ok|okay|yes|no|sure|right|great|alright|thanks|thank you|you're welcome"
    r"|of course|absolutely|certainly|noted)\s*\.?$",
    re.IGNORECASE,
)


def validate_answer(answer: str, result: RetrievalResult) -> tuple[bool, str]:
    """
    Check citation completeness.

    Rules:
    1. The REFUSAL constant always passes.
    2. Every [id] cited must exist in result.chunks.
    3. Every sentence that is a factual claim (not a pleasantry, not the refusal
       string, not a question) must contain at least one [chunk_id].

    Returns (True, "ok") or (False, reason_string).
    """
    # Rule 0: refusal is always valid.
    if answer.strip() == REFUSAL.strip():
        return True, "ok"

    valid_ids = {c.chunk_id for c in result.chunks}

    # Rule 2: every cited id must be in result.chunks.
    for cited_id in _CITATION_RE.findall(answer):
        if cited_id not in valid_ids:
            return False, f"Cited chunk_id [{cited_id}] not found in retrieval result."

    # Rule 3: every factual sentence must contain a citation.
    sentences = _SENTENCE_RE.split(answer.strip())
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        if _is_non_factual(sentence):
            continue
        if not _CITATION_RE.search(sentence):
            return False, (
                f"Factual sentence missing citation: \"{sentence[:80]}\""
            )

    return True, "ok"


def _is_non_factual(sentence: str) -> bool:
    """Return True if the sentence is unlikely to be a factual claim."""
    if _NON_CLAIM_PATTERNS.match(sentence):
        return True
    # Questions are not claims.
    if sentence.endswith("?"):
        return True
    # Very short sentences (≤3 words) that contain no nouns are probably greetings.
    words = sentence.split()
    if len(words) <= 3 and not any(w[0].isupper() for w in words[1:]):
        return True
    return False
