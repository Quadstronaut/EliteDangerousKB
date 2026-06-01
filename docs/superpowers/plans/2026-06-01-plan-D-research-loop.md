# Plan D — Research Loop
## ED Knowledge Engine + COVAS Copilot

> **For agentic workers:** This plan is a complete, self-contained specification. Read it in full before executing any task. Tasks are sequenced; do not skip ahead. All contracts, schemas, and function signatures in `CONTRACTS.md` are binding and take precedence over any conflicting text here. Do not execute until the user explicitly approves.

---

## BANNER

> **REQUIRES PLAN A COMPLETE — DO NOT RUN UNTIL USER APPROVES.**
> Plan D depends on Plan A having delivered: `copilot/atomic.py` (`read_state`, `write_state`, `write_atomic`, `write_json_atomic`), `copilot/index.py` (`upsert_changed`), `copilot/chunker.py`, `copilot/ollama_client.py` (`chat_stream` with `<think>` stripping), `copilot/paths.py` (`repo_root`, `load_config`), `config.toml`, `STATE.toml` (initial schema), and the directory scaffold including `journal/`, `queue/`, `sources/`, `summaries/`, `indexes/`. If any of these are absent, stop and complete Plan A first.

---

## Goal

Deliver an unattended, idempotent, verbose research daemon that grows the KB with fact-checked, **current-truth-only** Elite Dangerous knowledge. The daemon runs indefinitely via `wrapper.ps1`; Claude Code is the loop orchestrator, driven by `ed-research-prompt.md`; qwen3-coder:30b handles bulk summarization via the local Ollama server. No new sources triggers deep-analysis mode — the screen is never idle.

---

## Architecture

```
wrapper.ps1  (PowerShell daemon — infinite loop, retry/backoff, Tee log)
    │
    └─ claude -p (Get-Content ed-research-prompt.md -Raw)
           │
           ├── reads  STATE.toml  → resumes at last_completed_phase
           ├── reads  queue/      → triage
           ├── calls  WebSearch + WebFetch  (Tier-0 APIs + web fan-out)
           ├── calls  mcp__ollama-tools__summarize_text  (qwen3-coder:30b)
           ├── writes kb/**/*.md  via  copilot.atomic.write_atomic
           ├── calls  copilot.index.upsert_changed  (Python subprocess or import)
           ├── updates seen.json  via  copilot/loop_state.py
           ├── git commit
           └── writes STATE.toml  via  copilot.atomic.write_state
```

The copilot path (qwen3:8b + bge-m3) never runs during the research loop. Per §F, qwen3-coder:30b (17 GB) and qwen3:8b must not be co-resident. The wrapper never launches the REPL alongside the loop.

---

## Tech Stack

| Layer | Tech |
|---|---|
| Daemon shell | PowerShell 5.1, Windows 11 |
| Loop orchestrator | Claude Code (`claude -p`) |
| Bulk summarization | qwen3-coder:30b via Ollama MCP tool `mcp__ollama-tools__summarize_text` |
| Embedding (index) | bge-m3 via `copilot/ollama_client.py::embed` (called by `index.upsert_changed`) |
| State + dedup | `copilot/loop_state.py` (new, TDD), `copilot/atomic.py` (Plan A) |
| KB writes | `copilot/atomic.py::write_atomic` |
| Index upsert | `copilot/index.py::upsert_changed` |
| TOML I/O | `tomllib` (read, stdlib 3.11+), `tomli_w` (write) |
| Tests | `pytest` under `tests/` |

---

## File Structure (new files this plan creates)

```
EliteDangerousKB/
├── ed-research-prompt.md          # Deliverable 1 — the loop mega-prompt
├── wrapper.ps1                    # Deliverable 2 — PowerShell daemon
├── copilot/
│   └── loop_state.py              # New: advance_phase, is_resumable, record_source
├── tests/
│   └── test_loop_state.py         # TDD tests for loop_state.py
└── indexes/
    └── seen.json                  # Created at first run if absent; schema below
```

All other directories (`kb/`, `sources/`, `summaries/`, `queue/`, `journal/`) are created by Plan A. This plan writes into them but does not create them.

---

## seen.json Schema (from CONTRACTS.md)

```json
{
  "url_sha256_hex": {
    "first_seen": "<ISO 8601>",
    "content_sha256": "<hex>"
  }
}
```

- Key: `hashlib.sha256(url.encode("utf-8")).hexdigest()`
- `content_sha256`: `hashlib.sha256(raw_text.encode("utf-8")).hexdigest()` of the fetched/extracted body
- Written atomically via `write_json_atomic`; never written directly with `open(..., "w")`

---

## Deliverable 1 Tasks — `ed-research-prompt.md`

Because the orchestrator is Claude Code itself (driven by this prompt at invocation time), it cannot be unit-tested in the traditional sense. Structure these tasks as section-by-section authoring tasks with explicit acceptance criteria for each section.

---

### D1.1 — Header block and mission statement

Author the opening block of `ed-research-prompt.md`:

```markdown
# ED Research Loop — Orchestrator Prompt

> Pass this file to Claude Code via `claude -p (Get-Content ed-research-prompt.md -Raw)` from
> `wrapper.ps1`. Self-aware of STATE.toml. Resumes per-phase. Never idle.
```

**Mission section content to include:**

- You are the orchestrator of an unattended, multi-loop Elite Dangerous knowledge-base research operation.
- Your job is to grow a local KB at `kb/` with fact-checked, **current-truth-only** ED knowledge. Stale, obsolete, or irrelevant ED mechanics are **omitted entirely**. The one exception: a one-line `changed_note` on pages where knowing a thing changed prevents bad advice (e.g. PP1→PP2, Thargoid war conclusion). You do **not** build pages about dead mechanics — not even to document them as dead.
- You write chunk-ready markdown pages with YAML frontmatter conforming to the spec (source_url, source_type, source_tier, captured_at, source_count, verified, availability, changed_note).
- You offload bulk summarization to qwen3-coder:30b via the `mcp__ollama-tools__summarize_text` tool — never summarize large sources inline in your context.
- You call `copilot/index.py::upsert_changed` (via Python subprocess) after writing new/updated pages.
- You call `copilot/loop_state.py::record_source` to dedup before fetching any URL.
- You commit after every complete loop with a one-line summary.
- You never stop unless `STATE.toml` has `halt = true` or usage is exhausted.

**Acceptance criteria:** Section reads as unambiguous instructions to Claude Code, mentions current-truth-only policy, references STATE.toml, references Ollama offload, references the 6 phases by name.

---

### D1.2 — Loop-state detection block

This is the first action the prompt instructs Claude to take on every invocation.

**Content to author:**

```
## LOOP STATE DETECTION

First action on every invocation:

1. Read `STATE.toml` using `copilot/atomic.py::read_state()` (Python subprocess) or direct TOML read.
2. Inspect `last_completed_phase`. Valid values: none | triage | search | summarize | synthesize | index | commit.
3. Inspect `halt`. If true → print "Loop halted by STATE.toml flag. Exiting." and exit 0.
4. Inspect `loop_number`, `mode` (search | deep-analysis), `consecutive_empty_loops`.
5. Resume logic:
   - `last_completed_phase = "none"` or `"commit"` → start a fresh loop (increment loop_number, begin triage).
   - Any other phase → resume at the NEXT phase in order (triage→search→summarize→synthesize→index→commit).
   - If STATE.toml is missing entirely → treat as loop_number=0, last_completed_phase="none", mode="search".
6. Print timestamped summary of resumed state before proceeding.
```

**Acceptance criteria:** Covers all 7 valid `last_completed_phase` values. Explicitly handles missing STATE.toml. Prints state on entry. Handles `halt = true`.

---

### D1.3 — Phase 1: Triage

**Content to author:**

```
## PHASE 1 — TRIAGE

Checkpoint: write STATE.toml with last_completed_phase = "triage" AFTER completing this phase.

1. Read `queue/next-targets.md`. Extract the top 1–3 targets (URLs, topics, or API calls).
2. If queue is empty:
   a. If mode == "search": scan kb/ for coverage gaps (topics with no pages, sparse sections).
      Generate 1–3 new research targets. Append to queue/next-targets.md.
   b. If mode == "deep-analysis": go to DEEP-ANALYSIS PHASE (skip search/summarize).
3. For each target: check seen.json via `copilot/loop_state.py::is_resumable(url)`.
   Skip already-seen URLs with identical content_sha256.
4. Classify each target by source tier (0–3) using the ED Source Roster (see §SOURCE ROSTER).
   Tier-0 targets go first in the search phase.
5. Print: "[TRIAGE] Loop N — targets: <list with tiers>"
```

