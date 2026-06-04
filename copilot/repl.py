"""
COVAS interactive REPL.

answer():  retrieve → gate on grounded → build_messages → chat_stream
           → validate_answer → regen once if invalid → else REFUSAL.
main():    load CmdrState once; read-print loop streaming to stdout.
"""

from __future__ import annotations

import io
import sys

from copilot import assemble, ollama_client, retriever
from copilot.assemble import REFUSAL
from copilot.models import CmdrState
from copilot.ollama_client import OllamaUnavailable
from copilot.paths import load_config
from copilot.retriever import retrieval_filters


def answer(query: str, state: CmdrState | None) -> str:
    """
    Full retrieval + generation pipeline with anti-hallucination gate.

    Returns the answer string, or REFUSAL when the gate fires.
    """
    cfg = load_config()
    max_regen: int = cfg.get("copilot", {}).get("max_regen", 1)

    # 1. Retrieve (honouring verified_only / include_unverified mode).
    result = retriever.retrieve(query, filters=retrieval_filters(cfg))
    if not result.grounded:
        return REFUSAL

    # 2. Build messages and generate.
    messages = assemble.build_messages(query, result, state)

    def _generate() -> str:
        parts: list[str] = []
        for delta in ollama_client.chat_stream(messages):
            parts.append(delta)
        return "".join(parts)

    # 3. Generate, then regen up to max_regen times if the gate fires.
    # First attempt always runs; max_regen controls how many extra tries follow.
    text = _generate()
    ok, _ = assemble.validate_answer(text, result)
    if ok:
        return text

    for _ in range(max_regen):
        text = _generate()
        ok, _ = assemble.validate_answer(text, result)
        if ok:
            return text

    return REFUSAL


def main() -> None:
    """Interactive REPL: load state once, loop stdin → stdout (streamed)."""
    # PowerShell 5.1 prepends a UTF-8 BOM (U+FEFF) on the first piped line.
    # Re-wrapping stdin with utf-8-sig auto-strips it so 'exit' is recognised.
    # Guard: only rewrap when stdin has a real binary buffer AND is not already
    # using utf-8-sig (e.g. second call to main(), or already re-wrapped).
    try:
        buf = getattr(sys.stdin, "buffer", None)
        enc = getattr(sys.stdin, "encoding", None)
        if buf is not None and enc != "utf-8-sig" and hasattr(buf, "raw"):
            sys.stdin = io.TextIOWrapper(buf, encoding="utf-8-sig")
    except Exception:  # noqa: BLE001 — never let BOM-strip break the REPL boot
        pass

    from copilot.profile import load_cmdr_state

    try:
        state = load_cmdr_state()
    except Exception as exc:  # noqa: BLE001
        print(f"[COVAS] Warning: could not load CMDR state ({exc}). Continuing without profile.")
        state = None

    print(f"[COVAS] Ready. CMDR {state.name if state else 'Commander'}, how can I help?")
    print("[COVAS] Type 'exit' or Ctrl-C to quit.\n")

    while True:
        try:
            query = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[COVAS] Goodbye, Commander.")
            break

        if not query:
            continue
        if query.lower() in {"exit", "quit", "q"}:
            print("[COVAS] Goodbye, Commander.")
            break

        # Route through answer(): it retrieves, generates, and runs the
        # anti-hallucination gate BEFORE returning. We never display ungated
        # text — a hallucinated draft must not flash on screen ahead of the
        # gate. Streaming is traded away for that guarantee.
        print("[COVAS] ...thinking", flush=True)
        try:
            reply = answer(query, state)
        except OllamaUnavailable as exc:
            print(f"COVAS: Ollama is unavailable right now ({exc}).")
            print("       Start it with `ollama serve`, then ask again.\n")
            continue
        except Exception as exc:  # noqa: BLE001 — never let the loop die
            print(f"COVAS: Sorry, that query failed ({exc}). Try again.\n")
            continue

        print(f"COVAS: {reply}\n")


if __name__ == "__main__":
    main()
