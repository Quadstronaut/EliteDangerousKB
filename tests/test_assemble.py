"""Tests for copilot/assemble.py — message building and answer validation."""
import pytest
from copilot.models import Chunk, CmdrState, RetrievalResult


def _make_chunk(
    chunk_id: str,
    text: str = "To unlock Felicity Farseer, provide Meta-Alloys and visit Deciat.",
) -> Chunk:
    return Chunk(
        chunk_id=chunk_id,
        text=text,
        kb_path="kb/test.md",
        heading_path="Test > Section",
        source_url="https://example.com",
        source_tier=1,
        source_count=2,
        verified=True,
        availability="live",
        changed_note=None,
        score=0.85,
    )


def _result(*chunk_ids: str) -> RetrievalResult:
    chunks = [_make_chunk(cid) for cid in chunk_ids]
    return RetrievalResult(
        query="test query",
        chunks=chunks,
        max_score=0.85,
        grounded=True,
    )


def _state() -> CmdrState:
    return CmdrState(
        name="Duvrazh",
        ranks={"combat": "Expert"},
        balance_cr=3_000_000_000,
    )


# ---------------------------------------------------------------------------
# build_messages
# ---------------------------------------------------------------------------

def test_build_messages_structure():
    from copilot import assemble
    result = _result("abc12345", "def67890")
    state = _state()

    msgs = assemble.build_messages("How to unlock Farseer?", result, state)

    roles = [m["role"] for m in msgs]
    assert roles[0] == "system"
    assert roles[-1] == "user"

    system_content = msgs[0]["content"]
    # System prompt must instruct citation and refusal
    assert "chunk_id" in system_content.lower() or "[" in system_content
    assert "I don't have" in system_content or "refusal" in system_content.lower() or "insufficient" in system_content.lower()

    # Profile block present
    combined = " ".join(m["content"] for m in msgs)
    assert "Duvrazh" in combined

    # Context block: each chunk_id must appear prefixed
    assert "[abc12345]" in combined
    assert "[def67890]" in combined

    # User query is last message content
    assert "How to unlock Farseer?" in msgs[-1]["content"]


def test_build_messages_manual_facts_labeled(monkeypatch):
    """Manual origin facts must be labeled '(manual, unverified)' in the profile block."""
    from copilot import assemble
    from copilot.models import ProfileFact

    state = CmdrState(
        name="Duvrazh",
        facts=[
            ProfileFact(
                key="goal.engineering",
                value="unlock all engineers",
                origin="manual",
                freshness="unknown",
                verified=False,
            )
        ],
    )
    result = _result("aaaa1111")
    msgs = assemble.build_messages("query", result, state)
    combined = " ".join(m["content"] for m in msgs)
    assert "(manual, unverified)" in combined


def test_build_messages_changed_note_present():
    """A chunk with a changed_note should surface the note in the context block."""
    from copilot import assemble
    chunk = Chunk(
        chunk_id="cccc2222",
        text="Powerplay 2 replaced Powerplay 1 in 2024.",
        kb_path="kb/powerplay/overview.md",
        heading_path="Powerplay > Overview",
        source_url=None,
        source_tier=1,
        source_count=1,
        verified=True,
        availability="changed",
        changed_note="Powerplay 1 → Powerplay 2, 2024 — old pledge modules gone.",
        score=0.80,
    )
    result = RetrievalResult(query="powerplay", chunks=[chunk], max_score=0.80, grounded=True)
    state = CmdrState(name="Duvrazh")
    msgs = assemble.build_messages("powerplay", result, state)
    combined = " ".join(m["content"] for m in msgs)
    assert "Powerplay 1 → Powerplay 2" in combined


# ---------------------------------------------------------------------------
# validate_answer
# ---------------------------------------------------------------------------

def test_validate_answer_clean_cited():
    """Every factual sentence carries a valid chunk_id → (True, 'ok')."""
    from copilot import assemble
    result = _result("abc12345")
    answer = "To unlock Farseer provide Meta-Alloys [abc12345]. Visit Deciat [abc12345]."
    ok, reason = assemble.validate_answer(answer, result)
    assert ok is True
    assert reason == "ok"


def test_validate_answer_no_citation_at_all():
    """An answer with ZERO citations is not grounded → (False, <reason>)."""
    from copilot import assemble
    result = _result("abc12345")
    answer = "Provide Meta-Alloys to Farseer. She is in Deciat."
    ok, reason = assemble.validate_answer(answer, result)
    assert ok is False
    assert reason  # non-empty explanation


def test_validate_answer_partial_citation_ok():
    """At least one valid citation + no fabricated ids → valid, even if not every
    sentence is cited. Real models cite claims but not list intros/transitions."""
    from copilot import assemble
    result = _result("abc12345")
    answer = "To unlock Farseer: provide Meta-Alloys [abc12345]. She is in Deciat."
    ok, reason = assemble.validate_answer(answer, result)
    assert ok is True
    assert reason == "ok"


def test_validate_answer_hallucinated_id():
    """A [chunk_id] not in result.chunks → (False, <reason>)."""
    from copilot import assemble
    result = _result("abc12345")
    # "xyz99999" is not in the result set.
    answer = "Farseer needs Meta-Alloys [xyz99999]."
    ok, reason = assemble.validate_answer(answer, result)
    assert ok is False
    assert "xyz99999" in reason or reason


def test_validate_answer_refusal_string_is_always_valid():
    """The REFUSAL constant itself must always pass validation (no citations needed)."""
    from copilot import assemble
    result = _result("abc12345")
    ok, reason = assemble.validate_answer(assemble.REFUSAL, result)
    assert ok is True


# ---------------------------------------------------------------------------
# council round-2: short-span grounded_count laundering fix
# ---------------------------------------------------------------------------

def test_short_intro_span_does_not_launder_fabricated_subsequent_claim():
    """A 1-word intro span before the first citation must NOT inflate grounded_count,
    allowing a subsequent fabricated claim with a valid [id] to pass undetected.

    Regression for: _check_claim_grounding short-span branch used to do
    `grounded_count += 1; continue` — letting any following ungrounded span
    pass as an 'uncertain paraphrase' even when it shares zero content words
    with its cited chunk.
    """
    from copilot import assemble
    from copilot.models import Chunk, RetrievalResult

    def _c(cid, text):
        return Chunk(
            chunk_id=cid, text=text, kb_path="kb/x.md", heading_path="X",
            source_url=None, source_tier=1, source_count=1, verified=True,
            availability="live", changed_note=None, score=0.9,
        )

    # chunk_a: words like "Farseer", "Meta-Alloys" — matched by short "alpha" span? No.
    chunk_a = _c("aa11bb22cc33dd44", "Farseer needs Meta-Alloys to unlock engineering.")
    # chunk_b: completely different domain words
    chunk_b = _c("bb33cc44dd55ee66", "Deciat star system location coordinates approach vector.")
    result = RetrievalResult(query="q", chunks=[chunk_a, chunk_b], max_score=0.9, grounded=True)

    # "alpha" = 1 content word (< 3) → neutral skip.
    # "omega sigma kappa lambda mu nu" = 6 content words, zero overlap with chunk_b → fabrication.
    answer = "alpha [aa11bb22cc33dd44]. omega sigma kappa lambda mu nu [bb33cc44dd55ee66]."
    ok, reason = assemble.validate_answer(answer, result, claim_grounding=True)

    assert ok is False, f"Expected rejection but got ok=True, reason={reason!r}"
    assert "bb33cc44dd55ee66" in reason
