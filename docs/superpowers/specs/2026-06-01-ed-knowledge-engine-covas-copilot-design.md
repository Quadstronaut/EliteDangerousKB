# Design: Elite Dangerous Knowledge Engine + COVAS Copilot

**Date:** 2026-06-01
**For:** CMDR Duvrazh (user)
**Status:** Approved design — pending implementation plan

---

## Purpose

Build a powerful, multi-tier, iterated research loop that consolidates **fact-checked, current-truth-only** Elite Dangerous knowledge into a local knowledge base, plus a personalized chat copilot ("COVAS") that answers any question about ships, engineers, locations, mechanics, outfitting, careers, Powerplay, colonisation, community goals, and current AX/Thargoid content — grounded only in that verified KB.

The user has played since day 1 but never dove deep: wealthy (3B+ on foot, billions more in 2 fleet carriers, ~3B rebuy implying a large-ship fleet), ranks Combat Expert / Trade Elite V / Explorer Elite / Exobiology Directionless / Mercenary Defenceless / CQC Helpless. **Money is not the constraint** — the goal is capability, progression, and mastery in the grind-gated and knowledge-gated areas money can't buy.

---

## Core problem this solves

ED community knowledge is full of stale and contradictory information (pre-Odyssey, pre-Powerplay-2.0, pre-Colonisation claims presented as current). An 8B local model will confidently hallucinate ED facts. The KB holds **only what is true and relevant now** — obsolete mechanics are omitted, not catalogued. The system defeats both failure modes:

1. **RAG grounding** — the copilot answers *only* from retrieved verified KB chunks, with citations. "I don't have a verified source" is a valid, required answer.
2. **Current-truth-only KB** — obsolete-and-pointless mechanics are omitted entirely; the rare stale fact that still matters survives as a one-line `changed_note`, so the copilot never presents dead mechanics as current or sends the user chasing content that ended.

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
| `copilot/repl.py` | Python | Interactive chat: retrieval → qwen3:8b → streamed answer with citations + `changed_note` when relevant |
| `copilot/mcp_server.py` | Python (MCP) | Same retrieval + live-API tools, exposed to Claude Code |
| `copilot/ollama_client.py` | Python | Thin Ollama HTTP client (chat + embeddings + vision) |
| `copilot/profile.py` | Python | `ProfileSource` interface; merges all CMDR data sources into `CmdrState`, injects into every answer |
| `copilot/data_discovery.py` | Python | Scans the system for ED-related data files, emits a source manifest (see §I) |
| `copilot/vision_ingest.py` | Python | Parses screenshots (ranks, assets, loadouts) via `qwen3-vl:8b` into structured profile facts |
| `cmdr/duvrazh.md` | Markdown | CMDR profile: assets, ranks, ships, carriers, goals — bootstrapped from data, human-editable |

---

## Data sources & trust tiers

The ED edge: much ground truth is **structured**, not prose. Trust accordingly.

- **Tier 0 — canonical/structured:** Coriolis-data JSON (every ship/module stat), EDCD `FDevIDs`, EDSM API, **Spansh** API + galaxy dumps (bodies/bio-signal counts, neutron + carrier routing, colonisation candidates), **Canonn** (`api.canonn.tech` — Guardian sites, Thargoid structures/spawns, biological signal locations), **Frontier patch notes & GalNet** (the version anchor).
- **Tier 1 — authoritative prose:** INARA (`inara.cz` — engineers, blueprints, commodities, CGs; **community-contributed, rate-limited 25 req / 15 min → needs a dedicated rate-limiter + cache**), official forum dev posts.
- **Tier 2 — community curated:** Fandom wiki, established guide sites.
- **Tier 3 — anecdotal:** Reddit (r/EliteDangerous, r/EliteOdyssey, r/EliteExobiology, r/EliteMiners, r/EliteExplorers, r/EliteCQC), YouTube guides (transcribed), forum posts. Kept, but must be corroborated to graduate.

> **EDDB is dead (offline since 2023) — do not use.** Trust is carried by discrete fields (`tier` + `availability` + `source_count`), **not** a composite score. The original multiplicative "tier × corroboration × recency" formula is dropped (it was undefined and tier-inverted).

---

## Fact metadata (frontmatter on every claim/summary)