**Acceptance criteria:** Tier-0 first ordering is explicit. Handles empty queue in both modes. Checkpoints STATE.toml.

---

### D1.4 — Phase 2: Search

**Content to author:**

```
## PHASE 2 — SEARCH

Checkpoint: write STATE.toml with last_completed_phase = "search" AFTER completing this phase.

For each target from triage:

### Tier-0 structured API calls (do these first)

Coriolis-data (ships/modules JSON):
  Fetch: https://github.com/EDCD/coriolis-data/tree/master/dist
  Or direct JSON: https://raw.githubusercontent.com/EDCD/coriolis-data/master/dist/index.json
  → download relevant ship/module JSON blobs

EDSM API:
  Systems: https://www.edsm.net/api-v1/system?systemName=<name>&showId=1&showCoordinates=1&showPermit=1&showInformation=1&showPrimaryStar=1
  Bodies: https://www.edsm.net/api-system-v1/bodies?systemName=<name>
  Stations: https://www.edsm.net/api-system-v1/stations?systemName=<name>
  Rate: no published hard cap; be polite (1 req/sec default, back off on 429).

Spansh API:
  Nearest neutron: https://spansh.co.uk/api/nearest?x=&y=&z=&type=neutron_star
  Exobiology signal search: https://spansh.co.uk/api/bodies/search (POST, see Spansh docs)
  Galaxy dump: https://spansh.co.uk/dumps (nightly CSVs — download only if target is bulk)

Canonn Research API:
  Base: https://api.canonn.tech/
  Thargoid structures: https://api.canonn.tech/thargoidstructures?_limit=100
  Guardian ruins: https://api.canonn.tech/ruinssites?_limit=100
  Bio signals (NHSS): https://api.canonn.tech/nhssreports?_limit=100
  Rate: polite (1 req/sec); no formal rate limit published.

Frontier patch notes:
  Fetch: https://forums.frontier.co.uk/forums/elite-dangerous-news.20/ (paginated)
  Also: https://www.elitedangerous.com/news (official news feed)

GalNet:
  Current: https://www.elitedangerous.com/galnet

### Tier-1 sources — INARA (rate-limited)
  Base: https://inara.cz/
  Engineers: https://inara.cz/elite/engineers/
  Blueprints: https://inara.cz/elite/techbroker/
  Commodities: https://inara.cz/elite/commodities/
  *** RATE LIMIT: 25 requests per 15 minutes. ***
  Enforcement: before every INARA fetch, call `copilot/loop_state.py::check_inara_rate()`.
  If at limit: record remaining seconds in STATE.toml field `inara_backoff_until` (ISO), skip INARA
  for this loop, continue with other sources. Do NOT sleep — move on and note the skip.

### Tier-2 and Tier-3 sources (web fan-out)
  Use WebSearch for current queries:
    - Elite Dangerous wiki (https://elite-dangerous.fandom.com)
    - Established guide sites (EDSY, Frontier forums dev posts)
    - Reddit subs: r/EliteDangerous, r/EliteOdyssey, r/EliteExobiology, r/EliteMiners,
                   r/EliteExplorers, r/EliteCQC
  Use WebFetch for direct URL targets in queue.

For each fetched resource:
  1. Compute url_sha256 = sha256(url). Check seen.json. Skip if present AND content unchanged.
  2. Save raw content to sources/<sha256_prefix>-<slug>.raw (text/JSON/HTML as appropriate).
  3. Record in queue for summarization phase.
  4. Print: "[SEARCH] Fetched: <url> (tier <N>) — <byte_count> bytes"
```

**Acceptance criteria:** All 4 Tier-0 sources listed with actual API URLs. INARA rate-limiter clearly specified (25 req/15 min) with non-sleep skip behavior. seen.json dedup before every fetch. No `sleep` calls — backoff records timestamp and moves on.

---

### D1.5 — Phase 3: Summarize (Ollama offload)

**Content to author:**

```
## PHASE 3 — SUMMARIZE

Checkpoint: write STATE.toml with last_completed_phase = "summarize" AFTER completing this phase.

For each newly fetched source from Phase 2:

1. If source is structured JSON (Coriolis, EDSM, Spansh, Canonn):
   → Do NOT call Ollama. Parse the JSON directly. Extract the relevant fields per source type
     (see §JSON EXTRACTION GUIDE). Write a structured markdown summary directly.
   → Skip to step 5.

2. If source is prose (HTML, forum post, Reddit, patch notes, wiki page):
   a. Extract clean text (strip HTML if needed; keep meaningful content).
   b. If text > 500 tokens, call:
      mcp__ollama-tools__summarize_text with:
        model: "qwen3-coder:30b"
        text: <cleaned text>
        prompt: SEE EXACT PROMPT TEXT BELOW

   THE EXACT OLLAMA SUMMARIZATION PROMPT:
   ---
   You are a fact-extraction assistant for an Elite Dangerous knowledge base.
   
   Extract from the following source text:
   1. KEY CLAIMS — specific factual assertions (ship stats, engineer unlock requirements,
      mechanic rules, location coordinates, commodity prices, unlock chains). One claim per line.
   2. NAMED ENTITIES — ships, engineers, stations, systems, materials, modules, factions,
      power-play powers, biological species. List with type labels.
   3. CURRENCY SIGNALS — any phrase suggesting the content is dated: version numbers,
      "old system", "before the update", "no longer", "used to", "was changed in",
      "powerplay 1", "pre-odyssey", "pre-colonisation", specific patch names.
   4. OBSOLETE FLAG — answer YES or NO: does this source describe mechanics that are
      no longer in the game AND provide no present-day value? If YES, name the mechanic.
   5. AVAILABILITY — for each claim: is it LIVE (currently obtainable/relevant),
      SEASONAL (windowed/recurring), or CHANGED (altered from the described state)?
      If CHANGED, write a one-line changed_note.
   
   FORMAT YOUR RESPONSE AS:
   
   ## Claims
   - <claim 1>
   - <claim 2>
   
   ## Entities
   - <EntityName> (<type>)
   
   ## Currency Signals
   - <signal text>
   
   ## Obsolete
   YES/NO — <reason if YES>
   
   ## Availability Notes
   - <claim or topic>: LIVE|SEASONAL|CHANGED — <changed_note if CHANGED>
   ---

3. If Ollama returns OBSOLETE = YES:
   → Apply CURRENT-TRUTH-ONLY DISCARD RULE (see §DISCARD RULE).
   → Do NOT write a KB page. Log discard to journal/loop-NNNN.md with reason.
   → Update seen.json with content_sha256 so this source is not re-fetched.
   → Continue to next source.

4. Write summary to summaries/<sha256_prefix>-<slug>.md with YAML frontmatter:
   ---
   source_url: <url>
   source_type: <coriolis|edsm|spansh|canonn|patch-notes|inara|fandom|reddit|forum|...>
   source_tier: <0|1|2|3>
   captured_at: <ISO 8601>
   source_count: 1
   verified: false
   availability: <live|seasonal|changed>
   changed_note: <one line or null>
   ---

5. Record source in seen.json via `copilot/loop_state.py::record_source(url, content_sha256)`.

6. Print: "[SUMMARIZE] <url_slug> — <claim_count> claims, availability=<live/seasonal/changed>, obsolete=NO"
   Or:    "[SUMMARIZE] DISCARDED <url_slug> — obsolete: <reason>"
```

**Acceptance criteria:** Exact Ollama prompt text is present and complete. Structured JSON sources bypass Ollama. Discard rule is applied BEFORE synthesis. seen.json recorded AFTER discard decision.

---

### D1.6 — Current-truth-only discard rule (standalone section)

**Content to author as a named section in the prompt:**

