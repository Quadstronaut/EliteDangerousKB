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


# ===========================================================================
# Meta-commands (council-v2-spec Stage 1)
# ===========================================================================
# Questions about the TOOL ("help", "what's in your database", "sources") are
# not KB facts — routing them through answer() -> RAG -> gate yields a spurious
# REFUSAL. meta_command() intercepts a small, CLOSED set of these BEFORE
# answer(), serving responses built ONLY from static text + the KB manifest.
#
# PURITY (hard contract): no network, no Ollama, no retriever.retrieve. The
# ONLY external read is index.load_manifest() (which honours the paths
# indirection tests monkeypatch). Recognition is WHOLE-STRING equality against
# the closed token/phrasing sets below — never substring/prefix/fuzzy — so a
# real question with an appended subject ("what do you know about sol") falls
# through to answer() and the gate stays in charge of real facts.

# Group A — capabilities ("help").
_HELP_TOKENS: frozenset[str] = frozenset({
    "help", "?", "commands", "menu",
    "what can you do",
    "what commands can you accept",
    "what commands do you accept",
    "what can i type",
    "what can i ask",
    "how do i use this",
})

# Group B — knowledge inventory ("topics").
_TOPICS_TOKENS: frozenset[str] = frozenset({
    "topics", "topic", "coverage",
    "what do you know",
    "what do you know about",
    "what topics do you know",
    "what's in your database",
    "whats in your database",
    "what is in your database",
    "what's in your knowledge base",
    "whats in your knowledge base",
    "what pages do you have",
})

# Group C — sources roster ("sources").
_SOURCES_TOKENS: frozenset[str] = frozenset({
    "sources", "source",
    "where do you get your data",
    "what are your sources",
})

# Max KB pages to render verbatim before collapsing the tail into "(+K more)".
# The COUNT always reflects the true total regardless of this cap.
_MAX_VISIBLE_PAGES = 40


def _normalize(query: str) -> str:
    """Spec-fixed normalization: strip, lowercase, drop trailing '?', strip again.

    Trailing '?' and case are ignored; interior text is NOT otherwise mangled.
    Exception: a bare "?" is itself a recognised help token, so when stripping
    the trailing '?' would empty the string we keep the literal "?" instead of
    collapsing it to "" (which would otherwise fall through to answer()).
    """
    base = query.strip().lower()
    stripped = base.rstrip("?").strip()
    if not stripped and base:
        # The whole input was "?" (or "???") — preserve the bare help token.
        return "?"
    return stripped


def _help_text(state: CmdrState | None) -> str:
    """Capability summary. Static — no manifest, no network.

    Assembled via a join on newline so no literal colon-then-backslash sequence
    appears in source (the portability guard's drive-letter regex would
    false-positive on a header line that ends in a colon before an escaped
    newline); newlines are added at join time, not inside string literals.
    """
    name = state.name if state is not None else "Commander"
    lines = [
        f"I'm COVAS, your Elite Dangerous knowledge assistant, CMDR {name}.",
        "I answer ONLY from my verified knowledge base. If I can't ground an "
        "answer in a source, I refuse and say I have no verified source for it, "
        "rather than guess.",
        "",
        "Commands you can type",
        "  help     - show this (also '?', 'commands', 'menu')",
        "  topics   - what my knowledge base covers (pages + chunk counts)",
        "  sources  - where my data comes from (the source roster + tiers)",
        "  exit     - quit (also 'quit', 'q', or Ctrl-C)",
        "",
        "Anything else is treated as a question. Ask about engineers, systems, "
        "ships, materials, unlocks, sites; I'll answer if I have a verified "
        "source, and refuse if I don't.",
    ]
    return "\n".join(lines)


def _topics_text() -> str:
    """Knowledge inventory rendered from the KB manifest only.

    Tolerates a missing/empty manifest and malformed entries (missing kb_path
    are skipped, not raised). Page list is sorted for deterministic output.
    """
    from copilot import index

    try:
        manifest = index.load_manifest()
    except Exception:  # noqa: BLE001 — never let a bad manifest crash a meta reply
        manifest = {}

    if not manifest:
        return (
            "My knowledge base is empty right now — I have no indexed pages yet. "
            "The research loop populates it over time; once it has run and the "
            "index is built, ask 'topics' again to see what I cover."
        )

    chunks = len(manifest)
    pages = sorted({
        kb_path
        for entry in manifest.values()
        if (kb_path := (entry.get("kb_path") if isinstance(entry, dict) else None))
    })
    page_count = len(pages)

    visible = pages[:_MAX_VISIBLE_PAGES]
    hidden = page_count - len(visible)

    lines = [
        f"My knowledge base covers {page_count} page(s) across {chunks} indexed "
        "chunk(s):",
    ]
    for kb_path in visible:
        # Prettify for readability but keep the raw kb_path verbatim and
        # discoverable (spec-fixed: the full kb_path string must appear).
        pretty = kb_path
        if pretty.startswith("kb/"):
            pretty = pretty[len("kb/"):]
        if pretty.endswith(".md"):
            pretty = pretty[: -len(".md")]
        lines.append(f"  - {pretty}  [{kb_path}]")
    if hidden > 0:
        lines.append(f"  (+{hidden} more)")
    lines.append("\nAsk me about any of these and I'll answer from the verified source.")
    return "\n".join(lines)


def _sources_text() -> str:
    """Source roster built from the static ED_SOURCES table — no network."""
    from copilot.acquire_sources import ED_SOURCES

    lines = ["I draw on these Elite Dangerous data sources (by trust Tier):"]
    # Sort by tier then key for deterministic, readable output.
    for src in sorted(ED_SOURCES, key=lambda s: (s.tier, s.key)):
        lines.append(f"  - {src.key}  (Tier {src.tier}, {src.kind})")
    lines.append(
        "\nTier 0 is most authoritative; higher tiers are corroborating. I only "
        "answer from material that made it into my verified knowledge base."
    )
    return "\n".join(lines)


def meta_command(query: str, state: CmdrState | None) -> str | None:
    """Intercept tool-about meta-commands before answer().

    Returns the response text for a RECOGNISED command, or None to fall through
    to the unchanged answer() RAG path. Recognition is whole-string equality of
    the normalized query against the closed Group A/B/C token sets. Pure: the
    only external read is index.load_manifest(); no network, no Ollama, no
    retriever. Never raises on a missing/empty/malformed manifest. Returns None
    for exit/quit/q so the existing exit branch in main() is never shadowed.
    """
    norm = _normalize(query)
    if not norm:
        return None
    if norm in _HELP_TOKENS:
        return _help_text(state)
    if norm in _TOPICS_TOKENS:
        return _topics_text()
    if norm in _SOURCES_TOKENS:
        return _sources_text()
    return None


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
    print("[COVAS] Type 'help' for what I can do, or 'exit' (Ctrl-C) to quit.\n")

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

        # Meta-commands ("help", "topics", "sources") are questions about the
        # TOOL, not KB facts. Intercept them BEFORE answer() so they're instant
        # and never hit the RAG gate (which would spuriously REFUSE). A None
        # return means "not a meta-command" — fall through to answer() unchanged.
        meta = meta_command(query, state)
        if meta is not None:
            print(f"COVAS: {meta}\n")
            continue

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