**Authoring is page-level; trust resolves at the chunk level** (see Council §A). A page's frontmatter holds *defaults* inherited by its chunks; an H2/H3 section may override via an inline `<!-- tier:3 src:reddit -->` directive for the mixed-trust case (a Tier-0 Coriolis stat sitting next to a Tier-3 Reddit tip on the same page). The chunker resolves per-chunk metadata into the vector payload.

```yaml
# page-level defaults
---
source_url: <url>
source_type: <coriolis|edsm|spansh|canonn|inara|patch-notes|fandom|reddit|youtube|forum|...>
source_tier: <0|1|2|3>
captured_at: <ISO>
source_count: <int>          # independent corroborating sources
verified: <true|false>       # promoted in Phase 2
availability: <live|seasonal|changed>   # current-truth only; `changed` carries a one-line note
changed_note: <one line, only when availability=changed>
---
```

**The KB stores what is true and relevant NOW.** Obsolete mechanics with no present purpose are **omitted entirely** — the loop does not research them and they get no pages. `availability` values:
- `live` — currently obtainable/relevant (e.g. post-war AX combat, Spire sites, Titan-wreck diving, exobiology, Trailblazers colonisation). **This is the default and the bulk of the KB.**
- `seasonal` / time-limited — currently relevant but recurring or windowed (e.g. active CGs).
- `changed` — **the only concession to stale content.** Used ONLY when knowing a thing changed has present value (prevents bad advice or corrects a misconception the user will hit in old guides). Stored as a **one-line `changed_note`** ("Powerplay 1 → Powerplay 2, 2024 — old modules gone"; "Thargoid war concluded — hearts/Titan-active rewards no longer obtainable"), **never a researched branch.** A thin myth-correction layer, not a museum.

There is **no `superseded`/`removed` page-building**: if a dead mechanic has no `changed_note` value, it is simply absent. The copilot answering "that's no longer in the game, here's what's current" comes from a one-line note or from the absence itself — not from catalogued dead content.

**Mandatory v1 correctness:** AX combat/Spire/Titan-diving are tagged `live` (the war narrative ended but the content is current — must never be presented as gone). Colonisation uses the live term **Trailblazers** (Feb 2025). Deferred to v2: `unlock_chain`/`prerequisite` as structured fields (carried in body text for v1), `relates_to`, `key_entities`.

---

## Verification maturity ramp (user-chosen #3 → #2 → #1)

Built in stages so nothing is mishandled. `config.toml` carries the current `verification_tier`.

- **Phase 1 — Capture-everything, flag-later:** broad coverage fast; every fact gets frontmatter even when single-source.
- **Phase 2 — Multi-source consensus:** cross-reference pass promotes facts with 2+ independent agreeing sources to `verified: true`. Conflicts logged, never silently resolved.
- **Phase 3 — Currency validation & purge:** check verified facts against current patch notes; structured (Tier 0) data overrides prose on conflict. Facts that are no longer true are **deleted** (current-truth-only policy, §D), EXCEPT where they earn a one-line `changed_note` because the stale belief actively misleads. No museum of dead mechanics.

The copilot can answer in "verified only" mode or "include unverified (warned)" mode.

---

## Data flow (one loop)

Triage queue → **Search** (web + Tier-0 APIs) → dedup via `seen.json` → **Summarize** (qwen3-coder:30b extracts claims, entities, currency signals) → **Discard obsolete-and-pointless facts** → **Synthesize** (route current-truth facts to KB pages, add `[[wikilinks]]`, set tier/source_count) → **Re-embed** changed pages (bge-m3) → **Index + git commit** → regenerate `README.md` dashboard → update `STATE.toml`.

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
│   ├── powerplay/  colonisation/  community-goals/  ax-thargoid/   # AX = live content
│   └── entities/
├── sources/  summaries/  live/  indexes/  embeddings/  queue/  journal/
└── copilot/
    ├── retriever.py   assemble.py   repl.py   mcp_server.py
    ├── ollama_client.py   profile.py   data_discovery.py   vision_ingest.py
