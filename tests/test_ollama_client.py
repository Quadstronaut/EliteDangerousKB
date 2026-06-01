# tests/test_ollama_client.py
"""Tests for copilot/ollama_client.py — all mocked; no live Ollama required."""

import base64
import io
import json
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest


# ---------------------------------------------------------------------------
# Helpers to build fake streaming responses
# ---------------------------------------------------------------------------

def _stream_lines(*dicts) -> list[bytes]:
    """Return a list of newline-terminated JSON bytes, as Ollama would stream."""
    return [json.dumps(d).encode("utf-8") + b"\n" for d in dicts]


def _fake_post_embed(url, json=None, stream=False, timeout=None):
    """Fake requests.post for /api/embed — returns a single embedding vector."""
    n = len(json.get("input", []))
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    # bge-m3 returns 1024-dim vectors; use deterministic fake values
    resp.json.return_value = {
        "embeddings": [[float(i % 100) / 100.0] * 1024 for i in range(n)]
    }
    return resp


def _fake_post_chat_stream(chunks):
    """Return a mock requests.post for /api/chat stream=True."""
    def _post(url, json=None, stream=False, timeout=None):
        resp = MagicMock()
        resp.raise_for_status = MagicMock()
        resp.iter_lines.return_value = _stream_lines(*chunks)
        return resp
    return _post


# ---------------------------------------------------------------------------
# embed()
# ---------------------------------------------------------------------------

def test_embed_shape(monkeypatch):
    import requests
    from copilot import ollama_client
    monkeypatch.setattr(requests, "post", _fake_post_embed)

    result = ollama_client.embed(["hello", "world"])
    assert result.shape == (2, 1024), f"Expected (2, 1024), got {result.shape}"


def test_embed_dtype_float32(monkeypatch):
    import requests
    from copilot import ollama_client
    monkeypatch.setattr(requests, "post", _fake_post_embed)

    result = ollama_client.embed(["test"])
    assert result.dtype == np.float32, f"Expected float32, got {result.dtype}"


def test_embed_l2_normalized(monkeypatch):
    import requests
    from copilot import ollama_client
    monkeypatch.setattr(requests, "post", _fake_post_embed)

    result = ollama_client.embed(["normalize me", "and me"])
    norms = np.linalg.norm(result, axis=1)
    np.testing.assert_allclose(norms, np.ones(2), atol=1e-5,
                               err_msg="Each row must be L2-normalized to unit length")


def test_embed_single_text(monkeypatch):
    import requests
    from copilot import ollama_client
    monkeypatch.setattr(requests, "post", _fake_post_embed)

    result = ollama_client.embed(["solo"])
    assert result.shape == (1, 1024)


# ---------------------------------------------------------------------------
# OllamaUnavailable
# ---------------------------------------------------------------------------

def test_embed_raises_ollama_unavailable_on_connection_error(monkeypatch):
    import requests
    from copilot import ollama_client

    def _fail(*args, **kwargs):
        raise requests.ConnectionError("connection refused")

    monkeypatch.setattr(requests, "post", _fail)
    with pytest.raises(ollama_client.OllamaUnavailable):
        ollama_client.embed(["test"])


def test_chat_stream_raises_ollama_unavailable_on_connection_error(monkeypatch):
    import requests
    from copilot import ollama_client

    def _fail(*args, **kwargs):
        raise requests.ConnectionError("connection refused")

    monkeypatch.setattr(requests, "post", _fail)
    with pytest.raises(ollama_client.OllamaUnavailable):
        list(ollama_client.chat_stream([{"role": "user", "content": "hi"}]))


# ---------------------------------------------------------------------------
# chat_stream() — basic
# ---------------------------------------------------------------------------

def test_chat_stream_yields_content_deltas(monkeypatch):
    import requests
    from copilot import ollama_client

    chunks = [
        {"message": {"content": "Hello"}, "done": False},
        {"message": {"content": " Commander"}, "done": False},
        {"message": {"content": "."}, "done": True},
    ]
    monkeypatch.setattr(requests, "post", _fake_post_chat_stream(chunks))

    result = "".join(ollama_client.chat_stream([{"role": "user", "content": "greet"}]))
    assert result == "Hello Commander."


def test_chat_stream_empty_content_skipped(monkeypatch):
    import requests
    from copilot import ollama_client

    chunks = [
        {"message": {"content": "A"}, "done": False},
        {"message": {"content": ""}, "done": False},
        {"message": {"content": "B"}, "done": True},
    ]
    monkeypatch.setattr(requests, "post", _fake_post_chat_stream(chunks))

    result = "".join(ollama_client.chat_stream([{"role": "user", "content": "test"}]))
    assert result == "AB"


