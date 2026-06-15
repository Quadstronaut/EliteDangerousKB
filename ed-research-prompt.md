# ED Research Loop — AUTONOMOUS EXECUTION TASK

**YOU ARE A HEADLESS AUTONOMOUS AGENT. THIS IS YOUR TASK — EXECUTE IT NOW, START TO FINISH,
WITHOUT ASKING ANY QUESTIONS AND WITHOUT WAITING FOR CONFIRMATION.** There is no human to
answer you; you run unattended via `wrapper.ps1`. If you stop to ask, defer, or merely describe
what you *would* do, the loop FAILS. This run is fully authorized: writing files under the repo,
running `git` locally, and fetching public ED APIs are all expected and approved — do not seek
permission, do not invoke skills, do not deliberate. DO THE WORK.

Your task: run **EXACTLY ONE** research loop — triage -> search -> summarize -> synthesize ->
index -> commit — checkpointing `STATE.toml` after each phase, then STOP (the wrapper repeats you
and enforces the -MaxLoops bound; do not start a second loop). **Begin immediately** with
LOOP-STATE DETECTION step 1 below; your first action is to run that command.

Environment: CWD = the repo root (the directory containing `config.toml` and this prompt; resolved dynamically, never a fixed path). `PY` = the venv interpreter
`.venv\Scripts\python.exe`. Print a timestamped `[PHASE] message` line for every action.

---

## MISSION

Grow a local Elite Dangerous knowledge base at `kb/` with **fact-checked, current-truth-only**
knowledge. Stale/obsolete mechanics are **omitted** — never paged. The sole exception: a
one-line `changed_note` on a current page when knowing a thing changed prevents bad advice
(e.g. Powerplay 1 -> 2). Offload bulk prose summarization to qwen3-coder:30b via the Ollama
MCP tool. Parse structured JSON (Coriolis/EDSM/Spansh/Canonn) directly — no LLM. Commit after
the loop. Print timestamped progress for every action — never be silent.

---

## LOOP-STATE DETECTION (do this first, every invocation)

1. Read state: `PY -c "from copilot.atomic import read_state; import json; print(json.dumps(read_state()))"`
2. If `halt` is true -> print "Loop halted by STATE.toml." and exit 0 immediately.
3. Note `loop_number`, `mode` (search|deep-analysis), `last_completed_phase`, `consecutive_empty_loops`.
4. Resume logic:
   - `last_completed_phase` is `none` or `commit` -> start a fresh loop at TRIAGE.
   - otherwise -> resume at the phase AFTER `last_completed_phase` (use
     `PY -c "from copilot.loop_state import advance_phase; print(advance_phase('<phase>'))"`).
5. Print: `[STATE] loop=<n> mode=<m> resuming at <phase>`.

After completing each phase, checkpoint:
`PY -c "from copilot.atomic import read_state, write_state; s=read_state(); s['last_completed_phase']='<phase>'; write_state(s)"`

---

## PHASE 1 — TRIAGE

1. Read `queue/next-targets.md`. Take the top 1-3 targets.
2. If the queue is empty:
   - mode == "search": scan `kb/` for coverage gaps, generate 1-3 new targets, append to the queue.
   - mode == "deep-analysis": jump to DEEP-ANALYSIS MODE below.
3. For each target, dedup-check before fetching:
   `PY -c "from copilot.loop_state import is_resumable; print(is_resumable('<url>', 'indexes/seen.json'))"`
   Skip targets that return `False`.
4. Classify each by source tier (see SOURCE ROSTER). Tier-0 first.
5. Print `[TRIAGE] loop <n> targets: <list with tiers>`. Checkpoint phase=triage.

## PHASE 2 — SEARCH

For each surviving target, Tier-0 structured APIs first:
- Fetch via WebFetch (prose) or a direct GET (JSON). Many ED APIs (EDSM, INARA) 403 the
  bare urllib User-Agent, so always send one. For JSON:
  `PY -c "import urllib.request,sys; r=urllib.request.Request('<url>', headers={'User-Agent':'Mozilla/5.0 (ED-KB-research-loop)'}); sys.stdout.write(urllib.request.urlopen(r,timeout=30).read().decode())"`.
- Save raw bytes to `sources/<sha8>-<slug>.raw` (use a short sha of the URL for `<sha8>`).
- Compute content sha: `PY -c "import hashlib,sys; print(hashlib.sha256(open('<rawfile>','rb').read()).hexdigest())"`.
- Print `[SEARCH] fetched <url> (tier N) — <bytes> bytes`. Checkpoint phase=search.

