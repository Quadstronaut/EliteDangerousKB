"""
COVAS interactive REPL.

answer():  retrieve → gate on grounded → build_messages → chat_stream
           → validate_answer → regen once if invalid → else REFUSAL.
main():    load CmdrState once; read-print loop streaming to stdout.
"""

from __future__ import annotations

import sys
from typing import Iterator

from copilot import assemble, ollama_client, retriever
from copilot.models import CmdrState
from copilot.ollama_client import OllamaUnavailable
from copilot.paths import load_config

REFUSAL: str = "I don't have a verified source for that."


def _retrieval_filters(cfg: dict) -> dict | None:
    """Translate config[copilot][mode] into retrieve() filters.

    verified_only (the default) restricts retrieval to chunks flagged
    verified=True — the trust boundary the spec promises. include_unverified
    drops the filter so lower-tier capture chunks are eligible.
    """
    mode = cfg.get("copilot", {}).get("mode", "verified_only")
    return {"verified": True} if mode == "verified_only" else None


def answer(query: str, state: CmdrState | None) -> str:
    """
    Full retrieval + generation pipeline with anti-hallucination gate.

    Returns the answer string, or REFUSAL when the gate fires.
    """
    cfg = load_config()
    max_regen: int = cfg.get("copilot", {}).get("max_regen", 1)

    # 1. Retrieve (honouring verified_only / include_unverified mode).
    result = retriever.retrieve(query, filters=_retrieval_filters(cfg))
    if not result.grounded:
        return REFUSAL

    # 2. Build messages and generate.
    messages = assemble.build_messages(query, result, state)

    def _generate() -> str:
        parts: list[str] = []
        for delta in ollama_client.chat_stream(messages):
            parts.append(delta)
        return "".join(parts)

    text = _generate()
    ok, _ = assemble.validate_answer(text, result)
    if ok:
        return text

    # 3. One regen attempt.
    if max_regen >= 1:
        text = _generate()
        ok, _ = assemble.validate_answer(text, result)
        if ok:
            return text

    return REFUSAL


def main() -> None:
    """Interactive REPL: load state once, loop stdin → stdout (streamed)."""
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
