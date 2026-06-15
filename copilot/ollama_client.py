# copilot/ollama_client.py
"""Thin Ollama HTTP client for the ED Knowledge Engine + COVAS Copilot.

Three entry points:
  embed()       — bge-m3 embeddings → L2-normalised float32 ndarray
  chat_stream() — qwen3:8b streaming chat with <think>…</think> stripped
  vision()      — qwen3-vl:8b multimodal (image + prompt → str)

OllamaUnavailable is raised on any requests.RequestException (connection
refused, read timeout, HTTP error, mid-stream drop) and on malformed
responses, so callers degrade gracefully rather than propagate raw errors.

Spec §F: the copilot path (embed + chat_stream) uses only lightweight models
(bge-m3, qwen3:8b) so it stays fast even when qwen3-coder:30b is resident.
"""

import base64
import json
from pathlib import Path
from typing import Iterator

import numpy as np
import requests


class OllamaUnavailable(RuntimeError):
    """Raised when the local Ollama server at localhost:11434 is unreachable."""


def _base_url() -> str:
    """Read base_url from config at call time (allows test patching of config.toml)."""
    try:
        from copilot.paths import load_config
        return load_config()["ollama"]["base_url"]
    except Exception:
        return "http://localhost:11434"


def _model(key: str) -> str:
    """Read a model name from config[ollama][key]."""
    try:
        from copilot.paths import load_config
        return load_config()["ollama"][key]
    except Exception:
        defaults = {
            "chat_model": "qwen3:8b",
            "embed_model": "bge-m3",
            "vision_model": "qwen3-vl:8b",
        }
        return defaults.get(key, "qwen3:8b")


def _keep_alive() -> str:
    """Read keep_alive from config[ollama]; controls how long Ollama keeps a model
    resident after a call. Wiring it (CONTRACTS lists keep_alive but it was never
    sent — DRIFT-6) avoids cold-reloads between loop phases and REPL turns. Default
    '5m' matches config.toml."""
    try:
        from copilot.paths import load_config
        return str(load_config()["ollama"].get("keep_alive", "5m"))
    except Exception:
        return "5m"


# ---------------------------------------------------------------------------
# Embedding
# ---------------------------------------------------------------------------

def embed(texts: list[str]) -> np.ndarray:
    """Embed *texts* via bge-m3 and return an (N, 1024) float32 L2-normalised array.

    POST /api/embed with {"model": embed_model, "input": texts}.
    Raises OllamaUnavailable on connection failure.
    """
    try:
        resp = requests.post(
            f"{_base_url()}/api/embed",
            json={"model": _model("embed_model"), "input": texts, "keep_alive": _keep_alive()},
            timeout=120,
        )
        resp.raise_for_status()
    except requests.RequestException as exc:
        # ConnectionError (server down), ReadTimeout (slow/hung model),
        # HTTPError (model not loaded → 4xx/5xx) are all RequestException
        # subclasses. Collapse them so callers degrade gracefully instead of
        # crashing on a raw traceback.
        raise OllamaUnavailable(
            f"Ollama embedding request failed: {exc}. "
            "Ensure `ollama serve` is running and bge-m3 is pulled."
        ) from exc

    data = resp.json()
    if "embeddings" not in data:
        raise OllamaUnavailable(
            f"Malformed Ollama embed response (no 'embeddings' field): {data!r}"
        )
    vectors = np.array(data["embeddings"], dtype=np.float32)  # (N, 1024)

    # L2-normalise each row so cosine similarity = dot product.
    # Zero-vector rows (degenerate input) can't be scaled to unit length, so
    # substitute a canonical unit vector (component 0 = 1.0) to preserve the
    # "every row L2-normalised" invariant downstream code relies on.
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    zero_rows = (norms[:, 0] == 0)
    if np.any(zero_rows):
        vectors[zero_rows, 0] = 1.0
        norms[zero_rows, 0] = 1.0
    return vectors / norms


# ---------------------------------------------------------------------------
# Chat streaming with <think> stripping
# ---------------------------------------------------------------------------

