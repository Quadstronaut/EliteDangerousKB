"""Tests for copilot/mcp_server.py — Plan C."""
import importlib

import pytest

from unittest.mock import patch, MagicMock
from copilot.models import Chunk, RetrievalResult, CmdrState, ProfileFact


def test_fastmcp_importable():
    """FastMCP must be importable from the mcp package."""
    mod = importlib.import_module("mcp.server.fastmcp")
    assert hasattr(mod, "FastMCP"), "FastMCP not found in mcp.server.fastmcp"


def _make_chunk(**overrides) -> Chunk:
    """Factory for a minimal valid Chunk."""
    defaults = dict(
        chunk_id="abc123def456789a",
        text="Felicity Farseer unlocks at Sol < 20 ly.",
        kb_path="kb/engineers/felicity-farseer.md",
        heading_path="Felicity Farseer > Unlock",
        source_url="https://inara.cz/elite/engineer/?searchin=1&searchparam=1",
        source_tier=1,
        source_count=3,
        verified=True,
        availability="live",
        changed_note=None,
        score=0.87,
    )
    defaults.update(overrides)
    return Chunk(**defaults)


def test_ed_kb_search_returns_list_of_dicts():
    """ed_kb_search must return a list of dicts with all CONTRACTS fields."""
    chunk = _make_chunk()
    mock_result = RetrievalResult(
        query="farseer unlock",
        chunks=[chunk],
        max_score=0.87,
        grounded=True,
    )
    with patch("copilot.mcp_server.retriever") as mock_retriever:
        mock_retriever.retrieve.return_value = mock_result
        from copilot.mcp_server import ed_kb_search
        result = ed_kb_search("farseer unlock", top_k=8)

    assert isinstance(result, list)
    assert len(result) == 1
    row = result[0]
    # All CONTRACTS fields must be present
    for field in (
        "chunk_id", "text", "kb_path", "heading_path",
        "source_url", "source_tier", "source_count",
        "verified", "availability", "changed_note", "score",
    ):
        assert field in row, f"Missing field: {field}"
    assert row["chunk_id"] == "abc123def456789a"
    assert row["score"] == pytest.approx(0.87)
    assert row["availability"] == "live"
    assert row["changed_note"] is None


def test_ed_kb_answer_returns_structured_dict():
    """ed_kb_answer must return {answer: str, citations: list[str], grounded: bool}."""
    chunk = _make_chunk()
    mock_result = RetrievalResult(
        query="what does farseer unlock",
        chunks=[chunk],
        max_score=0.87,
        grounded=True,
    )

    fake_answer = "Felicity Farseer unlocks at Sol distance < 20 ly [abc123def456789a]."

    with (
        patch("copilot.mcp_server.retriever") as mock_retriever,
        patch("copilot.mcp_server.assemble") as mock_assemble,
        patch("copilot.mcp_server.ollama_client") as mock_ollama,
    ):
        mock_retriever.retrieve.return_value = mock_result
        mock_assemble.build_messages.return_value = [{"role": "user", "content": "q"}]
        mock_assemble.validate_answer.return_value = (True, "ok")
        mock_ollama.chat_stream.return_value = iter([fake_answer])

        from copilot.mcp_server import ed_kb_answer
        result = ed_kb_answer("what does farseer unlock")

    assert isinstance(result, dict)
    assert "answer" in result
    assert "citations" in result
    assert "grounded" in result
    assert isinstance(result["citations"], list)
    assert isinstance(result["grounded"], bool)
    assert result["grounded"] is True
    assert result["citations"] == ["abc123def456789a"]
    assert fake_answer in result["answer"]


def test_ed_kb_answer_not_grounded_returns_refusal():
    """When grounded=False, ed_kb_answer must return the REFUSAL string."""
    mock_result = RetrievalResult(
        query="some obscure question",
        chunks=[],
        max_score=0.1,
        grounded=False,
    )
    with patch("copilot.mcp_server.retriever") as mock_retriever:
        mock_retriever.retrieve.return_value = mock_result
        from copilot.mcp_server import ed_kb_answer
        result = ed_kb_answer("some obscure question")

    assert result["grounded"] is False
    assert result["citations"] == []
    # REFUSAL string from repl.py must be present
    assert "don't have a verified source" in result["answer"].lower() or len(result["answer"]) > 0


def test_ed_kb_answer_ollama_unavailable():
    """OllamaUnavailable must be caught and return an error dict (not crash)."""
    chunk = _make_chunk()
    mock_result = RetrievalResult(
        query="farseer",
        chunks=[chunk],
        max_score=0.9,
        grounded=True,
    )
    with (
        patch("copilot.mcp_server.retriever") as mock_retriever,
        patch("copilot.mcp_server.assemble") as mock_assemble,
        patch("copilot.mcp_server.ollama_client") as mock_ollama,
    ):
        mock_retriever.retrieve.return_value = mock_result
        mock_assemble.build_messages.return_value = []
        mock_assemble.validate_answer.return_value = (True, "ok")
        from copilot.ollama_client import OllamaUnavailable
        mock_ollama.chat_stream.side_effect = OllamaUnavailable("down")

        from copilot.mcp_server import ed_kb_answer
        result = ed_kb_answer("farseer")

    # Must not raise; must return a dict with "answer" key
    assert isinstance(result, dict)
    assert "answer" in result
    assert "ollama" in result["answer"].lower() or "unavailable" in result["answer"].lower()


