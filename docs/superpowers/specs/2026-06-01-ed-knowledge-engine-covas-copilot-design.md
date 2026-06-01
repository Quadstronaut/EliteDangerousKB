# Design: Elite Dangerous Knowledge Engine + COVAS Copilot

**Date:** 2026-06-01
**For:** CMDR Duvrazh (user)
**Status:** Approved design — pending implementation plan

---

## Purpose

Build a powerful, multi-tier, iterated research loop that consolidates **fact-checked, version-tagged** Elite Dangerous knowledge into a local knowledge base, plus a personalized chat copilot ("COVAS") that answers any question about ships, engineers, locations, mechanics, outfitting, careers, Powerplay, colonisation, community goals, and the Thargoid war — grounded only in that verified KB.

The user has played since day 1 but never dove deep: wealthy (3B+ on foot, billions more in 2 fleet carriers, ~3B rebuy implying a large-ship fleet), ranks Combat Expert / Trade Elite V / Explorer Elite / Exobiology Directionless / Mercenary Defenceless / CQC Helpless. **Money is not the constraint** — the goal is capability, progression, and mastery in the grind-gated and knowledge-gated areas money can't buy.

---

## Core problem this solves

ED community knowledge is full of stale and contradictory information (pre-Odyssey, pre-Powerplay-2.0, pre-Colonisation claims presented as current). An 8B local model will confidently hallucinate ED facts. The system defeats both:

1. **RAG grounding** — the copilot answers *only* from retrieved verified KB chunks, with citations. "I don't have a verified source" is a valid, required answer.
2. **Version + availability tagging** — every fact is anchored to a game epoch and an availability status, so the copilot never presents stale mechanics as current or sends the user chasing content that ended.

---

## Architecture — three layers, one shared retrieval core

```
   THE LOOP (unattended Claude Code orchestrator + qwen3-coder:30b bulk offload)
        │ writes
        ▼
   THE KB (hyperlinked markdown + bge-m3 vector index)
        │ read via SHARED RETRIEVAL CORE (copilot/retriever.py)
        ├──────────────────────────────┐
        ▼                               ▼
   COVAS REPL (qwen3:8b, local)    MCP server (ed_kb_search / ed_kb_answer /
   launch-copilot.ps1             live tools) → consumed by Claude Code
```

The retrieval logic is written **once** in `retriever.py` and consumed two ways (local REPL + MCP server) so there is zero drift between what qwen3:8b sees and what Claude sees. When qwen's answer is unsatisfactory, the user sleeves Claude onto the identical KB via MCP.

### Model assignment (local Ollama @ localhost:11434)
- `qwen3-coder:30b` — heavy synthesis/summarization in the loop (strongest local reasoning).
- `qwen3:8b` — the COVAS chat model (fast, fits VRAM with large context).
- `qwen3-vl:8b` — vision; reads in-game screenshots the user pastes.
- `bge-m3` — embeddings for the KB vector index and query retrieval.

---

## Components

| Component | Tech | Job |
|---|---|---|
| `ed-research-prompt.md` | Markdown mega-prompt | Loop brain; self-aware of STATE, resumes correctly each invocation |
| `wrapper.ps1` | PowerShell daemon | Infinite loop runner with retry/backoff (Subject-K pattern) |
| `launch-copilot.ps1` | PowerShell | **User entry script**; health-checks Ollama then launches the REPL |
| `copilot/retriever.py` | Python | Shared core: embed query (bge-m3) → vector search KB → rank → assemble context + CMDR profile |
| `copilot/repl.py` | Python | Interactive chat: retrieval → qwen3:8b → streamed answer with citations + version/availability tags |
| `copilot/mcp_server.py` | Python (MCP) | Same retrieval + live-API tools, exposed to Claude Code |
| `copilot/ollama_client.py` | Python | Thin Ollama HTTP client (chat + embeddings) |
| `copilot/profile.py` | Python | Loads CMDR profile, injects into every answer |
| `cmdr/duvrazh.md` | Markdown | CMDR profile: assets, ranks, ships, carriers, goals |

---

## Data sources & trust tiers

The ED edge: much ground truth is **structured**, not prose. Trust accordingly.

- **Tier 0 — canonical/structured:** Coriolis-data JSON (every ship/module stat), EDCD `FDevIDs`, EDSM / Spansh / INARA APIs, **Frontier patch notes & GalNet** (the version anchor).
- **Tier 1 — authoritative prose:** INARA guides, official forum dev posts.
- **Tier 2 — community curated:** Fandom wiki, established guide sites.
- **Tier 3 — anecdotal:** Reddit (r/EliteDangerous, r/EliteOdyssey, r/EliteExobiology, r/EliteMiners, r/EliteExplorers, r/EliteCQC), YouTube guides (transcribed), forum posts. Kept, but must be corroborated to graduate.

Confidence = source tier × corroboration count × version recency.

---

## Fact metadata (frontmatter on every claim/summary)

```yaml
---
source_url: <url>
source_type: <coriolis|edsm|spansh|inara|patch-notes|fandom|reddit|youtube|forum|...>
source_tier: <0|1|2|3>
captured_at: <ISO>
confidence: <high|medium|low|single-source>
source_count: <int>          # independent corroborating sources
verified: <true|false>       # promoted in Phase 2
version_epoch: <horizons|odyssey|u14|powerplay-2.0|thargoid-war-end|colonisation-2025|unknown>
availability: <current|limited-time|missed-permanent|unknown>
relates_to: <kb path(s)>
key_entities: [list]
---
```