# ---------------------------------------------------------------------------
# chat_stream() — <think> stripping
# ---------------------------------------------------------------------------

def test_think_strip_complete_tag_in_single_chunk(monkeypatch):
    import requests
    from copilot import ollama_client

    chunks = [
        {"message": {"content": "<think>internal reasoning</think>actual answer"}, "done": True},
    ]
    monkeypatch.setattr(requests, "post", _fake_post_chat_stream(chunks))

    result = "".join(ollama_client.chat_stream([{"role": "user", "content": "q"}]))
    assert "<think>" not in result
    assert "internal reasoning" not in result
    assert "actual answer" in result


def test_think_strip_tags_split_across_chunks(monkeypatch):
    """<think> opens in one chunk, </think> closes in a later chunk — must strip across boundary."""
    import requests
    from copilot import ollama_client

    # Tags intentionally split: "<think" + ">" and "</think" + ">"
    chunks = [
        {"message": {"content": "Before <think"}, "done": False},
        {"message": {"content": ">this is reasoning"}, "done": False},
        {"message": {"content": " continues</think"}, "done": False},
        {"message": {"content": "> After"}, "done": True},
    ]
    monkeypatch.setattr(requests, "post", _fake_post_chat_stream(chunks))

    result = "".join(ollama_client.chat_stream([{"role": "user", "content": "q"}]))
    assert "reasoning" not in result
    assert "Before" in result
    assert "After" in result
    assert "<think" not in result
    assert "</think>" not in result


def test_think_strip_multiple_think_blocks(monkeypatch):
    import requests
    from copilot import ollama_client

    chunks = [
        {"message": {"content": "<think>first</think>answer1<think>second</think>answer2"}, "done": True},
    ]
    monkeypatch.setattr(requests, "post", _fake_post_chat_stream(chunks))

    result = "".join(ollama_client.chat_stream([{"role": "user", "content": "q"}]))
    assert result == "answer1answer2"


def test_think_strip_no_think_tag_passes_through(monkeypatch):
    import requests
    from copilot import ollama_client

    chunks = [
        {"message": {"content": "clean output"}, "done": True},
    ]
    monkeypatch.setattr(requests, "post", _fake_post_chat_stream(chunks))

    result = "".join(ollama_client.chat_stream([{"role": "user", "content": "q"}]))
    assert result == "clean output"


# ---------------------------------------------------------------------------
# vision()
# ---------------------------------------------------------------------------

def test_vision_returns_string(tmp_path, monkeypatch):
    import requests
    from copilot import ollama_client

    # Create a tiny fake PNG (1x1 pixel)
    fake_image = tmp_path / "screenshot.png"
    fake_image.write_bytes(
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
        b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00"
        b"\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18"
        b"\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
    )

    def _fake_vision_post(url, json=None, stream=False, timeout=None):
        resp = MagicMock()
        resp.raise_for_status = MagicMock()
        resp.json.return_value = {
            "message": {"content": "Combat: Expert, Trade: Elite V"}
        }
        return resp

    monkeypatch.setattr(requests, "post", _fake_vision_post)

    result = ollama_client.vision(str(fake_image), "What are the ranks?")
    assert isinstance(result, str)
    assert "Expert" in result


def test_vision_encodes_image_as_base64(tmp_path, monkeypatch):
    """Verify that the request payload contains a base64-encoded images field."""
    import requests
    from copilot import ollama_client

    fake_image = tmp_path / "img.png"
    raw_bytes = b"\x89PNG fake image bytes"
    fake_image.write_bytes(raw_bytes)

    captured_payload = {}

    def _capture_post(url, json=None, stream=False, timeout=None):
        captured_payload.update(json or {})
        resp = MagicMock()
        resp.raise_for_status = MagicMock()
        resp.json.return_value = {"message": {"content": "ok"}}
        return resp

    monkeypatch.setattr(requests, "post", _capture_post)
    ollama_client.vision(str(fake_image), "describe")

    assert "messages" in captured_payload
    msg = captured_payload["messages"][0]
    assert "images" in msg
    expected_b64 = base64.b64encode(raw_bytes).decode("ascii")
    assert msg["images"][0] == expected_b64


# ---------------------------------------------------------------------------
# Integration marker (skipped unless -m integration)
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_embed_live():
    from copilot import ollama_client
    result = ollama_client.embed(["Felicity Farseer unlock requirements"])
    assert result.shape == (1, 1024)
    norm = float(np.linalg.norm(result[0]))
    assert abs(norm - 1.0) < 1e-4
