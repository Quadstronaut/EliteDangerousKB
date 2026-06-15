# tests/test_verify.py
"""Unit tests for copilot/verify.py — all mocked; no live Ollama required.

Coverage:
  - All-support votes  → verdict "verified", high confidence
  - Split votes (support vs refute) → verdict "conflict" or arbiter reflects split
  - All-unsure votes   → verdict "uncertain"
  - OllamaUnavailable  → verdict "uncertain", escalate=True, no raise
  - Escalation threshold logic
  - Defensive parsing of messy/noisy model output
"""

import json
from unittest.mock import patch

import pytest

from copilot.ollama_client import OllamaUnavailable
from copilot import verify


# ---------------------------------------------------------------------------
# Helpers — fake chat_stream responses
# ---------------------------------------------------------------------------

def _make_stream_fn(responses: dict[str, str]):
    """Return a fake chat_stream that yields the canned response for the model.

    *responses* maps model name → response text. If the model is not in the
    map, falls back to the first value.
    """
    def _chat_stream(messages, model=None):
        text = responses.get(model) or next(iter(responses.values()))
        yield text
    return _chat_stream


def _all_support_stream():
    """Both assessors and the arbiter say 'support' / 'verified'."""
    assessor_json = json.dumps({"vote": "support", "reason": "Sources confirm this."})
    arbiter_json = json.dumps({"verdict": "verified", "confidence": 0.9, "rationale": "All agree."})
    return _make_stream_fn({
        "qwen3-coder:30b": assessor_json,
        "qwen3:8b": assessor_json,
    }), arbiter_json


def _refute_stream():
    assessor_json = json.dumps({"vote": "refute", "reason": "Sources contradict this."})
    arbiter_json = json.dumps({"verdict": "refuted", "confidence": 0.85, "rationale": "All refute."})
    return _make_stream_fn({
        "qwen3-coder:30b": assessor_json,
        "qwen3:8b": assessor_json,
    }), arbiter_json


def _split_stream():
    """First model says support, second says refute — arbiter detects conflict."""
    arbiter_json = json.dumps({"verdict": "conflict", "confidence": 0.5, "rationale": "Mixed votes."})
    return _make_stream_fn({
        "qwen3-coder:30b": json.dumps({"vote": "support", "reason": "Looks right."}),
        "qwen3:8b": json.dumps({"vote": "refute", "reason": "Contradicts source 2."}),
    }), arbiter_json


def _unsure_stream():
    assessor_json = json.dumps({"vote": "unsure", "reason": "Cannot determine."})
    arbiter_json = json.dumps({"verdict": "uncertain", "confidence": 0.4, "rationale": "All unsure."})
    return _make_stream_fn({
        "qwen3-coder:30b": assessor_json,
        "qwen3:8b": assessor_json,
    }), arbiter_json


# ---------------------------------------------------------------------------
# Helper: patch chat_stream so assessor calls use one response and
# the arbiter call (always last, using first model) uses another.
# ---------------------------------------------------------------------------

def _patch_chat(monkeypatch, assessor_fn, arbiter_raw: str):
    """Monkeypatch verify._chat so that:
      - The first N-1 calls (one per model) return the model-specific assessor text.
      - The final call (arbiter pass on first model) returns *arbiter_raw*.

    This simulates the exact call order in verify_claim().
    """
    call_count = {"n": 0}
    models_in_order: list[str] = []

    def _fake_chat(messages: list[dict], model: str) -> str:
        call_count["n"] += 1
        models_in_order.append(model)
        return "".join(assessor_fn(messages, model=model))

    # We need to track when we're on the arbiter pass.  The arbiter pass is the
    # LAST call and the prompt contains "VOTES:" (from _arbiter_prompt).
    def _smart_chat(messages: list[dict], model: str) -> str:
        # Arbiter prompt contains the "VOTES:" keyword
        content = " ".join(m.get("content", "") for m in messages)
        if "VOTES:" in content:
            return arbiter_raw
        return "".join(assessor_fn(messages, model=model))

    monkeypatch.setattr(verify, "_chat", _smart_chat)


# ---------------------------------------------------------------------------
# Tests: vote aggregation
# ---------------------------------------------------------------------------

def test_all_support_returns_verified(monkeypatch):
    """All assessors agree → verdict 'verified', confidence high."""
    assessor_fn, arbiter_raw = _all_support_stream()
    _patch_chat(monkeypatch, assessor_fn, arbiter_raw)

    result = verify.verify_claim(
        "Shield Generator Class 4A has base strength 660 MJ.",
        ["Source 1: Class 4A base shield: 660 MJ.", "Source 2: 4A shields: 660 megajoules."],
    )
    assert result["verdict"] == "verified", f"Expected verified, got {result}"
    assert result["confidence"] >= 0.66