`availability` is a first-class field: the copilot never recommends chasing content that has ended (e.g., the concluded Thargoid war's rewards, past CGs, limited decals) and always flags what is still obtainable.

---

## Verification maturity ramp (user-chosen #3 → #2 → #1)

Built in stages so nothing is mishandled. `config.toml` carries the current `verification_tier`.

- **Phase 1 — Capture-everything, flag-later:** broad coverage fast; every fact gets frontmatter even when single-source.
- **Phase 2 — Multi-source consensus:** cross-reference pass promotes facts with 2+ independent agreeing sources to `verified: true`. Conflicts logged, never silently resolved.
- **Phase 3 — Version-aware validation:** anchor every verified fact to a game epoch via patch notes; stale claims **demoted and flagged, not deleted**; structured (Tier 0) data overrides prose on conflict.

The copilot can answer in "verified only" mode or "include unverified (warned)" mode.

---

## Data flow (one loop)

Triage queue → **Search** (web + Tier-0 APIs) → dedup via `seen.json` → **Summarize** (qwen3-coder:30b extracts claims, entities, version + availability signals) → **Synthesize** (route to KB pages, add `[[wikilinks]]`, set confidence) → **Re-embed** changed pages (bge-m3) → **Index + git commit** → regenerate `README.md` dashboard → update `STATE.toml`.

Deep-analysis mode triggers after N consecutive empty loops: expand inward (cross-reference clusters, gap-analysis, generate new targets).

---

## CMDR profile (seeded, then user-maintained)

From the screenshot + stated goals:
- **Identity:** CMDR Duvrazh. Balance hidden in screenshot but 3B+ on foot, billions in carriers; rebuy ~3B (large-ship fleet). Notoriety 0.
- **Ranks:** Combat Expert, Trade Elite V, Explorer Elite, Exobiology Directionless, Mercenary Defenceless, CQC Helpless.
- **Assets:** 2 fleet carriers (one shared with a 3–4 person private squad), many ships.
- **Goals (all selected):**
  1. Engineering & meta builds (unlock all engineers, god-roll key ships) — primary capability wall.
  2. Master ship combat & AX/Thargoid.
  3. Exobiology from zero (pure knowledge + patience).
  4. System Colonisation project (wealthy-commander endgame using carriers).
  5. Learn Odyssey on-foot gameplay from near-scratch — catch up on missed content.
- **Constraint awareness:** some content is permanently missed; that is acceptable. The KB's `availability` tagging serves this directly.

---

## Directory structure

```
EliteDangerousKB/
├── ed-research-prompt.md   wrapper.ps1   launch-copilot.ps1
├── config.toml   STATE.toml   README.md   .gitignore   graph.json
├── cmdr/duvrazh.md
├── kb/
│   ├── trunk.md
│   ├── ships/  engineers/  outfitting/  mechanics/  locations/
│   ├── careers/        # combat, trade, explore, exobio, mining, AX, mercenary/on-foot
│   ├── powerplay/  colonisation/  community-goals/  thargoid-war/
│   └── entities/
├── sources/  summaries/  live/  indexes/  embeddings/  queue/  journal/
└── copilot/
    ├── retriever.py   repl.py   mcp_server.py   ollama_client.py   profile.py
```

---

## Staged build order

1. **Scaffold** — directory skeleton, `cmdr/duvrazh.md`, `config.toml`, `STATE.toml`, `.gitignore`, git init on `master`.
2. **Copilot core (thin slice)** — `retriever.py` + `repl.py` + `launch-copilot.ps1` against a small seeded KB; user can chat on day one.
3. **MCP server** — `mcp_server.py` wrapping the same retriever; registered so Claude Code can sleeve on.
4. **The loop** — `ed-research-prompt.md` + `wrapper.ps1`; Tier-0 structured ingest first (Coriolis/EDSM), then web fan-out.
5. **Verification ramp** — Phase 1 → 2 → 3 as the KB fills.
6. **Live-data refresh** — periodic API pulls for CGs / Powerplay / galaxy state into `live/`.

---

## Error handling & safety

- Loop self-heals `config.toml`, retries with backoff, never stops unless `halt = true` or usage exhausted.
- Ollama-unreachable → REPL and MCP server degrade gracefully with a clear message.
- Every copilot answer carries citations + version + availability tags; empty context → "no verified source," never a guess.
- Git commit every loop; KB is the source of truth. Paraphrase sources (fair use), cite URLs.

---

## Testing / verification

- **Retriever:** golden-question set (e.g. "Farseer unlock requirement," "meta exploration FSD roll") with known KB answers → assert correct chunks retrieved.
- **Copilot anti-hallucination gate:** assert it refuses to answer when retrieved context is empty.
- **Loop dry-run:** single iteration advances `STATE.toml` and produces a git commit.
- **MCP parity:** `ed_kb_search` returns identical results to the local retriever for the same query.

---

## Out of scope (YAGNI for v1)

- No fine-tuning / Modelfile-baked KB (retrieval beats baking; cited and updatable).
- No live EDDN firehose consumption (complex; periodic API pulls cover live needs).
- No GUI — terminal REPL + MCP only.
- No voice I/O (despite the COVAS name) — text only for v1.