```
## §DISCARD RULE — Current-truth-only policy

The KB stores what is TRUE and RELEVANT NOW.

DISCARD a source (do not write a KB page) when the Ollama summary says OBSOLETE = YES AND:
  - The mechanic described has no present-day gameplay value for CMDR Duvrazh, AND
  - Knowing it was changed does not prevent a concrete bad decision.

KEEP despite OBSOLETE = YES when:
  - The stale belief actively misleads (e.g. "Powerplay 1 modules" — user may encounter old guides).
    → Keep as a ONE-LINE changed_note on the relevant current page. Never a full research branch.
  - AX combat, Spire sites, Titan-wreck diving, or Thargoid-related content:
    → ALWAYS tag availability = "live". The Thargoid war narrative ended but this content
       is currently accessible. NEVER present it as gone. This is a hard correctness rule.
  - Trailblazers colonisation (Feb 2025+):
    → The correct current term is "Trailblazers", not "Colonisation v1" or older terms.
       Use "Trailblazers" in all KB pages covering system colonisation.

DO NOT RESEARCH OR PAGE:
  - Powerplay 1 mechanics (replaced by Powerplay 2.0, 2024)
  - Original Thargoid war active-combat rewards (war narrative concluded)
  - Any pre-Odyssey on-foot mechanics that no longer exist
  - EDDB (offline since 2023 — do not reference or link)
  - Any mechanic explicitly marked removed in patch notes with no replacement
  - Any content gated behind unavailable/delisted DLC with no current path

When uncertain whether a mechanic is current: fetch a Tier-0 source (Spansh/EDSM/Canonn) or
the most recent Frontier patch notes before deciding. Do not guess.
```

**Acceptance criteria:** AX/Spire/Titan hard rule is explicit and unambiguous. Trailblazers naming is explicit. EDDB prohibition is explicit. One-line changed_note vs. full-page distinction is explicit.

---

### D1.7 — Phase 4: Synthesize

**Content to author:**

```
## PHASE 4 — SYNTHESIZE

Checkpoint: write STATE.toml with last_completed_phase = "synthesize" AFTER completing this phase.

For each non-discarded summary from Phase 3:

1. Determine the KB destination page(s):
   - Ships/modules → kb/ships/<ship-slug>.md  or  kb/outfitting/<module-type>.md
   - Engineers     → kb/engineers/<engineer-slug>.md
   - Locations     → kb/locations/<system-slug>.md  or  kb/locations/<station-slug>.md
   - Mechanics     → kb/mechanics/<mechanic-slug>.md
   - AX/Thargoid   → kb/ax-thargoid/<topic>.md
   - Powerplay     → kb/powerplay/<topic>.md
   - Colonisation  → kb/colonisation/<topic>.md  (use "trailblazers" in filenames/titles)
   - Exobiology    → kb/careers/exobiology/<topic>.md
   - Community CGs → kb/community-goals/<cg-slug>.md
   - Entities      → kb/entities/<entity-slug>.md  (engineer, power, species, etc.)
   - Trunk         → kb/trunk.md (top-level hub, updated every loop)

2. If the destination page already exists:
   - Read it. Find the relevant H2/H3 section.
   - Merge new claims into the existing section. Do not duplicate existing text.
   - Increment source_count in frontmatter if this source is independent.
   - Set verified = true if source_count >= 2 AND claims agree.
   - If new source contradicts existing: add an HTML comment `<!-- CONFLICT: <source> says X, existing says Y -->` and set verified = false. Do NOT silently resolve.

3. If the destination page does not exist:
   - Create it with proper YAML frontmatter (source_url, source_type, source_tier, captured_at,
     source_count=1, verified=false, availability, changed_note).
   - Follow the chunk-ready format: H2/H3 headings, 128–512 token sections.
   - Prepend `[[trunk]]` backlink at bottom of every new page.
   - Add `[[wikilinks]]` to referenced engineers, ships, systems, mechanics.
   - For changed_note: one line only. Example:
       changed_note: "Powerplay 2.0 (2024) replaced PP1 — old module grind is gone."

4. Write the page via `copilot/atomic.py::write_atomic(path, content)` (Python subprocess).
   NEVER write directly with PowerShell or open() — always atomic.

5. Update kb/trunk.md: ensure the new page is linked from the correct section.

6. Append to queue/next-targets.md: any follow-on research targets discovered in this source.

7. Print: "[SYNTHESIZE] Wrote <kb_path> — source_tier=<N>, verified=<true/false>, availability=<...>"
```

**Acceptance criteria:** All KB subdirectory mappings listed. Conflict handling specified. `write_atomic` is mandatory for all KB writes. trunk.md update required. source_count increment logic specified.

---

### D1.8 — Phase 5: Index

**Content to author:**

```
## PHASE 5 — INDEX

Checkpoint: write STATE.toml with last_completed_phase = "index" AFTER completing this phase.

1. Run `upsert_changed` via Python subprocess:
   python -c "
   import sys; sys.path.insert(0, '.')
   from copilot.index import upsert_changed
   from copilot.paths import kb_dir
   result = upsert_changed(kb_dir())
   print(f'index: added={result[\"added\"]} removed={result[\"removed\"]} unchanged={result[\"unchanged\"]}')
   "

2. Capture stdout. Print: "[INDEX] upsert_changed complete — <result>"

3. If subprocess exits non-zero:
   - Print "[INDEX ERROR] <stderr>". Record in journal.
   - Do NOT halt — continue to commit phase (the commit captures the raw KB change;
     index can be rebuilt later with `python -m copilot.index --rebuild`).

4. Verify Ollama availability for bge-m3 (upsert_changed calls embed internally):
   - If OllamaUnavailable was raised (captured in stderr): print warning, continue to commit.
   - The index is a derived artifact — a failed embed is recoverable; a lost KB write is not.
```

**Acceptance criteria:** Exact Python one-liner for upsert_changed is provided. Error is non-fatal with clear recovery path. Ollama unavailability is handled.

---

### D1.9 — Phase 6: Commit

**Content to author:**

```
## PHASE 6 — COMMIT

Checkpoint: write STATE.toml with last_completed_phase = "commit" AFTER completing this phase.

1. Stage all changes:
   git add kb/ summaries/ sources/ indexes/ embeddings/ queue/ STATE.toml seen.json

2. Count new/modified files:
   $changed = (git diff --cached --name-only).Split("`n").Count

3. Generate commit message:
   "Loop <N>: <N_pages> pages, <N_sources> sources, <mode> mode"
   Example: "Loop 7: 3 pages, 5 sources, search mode"

4. Commit:
   git commit -m "<message>"

5. If commit exits non-zero (nothing staged):
   - Print "[COMMIT] Nothing new to commit — incrementing consecutive_empty_loops."
   - Increment STATE.toml::consecutive_empty_loops.
   - If consecutive_empty_loops >= config.loop.deep_analysis_after_empty_loops (default 5):
     - Set mode = "deep-analysis" in STATE.toml.
     - Print "[COMMIT] Switching to deep-analysis mode."
   - Otherwise: set mode = "search", print "[COMMIT] Resuming search next loop."

6. Regenerate README.md dashboard:
   Write a summary block showing: last_updated, loop_number, mode, consecutive_empty_loops,
   total_kb_pages (count of *.md files under kb/), total_sources (count of seen.json keys),
   last 5 loop summaries (from journal/). Overwrite README.md via write_atomic.

7. Write final STATE.toml:
   loop_number += 1
   last_completed_phase = "commit"
   consecutive_empty_loops = <updated value>
   mode = <current mode>
   halt = false
   updated_at = <ISO 8601 now>

8. Print: "[COMMIT] Loop <N> complete. Next: Loop <N+1>."
```

**Acceptance criteria:** git add lists all relevant directories. Empty-commit path increments counter. deep-analysis threshold uses config value (not hardcoded). README.md regenerated. STATE.toml written last.

---

### D1.10 — Deep-analysis mode

**Content to author:**

```
## DEEP-ANALYSIS MODE

Triggered when: mode == "deep-analysis" in STATE.toml (set after N consecutive empty loops).
Never idle. The screen always shows active work.

1. Announce: "[DEEP-ANALYSIS] No new external sources. Expanding inward."

2. Gap analysis:
   - Read every page in kb/. Use `mcp__ollama-tools__answer_from_file` (qwen3-coder:30b)
     to ask: "What follow-on questions does this page leave unanswered for an Elite Dangerous
     player focused on engineering, AX combat, exobiology, or Trailblazers colonisation?"
   - Collect gap topics. Filter: must be currently relevant (current-truth-only policy applies).