class _ThinkStripper:
    """Stateful filter that removes <think>…</think> spans from a token stream.

    Tags may be split across chunk boundaries:
      chunk 1: "prefix <think"
      chunk 2: ">reasoning here</think"
      chunk 3: "> suffix"
    The buffer accumulates partial tag text and flushes only when it can
    determine whether the buffered text is safe to emit.
    """

    def __init__(self):
        self._buf = ""          # partial tag accumulation
        self._in_think = False  # True while inside a <think>…</think> span

    def feed(self, text: str) -> str:
        """Process *text*, return the filtered string safe to emit now."""
        self._buf += text
        output = []

        while self._buf:
            if self._in_think:
                # Consume until we find </think>
                end = self._buf.find("</think>")
                if end == -1:
                    # Might still be a partial </think> tag at the tail
                    # Keep enough to detect a split close-tag
                    safe_len = max(0, len(self._buf) - len("</think>"))
                    # Nothing to emit while inside think
                    self._buf = self._buf[safe_len:]  # discard consumed
                    break
                else:
                    # Consume through the closing tag; emit nothing
                    self._buf = self._buf[end + len("</think>"):]
                    self._in_think = False
            else:
                # Look for the next opening tag
                start = self._buf.find("<think>")
                if start == -1:
                    # No complete opening tag — check for a partial at tail
                    # The longest possible partial prefix of "<think>" is 7 chars
                    partial_len = min(len("<think>") - 1, len(self._buf))
                    tail = self._buf[-partial_len:] if partial_len else ""
                    # Check if tail is a prefix of "<think>"
                    is_partial = any(
                        "<think>".startswith(tail[-i:])
                        for i in range(1, len(tail) + 1)
                    ) if tail else False

                    if is_partial:
                        # Emit everything before the possible partial tag
                        safe_part = self._buf[:-len(tail)]
                        output.append(safe_part)
                        self._buf = tail
                    else:
                        output.append(self._buf)
                        self._buf = ""
                    break
                else:
                    # Emit text before the opening tag, then enter think mode
                    output.append(self._buf[:start])
                    self._buf = self._buf[start + len("<think>"):]
                    self._in_think = True

        return "".join(output)

    def flush(self) -> str:
        """Flush any remaining buffered text that is not inside a think block."""
        if self._in_think:
            self._buf = ""
            return ""
        result = self._buf
        self._buf = ""
        return result


def chat_stream(
    messages: list[dict],
    model: str | None = None,
) -> Iterator[str]:
    """Stream a chat completion from Ollama, yielding text deltas.

    - Uses chat_model from config unless *model* is provided.
    - Strips <think>…</think> spans (qwen3 reasoning) even when tags split
      across streaming chunks.
    - Raises OllamaUnavailable on connection failure.
    """
    use_model = model or _model("chat_model")
    # think=False disables qwen3's chain-of-thought at the source: otherwise the
    # model spends the entire timeout emitting reasoning we'd only strip anyway
    # (a cold load + thinking blew past 300s; think=False returns in ~load time).
    # The _ThinkStripper below stays as a safety net for models that ignore the flag.
    try:
        resp = requests.post(
            f"{_base_url()}/api/chat",
            json={"model": use_model, "messages": messages, "stream": True,
                  "think": False, "keep_alive": _keep_alive()},
            stream=True,
            # First-token timeout. A cold model swap under VRAM pressure can take
            # minutes (observed ~298s); keep headroom so a load never trips it.
            # The launch healthcheck (5s /api/tags) already catches a down server.
            timeout=600,
        )
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise OllamaUnavailable(
            f"Ollama chat request failed: {exc}. Ensure `ollama serve` is running."
        ) from exc

    stripper = _ThinkStripper()
    try:
        for raw_line in resp.iter_lines():
            if not raw_line:
                continue
            try:
                obj = json.loads(raw_line)
            except json.JSONDecodeError:
                continue
            delta = obj.get("message", {}).get("content", "")
            if delta:
                filtered = stripper.feed(delta)
                if filtered:
                    yield filtered
    except requests.RequestException as exc:
        # Connection dropped mid-stream (ChunkedEncodingError / ReadTimeout
        # while iterating). Surface as OllamaUnavailable so the REPL/MCP loop
        # can recover instead of dying.
        raise OllamaUnavailable(f"Ollama stream interrupted: {exc}") from exc

    # Flush any buffered text after the stream ends
    tail = stripper.flush()
    if tail:
        yield tail


# ---------------------------------------------------------------------------
# Vision
# ---------------------------------------------------------------------------

def vision(image_path: str, prompt: str) -> str:
    """Describe or extract data from *image_path* using qwen3-vl:8b.

    Encodes the image as base64 and sends it to /api/chat with the user prompt.
    Returns the full response content string.
    Raises OllamaUnavailable on connection failure.
    """
    try:
        image_bytes = Path(image_path).read_bytes()
    except OSError as exc:
        # Missing/unreadable screenshot is a caller error, not an Ollama outage.
        raise FileNotFoundError(f"Vision image not readable: {image_path} ({exc})") from exc
    b64 = base64.b64encode(image_bytes).decode("ascii")

    try:
        resp = requests.post(
            f"{_base_url()}/api/chat",
            json={
                "model": _model("vision_model"),
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                        "images": [b64],
                    }
                ],
                "stream": False,
                "keep_alive": _keep_alive(),
            },
            timeout=300,
        )
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise OllamaUnavailable(
            f"Ollama vision request failed: {exc}. Ensure `ollama serve` is running."
        ) from exc

    data = resp.json()
    try:
        return data["message"]["content"]
    except (KeyError, TypeError) as exc:
        raise OllamaUnavailable(
            f"Malformed Ollama vision response: {data!r}"
        ) from exc
