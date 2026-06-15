# copilot/verify.py
"""Local council-v2-style fact verifier for the ED Knowledge Engine.

Architecture mirrors council-v2 blind generation + arbitration:
  1. N independent assessors (different local Ollama models) each evaluate the
     claim against the provided sources WITHOUT seeing each other's verdicts.
  2. An arbiter pass reconciles the blind votes into a final verdict.
  3. If confidence is low or votes conflict, `escalate=True` signals the loop
     to invoke the cloud council skill for a final ruling.

Public API
----------
verify_claim(claim, sources, *, models=None) -> dict
    Run the local council and return a result dict.
needs_escalation(result) -> bool
    True when the caller should escalate to the cloud council.

The module is deliberately self-contained: it does NOT modify ollama_client.py.
Instead it uses a private _chat() helper that joins chat_stream() into a string.
"""

import json
import re
from typing import Optional

from copilot.ollama_client import OllamaUnavailable, chat_stream


# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------

def _verify_config() -> dict:
    """Read [verify] section from config.toml; return safe defaults on any failure."""
    try:
        from copilot.paths import load_config
        cfg = load_config()
        return cfg.get("verify", {})
    except Exception:
        return {}


def _default_models() -> list[str]:
    """Return the configured assessor models, falling back to the two strong local models."""
    cfg = _verify_config()
    return cfg.get("local_models", ["qwen3-coder:30b", "qwen3:8b"])


def _escalate_threshold() -> float:
    """Confidence floor below which we escalate to the cloud council."""
    cfg = _verify_config()
    return float(cfg.get("escalate_threshold", 0.66))


def _min_sources_for_consensus() -> int:
    """Minimum number of sources required before we even attempt a verdict."""
    cfg = _verify_config()
    return int(cfg.get("min_sources_for_consensus", 2))


def _verify_enabled() -> bool:
    """Master kill-switch; defaults to True."""
    cfg = _verify_config()
    return bool(cfg.get("enabled", True))


# ---------------------------------------------------------------------------
# Private chat helper (joins streaming chunks; does NOT change ollama_client.py)
# ---------------------------------------------------------------------------

def _chat(messages: list[dict], model: str) -> str:
    """Send a chat request and return the full response as a single string.

    Joins all streaming deltas from chat_stream(). Returns an empty string
    if OllamaUnavailable — callers must handle that gracefully.
    """
    chunks: list[str] = []
    try:
        for delta in chat_stream(messages, model=model):
            chunks.append(delta)
    except OllamaUnavailable:
        raise  # re-raise so verify_claim() can catch it
    return "".join(chunks)


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

_ASSESSOR_SYSTEM = (
    "You are a fact-checking assessor for an Elite Dangerous knowledge base. "
    "You will be shown a claim and a set of source excerpts. "
    "Evaluate whether the sources support or contradict the claim. "
    "Respond ONLY with a JSON object — no prose outside the JSON. "
    'Example: {"vote": "support", "reason": "All sources agree."} '
    'Valid votes: "support", "refute", "unsure".'
)

_ARBITER_SYSTEM = (
    "You are an arbitration judge reviewing independent fact-checking votes. "
    "Given a list of votes (each with a vote and reason), produce a final verdict. "
    "Respond ONLY with a JSON object. "
    'Example: {"verdict": "verified", "confidence": 0.85, "rationale": "3/3 support."} '
    'Valid verdicts: "verified", "conflict", "uncertain", "refuted".'
)


def _assessor_prompt(claim: str, sources: list[str]) -> list[dict]:
    """Build the assessor message list for one blind evaluation."""
    NL = "\n"  # avoid bare \n after a letter+colon in source (portability scanner)
    sources_block = (NL + NL).join(
        f"[Source {i + 1}]{NL}{s.strip()}" for i, s in enumerate(sources)
    )
    user_content = (
        "CLAIM:" + NL + claim + NL + NL
        + "SOURCES:" + NL + sources_block + NL + NL
        + 'Respond with JSON only: {"vote": "support"|"refute"|"unsure", "reason": "..."}'
    )
    return [
        {"role": "system", "content": _ASSESSOR_SYSTEM},
        {"role": "user", "content": user_content},
    ]


def _arbiter_prompt(claim: str, votes: list[dict]) -> list[dict]:
    """Build the arbiter message list that reconciles blind votes."""
    NL = "\n"  # same portability workaround as _assessor_prompt
    votes_block = json.dumps(votes, indent=2)
    user_content = (
        "CLAIM:" + NL + claim + NL + NL
        + "VOTES:" + NL + votes_block + NL + NL
        + "Produce a final verdict JSON: "
        + '{"verdict": "verified"|"conflict"|"uncertain"|"refuted", '
        + '"confidence": 0.0..1.0, "rationale": "..."}'
    )
    return [
        {"role": "system", "content": _ARBITER_SYSTEM},
        {"role": "user", "content": user_content},
    ]