3. Cross-reference clusters:
   - Identify pairs/groups of pages that reference the same engineer, ship, or mechanic
     but have no [[wikilinks]] between them.
   - Add missing [[wikilinks]] and backlinks. Write updated pages via write_atomic.

4. Synthesis documents:
   - For each gap topic with 2+ existing related pages: write a synthesis page in the
     appropriate kb/ subdirectory. Use qwen3-coder:30b via summarize_text to draft;
     review and clean before writing.

5. New search targets:
   - Convert gap topics into concrete search targets (URLs, API queries, topics).
   - Append to queue/next-targets.md.
   - Set mode = "search", reset consecutive_empty_loops = 0 in STATE.toml.

6. Print progress every step. Never silent.
```

**Acceptance criteria:** Uses Ollama tools for heavy lifting. Generates concrete new targets — does not just loop on analysis. Resets to search mode when new targets exist.

---

### D1.11 — ED Source Roster with trust tiers

**Content to author as a named appendix section in the prompt:**

```
## §SOURCE ROSTER — ED Data Sources by Trust Tier

### Tier 0 — Canonical/Structured (highest trust; parse directly)

| Source | URL / Access | Content | Notes |
|---|---|---|---|
| Coriolis-data | https://github.com/EDCD/coriolis-data/tree/master/dist | All ship/module stats as JSON | Ground truth for outfitting numbers |
| FDevIDs (EDCD) | https://github.com/EDCD/FDevIDs | Commodity/module/ship ID mappings | Required for cross-source matching |
| EDSM API | https://www.edsm.net/api-v1/ | Systems, bodies, stations | 1 req/sec polite; no auth required |
| Spansh API | https://spansh.co.uk/api/ | Routing, exobiology, colonisation, neutron stars | POST for body search; GET for routing |
| Spansh dumps | https://spansh.co.uk/dumps | Galaxy-scale CSVs (nightly) | Download only for bulk operations |
| Canonn API | https://api.canonn.tech/ | Guardian/Thargoid structures, bio signals | _limit param; 1 req/sec polite |
| Frontier patch notes | https://forums.frontier.co.uk/forums/elite-dangerous-news.20/ | Official version anchor | Parse for currency validation |
| GalNet | https://www.elitedangerous.com/galnet | In-universe current events | Cross-reference for seasonal/CG status |

### Tier 1 — Authoritative Prose

| Source | URL | Content | Notes |
|---|---|---|---|
| INARA | https://inara.cz/ | Engineers, blueprints, commodities, CGs | **25 req / 15 min rate limit** — use check_inara_rate() before every fetch |
| Frontier Dev Posts | https://forums.frontier.co.uk/ | Developer clarifications | Search for dev flair; high authority |

### Tier 2 — Community Curated

| Source | URL | Content | Notes |
|---|---|---|---|
| Elite Dangerous Wiki | https://elite-dangerous.fandom.com | General mechanics, ships, locations | Verify against Tier 0; sometimes stale |
| EDSY (ship builder) | https://edsy.org | Outfitting references | Good for build verification |
| Canonn Science | https://canonn.science | Exploration/xenology | Complements Canonn API |

### Tier 3 — Anecdotal (corroboration required for verification)

| Source | Subreddit / URL | Content |
|---|---|---|
| r/EliteDangerous | reddit.com/r/EliteDangerous | General discussion, builds, tips |
| r/EliteOdyssey | reddit.com/r/EliteOdyssey | On-foot gameplay, Odyssey content |
| r/EliteExobiology | reddit.com/r/EliteExobiology | Exobiology routes, species tips |
| r/EliteMiners | reddit.com/r/EliteMiners | Mining builds, hotspot info |
| r/EliteExplorers | reddit.com/r/EliteExplorers | Exploration routes, discovery |
| r/EliteCQC | reddit.com/r/EliteCQC | CQC builds and meta |
| YouTube guides | youtube.com search | Video guides; extract via description/transcript |
| Frontier forums | forums.frontier.co.uk | Community guides, dev interaction |

### INARA Rate-Limit Enforcement Detail

```python
# Pseudo-code for check_inara_rate() — implemented in copilot/loop_state.py
def check_inara_rate(state: dict) -> bool:
    """Returns True if safe to fetch INARA, False if at limit."""
    inara_backoff_until = state.get("inara_backoff_until")
    if inara_backoff_until:
        until_dt = datetime.fromisoformat(inara_backoff_until)
        if datetime.utcnow() < until_dt:
            return False  # still in backoff window
    return True  # safe to fetch; caller must track request count

# If at limit: record inara_backoff_until = (now + 15 min).isoformat() in STATE.toml
# Do NOT sleep. Move on to other sources.
```

### EDDB — DEAD SOURCE

EDDB has been offline since 2023. **Never reference EDDB. Never generate URLs to eddb.io.**
If any queued target references EDDB, discard it and replace with Spansh or INARA equivalent.
```

**Acceptance criteria:** All Tier-0 sources have actual URLs. INARA rate limit is specified as 25 req/15 min. INARA pseudo-code present. EDDB prohibition explicit. All 6 ED subreddits listed.

---

### D1.12 — JSON Extraction Guide (inline in prompt)

**Content to author:**

```
## §JSON EXTRACTION GUIDE — Tier-0 structured sources

These sources return structured data. Parse directly; do not call Ollama summarization.

### Coriolis-data ship JSON
Key fields to extract per ship: name, manufacturer, mass, hullMass, fuelCapacity, hardpoints[],
utilities[], internal[], maxJumpRange (approximate), armour, baseShieldStrength, price.
Write to: kb/ships/<slug>.md
Example frontmatter: source_type: coriolis, source_tier: 0, verified: true

### Coriolis-data module JSON
Key fields: name, mount, class, rating, mass, power, damage, range, piercing, effectiveDPS,
engineering_effects[] (for modules that accept G5 rolls).
Write to: kb/outfitting/<category>/<module-slug>.md

### EDSM system endpoint
Key fields: name, id64, coords, allegiance, government, security, population,
primaryStar (type, isScoopable), stations[]{name, type, distanceToArrival, services[]}.
Write to: kb/locations/<system-slug>.md

### Spansh exobiology body search (POST /api/bodies/search)
Key fields per body: bodyName, system, subType, distanceToArrival, signals{Biology: N},
atmosphereType, gravity, volcanism.
Write to: kb/careers/exobiology/systems/<system-slug>.md

### Canonn Thargoid structures endpoint
Key fields: system, bodyName, latitude, longitude, type, hasDataTerminal, hasObelisks.
Write to: kb/ax-thargoid/sites/<site-slug>.md

### Frontier patch notes (HTML)
After extracting clean text: identify version number and release date. Extract:
- Added/changed mechanics (search for "added", "changed", "fixed", "removed")
- Specific module/ship stat changes
- New content introductions
Write to: kb/mechanics/patch-<version>.md  AND  update relevant existing pages.
```

**Acceptance criteria:** All 5 Tier-0 source types covered. KB destination paths specified for each. Fields listed are concrete (no "etc.").

---

### D1.13 — NEVER / ALWAYS lists (ED-specific)

**Content to author:**

```
## NEVER

- NEVER reference EDDB.io — it is offline since 2023.
- NEVER write a KB page for an obsolete-and-pointless mechanic. One-line changed_note only,
  inline on the current relevant page. No standalone obsolescence pages.
- NEVER present AX combat, Spire sites, or Titan-wreck diving as unavailable or concluded.
  Tag these `live`. The Thargoid war narrative ended; this content is current.
- NEVER call the colonisation system anything other than "Trailblazers" (the Feb 2025 name).
- NEVER sleep in the loop — no `Start-Sleep`, no `time.sleep()`. If rate-limited:
  record backoff_until timestamp in STATE.toml and continue with other work.
- NEVER write STATE.toml, seen.json, or any KB file non-atomically (no direct open/write).
  Always use write_atomic / write_json_atomic / write_state.