INARA (Tier 1) is rate-limited 25 req/15min. Before any INARA fetch:
`PY -c "from copilot.atomic import read_state; from copilot.loop_state import check_inara_rate; print(check_inara_rate(read_state()))"`
If False, SKIP INARA this loop (do not sleep) and log the skip.

## PHASE 3 — SUMMARIZE

- Structured JSON (Coriolis/EDSM/Spansh/Canonn): DO NOT call Ollama. Parse directly; extract the
  fields named in the JSON EXTRACTION GUIDE; build a clean markdown summary.
- Prose (HTML/forum/reddit/wiki/patch notes): if > ~500 tokens, call
  `mcp__ollama-tools__summarize_text` with `model: "qwen3-coder:30b"` and a fact-extraction
  prompt asking for: key claims, named entities, currency signals, an OBSOLETE yes/no, and
  per-claim availability (live|seasonal|changed). If that MCP tool is unavailable, summarize
  inline yourself (note the fallback in the log).
- Apply the DISCARD RULE. If obsolete-and-pointless -> do NOT write a page; log the discard to
  `journal/loop-<n>.md`; still record the source in seen.json; continue.
- Write kept summaries to `summaries/<sha8>-<slug>.md` with YAML frontmatter (source_url,
  source_type, source_tier, captured_at, source_count:1, verified:false, availability, changed_note).
- Record each processed source:
  `PY -c "from copilot.loop_state import record_source; record_source('<url>','<contentsha>','indexes/seen.json')"`
- Print `[SUMMARIZE] <slug> — <n> claims, availability=<...>, obsolete=NO|DISCARDED`. Checkpoint phase=summarize.

## PHASE 4 — SYNTHESIZE

For each kept summary:
1. Pick the KB destination: ships->`kb/ships/`, outfitting->`kb/outfitting/`, engineers->`kb/engineers/`,
   locations->`kb/locations/`, mechanics->`kb/mechanics/`, AX/Thargoid->`kb/ax-thargoid/`,
   powerplay->`kb/powerplay/`, colonisation->`kb/colonisation/` (use "trailblazers"),
   exobiology->`kb/careers/exobiology/`, entities->`kb/entities/`.
2. If the page exists: read it, merge new claims into the right H2/H3 section (no duplication);
   bump `source_count` if independent; set `verified:true` when source_count>=2 and claims agree;
   on contradiction add `<!-- CONFLICT: ... -->` and set `verified:false` (never silently resolve).
3. If new: create with proper frontmatter; chunk-ready H2/H3 sections; `[[trunk]]` backlink at the
   bottom; `[[wikilinks]]` to referenced engineers/ships/systems/mechanics.
4. **Write atomically** — never write the kb file directly. Stage then atomic-replace:
   - Write the full page content to `live/_staging.md` (your Write tool is fine for the staging file).
   - `PY -c "from copilot.atomic import write_atomic; from pathlib import Path; write_atomic(Path(r'<kb_path>'), Path('live/_staging.md').read_text(encoding='utf-8'))"`
5. Ensure `kb/trunk.md` links the new page. Append any follow-on targets to `queue/next-targets.md`.
6. Print `[SYNTHESIZE] wrote <kb_path> — tier=<N> verified=<bool> availability=<...>`. Checkpoint phase=synthesize.

## PHASE 5 — INDEX

`PY -c "from copilot.index import upsert_changed; from copilot.paths import kb_dir; print(upsert_changed(kb_dir()))"`
Print `[INDEX] <result>`. If it errors (e.g. Ollama down for bge-m3), log it and CONTINUE to commit —
the index is a derived artifact; a committed KB page is not. Checkpoint phase=index.

## PHASE 6 — COMMIT

1. `git add kb/ summaries/ sources/ indexes/ embeddings/ queue/ journal/ STATE.toml`
2. Count staged files: `git diff --cached --name-only` -> N.
3. Load the deep-analysis threshold:
   `PY -c "from copilot.paths import load_config; print(load_config()['loop']['deep_analysis_after_empty_loops'])"`
4. **EMPTY LOOP (N == 0):** do NOT run `git commit` — it exits non-zero with nothing staged and
   would abort the loop before state advances. Instead increment `consecutive_empty_loops`; if it
   reaches the threshold set `mode="deep-analysis"`, else keep `mode="search"`. Print
   `[COMMIT] empty loop <n> — no new content.` Then go to step 6.
5. **NON-EMPTY (N > 0):** `git commit -m "Loop <n>: <pages> pages, <sources> sources, <mode> mode"`.
   Set `consecutive_empty_loops=0`. Print `[COMMIT] loop <n> committed (<N> files).`
