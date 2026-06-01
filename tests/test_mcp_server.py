"""Tests for copilot/mcp_server.py — Plan C."""
import importlib

import pytest

from unittest.mock import patch, MagicMock
from copilot.models import Chunk, RetrievalResult


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