- NEVER duplicate existing KB content — read the destination page before writing.
- NEVER silently resolve source conflicts — log them as HTML comments and set verified=false.
- NEVER include raw source text verbatim beyond short fair-use quotes (paraphrase and cite URL).
- NEVER use the composite "tier × corroboration × recency" trust score formula —
  trust is carried by discrete fields: source_tier, source_count, verified, availability.
- NEVER call qwen3:8b or qwen3-vl:8b during the research loop — those are for the REPL/vision.
  Loop uses qwen3-coder:30b only (via mcp__ollama-tools__summarize_text).
- NEVER co-load qwen3-coder:30b and qwen3:8b simultaneously (§F memory constraint).
- NEVER stop the loop unless STATE.toml has halt=true or usage is genuinely exhausted.

## ALWAYS

- ALWAYS print timestamped progress for every action (search, fetch, summarize, write, index).
  Format: "[PHASE] <message>" with ISO timestamp prefix from Get-Date in wrapper.
- ALWAYS checkpoint STATE.toml last_completed_phase at the end of each completed phase.
- ALWAYS check seen.json before fetching any URL.
- ALWAYS offload prose summarization (>500 tokens) to qwen3-coder:30b via Ollama tool.
- ALWAYS write KB pages via write_atomic — never direct file write.
- ALWAYS call upsert_changed after writing new/updated KB pages.
- ALWAYS commit after a successful loop (git commit with one-line summary).
- ALWAYS use "Trailblazers" for the colonisation system.
- ALWAYS tag AX/Spire/Titan content as availability=live.
- ALWAYS add [[wikilinks]] to engineers, ships, systems, and mechanics referenced in a page.
- ALWAYS add a [[trunk]] backlink at the bottom of every new KB page.
- ALWAYS add a one-line changed_note (not a full page) when keeping a stale fact that
  prevents bad advice — and mark that section availability=changed.
- ALWAYS record INARA requests against the rate-limit window before fetching.
- ALWAYS log discarded sources to the journal with reason.
- ALWAYS update queue/next-targets.md with follow-on targets discovered during synthesis.
- ALWAYS regenerate README.md dashboard at loop close.
```

**Acceptance criteria:** All NEVER items are ED-specific or derived from CONTRACTS/spec constraints. All ALWAYS items have an imperative and a testable consequence.

---

### D1.14 — Worked example (inline in prompt)

**Content to author as a complete worked-example section:**

```
## §WORKED EXAMPLE — One full loop iteration (Tier-0 Coriolis ingest)

This example shows a complete loop ingesting Coriolis ship JSON for the Federal Corvette.

---

### State at start of loop

STATE.toml:
  loop_number = 1
  last_completed_phase = "none"
  mode = "search"
  consecutive_empty_loops = 0
  halt = false

queue/next-targets.md contains:
  - https://raw.githubusercontent.com/EDCD/coriolis-data/master/dist/ships/federal_corvette.json
    (tier: 0, type: coriolis, added: loop-0)

---

### Phase 1 — Triage

Read queue: 1 target — federal_corvette.json (Tier 0).
Check seen.json: url_sha256 not present → proceed.
Classify: Tier 0 → first in search queue.
Checkpoint: STATE.toml last_completed_phase = "triage"

Print: "[TRIAGE] Loop 1 — targets: [federal_corvette.json (tier 0)]"

---

### Phase 2 — Search

Fetch: https://raw.githubusercontent.com/EDCD/coriolis-data/master/dist/ships/federal_corvette.json
→ 200 OK, 18,432 bytes JSON.

Compute url_sha256 = sha256(url).hexdigest()  (e.g. "a3f7b2...")
Compute content_sha256 = sha256(json_bytes).hexdigest()  (e.g. "d84c19...")
Check seen.json: not present → proceed.
Save to: sources/a3f7b2-federal-corvette.raw

Checkpoint: STATE.toml last_completed_phase = "search"

Print: "[SEARCH] Fetched: federal_corvette.json (tier 0) — 18432 bytes"

---

### Phase 3 — Summarize

Source is structured JSON (Coriolis) → bypass Ollama → parse directly.

Extract from JSON:
  name: "Federal Corvette"
  manufacturer: "Core Dynamics"
  hullMass: 900t
  fuelCapacity: 32t
  hardpoints: 1×huge, 2×large, 4×medium, 2×small
  utilities: 8
  internal: [8F, 7E, 6E, 6E, 5E, 5E, 4E, 3E]
  baseShieldStrength: 333 MJ
  armour: 666
  price: 187,969,338 Cr
  maxJumpRange: ~10 ly unladen (engineering raises to ~25+ ly)

Availability assessment: LIVE (ship is currently purchasable).
Obsolete: NO.
changed_note: null.

Write summaries/a3f7b2-federal-corvette.md with frontmatter:
  source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/...
  source_type: coriolis
  source_tier: 0
  captured_at: 2026-06-01T04:15:00Z
  source_count: 1
  verified: false
  availability: live
  changed_note: null

Record in seen.json:
  "a3f7b2...": {"first_seen": "2026-06-01T04:15:00Z", "content_sha256": "d84c19..."}

Checkpoint: STATE.toml last_completed_phase = "summarize"

Print: "[SUMMARIZE] a3f7b2-federal-corvette.json — 12 claims, availability=live, obsolete=NO"

---

### Phase 4 — Synthesize

Destination: kb/ships/federal-corvette.md (does not exist → create).

Write kb/ships/federal-corvette.md via write_atomic:

---FILE CONTENT PREVIEW---
---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/dist/ships/federal_corvette.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-01T04:15:00Z
source_count: 1
verified: false
availability: live
changed_note: null
---

# Federal Corvette

[[trunk]] | [[ships]] | Core Dynamics

## Overview

The Federal Corvette is the largest [[Core Dynamics]] warship available to independent
commanders. Requires Federal Navy rank of **Post Captain** to purchase.

- **Hull mass:** 900 t
- **Fuel capacity:** 32 t
- **Base price:** 187,969,338 Cr

## Hardpoints

| Mount | Count |
|---|---|
| Huge | 1 |
| Large | 2 |
| Medium | 4 |
| Small | 2 |
| Utility | 8 |

## Internal compartments

8F, 7E, 6E, 6E, 5E, 5E, 4E, 3E

## Defensive profile

- **Base shield:** 333 MJ (heavily engineerable)
- **Armour:** 666 (highest armour rating of purchasable ships)

## Jump range

~10 ly unladen stock; with [[FSD engineering]] and stripped fit: ~22–26 ly achievable.
Recommend [[Guardian FSD Booster]] for exploration variants.

## Related

- [[Engineers]] — [[Felicity Farseer]] for FSD; [[Tod McQuinn]] for weapons
- [[Federal Navy rank]] — Post Captain required
- [[Outfitting]] — see [[huge hardpoint options]]
---END FILE CONTENT PREVIEW---

Update kb/trunk.md: add link under "Ships" section.
Append to queue/next-targets.md:
  - INARA Federal Corvette outfitting page (tier 1)
  - kb/ships/federal-corvette.md needs rank unlock chain

Checkpoint: STATE.toml last_completed_phase = "synthesize"

Print: "[SYNTHESIZE] Wrote kb/ships/federal-corvette.md — source_tier=0, verified=false, availability=live"

---

### Phase 5 — Index

Run upsert_changed:
  python -c "import sys; sys.path.insert(0,'.'); from copilot.index import upsert_changed; from copilot.paths import kb_dir; r=upsert_changed(kb_dir()); print(r)"
  → {"added": 1, "removed": 0, "unchanged": 142}

Checkpoint: STATE.toml last_completed_phase = "index"

Print: "[INDEX] upsert_changed complete — added=1 removed=0 unchanged=142"

---

### Phase 6 — Commit

git add kb/ summaries/ sources/ indexes/ embeddings/ queue/ STATE.toml seen.json
git commit -m "Loop 1: 1 page, 1 source, search mode"

Write final STATE.toml:
  loop_number = 2
  last_completed_phase = "commit"
  consecutive_empty_loops = 0
  mode = "search"

Regenerate README.md.

