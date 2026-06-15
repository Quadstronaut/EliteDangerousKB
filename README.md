# Elite Dangerous Knowledge Engine + COVAS Copilot

A fact-checked, current-truth-only Elite Dangerous knowledge base plus a local RAG
chat copilot ("COVAS") for **CMDR Duvrazh**, grounded only in the verified KB with
citations. Built for capability/progression mastery (engineering, combat & AX/Thargoid,
exobiology, system colonisation, Odyssey on-foot).

## Status — 2026-06-15

| Subsystem | Plan | State |
|---|---|---|
| Foundation + Copilot Core | A | ✅ **built** — working end-to-end |
| Data-First Profile | B | ✅ **built** — discovery + journal/game-state/screenshot ingest |
| MCP Server | C | ✅ **built** — `ed_kb_search` / `ed_kb_answer` / `ed_cmdr_state` |
| Research Loop | D | ✅ **built + ran live** — wrote `kb/locations/deciat.md`; `STATE.toml` resumes per phase |
| Hybrid retrieval | — | ✅ **built** — BM25 (`sparse.py`) + dense RRF (`fusion.py`); default `fusion="dense"` (see below) |
| Multi-hop synthesis | — | 🟡 **scaffold (deferred)** — `multihop.py` + `[copilot] multihop=false`; flip when eval justifies |
| Local verification | — | ✅ **built** — council-v2-style local fact-check (`verify.py`, `[verify]`); cloud escalation is manual |
| Web acquisition | — | ✅ **built** — SSRF-hardened fetch (`ssrf.py`/`acquire.py`); wired into the loop's PHASE 2 |

- **461 tests passing** (`-m "not integration"`), plus a live integration eval gate
  (`pytest -m integration tests/test_hybrid_spec.py`). Four council-v2 reviews
  (quality, hybridization, acquisition, final review) shaped this slice.
- Anti-hallucination gate (empty-context refusal, τ=0.55 floor, forced citation,
  claim-grounding) holds on **every** path — including the multi-hop union and hybrid
  fusion: grounding is always the dense cosine, never an RRF/BM25 score.
- Eval harness: `python -m copilot.eval` → Recall@5 **1.00**, MRR **1.00**, 0 false
  refusals/answers (ceiling at the current **5-page / 27-chunk** KB; the loop grows it).
- Real end-to-end on live `bge-m3` + `qwen3:8b`: grounded queries cite; off-topic refuses.

## Launch COVAS (chat)

```powershell
# Ensure Ollama is running (qwen3:8b + bge-m3), then:
.\launch-copilot.ps1
```

If the index isn't built yet (or after editing the KB):

```powershell
.\.venv\Scripts\python.exe -c "from copilot import index; from copilot.paths import kb_dir; print(index.build_index(kb_dir()))"
```

## Use from Claude Code (MCP)

`.mcp.json` registers the server. In Claude Code, `/mcp` should list **ed-covas** with
the three tools. This sleeves Claude onto the identical KB when qwen's answer isn't enough.
The launch path is **clone-anywhere portable** (`${CLAUDE_PROJECT_DIR}`) — the repo works
from any path you clone it to.

## Retrieval, verification & acquisition (2026-06-15)

- **Hybrid retrieval** — `copilot/sparse.py` (self-rolled BM25+, zero new deps) +
  `copilot/fusion.py` (Reciprocal Rank Fusion). The sparse index is written *inside*
  the dense index's lock, so dense + sparse are always one atomic group. The shipped
  default is **`[retrieval] fusion = "dense"`**: on the current 27-chunk corpus, live
  eval shows `fusion="rrf"` *regresses* MRR 1.000→0.962 (BM25 promotes a lexical
  near-miss), so the non-regressing default ships while the full RRF path stays built,
  tested, and one flip away. Flip to `"rrf"` once the KB grows and eval shows
  `rrf MRR ≥ dense`. Grounding (refusal) always uses the dense cosine vs τ — a high
  BM25 score can never launder a false positive past the gate.
- **Multi-hop synthesis** — deferred behind `[copilot] multihop = false` (default).
  When off, `repl.answer()` is byte-identical to the single-retrieve path. When on, it
  decomposes the query, retrieves per sub-query, unions the chunks, and runs the
  *unchanged* claim-grounding gate over the union. Flip when an eval signal justifies it.
- **Local verification** — `copilot/verify.py` + `[verify]`: a local Ollama mini-council
  fact-checks a claim against its sources (sources are sanitized + spotlight-fenced;
  a "verified" verdict requires ≥ `min_sources_for_consensus`). Low-confidence verdicts
  escalate to the cloud `council` skill (manual invocation).
- **Web acquisition** — `copilot/acquire.py` fetches through `copilot/ssrf.py`, the single
  SSRF chokepoint: it refuses non-http(s) schemes, non-allowlisted hosts, blocked ports,
  and private/loopback/link-local/reserved IPs (including cloud-metadata `169.254.169.254`),
  checking the **resolved** IP and re-validating **every redirect hop**. Fetched text is
  sanitized before any LLM/KB write; ingested chunks are never auto-`verified`. Allowed ED
  domains live in `[acquire].allowlist` (`copilot/acquire_sources.py` roster). Playwright
  rendering is optional and OFF by default. Residual risk (logged): DNS-rebind TOCTOU is
  reduced, not eliminated — full closure needs an IP-pinned transport (follow-up).

## Pending / next steps

1. **Grow the KB via the research loop (Plan D)** — `.\wrapper.ps1 -MaxLoops 3 -SkipPermissions`.
   Proven live (1 loop). Each loop researches ED sources and commits a KB page; `STATE.toml`
   checkpoints per phase so Ctrl-C + relaunch resumes cleanly.
2. **Bootstrap your real profile:** with the game running (or its journals present), run the
   Plan B bootstrap to populate `cmdr/duvrazh.md` from live data + an optional screenshot:
   `python -m copilot.profile_sources --bootstrap [--screenshot PATH]` (or set `$env:ED_KB_SCREENSHOT`).
3. Journal-watcher live mode + verification Phase 2/3 are v1.1 (separate plans).

## Docs

- Spec: `docs/superpowers/specs/2026-06-01-ed-knowledge-engine-covas-copilot-design.md`
- Contracts: `docs/superpowers/plans/CONTRACTS.md`
- Plans: `docs/superpowers/plans/2026-06-01-plan-{A,B,C,D}-*.md`
