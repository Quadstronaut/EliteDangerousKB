"""
COVAS interactive REPL.

answer():  retrieve → gate on grounded → build_messages → chat_stream
           → validate_answer → regen once if invalid → else REFUSAL.
main():    load CmdrState once; read-print loop streaming to stdout.

Multi-hop path (config [copilot] multihop = true):
  decompose(query) → sub-queries → retrieve each → union chunks
  → single generation pass → UNCHANGED validate_answer gate over union.
  Default is false (byte-identical to today's single-hop path).
"""

from __future__ import annotations

import dataclasses
import io
import sys

from copilot import assemble, ollama_client, retriever
from copilot.assemble import REFUSAL
from copilot.models import CmdrState, RetrievalResult
from copilot.ollama_client import OllamaUnavailable
from copilot.paths import load_config
from copilot.retriever import retrieval_filters


def _union_results(results: list[RetrievalResult], tau: float) -> RetrievalResult:
    """Merge multiple RetrievalResults into one for a single generation pass.

    - Deduplicates chunks by chunk_id, keeping the copy with the higher score.
    - max_score = max over all chunks in the union.
    - grounded = union max_score >= tau.
    - query is taken from the first result (the original query).
    """
    if not results:
        # Edge case: return an empty, ungrounded result.
        return RetrievalResult(query="", chunks=[], max_score=0.0, grounded=False)

    by_id: dict[str, object] = {}  # chunk_id → Chunk (highest score wins)
    for res in results:
        for chunk in res.chunks:
            existing = by_id.get(chunk.chunk_id)
            if existing is None or chunk.score > existing.score:  # type: ignore[union-attr]
                by_id[chunk.chunk_id] = chunk

    union_chunks = list(by_id.values())
    max_score = max((c.score for c in union_chunks), default=0.0)  # type: ignore[union-attr]
    grounded = max_score >= tau

    return RetrievalResult(
        query=results[0].query,
        chunks=union_chunks,  # type: ignore[arg-type]
        max_score=max_score,
        grounded=grounded,
    )


def answer(query: str, state: CmdrState | None) -> str:
    """
    Full retrieval + generation pipeline with anti-hallucination gate.

    Returns the answer string, or REFUSAL when the gate fires.

    When config [copilot] multihop = true (default false):
      Uses copilot.multihop.decompose() to split the query into sub-queries,
      retrieves each independently, unions the chunks into one RetrievalResult
      (dedup by chunk_id, max_score = max over union), then runs a SINGLE
      generation pass and UNCHANGED validate_answer gate over the union.
      The empty-context refusal, tau floor, forced citation, and claim-grounding
      invariants all hold identically on the union path.
    """
    cfg = load_config()
    max_regen: int = cfg.get("copilot", {}).get("max_regen", 1)
    multihop: bool = bool(cfg.get("copilot", {}).get("multihop", False))
    filters = retrieval_filters(cfg)

    if multihop:
        # --- Multi-hop path ---
        # tau is only needed for union grounding; use 0.55 as the spec-defined floor.
        tau: float = float(cfg.get("retrieval", {}).get("tau", 0.55))
        from copilot.multihop import decompose
        sub_queries = decompose(query)
        sub_results = [
            retriever.retrieve(sq, filters=filters)
            for sq in sub_queries
        ]
        result = _union_results(sub_results, tau)
        # Restore original query for prompt assembly.
        result = dataclasses.replace(result, query=query)
    else:
        # --- Default single-hop path (byte-identical to before) ---
        # 1. Retrieve (honouring verified_only / include_unverified mode).
        result = retriever.retrieve(query, filters=filters)

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