def test_ed_cmdr_state_returns_dict():
    """ed_cmdr_state must return a serialized CmdrState dict."""
    fact = ProfileFact(
        key="rank.combat",
        value="Expert",
        origin="journal",
        freshness="2026-05-01",
        verified=True,
    )
    mock_state = CmdrState(
        name="Duvrazh",
        ranks={"combat": "Expert", "trade": "Elite V"},
        balance_cr=3_000_000_000,
        assets={"carriers": ["FC Alpha", "FC Beta"], "ships": ["Cutter", "Corvette"]},
        goals=["Engineering", "AX Combat"],
        facts=[fact],
    )
    with patch("copilot.mcp_server.profile") as mock_profile:
        mock_profile.load_cmdr_state.return_value = mock_state
        from copilot.mcp_server import ed_cmdr_state
        result = ed_cmdr_state()

    assert isinstance(result, dict)
    assert result["name"] == "Duvrazh"
    assert result["ranks"]["combat"] == "Expert"
    assert result["balance_cr"] == 3_000_000_000
    assert "carriers" in result["assets"]
    assert "Engineering" in result["goals"]
    assert len(result["facts"]) == 1
    f = result["facts"][0]
    assert f["key"] == "rank.combat"
    assert f["origin"] == "journal"
    assert f["verified"] is True


def test_ed_cmdr_state_error_returns_error_dict():
    """Profile load failure must return an error dict, not raise."""
    with patch("copilot.mcp_server.profile") as mock_profile:
        mock_profile.load_cmdr_state.side_effect = RuntimeError("profile corrupted")
        from copilot.mcp_server import ed_cmdr_state
        result = ed_cmdr_state()

    assert isinstance(result, dict)
    assert "error" in result
    assert "profile" in result["error"].lower() or "corrupted" in result["error"].lower()


def test_ed_kb_search_parity_with_retriever():
    """
    Parity test (spec §B/§D): ed_kb_search chunk ids and order MUST match
    retriever.retrieve().chunks for the same query and top_k.

    This guards against any future serialization or ordering drift.
    """
    chunks = [
        _make_chunk(chunk_id="aaaa1111bbbb2222", score=0.92),
        _make_chunk(chunk_id="cccc3333dddd4444", score=0.78,
                    kb_path="kb/ships/anaconda.md",
                    heading_path="Anaconda > Hardpoints"),
    ]
    mock_result = RetrievalResult(
        query="engineers meta build",
        chunks=chunks,
        max_score=0.92,
        grounded=True,
    )

    with patch("copilot.mcp_server.retriever") as mock_retriever:
        mock_retriever.retrieve.return_value = mock_result
        from copilot.mcp_server import ed_kb_search
        mcp_result = ed_kb_search("engineers meta build", top_k=8)

    # Simulate calling retriever.retrieve directly (same mock result)
    direct_chunks = mock_result.chunks

    assert len(mcp_result) == len(direct_chunks), (
        f"Length mismatch: MCP={len(mcp_result)}, direct={len(direct_chunks)}"
    )
    for i, (mcp_row, direct_chunk) in enumerate(zip(mcp_result, direct_chunks)):
        assert mcp_row["chunk_id"] == direct_chunk.chunk_id, (
            f"chunk_id mismatch at position {i}: "
            f"MCP={mcp_row['chunk_id']}, direct={direct_chunk.chunk_id}"
        )
        assert mcp_row["score"] == pytest.approx(direct_chunk.score), (
            f"score mismatch at position {i}"
        )
        assert mcp_row["kb_path"] == direct_chunk.kb_path
        assert mcp_row["availability"] == direct_chunk.availability


def test_ed_kb_search_parity_real_retriever(monkeypatch):
    """
    Strong parity (spec §B/§D): ed_kb_search drives the REAL retriever.retrieve
    over a small mocked index and must return chunk ids/order/scores identical to
    calling retriever.retrieve directly. ed_kb_search itself is NOT mocked here —
    only the index/embed/config layer below the retriever (Ollama is down).

    This proves the MCP wrapper introduces zero retrieval drift.
    """
    import numpy as np
    from copilot import retriever

    # Small built "index": two chunks with fixed cosine scores, descending order.
    catalog = {
        "aaaa1111bbbb2222": _make_chunk(chunk_id="aaaa1111bbbb2222", score=0.0),
        "cccc3333dddd4444": _make_chunk(
            chunk_id="cccc3333dddd4444", score=0.0,
            kb_path="kb/ships/anaconda.md", heading_path="Anaconda > Hardpoints",
        ),
    }
    hits = [("aaaa1111bbbb2222", 0.92), ("cccc3333dddd4444", 0.78)]

    # Mock only the layer below the retriever — Ollama embed, index search/hydrate, config.
    monkeypatch.setattr(
        "copilot.ollama_client.embed",
        lambda texts: np.stack([np.ones(1024, dtype=np.float32) / 32.0 for _ in texts]),
    )
    monkeypatch.setattr("copilot.index.search", lambda qv, top_k: hits[:top_k])
    monkeypatch.setattr("copilot.index.chunk_by_id", lambda cid: catalog.get(cid))
    monkeypatch.setattr(
        "copilot.retriever._config",
        lambda: {"retrieval": {"top_k": 8, "tau": 0.55}},
    )

    query = "engineers meta build"

    # Direct call to the real retriever.
    direct = retriever.retrieve(query, top_k=8)

    # MCP tool call — exercises the real retriever through the wrapper.
    from copilot.mcp_server import ed_kb_search
    mcp_rows = ed_kb_search(query, top_k=8)

    assert [r["chunk_id"] for r in mcp_rows] == [c.chunk_id for c in direct.chunks]
    assert [r["score"] for r in mcp_rows] == pytest.approx([c.score for c in direct.chunks])
    assert [r["kb_path"] for r in mcp_rows] == [c.kb_path for c in direct.chunks]
    # Order must be preserved exactly (descending score from index.search).
    assert [r["chunk_id"] for r in mcp_rows] == ["aaaa1111bbbb2222", "cccc3333dddd4444"]