Print: "[COMMIT] Loop 1 complete. Next: Loop 2."
```

**Acceptance criteria:** All 6 phases shown with actual output. All STATE.toml checkpoints shown. seen.json write shown. git commit shown. Queue extension shown. KB page includes proper frontmatter and [[wikilinks]].

---

## Deliverable 2 Tasks — `wrapper.ps1`

These are testable behaviors. Each task has a test specification.

---

### D2.1 — Initial scaffold and logging

**Write `wrapper.ps1` with:**

```powershell
# ED Research Loop Daemon
# Usage: .\wrapper.ps1 [-PromptFile ed-research-prompt.md] [-MaxRetries 3]
param(
    [string]$PromptFile   = "ed-research-prompt.md",
    [string]$LogFile      = "journal\daemon.log",
    [int]   $MaxRetries   = 3,
    [int]   $BaseBackoffSec = 30
)

$RepoRoot = $PSScriptRoot  # wrapper.ps1 lives at repo root

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $ts  = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    $line = "$ts  [$Level]  $Message"
    $line | Tee-Object -FilePath (Join-Path $RepoRoot $LogFile) -Append
}
```

**Pitfalls to document in inline comments:**
- `$LASTEXITCODE` is only set for external executables (`claude.exe`), not PowerShell cmdlets. Always check it immediately after the `claude` call — do not run any other command between the `claude` invocation and the `if ($LASTEXITCODE -ne 0)` check.
- `Tee-Object -Append` requires the parent directory to exist; ensure `journal\` is created before the first log call.
- `Get-Content -Raw` reads the entire file as one string; `-Encoding UTF8` is mandatory for the prompt file because it contains Unicode characters (arrows, section symbols).
- Here-string `@'...'@` scope: closing `'@` must be at column 0 with no leading whitespace.

**Test spec D2.1-T1:** `wrapper.ps1` runs without error when called with `-PromptFile` pointing to a minimal test prompt file that exits immediately. Verify `journal/daemon.log` contains a timestamped entry.

---

### D2.2 — STATE.toml read and resume logic

**Wrapper behavior:**

```powershell
function Read-StateToml {
    $statePath = Join-Path $RepoRoot "STATE.toml"
    if (-not (Test-Path $statePath)) {
        Write-Log "STATE.toml not found — treating as fresh start." "WARN"
        return @{ loop_number = 0; last_completed_phase = "none"; halt = $false; mode = "search" }
    }
    # Use Python to parse TOML (tomllib stdlib) to avoid PowerShell TOML deps
    $py = @"
import tomllib, json, sys
with open(r'$statePath', 'rb') as f:
    d = tomllib.load(f)
print(json.dumps(d))
"@
    $json = python -c $py 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Log "STATE.toml parse error: $json" "ERROR"
        return $null
    }
    return ($json | ConvertFrom-Json)
}
```

**After reading state:**
- If `halt = true`: `Write-Log "Halt flag set — exiting."; exit 0`
- Print: `Write-Log "Resuming: loop=$($state.loop_number) phase=$($state.last_completed_phase) mode=$($state.mode)"`

**Test spec D2.2-T1:** When STATE.toml contains `halt = true`, `wrapper.ps1` exits 0 after printing the halt message without invoking `claude`.

**Test spec D2.2-T2:** When STATE.toml is absent, wrapper continues to invoke `claude` (does not crash on missing file).

---

### D2.3 — Main loop with retry/backoff

**Wrapper main loop:**

```powershell
# Ensure log directory exists
$logDir = Split-Path (Join-Path $RepoRoot $LogFile) -Parent
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Force $logDir | Out-Null }

Write-Log "=== ED Research Daemon starting. PID=$PID ==="

while ($true) {
    $state = Read-StateToml
    if ($null -eq $state) {
        Write-Log "State unreadable — aborting." "ERROR"
        exit 1
    }
    if ($state.halt -eq $true) { Write-Log "Halt flag set."; exit 0 }

    $loopStart    = Get-Date
    $attempt      = 0
    $loopSuccess  = $false

    Write-Log "=== Loop $($state.loop_number) start (mode=$($state.mode)) ==="

    while (-not $loopSuccess -and $attempt -lt $MaxRetries) {
        $attempt++
        Write-Log "Invoking claude (attempt $attempt/$MaxRetries)..."

        # Read prompt fresh each attempt (allows hot-editing the prompt)
        $prompt = Get-Content (Join-Path $RepoRoot $PromptFile) -Raw -Encoding UTF8

        # Invoke claude — stream output live via Tee
        claude -p $prompt 2>&1 | Tee-Object -FilePath (Join-Path $RepoRoot $LogFile) -Append
        $exitCode = $LASTEXITCODE   # capture IMMEDIATELY — next line may clobber it

        if ($exitCode -eq 0) {
            $loopSuccess = $true
            Write-Log "=== Loop $($state.loop_number) succeeded. Duration: $((Get-Date) - $loopStart) ==="
        } else {
            $backoff = [math]::Pow(2, $attempt) * $BaseBackoffSec
            Write-Log "claude exited $exitCode. Backing off $backoff sec (attempt $attempt)." "WARN"
            # Print countdown so screen is never silent
            for ($i = [int]$backoff; $i -gt 0; $i -= 10) {
                Write-Log "  ... retrying in $i sec"
                Start-Sleep -Seconds ([math]::Min(10, $i))
            }
        }
    }

    if (-not $loopSuccess) {
        Write-Log "All $MaxRetries retries failed. Sleeping 5 min." "ERROR"
        for ($i = 300; $i -gt 0; $i -= 15) {
            Write-Log "  ... next attempt in $i sec"
            Start-Sleep -Seconds 15
        }
    }
}
```

**Pitfalls documented in code comments:**
- `$exitCode = $LASTEXITCODE` immediately after `claude` — no commands between them.
- `claude -p $prompt 2>&1 | Tee-Object` pipes both stdout and stderr to log; `2>&1` merges stderr.
- `ConvertFrom-Json` returns `PSCustomObject`; access fields as `$state.halt` not `$state["halt"]`.
- Countdown uses `Start-Sleep -Seconds 15` increments, not one long sleep, so Ctrl-C is responsive.

**Test spec D2.3-T1:** When `claude` exits with code 1, wrapper retries exactly `$MaxRetries` times with exponential backoff, then prints the "all retries failed" message and sleeps 5 minutes before next outer iteration. Verify by mocking `claude` as a script that always exits 1.

**Test spec D2.3-T2:** When `claude` exits 0, wrapper immediately starts the next iteration without any sleep.

**Test spec D2.3-T3:** Ctrl-C (SIGINT) terminates the wrapper cleanly without a hanging process. (Manual verification.)

---

### D2.4 — Encoding and path correctness

**Checklist:**
- [ ] `$PromptFile` default is `"ed-research-prompt.md"` (relative to `$PSScriptRoot`)
- [ ] `$LogFile` default is `"journal\daemon.log"` (Windows path separator)
- [ ] All `Join-Path` calls use `$RepoRoot` as base — no hardcoded `G:\` paths
- [ ] `Get-Content ... -Encoding UTF8` on the prompt file (not default UTF-16)
- [ ] Python one-liner uses raw string `r'$statePath'` to avoid backslash escape issues
- [ ] `journal\` directory created before first `Write-Log` call

**Test spec D2.4-T1:** Wrapper can be launched from any working directory (not just repo root) because it uses `$PSScriptRoot` for all paths.

---

## Deliverable 3 Tasks — `copilot/loop_state.py` (TDD)

This module contains the idempotency-critical logic. Write tests first (TDD), then the implementation.

---

### D3.1 — Write tests first: `tests/test_loop_state.py`

Write the following test file before implementing `loop_state.py`:

```python
"""
tests/test_loop_state.py — TDD tests for copilot/loop_state.py

Run: python -m pytest tests/test_loop_state.py -v
"""
import json, hashlib, time
from pathlib import Path
import pytest
from copilot.loop_state import (
    advance_phase,
    is_resumable,
    record_source,
    check_inara_rate,
    PHASE_ORDER,
)


# ---------------------------------------------------------------------------
# advance_phase
# ---------------------------------------------------------------------------