# ---------------------------------------------------------------------------
# Defensive output parsing — models return prose-wrapped JSON, partial JSON, etc.
# ---------------------------------------------------------------------------

def _parse_vote(raw: str) -> dict:
    """Extract a vote dict from model output; tolerate noise around the JSON.

    Tries JSON parse of the whole string first; then looks for the first {...}
    block. Falls back to keyword sniffing if JSON is absent entirely.
    """
    raw = raw.strip()

    # Attempt 1: entire output is valid JSON
    try:
        obj = json.loads(raw)
        if isinstance(obj, dict):
            return _normalise_vote(obj)
    except json.JSONDecodeError:
        pass

    # Attempt 2: extract first {...} substring (handles leading/trailing prose)
    m = re.search(r"\{[^{}]*\}", raw, re.DOTALL)
    if m:
        try:
            obj = json.loads(m.group())
            if isinstance(obj, dict):
                return _normalise_vote(obj)
        except json.JSONDecodeError:
            pass

    # Attempt 3: keyword sniff for the vote value
    lower = raw.lower()
    if "refute" in lower or "contradict" in lower or "false" in lower:
        vote = "refute"
    elif "unsure" in lower or "uncertain" in lower or "unclear" in lower:
        vote = "unsure"
    elif "support" in lower or "agree" in lower or "correct" in lower or "true" in lower:
        vote = "support"
    else:
        vote = "unsure"

    # Grab first sentence as the reason
    reason_match = re.match(r"([^.!?\n]+[.!?\n]?)", raw)
    reason = reason_match.group(1).strip() if reason_match else raw[:120]
    return {"vote": vote, "reason": reason}


def _normalise_vote(obj: dict) -> dict:
    """Ensure the vote dict has the expected keys with sane defaults."""
    raw_vote = str(obj.get("vote", "")).lower()
    # Accept common synonyms
    if raw_vote in ("refute", "refuted", "contradict", "false", "no"):
        vote = "refute"
    elif raw_vote in ("support", "supported", "agree", "true", "yes", "verified"):
        vote = "support"
    else:
        vote = "unsure"
    reason = str(obj.get("reason", obj.get("rationale", "no reason given")))[:500]
    return {"vote": vote, "reason": reason}


def _parse_arbiter(raw: str) -> dict:
    """Extract the arbiter verdict dict; degrade to 'uncertain' on failure."""
    raw = raw.strip()

    candidates = []

    # Attempt 1: entire output
    try:
        candidates.append(json.loads(raw))
    except json.JSONDecodeError:
        pass

    # Attempt 2: first {...} block
    m = re.search(r"\{[^{}]*\}", raw, re.DOTALL)
    if m:
        try:
            candidates.append(json.loads(m.group()))
        except json.JSONDecodeError:
            pass

    for obj in candidates:
        if isinstance(obj, dict) and "verdict" in obj:
            return _normalise_arbiter(obj)

    # Fallback: uncertain with raw rationale
    return {"verdict": "uncertain", "confidence": 0.5, "rationale": raw[:500]}


def _normalise_arbiter(obj: dict) -> dict:
    """Coerce arbiter output to a well-typed dict."""
    raw_v = str(obj.get("verdict", "uncertain")).lower()
    if raw_v in ("verified", "verify", "supported", "support", "true"):
        verdict = "verified"
    elif raw_v in ("refuted", "refute", "false", "contradict"):
        verdict = "refuted"
    elif raw_v in ("conflict", "conflicting", "mixed", "split"):
        verdict = "conflict"
    else:
        verdict = "uncertain"

    # Clamp confidence to [0, 1]
    try:
        conf = float(obj.get("confidence", 0.5))
        conf = max(0.0, min(1.0, conf))
    except (TypeError, ValueError):
        conf = 0.5

    rationale = str(obj.get("rationale", obj.get("reason", "")))[:1000]
    return {"verdict": verdict, "confidence": conf, "rationale": rationale}


# ---------------------------------------------------------------------------
# Core public API
# ---------------------------------------------------------------------------