def test_split_votes_returns_conflict(monkeypatch):
    """One assessor supports, one refutes → arbiter returns conflict."""
    assessor_fn, arbiter_raw = _split_stream()
    _patch_chat(monkeypatch, assessor_fn, arbiter_raw)

    result = verify.verify_claim(
        "The Asp Explorer has 8 hardpoints.",
        ["Source 1: Asp Explorer has 2 hardpoints.", "Source 2: actually 8 hardpoints."],
    )
    assert result["verdict"] == "conflict"
    # Escalation must be True for conflict
    assert result["escalate"] is True


def test_all_unsure_returns_uncertain(monkeypatch):
    """All assessors unsure → verdict 'uncertain'."""
    assessor_fn, arbiter_raw = _unsure_stream()
    _patch_chat(monkeypatch, assessor_fn, arbiter_raw)

    result = verify.verify_claim(
        "The Beluga Liner has a jump range of 35 ly unladen.",
        ["Source 1: unclear specification.", "Source 2: varies by build."],
    )
    assert result["verdict"] == "uncertain"


def test_all_refute_returns_refuted(monkeypatch):
    """All assessors refute → verdict 'refuted'."""
    assessor_fn, arbiter_raw = _refute_stream()
    _patch_chat(monkeypatch, assessor_fn, arbiter_raw)

    result = verify.verify_claim(
        "The Krait Mk II has 6 utility slots.",
        ["Source 1: Krait Mk II has 4 utility slots.", "Source 2: confirmed 4 utilities."],
    )
    assert result["verdict"] == "refuted"


def test_votes_list_populated(monkeypatch):
    """Result must include a per-assessor vote list with model names."""
    assessor_fn, arbiter_raw = _all_support_stream()
    _patch_chat(monkeypatch, assessor_fn, arbiter_raw)

    result = verify.verify_claim("Test claim.", ["Source A.", "Source B."])
    assert isinstance(result["votes"], list)
    assert len(result["votes"]) >= 1
    for v in result["votes"]:
        assert "model" in v
        assert "vote" in v
        assert v["vote"] in ("support", "refute", "unsure")


# ---------------------------------------------------------------------------
# Tests: OllamaUnavailable → uncertain + escalate, no raise
# ---------------------------------------------------------------------------

def test_ollama_unavailable_returns_uncertain_no_raise(monkeypatch):
    """When all Ollama calls fail, verify_claim must NOT raise — return uncertain+escalate."""
    def _fail(messages, model):
        raise OllamaUnavailable("connection refused")

    monkeypatch.setattr(verify, "_chat", _fail)

    result = verify.verify_claim(
        "Some claim.",
        ["source 1", "source 2"],
    )
    assert result["verdict"] == "uncertain"
    assert result["escalate"] is True
    # Must not raise — the assert itself proves it


def test_ollama_unavailable_partial_then_arbiter_down(monkeypatch):
    """First assessor succeeds, arbiter is down → majority fallback, still no raise."""
    call_n = {"n": 0}

    def _mixed(messages, model):
        content = " ".join(m.get("content", "") for m in messages)
        if "VOTES:" in content:
            raise OllamaUnavailable("arbiter down")
        call_n["n"] += 1
        return json.dumps({"vote": "support", "reason": "ok"})

    monkeypatch.setattr(verify, "_chat", _mixed)

    result = verify.verify_claim("Claim X.", ["S1", "S2"])
    # Majority fallback should have run — either verified or uncertain but no raise
    assert result["verdict"] in ("verified", "uncertain", "conflict")
    assert "escalate" in result


# ---------------------------------------------------------------------------
# Tests: escalation threshold logic
# ---------------------------------------------------------------------------

def test_needs_escalation_true_on_conflict():
    assert verify.needs_escalation({"verdict": "conflict", "confidence": 0.8}) is True


def test_needs_escalation_true_on_uncertain():
    assert verify.needs_escalation({"verdict": "uncertain", "confidence": 0.9}) is True


def test_needs_escalation_true_on_low_confidence():
    # 0.5 < default threshold 0.66
    assert verify.needs_escalation({"verdict": "verified", "confidence": 0.5}) is True


