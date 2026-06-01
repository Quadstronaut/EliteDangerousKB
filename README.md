# Elite Dangerous Knowledge Engine + COVAS Copilot

A fact-checked, current-truth-only Elite Dangerous knowledge base plus a local RAG
chat copilot ("COVAS") for **CMDR Duvrazh**, grounded only in the verified KB with
citations. Built for capability/progression mastery (engineering, combat & AX/Thargoid,
exobiology, system colonisation, Odyssey on-foot).

## Status — 2026-06-01

| Subsystem | Plan | State |
|---|---|---|
| Foundation + Copilot Core | A | ✅ **built** — 13 tasks, working end-to-end |
| Data-First Profile | B | ✅ **built** — discovery + journal/game-state/screenshot ingest |
| MCP Server | C | ✅ **built** — `ed_kb_search` / `ed_kb_answer` / `ed_cmdr_state` |
| Research Loop | D | 📝 **authored, NOT run** — start it yourself (see below) |

- **171 tests passing** (`-m "not integration"`).
- Real end-to-end verified against live `bge-m3` + `qwen3:8b`: grounded queries return
  cited answers; off-topic queries refuse.
- Seed KB = 4 pages / 22 chunks (Farseer, FSD, Python Mk II, trunk). The loop (Plan D)
  grows this.

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

## Pending / next steps

1. **Run the research loop (Plan D)** to grow the KB — `docs/superpowers/plans/2026-06-01-plan-D-research-loop.md`.
   It builds `ed-research-prompt.md` + an idempotent, verbose `wrapper.ps1`. *Not started — your call.*
2. **Bootstrap your real profile:** with the game running (or its journals present), run the
   Plan B bootstrap to populate `cmdr/duvrazh.md` from live data + a screenshot. The default
   screenshot path was absent at build time — drop one and re-run.
3. Journal-watcher live mode + verification Phase 2/3 are v1.1 (separate plans).

## Docs

- Spec: `docs/superpowers/specs/2026-06-01-ed-knowledge-engine-covas-copilot-design.md`
- Contracts: `docs/superpowers/plans/CONTRACTS.md`
- Plans: `docs/superpowers/plans/2026-06-01-plan-{A,B,C,D}-*.md`