```

---

## Staged build order

**Superseded by the council's §G — Revised build order (below).** See §G for the binding sequence (it adds data discovery + profile bootstrap, idempotent/verbose wrapper, and the journal-watcher step).

---

## Error handling & safety

- Loop self-heals `config.toml`, retries with backoff, never stops unless `halt = true` or usage exhausted.
- Ollama-unreachable → REPL and MCP server degrade gracefully with a clear message.
- Every copilot answer carries citations; surfaces a `changed_note` when relevant; empty/low-similarity context → "no verified source," never a guess.
- Git commit every loop; KB is the source of truth. Paraphrase sources (fair use), cite URLs.

---

## Testing / verification

- **Retriever:** golden-question set (e.g. "Farseer unlock requirement," "meta exploration FSD roll") with known KB answers → assert correct chunks retrieved.
- **Copilot anti-hallucination gate:** refusal-calibration fixtures — refuses on empty context AND on non-empty-but-irrelevant context below τ (the dangerous case).
- **Loop dry-run:** single iteration advances `STATE.toml` and produces a git commit.
- **Idempotent resume (§J):** kill the loop mid-phase, relaunch → it resumes at the last completed phase, re-runs nothing already committed, and state files are uncorrupted.
- **Data discovery (§I):** `data_discovery.py` finds the Saved Games journal dir + game-state JSON on this machine and writes a valid `indexes/data-sources.json`; `vision_ingest.py` parses the rank screenshot into the seed profile.
- **Index consistency:** `reindex --from-kb` output equals the incrementally-maintained index.
- **MCP parity:** `ed_kb_search` returns an identical `list[Chunk]` to the local retriever for the same query (compare structured chunks, not assembled prose).

---

## Out of scope (YAGNI for v1)

- No fine-tuning / Modelfile-baked KB (retrieval beats baking; cited and updatable).
- No live EDDN firehose consumption (complex; pull from Spansh colonisation + PP2 trackers on a short cycle instead).
- No GUI — terminal REPL + MCP only.
- No voice I/O (despite the COVAS name) — text only for v1.
- No `graph.json` (deleted — no consumer).
- No CAPI/EDMC integration in v1 (OAuth + Frontier approval is real scope) — v2.
- **No obsolete/dead mechanics** — current truth only; the loop does not research or page content with no present relevance. Stale facts survive only as a one-line `changed_note` where it prevents bad advice (see §D).

---

## Council Review Resolutions & v1 Build Contract (2026-06-01)

A 4-member adversarial council (Opus = architecture, Sonnet = ED domain, Haiku = pragmatism, qwen3-coder:30b = implementation) reviewed this spec over two rounds and argued the conflicts to convergence. The resolutions below **supersede** any conflicting text above. (Note: Ollama crashed under the 30B mid-review — see §Runtime; qwen's implementation claims were adjudicated by the architecture lens.)

### §A — Granularity (RESOLVED)
Page-level **authoring**, chunk-level **trust**. Chunker emits H2/H3 sections, 128–512 tokens, ~15% overlap, with a heading breadcrumb prepended to the embedded text. `chunk_id = sha256(kb_path + heading_path)`. Each chunk inherits page frontmatter; inline `<!-- tier: src: -->` overrides per section. **Strip frontmatter + wikilinks + raw URLs before embedding**; store all filterable metadata (tier, availability, source_url, source_count, verified) in the **vector payload**. Citation = `chunk_id + source_url`. Index is a **derived, rebuildable artifact**: `indexes/manifest.json` maps `chunk_id → {content_hash, kb_path, heading_path, payload}`; each loop diffs by content_hash → upsert changed, **tombstone removed**. A `reindex --from-kb` command + test ("rebuilt index == incremental index") is the consistency contract.

### §B — Anti-hallucination gate (RESOLVED, v1)
1. **Empty-context refusal.**
2. **τ retrieval-score floor** — if top-k max cosine < τ (in `config.toml`), refuse *even when context is non-empty*. Guards the dangerous "confident answer from garbage retrieval" case. (Judgment call: included in v1 over two members' deferral — it is a one-line check and directly serves the no-BS mandate.)
3. **Forced per-claim citation with one regen** — every factual claim carries `[chunk_id]`; a cheap post-hoc check rejects+regenerates once if any claim is uncited.
4. **Refusal-calibration fixtures** — golden questions with *deliberately irrelevant* retrieval that MUST trigger refusal. This is the acceptance gate that proves τ is tuned (not a magic number).

Deferred to v1.1: cited-span validation (verify the quoted span exists in the cited chunk).

### §C — Personalization / Journal ingest (RESOLVED)
Does **not** block day-1 chat. `profile.py` exposes a `ProfileSource` interface (`get_state() -> CmdrState`) from commit 1. v1 implementation = hand-seeded `cmdr/duvrazh.md` (template in repo from the start); answers drawn from it are **labeled as unverified/manual state**, never presented as live truth. **Journal-watcher** (polls `%USERPROFILE%\Saved Games\Frontier Developments\Elite Dangerous\Journal.*.log`) is a drop-in second `ProfileSource` — lands **v1.1 / Sprint 2** (well-trodden via EDMC; before any feature claiming live loadout/carrier accuracy). CAPI/EDMC = v2.

### §D — Availability + MCP (RESOLVED, amended by user 2026-06-01)
**User override of the council:** the KB stores **current truth only**. Obsolete mechanics with no present purpose are **omitted entirely** — not researched, not paged, not tagged. The council's `superseded`/`removed` "catalogue dead content" model is dropped. `availability` collapses to `live | seasonal | changed`, where `changed` is a thin myth-correction layer: a **one-line `changed_note`** kept ONLY when knowing a thing changed prevents bad advice or corrects a misconception the user will meet in old guides (PP1→PP2, "war is over"). Never a researched branch. The one hard correctness rule survives: AX/Spire/Titan content is `live` and must never be presented as gone. **MCP ships in v1** (user mandate) as a thin **FastMCP + stdio** wrapper over the pure retriever, registered via `.mcp.json`; sequenced after the copilot core but in the v1 release. Deferred: structured `unlock_chain`, deep-analysis mode, live-refresh automation, `graph.json` (deleted).

### §E — Implementation (RESOLVED)
- **Vector store:** numpy brute-force cosine for v1 (≈50k × 1024 float32 ≈ 200 MB, single matmul in ms; zero Windows install pain). Persist as `.npy` + `manifest.json`. **Switch threshold:** revisit `sqlite-vec` (pip-only, persistent) or `faiss-cpu` past ~100k chunks or if query latency > ~200 ms.
- **Embeddings:** bge-m3 via Ollama, 1024-dim, **L2-normalize** vectors for cosine; batch + retry/backoff.
- **Retriever contract:** `retriever.py` is pure — `retrieve(query, filters) -> list[Chunk]`. A separate `assemble.py` builds the qwen prompt (profile + chunks). REPL = retrieve→assemble→generate; MCP `ed_kb_search` returns raw `list[Chunk]` JSON. Parity test asserts identical `Chunk` lists, **not** identical assembled prose.
- **Stream UX:** strip qwen3 `<think>…</think>` reasoning from the streamed `/api/chat` response (or disable thinking in the request). Clean copilot output only.

### §F — Runtime / Ollama stability (NEW)
The loop's heavy model (`qwen3-coder:30b`, 17 GB) crashed the local Ollama server during review when contended. The **copilot path uses only `qwen3:8b` + `bge-m3`** (lightweight). The loop's 30B offload must be **sequential**, and `keep_alive` managed so the 30B and 8B are not co-resident under memory pressure. Both REPL and MCP must degrade gracefully when Ollama is unreachable.

### §G — Revised build order
1. Scaffold + `cmdr/duvrazh.md` template + `ProfileSource` interface + `config.toml`/`STATE.toml` (atomic writes, §J) + git (master). `graph.json` removed.
2. **Data discovery + profile bootstrap:** `data_discovery.py` scans the system (§I) → `indexes/data-sources.json`; `vision_ingest.py` parses the provided rank screenshot to seed `cmdr/duvrazh.md`; one-shot Journal/Status JSON backfill into `CmdrState`.
3. **Copilot core (chat day 1):** `retriever.py` (pure, chunk-level + numpy index) + `assemble.py` + `repl.py` + `launch-copilot.ps1`, against a small hand-seeded KB. Anti-hallucination gate §B included.
4. **MCP server** (FastMCP/stdio) over the same retriever; `.mcp.json` registration.
5. **The loop:** `ed-research-prompt.md` + `wrapper.ps1` (idempotent, verbose, always-live §J); **Tier-0 structured ingest first** (Coriolis / EDSM / Spansh / Canonn), then web fan-out. Phase-1 capture.
6. **Journal-watcher** live `ProfileSource` + deep-research-vetted supplemental tools (§I) — v1.1.
7. **Verification ramp** Phase 2 (consensus) → Phase 3 (currency validation & purge) as the KB matures.
8. Live-data refresh (Spansh colonisation + PP2 trackers, CGs) — later.

### §H — ED domain must-haves baked into v1
Canonn (Tier 0), Spansh expansion (exobio/routing/colonisation), INARA→Tier 1 + rate-limiter, drop "U14" → "Odyssey season", AX content tagged `live` (never presented as gone), `changed_note` for PP1→PP2 and war-end. Obsolete-and-pointless mechanics **omitted entirely**. Deferred: structured unlock chains, CAPI, EDMC.

### §I — Data-first profile acquisition (user requirement 2026-06-01)
The CMDR profile is built **from data, not by hand wherever possible.** `profile.py` merges multiple `ProfileSource` implementations into a single `CmdrState`; each fact carries its origin + freshness so the copilot can label confidence and never present a guess as live truth.

**Source priority (highest-trust first):**
1. **Live game-state JSON** — the game continuously writes `Status.json`, `Cargo.json`, `ShipLocker.json`, `Backpack.json`, `Market.json`, `Outfitting.json`, `Shipyard.json`, `ModulesInfo.json`, `NavRoute.json`, `FleetCarrier.json` to `%USERPROFILE%\Saved Games\Frontier Developments\Elite Dangerous\`. Zero-latency truth for current ship/cargo/carrier/loadout.
2. **Journal event logs** — `Journal.*.log` (same dir): engineer grades reached, bodies scanned (+ FirstDiscovered), kills, systems visited, rank-ups, credits. The historical ground truth. (v1.1 watcher; one-shot backfill parse can run earlier.)
3. **Screenshots → vision** — `vision_ingest.py` parses rank/asset/loadout screenshots via `qwen3-vl:8b` into structured facts. The rank screenshot the user already provided is the **v1 bootstrap** for `cmdr/duvrazh.md`. For anything not in the logs, the user can drop a screenshot and it's parsed.
4. **3rd-party tool exports** — if EDMC / EDDiscovery / EDEngineer are installed, ingest their exports/databases (read-only).
5. **Manual `cmdr/duvrazh.md`** — fallback + human override; always editable, flagged as manual/unverified.

**System-wide data discovery (`data_discovery.py`):** at setup and periodically, scan for ED-related data across `%USERPROFILE%`, `Documents`, `%LOCALAPPDATA%` + `%APPDATA%` (Frontier Developments, EDMC, EDDiscovery, EDEngineer, EDMarketConnector), the Pictures/Frontier screenshot folder, and the **`G:`** drive. Emit `indexes/data-sources.json` (path, type, last-modified, ingest-status). Read-only; never writes into game folders.

**Supplemental tool discovery (deep-research authorized):** the `deep-research` skill is authorized to locate third-party utilities/exporters/APIs that make acquisition or KB-building easier. **Gate:** any discovered tool must pass a functional test (does it run, does its output parse, is it current/maintained) before adoption, and the evaluation is logged to the journal. No silent dependency on an unvetted tool.

### §J — Idempotent wrapper + always-live output (user requirement 2026-06-01)
**Idempotency / crash-safety — a hard requirement, not best-effort.** The user will `Ctrl-C` and relaunch `wrapper.ps1` freely; it must **always resume cleanly from where it stopped.**
- All state (`STATE.toml`, `seen.json`, `indexes/manifest.json`) is written **atomically** (write temp file → `fsync` → rename) so a kill mid-write never corrupts state.
- The loop checkpoints **within** an iteration (per phase: triage → search → summarize → synthesize → index → commit), not only at loop end, so an interrupted loop resumes at the last completed phase, not the last completed loop.
- Operations are idempotent by content-hash: a source already in `seen.json` is skipped; an unchanged chunk is not re-embedded; a half-finished page is detectable and redone, not duplicated.
- `git` commit is the loop's durable boundary; on launch the wrapper reconciles uncommitted work against `STATE.toml`.

**Always-live verbose output — nothing is ever silent or "idle."** The user wants to watch work happen on screen at all times.
- `wrapper.ps1` and the loop stream **verbose, timestamped, real-time** progress to the console (every query issued, source considered/kept/rejected, summary produced, page written, embedding built, commit made) — `Tee`'d to `journal/daemon.log`, never buffered-until-end.
- When there are no new sources, the loop **does not sleep** — it switches to deep-analysis / cross-referencing / gap-hunting (visible work), so the screen always shows activity. True idle only occurs on hard error backoff, which is itself printed with a countdown.
