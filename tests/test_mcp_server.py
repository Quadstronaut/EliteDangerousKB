"""Tests for copilot/mcp_server.py — Plan C."""
import importlib

import pytest


def test_fastmcp_importable():
    """FastMCP must be importable from the mcp package."""
    mod = importlib.import_module("mcp.server.fastmcp")
    assert hasattr(mod, "FastMCP"), "FastMCP not found in mcp.server.fastmcp"