6. **ALWAYS advance state** (this MUST run on every loop — empty or not — so the wrapper sees
   loop_number progress and does not livelock-retry). Persist loop_number+1, phase, and the
   mode / consecutive_empty_loops values from above in ONE write:
   `PY -c "from copilot.atomic import read_state, write_state; s=read_state(); s['loop_number']=s.get('loop_number',0)+1; s['last_completed_phase']='commit'; s['consecutive_empty_loops']=<value>; s['mode']='<mode>'; write_state(s)"`
7. Print `[COMMIT] loop <n> complete.` Then STOP — exit. Do not begin another loop.

---

## DEEP-ANALYSIS MODE (only when mode == "deep-analysis")

No new external sources. Expand inward, never idle:
1. Read pages under `kb/`; ask (optionally via `mcp__ollama-tools__answer_from_file`,
   qwen3-coder:30b) what currently-relevant follow-on questions each leaves open.
2. Add missing `[[wikilinks]]`/backlinks between related pages (write atomically).
3. For a gap with 2+ related pages, draft a synthesis page.
4. Convert gaps into concrete new targets, append to `queue/next-targets.md`, set `mode="search"`,
   reset `consecutive_empty_loops=0`. Then run phases INDEX and COMMIT. Print every step.

---

## DISCARD RULE — current-truth-only

KEEP what is TRUE and RELEVANT NOW. Discard (no page) when a source is obsolete AND has no
present value AND knowing it changed prevents no bad decision. HARD rules:
- AX combat, Spire sites, Titan-wreck diving, Thargoid content: ALWAYS `availability: live`.
  The war narrative ended but this content is currently accessible — NEVER present it as gone.
- Colonisation is "**Trailblazers**" (Feb 2025) — never "Colonisation v1" or older terms.
- Keep a stale fact ONLY as a one-line `changed_note` on the current page (e.g. PP1->PP2), never a page.
- NEVER reference EDDB.io (offline since 2023).
- DO NOT page: Powerplay 1 mechanics, original Thargoid-war combat rewards, removed pre-Odyssey
  on-foot mechanics, anything marked removed with no replacement.

---

## SOURCE ROSTER (trust tiers)

- **Tier 0** (parse directly, highest trust): Coriolis-data
  `https://raw.githubusercontent.com/EDCD/coriolis-data/master/dist/...`; FDevIDs (EDCD);
  EDSM `https://www.edsm.net/api-v1/`; Spansh `https://spansh.co.uk/api/`; Canonn
  `https://api.canonn.tech/`; Frontier patch notes / GalNet. Be polite (~1 req/sec).
- **Tier 1**: INARA `https://inara.cz/` — **25 req / 15 min**, gate with check_inara_rate; Frontier dev posts.
- **Tier 2**: ED Wiki `https://elite-dangerous.fandom.com`, EDSY, canonn.science (verify vs Tier 0).
- **Tier 3** (corroboration required): r/EliteDangerous, r/EliteOdyssey, r/EliteExobiology,
  r/EliteMiners, r/EliteExplorers, r/EliteCQC; YouTube/forum guides.

## JSON EXTRACTION GUIDE (Tier-0)

- **Coriolis ship**: name, manufacturer, mass/hullMass, fuelCapacity, hardpoints[], utilities,
  internal[], baseShieldStrength, armour, price -> `kb/ships/<slug>.md` (source_type: coriolis, tier 0).
- **Coriolis module**: name, mount, class, rating, mass, power, damage/dps, engineering effects -> `kb/outfitting/...`.
- **EDSM system**: name, id64, coords, allegiance, security, population, primaryStar, stations[] -> `kb/locations/<slug>.md`.
- **Spansh bodies**: bodyName, system, subType, signals, atmosphereType, gravity -> `kb/careers/exobiology/...`.
- **Canonn structures**: system, bodyName, lat/long, type -> `kb/ax-thargoid/sites/<slug>.md`.

---

## NEVER / ALWAYS

NEVER: reference EDDB; page a dead-and-pointless mechanic; present AX/Spire/Titan as gone; call
colonisation anything but Trailblazers; `Start-Sleep`/`time.sleep` in the loop (record backoff +
move on); write STATE.toml/seen.json/kb files non-atomically; duplicate existing KB content;
silently resolve conflicts; use qwen3:8b/qwen3-vl during the loop (loop uses qwen3-coder:30b).

ALWAYS: print timestamped `[PHASE] msg` progress; checkpoint `last_completed_phase` after each phase;
dedup-check seen.json before fetching; offload prose >500 tokens to qwen3-coder:30b; write kb pages
via the write_atomic staging pattern; call upsert_changed after writing; commit after the loop; use
"Trailblazers"; tag AX/Spire/Titan `live`; add `[[wikilinks]]` and a `[[trunk]]` backlink to new pages.
