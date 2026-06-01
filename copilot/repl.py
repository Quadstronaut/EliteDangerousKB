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
from copilot.paths import load_config

REFUSAL: str = "I don't have a verified source for that."


def answer(query: str, state: CmdrState | None) -> str:
    """
    Full retrieval + generation pipeline with anti-hallucination gate.

    Returns the answer string, or REFUSAL when the gate fires.
    """
    cfg = load_config()
    max_regen: int = cfg.get("copilot", {}).get("max_regen", 1)

    # 1. Retrieve.
    result = retriever.retrieve(query)
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

        result = retriever.retrieve(query)
        if not result.grounded:
            print(f"COVAS: {REFUSAL}\n")
            continue

        messages = assemble.build_messages(query, result, state)
        print("COVAS: ", end="", flush=True)
        parts: list[str] = []
        for delta in ollama_client.chat_stream(messages):
            print(delta, end="", flush=True)
            parts.append(delta)
        print()  # newline after streamed answer

        text = "".join(parts)
        ok, reason = assemble.validate_answer(text, result)
        if not ok:
            # Try one regen silently; if it fails, print the refusal.
            parts2: list[str] = []
            for delta in ollama_client.chat_stream(messages):
                parts2.append(delta)
            text2 = "".join(parts2)
            ok2, _ = assemble.validate_answer(text2, result)
            if ok2:
                # Replace the printed answer with the valid regen.
                print(f"\r[corrected] COVAS: {text2}\n")
            else:
                print(f"\nCOVAS: {REFUSAL}\n")
        else:
            print()


if __name__ == "__main__":
    main()