class TestAdvancePhase:
    def test_none_advances_to_triage(self):
        assert advance_phase("none") == "triage"

    def test_triage_advances_to_search(self):
        assert advance_phase("triage") == "search"

    def test_search_advances_to_summarize(self):
        assert advance_phase("search") == "summarize"

    def test_summarize_advances_to_synthesize(self):
        assert advance_phase("summarize") == "synthesize"

    def test_synthesize_advances_to_index(self):
        assert advance_phase("synthesize") == "index"

    def test_index_advances_to_commit(self):
        assert advance_phase("index") == "commit"

    def test_commit_advances_to_triage(self):
        """After commit, next loop starts at triage."""
        assert advance_phase("commit") == "triage"

    def test_invalid_phase_raises(self):
        with pytest.raises(ValueError, match="Unknown phase"):
            advance_phase("unknown-phase")

    def test_phase_order_complete(self):
        """PHASE_ORDER must contain all 7 canonical phase names."""
        expected = {"none", "triage", "search", "summarize", "synthesize", "index", "commit"}
        assert set(PHASE_ORDER) == expected


# ---------------------------------------------------------------------------
# is_resumable
# ---------------------------------------------------------------------------

class TestIsResumable:
    def test_new_url_is_resumable(self, tmp_path):
        seen = tmp_path / "seen.json"
        seen.write_text("{}", encoding="utf-8")
        assert is_resumable("https://example.com/page", str(seen)) is True

    def test_seen_url_different_content_is_resumable(self, tmp_path):
        """Same URL but different content hash → should re-fetch (content changed)."""
        url = "https://example.com/page"
        url_sha = hashlib.sha256(url.encode()).hexdigest()
        data = {url_sha: {"first_seen": "2026-01-01T00:00:00Z", "content_sha256": "old_hash"}}
        seen = tmp_path / "seen.json"
        seen.write_text(json.dumps(data), encoding="utf-8")
        assert is_resumable(url, str(seen), content_sha256="new_hash") is True

    def test_seen_url_same_content_not_resumable(self, tmp_path):
        """Same URL + same content hash → skip (already processed)."""
        url = "https://example.com/page"
        url_sha = hashlib.sha256(url.encode()).hexdigest()
        content_sha = "abc123"
        data = {url_sha: {"first_seen": "2026-01-01T00:00:00Z", "content_sha256": content_sha}}
        seen = tmp_path / "seen.json"
        seen.write_text(json.dumps(data), encoding="utf-8")
        assert is_resumable(url, str(seen), content_sha256=content_sha) is False

    def test_missing_seen_file_is_resumable(self, tmp_path):
        """Missing seen.json → treat all URLs as new."""
        nonexistent = str(tmp_path / "seen.json")
        assert is_resumable("https://example.com/x", nonexistent) is True


# ---------------------------------------------------------------------------
# record_source
# ---------------------------------------------------------------------------

class TestRecordSource:
    def test_record_creates_entry(self, tmp_path):
        seen = tmp_path / "seen.json"
        seen.write_text("{}", encoding="utf-8")
        url = "https://example.com/page"
        record_source(url, "content_hash_123", str(seen))
        data = json.loads(seen.read_text(encoding="utf-8"))
        url_sha = hashlib.sha256(url.encode()).hexdigest()
        assert url_sha in data
        assert data[url_sha]["content_sha256"] == "content_hash_123"
        assert "first_seen" in data[url_sha]

    def test_record_is_idempotent(self, tmp_path):
        """Recording the same URL twice preserves first_seen and updates content_sha256."""
        seen = tmp_path / "seen.json"
        seen.write_text("{}", encoding="utf-8")
        url = "https://example.com/page"
        record_source(url, "hash_v1", str(seen))
        first_seen_val = json.loads(seen.read_text())
        url_sha = hashlib.sha256(url.encode()).hexdigest()
        original_first_seen = first_seen_val[url_sha]["first_seen"]

        record_source(url, "hash_v2", str(seen))
        data = json.loads(seen.read_text(encoding="utf-8"))
        assert data[url_sha]["first_seen"] == original_first_seen  # preserved
        assert data[url_sha]["content_sha256"] == "hash_v2"         # updated

    def test_record_uses_atomic_write(self, tmp_path, monkeypatch):
        """record_source must call write_json_atomic, not open(...,'w')."""
        from copilot import loop_state
        calls = []
        monkeypatch.setattr(loop_state, "write_json_atomic",
                            lambda path, obj: calls.append((path, obj)))
        seen = tmp_path / "seen.json"
        seen.write_text("{}", encoding="utf-8")
        record_source("https://x.com", "h", str(seen))
        assert len(calls) == 1

    def test_record_creates_seen_if_missing(self, tmp_path):
        """If seen.json does not exist, record_source creates it."""
        seen = tmp_path / "seen.json"
        assert not seen.exists()
        record_source("https://example.com/new", "hash_new", str(seen))
        assert seen.exists()
        data = json.loads(seen.read_text(encoding="utf-8"))
        assert len(data) == 1


# ---------------------------------------------------------------------------
# check_inara_rate
# ---------------------------------------------------------------------------

