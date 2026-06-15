"""keep_alive wiring (DRIFT-6) — config[ollama].keep_alive must be sent on every
Ollama request so models stay resident between loop phases and REPL turns.
"""
import json

from copilot import ollama_client


class _EmbedResp:
    def raise_for_status(self):
        pass

    def json(self):
        return {"embeddings": [[0.0] * 1024]}


class _ChatResp:
    def raise_for_status(self):
        pass

    def iter_lines(self):
        return iter([json.dumps({"message": {"content": "hi"}}).encode()])


class _VisionResp:
    def raise_for_status(self):
        pass

    def json(self):
        return {"message": {"content": "ok"}}


def _capture(monkeypatch, resp):
    captured = {}

    def fake_post(url, json=None, **kw):
        captured["json"] = json
        return resp

    monkeypatch.setattr(ollama_client.requests, "post", fake_post)
    return captured


def test_embed_sends_keep_alive(monkeypatch):
    captured = _capture(monkeypatch, _EmbedResp())
    ollama_client.embed(["x"])
    assert captured["json"].get("keep_alive")


def test_chat_stream_sends_keep_alive(monkeypatch):
    captured = _capture(monkeypatch, _ChatResp())
    list(ollama_client.chat_stream([{"role": "user", "content": "hi"}]))
    assert captured["json"].get("keep_alive")


def test_vision_sends_keep_alive(monkeypatch, tmp_path):
    img = tmp_path / "x.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n")
    captured = _capture(monkeypatch, _VisionResp())
    ollama_client.vision(str(img), "describe")
    assert captured["json"].get("keep_alive")