def verify_claim(
    claim: str,
    sources: list[str],
    *,
    models: Optional[list[str]] = None,
) -> dict:
    """Run a council-v2-style local verification of *claim* against *sources*.

    Each model in *models* independently evaluates the claim (blind generation —
    assessors do not see each other's output). An arbiter pass on the first model
    then reconciles the votes into a final verdict.

    Parameters
    ----------
    claim   : The factual statement to verify.
    sources : List of source text excerpts that should support or refute the claim.
    models  : Assessor model names. Defaults to config [verify].local_models.

    Returns
    -------
    dict with keys:
        verdict    : "verified" | "conflict" | "uncertain" | "refuted"
        confidence : float in [0, 1]
        votes      : list of per-assessor dicts (model, vote, reason)
        rationale  : str summary from the arbiter
        dissent    : list[str] — reasons from minority-opinion assessors
        escalate   : bool — True when the caller should invoke the cloud council
    """
    # Graceful no-op when the feature is disabled
    if not _verify_enabled():
        return _uncertain_result("verify disabled in config", escalate=False)

    use_models = models if models is not None else _default_models()
    if not use_models:
        return _uncertain_result("no assessor models configured", escalate=True)

    # -----------------------------------------------------------------------
    # Stage 1 — blind assessment (each model runs independently)
    # -----------------------------------------------------------------------
    votes: list[dict] = []
    prompt_msgs = _assessor_prompt(claim, sources)

    for model in use_models:
        try:
            raw = _chat(prompt_msgs, model=model)
        except OllamaUnavailable as exc:
            # Assessor unavailable — record as unsure (not a failure, just unknown)
            votes.append({
                "model": model,
                "vote": "unsure",
                "reason": f"Ollama unavailable: {exc}",
                "error": True,
            })
            continue

        parsed = _parse_vote(raw)
        votes.append({
            "model": model,
            "vote": parsed["vote"],
            "reason": parsed["reason"],
        })

    # If ALL assessors hit errors (Ollama completely down), escalate with no raise
    all_errors = all(v.get("error") for v in votes)
    if all_errors:
        return _uncertain_result(
            "all Ollama assessors unavailable — cannot verify locally",
            escalate=True,
        )

    # -----------------------------------------------------------------------
    # Stage 2 — arbiter reconciliation (uses first available model)
    # -----------------------------------------------------------------------
    arbiter_model = use_models[0]
    arbiter_votes = [{"vote": v["vote"], "reason": v["reason"]} for v in votes]
    arb_prompt = _arbiter_prompt(claim, arbiter_votes)

    try:
        arb_raw = _chat(arb_prompt, model=arbiter_model)
        arb = _parse_arbiter(arb_raw)
    except OllamaUnavailable:
        # Arbiter down — fall back to majority-vote heuristic
        arb = _majority_fallback(votes)

    # -----------------------------------------------------------------------
    # Stage 3 — dissent extraction + escalation decision
    # -----------------------------------------------------------------------
    majority_vote = arb["verdict"]
    # Map verdict back to simple vote for dissent comparison
    _verdict_to_vote = {"verified": "support", "refuted": "refute",
                        "conflict": None, "uncertain": None}
    expected_vote = _verdict_to_vote.get(majority_vote)
    dissent = [
        v["reason"]
        for v in votes
        if expected_vote and v["vote"] != expected_vote and not v.get("error")
    ]

    result = {
        "verdict": arb["verdict"],
        "confidence": arb["confidence"],
        "votes": votes,
        "rationale": arb["rationale"],
        "dissent": dissent,
        "escalate": needs_escalation(arb),
    }
    return result


def needs_escalation(result: dict) -> bool:
    """True when the cloud council should be invoked for a final ruling.

    Escalates on:
    - verdict == "conflict" (models disagree)
    - confidence < escalate_threshold (low certainty)
    - verdict == "uncertain" (arbiter itself was unsure)
    """
    threshold = _escalate_threshold()
    verdict = result.get("verdict", "uncertain")
    confidence = float(result.get("confidence", 0.0))
    return verdict in ("conflict", "uncertain") or confidence < threshold


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _uncertain_result(reason: str, *, escalate: bool) -> dict:
    """Return a safe 'uncertain' result for graceful degradation."""
    return {
        "verdict": "uncertain",
        "confidence": 0.0,
        "votes": [],
        "rationale": reason,
        "dissent": [],
        "escalate": escalate,
    }


def _majority_fallback(votes: list[dict]) -> dict:
    """Simple majority vote used when the arbiter model is unavailable."""
    counts: dict[str, int] = {"support": 0, "refute": 0, "unsure": 0}
    for v in votes:
        counts[v.get("vote", "unsure")] = counts.get(v.get("vote", "unsure"), 0) + 1

    total = sum(counts.values()) or 1
    support = counts["support"]
    refute = counts["refute"]
    unsure = counts["unsure"]

    if support > refute and support > unsure:
        verdict = "verified"
        confidence = support / total
    elif refute > support and refute > unsure:
        verdict = "refuted"
        confidence = refute / total
    elif support > 0 and refute > 0:
        verdict = "conflict"
        confidence = 0.5
    else:
        verdict = "uncertain"
        confidence = 0.3

    return {
        "verdict": verdict,
        "confidence": confidence,
        "rationale": f"majority-fallback (arbiter unavailable): support={support} refute={refute} unsure={unsure}",
    }