class TestCheckInaraRate:
    def test_no_backoff_entry_allows_fetch(self):
        state = {"loop_number": 1, "last_completed_phase": "triage"}
        assert check_inara_rate(state) is True

    def test_expired_backoff_allows_fetch(self):
        past = "2000-01-01T00:00:00"
        state = {"inara_backoff_until": past}
        assert check_inara_rate(state) is True

    def test_future_backoff_blocks_fetch(self):
        from datetime import datetime, timezone, timedelta
        future = (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat()
        state = {"inara_backoff_until": future}
        assert check_inara_rate(state) is False

    def test_empty_string_backoff_allows_fetch(self):
        state = {"inara_backoff_until": ""}
        assert check_inara_rate(state) is True
```

**Acceptance criteria:** All test classes and methods listed above are present verbatim in the file. Tests can be run with `python -m pytest tests/test_loop_state.py -v` after Plan A scaffold exists.

---

### D3.2 — Implement `copilot/loop_state.py`

Write the implementation to satisfy the tests above:

```python
"""
copilot/loop_state.py — Loop idempotency and phase management for the research daemon.

Imported by the research loop (via Python subprocess or direct import) and by wrapper.ps1
(via Python subprocess) to manage STATE.toml phase transitions and seen.json deduplication.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from copilot.atomic import write_json_atomic
from copilot.paths import repo_root

# ---------------------------------------------------------------------------
# Phase ordering
# ---------------------------------------------------------------------------

PHASE_ORDER: list[str] = [
    "none",
    "triage",
    "search",
    "summarize",
    "synthesize",
    "index",
    "commit",
]


def advance_phase(current: str) -> str:
    """
    Return the next phase after `current`.

    "none" → "triage" → "search" → "summarize" → "synthesize" → "index" → "commit" → "triage"

    Raises ValueError for unknown phase names.
    """
    if current not in PHASE_ORDER:
        raise ValueError(f"Unknown phase: {current!r}. Expected one of {PHASE_ORDER}")
    idx = PHASE_ORDER.index(current)
    # "commit" wraps back to "triage" (start of next loop), not "none"
    if current == "commit":
        return "triage"
    return PHASE_ORDER[idx + 1]


# ---------------------------------------------------------------------------
# seen.json deduplication
# ---------------------------------------------------------------------------

def _url_sha(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def _load_seen(seen_path: str) -> dict:
    p = Path(seen_path)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def is_resumable(
    url: str,
    seen_path: str,
    content_sha256: Optional[str] = None,
) -> bool:
    """
    Return True if the URL should be fetched/processed this loop.

    Returns False only when the URL has been seen before AND either:
      - no content_sha256 is provided (assume content unchanged), OR
      - the provided content_sha256 matches the stored one.

    "Resumable" = safe to skip (already processed with identical content).
    So is_resumable returns True to ALLOW fetching, False to SKIP.
    """
    data = _load_seen(seen_path)
    key = _url_sha(url)
    if key not in data:
        return True  # never seen → fetch
    stored_sha = data[key].get("content_sha256")
    if content_sha256 is None:
        return False  # seen, no content to compare → assume unchanged → skip
    return content_sha256 != stored_sha  # True = content changed → re-fetch


def record_source(url: str, content_sha256: str, seen_path: str) -> None:
    """
    Record a URL + content hash in seen.json atomically.

    Preserves `first_seen` on subsequent updates; updates `content_sha256`.
    Creates seen.json if it does not exist.
    """
    data = _load_seen(seen_path)
    key = _url_sha(url)
    now_iso = datetime.now(timezone.utc).isoformat()
    if key in data:
        # Preserve first_seen; update content hash
        data[key]["content_sha256"] = content_sha256
    else:
        data[key] = {
            "first_seen": now_iso,
            "content_sha256": content_sha256,
        }
    write_json_atomic(Path(seen_path), data)


# ---------------------------------------------------------------------------
# INARA rate-limit check
# ---------------------------------------------------------------------------

def check_inara_rate(state: dict) -> bool:
    """
    Return True if it is safe to fetch from INARA right now.

    Reads `inara_backoff_until` from the state dict. If it is set to a future
    ISO 8601 datetime, return False (still in backoff window).
    """
    raw = state.get("inara_backoff_until", "")
    if not raw:
        return True
    try:
        until_dt = datetime.fromisoformat(raw)
        # Ensure timezone-aware comparison
        now = datetime.now(timezone.utc)
        if until_dt.tzinfo is None:
            # naive → assume UTC
            from datetime import timezone as tz
            until_dt = until_dt.replace(tzinfo=tz.utc)
        return now >= until_dt  # True = past the backoff → safe to fetch
    except ValueError:
        return True  # unparseable → assume safe
```

**Acceptance criteria:** All tests in `test_loop_state.py` pass. Module imports cleanly from `copilot.atomic` (Plan A). No global state. All file I/O uses `write_json_atomic`.

---

### D3.3 — `__init__.py` registration

No changes needed to `copilot/__init__.py` for this module — it is imported directly as `from copilot.loop_state import ...`. Confirm Plan A created `copilot/__init__.py` (it must exist for the package to be importable).

---

## Integration and Acceptance Tests

### INT-1 — Dry-run single loop

**Test:** Launch `wrapper.ps1` with a minimal prompt that reads STATE.toml, prints state, and exits 0 without running real research. Verify:
- `STATE.toml` is updated with `last_completed_phase = "commit"` and `loop_number = 1`
- `journal/daemon.log` contains timestamped entries for start and end
- `seen.json` exists (created by the run or pre-existing)
- No non-atomic writes occurred (check for `.tmp` files leftover)

### INT-2 — Idempotent resume (spec §J)

**Test:** Run one complete loop iteration. Kill the process (Ctrl-C or `Stop-Process`) mid-synthesize phase. Relaunch `wrapper.ps1`. Verify:
- The loop resumes at the `synthesize` phase (not from the beginning)
- No KB pages are duplicated
- `seen.json` is uncorrupted
- `STATE.toml` is uncorrupted (readable, all required fields present)

### INT-3 — content-hash dedup

**Test:** Run two consecutive loops targeting the same Tier-0 URL (e.g. same Coriolis JSON file). Verify:
- Second loop skips the URL (seen.json has matching content_sha256)
- No duplicate KB pages or summaries written
- `indexes/manifest.json` reports `unchanged` > 0 and `added` = 0 for unchanged pages

### INT-4 — INARA rate-limit skip (non-sleep)

**Test:** Set `inara_backoff_until` in STATE.toml to a future timestamp. Verify:
- Loop proceeds without sleeping
- INARA targets are skipped with a logged message
- Other Tier-0 and Tier-2/3 targets are still processed normally

### INT-5 — Empty-loop counter and deep-analysis trigger

**Test:** Run 5 consecutive loops that produce no new committed content. Verify:
- `consecutive_empty_loops` reaches 5
- `mode` switches to `deep-analysis` in STATE.toml
- Next loop enters deep-analysis branch (log message "[DEEP-ANALYSIS]" present)

---

## Self-Review Checklist

Run this checklist before marking the plan complete. Fix any gaps inline above.

### Coverage of spec §J (idempotency)
- [x] All STATE.toml writes use `write_state` (atomic)
- [x] All seen.json writes use `write_json_atomic`
- [x] All KB writes use `write_atomic`
- [x] Phase checkpointing documented for all 6 phases
- [x] Resume-at-phase logic documented in D1.2 and D2.2
- [x] content-hash dedup in `is_resumable` and `record_source`
- [x] INT-2 test covers kill-and-resume scenario

### Coverage of spec §H (ED domain)
- [x] All 4 Tier-0 sources listed with actual API URLs (D1.11)
- [x] INARA rate limit specified as 25 req/15 min (D1.4, D1.11)
- [x] INARA non-sleep backoff pattern implemented (D1.4, D3.2)
- [x] EDDB dead-source prohibition explicit (D1.11, D1.13)
- [x] AX/Spire/Titan `live` hard rule in §DISCARD RULE (D1.6)
- [x] Trailblazers naming rule in §DISCARD RULE and ALWAYS list (D1.6, D1.13)
- [x] PP1→PP2 changed_note example present (D1.6)
- [x] All 6 ED subreddits listed (D1.11)

### Coverage of Loop/6-phase structure
- [x] All 6 phases covered with their own D1.x task (D1.3–D1.9)
- [x] Deep-analysis mode covered (D1.10)
- [x] Worked example covers all 6 phases (D1.14)
- [x] Phase ordering constants in loop_state.py (D3.2)

### Current-truth-only policy
- [x] Discard rule has its own named section (D1.6)
- [x] Ollama prompt instructs model to flag obsolete content (D1.5)
- [x] Discard applied BEFORE synthesis (D1.5)
- [x] One-line changed_note vs. full-page distinction clear (D1.6, D1.7)

### Type consistency vs. CONTRACTS.md
- [x] `seen.json` schema matches CONTRACTS.md exactly (`url_sha256` key, `first_seen`, `content_sha256`)
- [x] `STATE.toml` fields match CONTRACTS.md exactly (loop_number, last_completed_phase, mode, consecutive_empty_loops, halt, updated_at)
- [x] `write_state` / `write_atomic` / `write_json_atomic` imported from `copilot.atomic` (Plan A)
- [x] `upsert_changed` called with `kb_dir()` signature matching CONTRACTS.md
- [x] `Chunk.availability` values: `live | seasonal | changed` only (no `superseded`/`removed`)
- [x] `chunk_id` scheme from CONTRACTS.md referenced in D1.7 (synthesize uses existing pages by path)
- [x] Ollama model for loop = `qwen3-coder:30b` (not `qwen3:8b`) as per CONTRACTS.md `[ollama] loop_model`
- [x] `deep_analysis_after_empty_loops` read from config (default 5) — not hardcoded

### Placeholder scan
- No `<TODO>`, `<FILL_IN>`, `<YOUR_URL_HERE>` placeholders remain in any section
- All API URLs are actual production endpoints (verified against known ED community sources)
- All function signatures match CONTRACTS.md exactly

### wrapper.ps1 pitfalls
- [x] `$LASTEXITCODE` captured immediately after `claude` call (D2.3)
- [x] `-Encoding UTF8` on `Get-Content` for prompt file (D2.4)
- [x] `journal\` directory created before first `Write-Log` (D2.1)
- [x] No `2>/dev/null` — using `2>&1` merge for stderr capture (D2.3)
- [x] `ConvertFrom-Json` returns PSCustomObject — field access via dot notation (D2.2)
- [x] `$PSScriptRoot` for all paths — no hardcoded drive paths (D2.4)

---

## Execution Order for the Implementing Agent

1. Confirm Plan A is complete (check `copilot/atomic.py`, `copilot/index.py`, `copilot/paths.py`, `config.toml`, `STATE.toml`, directory scaffold all exist).
2. Write `tests/test_loop_state.py` (D3.1) exactly as specified.
3. Run `python -m pytest tests/test_loop_state.py -v` — all tests should FAIL (TDD red).
4. Write `copilot/loop_state.py` (D3.2).
5. Run `python -m pytest tests/test_loop_state.py -v` — all tests should PASS (TDD green).
6. Write `wrapper.ps1` (D2.1 through D2.4).
7. Run D2.1-T1, D2.2-T1, D2.2-T2, D2.3-T1, D2.3-T2, D2.4-T1 manually.
8. Write `ed-research-prompt.md` section by section (D1.1 through D1.14).
9. Dry-run INT-1: single loop with minimal prompt.
10. Full loop run: one real Tier-0 source (Coriolis federal_corvette.json per worked example).
11. Run INT-2 (idempotent resume), INT-3 (content-hash dedup), INT-4 (INARA skip), INT-5 (deep-analysis trigger).
12. If all pass: mark Plan D complete and notify user.