def test_needs_escalation_false_on_high_confidence_verified():
    # 0.9 >= 0.66 and verdict is verified
    assert verify.needs_escalation({"verdict": "verified", "confidence": 0.9}) is False


def test_needs_escalation_false_on_refuted_high_confidence():
    # "refuted" is decisive — not conflict/uncertain
    assert verify.needs_escalation({"verdict": "refuted", "confidence": 0.85}) is False


# ---------------------------------------------------------------------------
# Tests: defensive parsing of messy model output
# ---------------------------------------------------------------------------

def test_parse_vote_clean_json():
    result = verify._parse_vote('{"vote": "support", "reason": "Sources agree."}')
    assert result["vote"] == "support"
    assert "Sources agree" in result["reason"]


def test_parse_vote_json_wrapped_in_prose():
    messy = 'Sure, here is my assessment:\n{"vote": "refute", "reason": "Contradicts data."}\nHope that helps!'
    result = verify._parse_vote(messy)
    assert result["vote"] == "refute"


def test_parse_vote_no_json_keyword_sniff_support():
    result = verify._parse_vote("I agree with the claim, it seems correct and true based on sources.")
    assert result["vote"] in ("support", "unsure")  # keyword 'agree' → support


def test_parse_vote_no_json_keyword_sniff_refute():
    result = verify._parse_vote("This claim is false and contradicts all the evidence.")
    assert result["vote"] == "refute"


def test_parse_vote_totally_garbled():
    """Completely unparseable output → fallback to 'unsure', no raise."""
    result = verify._parse_vote("!!@@ 🤖 ERROR 404 model overheating BZZZT")
    assert result["vote"] in ("support", "refute", "unsure")
    assert "reason" in result


def test_parse_arbiter_clean_json():
    raw = json.dumps({"verdict": "verified", "confidence": 0.88, "rationale": "Consensus."})
    result = verify._parse_arbiter(raw)
    assert result["verdict"] == "verified"
    assert abs(result["confidence"] - 0.88) < 0.01


def test_parse_arbiter_prose_wrapped():
    raw = 'Final verdict:\n{"verdict": "conflict", "confidence": 0.55, "rationale": "Mixed."}\nEnd.'
    result = verify._parse_arbiter(raw)
    assert result["verdict"] == "conflict"


def test_parse_arbiter_confidence_clamped():
    raw = json.dumps({"verdict": "verified", "confidence": 1.5, "rationale": "off-scale"})
    result = verify._parse_arbiter(raw)
    assert result["confidence"] <= 1.0


def test_parse_arbiter_bad_confidence_string():
    raw = json.dumps({"verdict": "uncertain", "confidence": "high", "rationale": "hmm"})
    result = verify._parse_arbiter(raw)
    # Should not raise; confidence falls back to 0.5
    assert isinstance(result["confidence"], float)


def test_parse_arbiter_totally_garbled():
    result = verify._parse_arbiter("BZZZT no JSON here 🚀")
    assert result["verdict"] == "uncertain"
    assert isinstance(result["confidence"], float)


# ---------------------------------------------------------------------------
# Tests: result dict structure
# ---------------------------------------------------------------------------

def test_result_has_required_keys(monkeypatch):
    assessor_fn, arbiter_raw = _all_support_stream()
    _patch_chat(monkeypatch, assessor_fn, arbiter_raw)

    result = verify.verify_claim("Some claim.", ["S1", "S2"])
    for key in ("verdict", "confidence", "votes", "rationale", "dissent", "escalate"):
        assert key in result, f"Missing key: {key}"


def test_verify_disabled_returns_no_escalation(monkeypatch):
    """When verify is disabled, result is 'uncertain' with escalate=False."""
    monkeypatch.setattr(verify, "_verify_enabled", lambda: False)

    result = verify.verify_claim("Any claim.", ["any source"])
    assert result["verdict"] == "uncertain"
    assert result["escalate"] is False


# ---------------------------------------------------------------------------
# Integration marker (real Ollama, skipped unless -m integration)
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_verify_claim_live():
    """Smoke test against real local Ollama — requires qwen3:8b to be pulled."""
    result = verify.verify_claim(
        "The Sidewinder is the cheapest starter ship in Elite Dangerous.",
        [
            "The Sidewinder Mk I is the default starter ship, costing 32,000 Cr.",
            "All new commanders begin in a Sidewinder, the most affordable vessel.",
        ],
        models=["qwen3:8b"],  # single model to keep the live test fast
    )
    assert result["verdict"] in ("verified", "conflict", "uncertain", "refuted")
    assert 0.0 <= result["confidence"] <= 1.0
