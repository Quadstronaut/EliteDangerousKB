"""
MCP server for the ED Knowledge Engine COVAS copilot.

Exposes the shared retrieval core (retriever / assemble / profile) to Claude Code
via FastMCP over stdio. ZERO retrieval logic is implemented here — this module only
wraps Plan A functions.

Launch:
    python -m copilot.mcp_server
"""
from __future__ import annotations

import re

from mcp.server.fastmcp import FastMCP

from copilot import retriever, assemble, profile, ollama_client
from copilot.ollama_client import OllamaUnavailable
from copilot.paths import load_config
from copilot.repl import REFUSAL, _retrieval_filters

mcp = FastMCP("ed-covas")

# Same citation pattern the gate uses, to extract the ids the model actually cited.
_CITATION_RE = re.compile(r"\[([a-f0-9]{6,16})\]")


# ---------------------------------------------------------------------------
# Tool: ed_kb_search
# ---------------------------------------------------------------------------

@mcp.tool()
def ed_kb_search(query: str, top_k: int = 8) -> list[dict]:
    """
    Search the Elite Dangerous knowledge base.

    Returns a list of matching knowledge chunks ranked by semantic similarity.
    Each dict contains all CONTRACTS fields: chunk_id, text, kb_path,
    heading_path, source_url, source_tier, source_count, verified,
    availability, changed_note, score.

    Returns an error dict if retrieval fails.
    """
    try:
        filters = _retrieval_filters(load_config())
        result = retriever.retrieve(query, top_k=top_k, filters=filters)
        return [_chunk_to_dict(c) for c in result.chunks]
    except OllamaUnavailable:
        return [{"error": "Ollama unavailable — ensure localhost:11434 is running"}]
    except Exception as exc:  # noqa: BLE001
        return [{"error": f"Retrieval error: {exc}"}]


# ---------------------------------------------------------------------------
# Tool: ed_kb_answer
# ---------------------------------------------------------------------------

@mcp.tool()
def ed_kb_answer(query: str) -> dict:
    """
    Answer a question about Elite Dangerous using the verified knowledge base.

    Returns {answer, citations, grounded}.
    - answer: str — the generated answer (or a refusal string if not grounded)
    - citations: list[str] — chunk_ids cited in the answer
    - grounded: bool — True if retrieval score exceeded the tau threshold
    """
    try:
        filters = _retrieval_filters(load_config())
        result = retriever.retrieve(query, filters=filters)
        if not result.grounded:
            return {"answer": REFUSAL, "citations": [], "grounded": False}

        cmdr = _load_state_safe()
        messages = assemble.build_messages(query, result, cmdr)

        tokens: list[str] = []
        for delta in ollama_client.chat_stream(messages):
            tokens.append(delta)
        answer_text = "".join(tokens)

        ok, _reason = assemble.validate_answer(answer_text, result)
        if not ok:
            # One regen attempt, identical prompt
            tokens = []
            for delta in ollama_client.chat_stream(messages):
                tokens.append(delta)
            answer_text = "".join(tokens)
            ok, _reason = assemble.validate_answer(answer_text, result)

        if not ok:
            return {"answer": REFUSAL, "citations": [], "grounded": result.grounded}

        # Report the chunk_ids the answer ACTUALLY cited (intersected with the
        # retrieved set), not every retrieved chunk — a consumer must not be
        # told eight sources back a claim the model drew from one.
        retrieved_ids = {c.chunk_id for c in result.chunks}
        cited = [cid for cid in _CITATION_RE.findall(answer_text) if cid in retrieved_ids]
        # De-dupe while preserving order.
        citations = list(dict.fromkeys(cited))
        return {"answer": answer_text, "citations": citations, "grounded": result.grounded}

    except OllamaUnavailable:
        return {
            "answer": "Ollama unavailable — ensure localhost:11434 is running.",
            "citations": [],
            "grounded": False,
        }
    except Exception as exc:  # noqa: BLE001
        return {"answer": f"Error: {exc}", "citations": [], "grounded": False}


# ---------------------------------------------------------------------------
# Tool: ed_cmdr_state
# ---------------------------------------------------------------------------

@mcp.tool()
def ed_cmdr_state() -> dict:
    """
    Return the current CMDR state (name, ranks, balance, assets, goals, facts).

    Serializes profile.load_cmdr_state() to a plain dict suitable for JSON.
    """
    try:
        state = profile.load_cmdr_state()
        return _cmdr_state_to_dict(state)
    except Exception as exc:  # noqa: BLE001
        return {"error": f"Profile load error: {exc}"}


# ---------------------------------------------------------------------------
# Serialization helpers (not tools — internal only)
# ---------------------------------------------------------------------------

def _chunk_to_dict(chunk) -> dict:
    """Serialize a Chunk dataclass to a plain dict (all CONTRACTS fields)."""
    return {
        "chunk_id": chunk.chunk_id,
        "text": chunk.text,
        "kb_path": chunk.kb_path,
        "heading_path": chunk.heading_path,
        "source_url": chunk.source_url,
        "source_tier": chunk.source_tier,
        "source_count": chunk.source_count,
        "verified": chunk.verified,
        "availability": chunk.availability,
        "changed_note": chunk.changed_note,
        "score": float(chunk.score),
    }


def _cmdr_state_to_dict(state) -> dict:
    """Serialize a CmdrState dataclass to a plain dict."""
    return {
        "name": state.name,
        "ranks": dict(state.ranks),
        "balance_cr": state.balance_cr,
        "assets": state.assets,
        "goals": list(state.goals),
        "facts": [
            {
                "key": f.key,
                "value": f.value,
                "origin": f.origin,
                "freshness": f.freshness,
                "verified": f.verified,
            }
            for f in state.facts
        ],
    }


def _load_state_safe():
    """Load CmdrState, returning None on any error (profile is non-critical)."""
    try:
        return profile.load_cmdr_state()
    except Exception:  # noqa: BLE001
        return None


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
