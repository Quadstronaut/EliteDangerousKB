# Shared Contracts — ED Knowledge Engine + COVAS

> **Single source of truth for all four implementation plans (A/B/C/D).** Every plan MUST use these exact names, signatures, paths, and schemas. If a plan needs to change a contract, change it HERE first and note it. This doc prevents cross-plan type drift.

**Spec:** `docs/superpowers/specs/2026-06-01-ed-knowledge-engine-covas-copilot-design.md`

---

## Runtime & conventions

- **Language:** Python 3.11+ in a repo-local venv at `.venv/`. PowerShell launchers/daemon are Windows-native.
- **Tests:** `pytest`. Test files mirror source under `tests/` (e.g. `copilot/retriever.py` → `tests/test_retriever.py`).
- **Paths:** repo root = the directory containing `config.toml`, resolved dynamically by `copilot/paths.py::repo_root()`. **The repo is clone-anywhere portable — never hardcode an absolute machine path in any tracked file.** All Python uses `pathlib.Path`; never hardcode separators. Resolve paths relative to repo root via `repo_root()`; PowerShell uses `$PSScriptRoot`; `.mcp.json` uses `${CLAUDE_PROJECT_DIR:-.}`.
- **Encoding:** all file I/O is UTF-8, newline `\n`. JSON via stdlib `json`. TOML read via `tomllib` (stdlib 3.11+), write via `tomli_w`.
- **Numerics:** `numpy` only for vectors. No faiss/chroma/sqlite-vec in v1 (see spec §E; revisit > 100k chunks).
- **Ollama:** local at `http://localhost:11434`. Models: chat `qwen3:8b`, embed `bge-m3`, vision `qwen3-vl:8b`, loop `qwen3-coder:30b`.

---

## Directory layout (created by Plan A, step 1)

```
EliteDangerousKB/
├── config.toml              STATE.toml            .gitignore
├── launch-copilot.ps1       wrapper.ps1           ed-research-prompt.md
├── cmdr/duvrazh.md
├── kb/  (trunk.md, ships/, engineers/, outfitting/, mechanics/, locations/,
│        careers/, powerplay/, colonisation/, community-goals/, ax-thargoid/, entities/)
├── sources/  summaries/  live/  queue/  journal/
├── indexes/   (manifest.json, data-sources.json)
├── embeddings/  (vectors.npy, chunk_ids.json)
├── copilot/
│   ├── __init__.py   paths.py     atomic.py     models.py
│   ├── ollama_client.py           chunker.py    index.py
│   ├── retriever.py               assemble.py   repl.py
│   ├── profile.py                 data_discovery.py   vision_ingest.py
│   └── mcp_server.py
├── tests/
└── .mcp.json
```

---

## config.toml (canonical schema — Plan A creates it)

```toml
[ollama]
base_url   = "http://localhost:11434"
chat_model = "qwen3:8b"
embed_model = "bge-m3"
vision_model = "qwen3-vl:8b"
loop_model = "qwen3-coder:30b"
keep_alive = "5m"

[retrieval]
top_k = 8
tau = 0.55              # cosine-similarity floor; max_score < tau ⇒ refuse (spec §B)
embed_dim = 1024
chunk_min_tokens = 128
chunk_max_tokens = 512
chunk_overlap = 0.15
# Hybrid retrieval (2026-06-15). fusion="dense" is the kill switch / shipped default
# (rrf regresses MRR on the current tiny corpus); "rrf" fuses BM25+dense. Grounding
# always uses dense cosine vs tau regardless of this value.
fusion = "dense"        # "rrf" | "dense"
rrf_k = 60
candidate_k = 32
rerank = "off"          # "off" | "llm" | "cross_encoder"

[copilot]
mode = "verified_only"  # "verified_only" | "include_unverified"
forced_citation = true
max_regen = 1
claim_grounding_check = true   # cited claim must share content with its chunk (anti-fabrication)
multihop = false               # multi-hop decomposition seam (scaffold; default off = single retrieve)

[paths]
kb = "kb"
embeddings = "embeddings"
indexes = "indexes"
cmdr_profile = "cmdr/duvrazh.md"

[loop]
verification_tier = 1               # 1=capture, 2=consensus, 3=currency-purge
git_commit_every_loop = true
deep_analysis_after_empty_loops = 5

# Local council-v2-style fact verification (verify.py). Cloud escalation is manual.
[verify]
enabled = true
local_models = ["qwen3-coder:30b", "qwen3:8b"]
escalate_threshold = 0.66
min_sources_for_consensus = 2

# Web-acquisition layer (acquire.py + ssrf.py). allow_any/allow_private are honored
# True ONLY when explicitly set true; allowlist defaults to acquire_sources roster.
[acquire]
user_agent   = "EliteDangerousKB-research/0.1 (+local; polite)"
timeout      = 30.0
min_interval = 1.0
jitter       = 0.5
max_attempts = 3
max_bytes    = 5000000
render       = false
allow_any    = false
allow_private = false
allowed_ports = [80, 443]
allowlist = ["edsm.net", "spansh.co.uk", "inara.cz", "raw.githubusercontent.com",
             "api.canonn.tech", "elite-dangerous.fandom.com", "edsy.org",
             "coriolis.io", "forums.frontier.co.uk"]
```

Load via `copilot/paths.py::load_config() -> dict`.

---

## STATE.toml (canonical schema — Plan A creates it, Plan D drives it)

```toml
loop_number = 0
last_completed_phase = "none"   # none|triage|search|summarize|synthesize|verify|index|commit
mode = "search"                 # search|deep-analysis
consecutive_empty_loops = 0
halt = false
updated_at = ""                 # ISO 8601; set by writer
```

Read/write via `copilot/atomic.py` helpers (below). Never write STATE.toml non-atomically.

---

## copilot/models.py (dataclasses — Plan A defines, all plans import)

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Chunk:
    chunk_id: str            # = sha256((kb_path + "::" + heading_path).encode()).hexdigest()[:16]
    text: str                # clean embeddable text: breadcrumb prepended; frontmatter/wikilinks/URLs stripped
    kb_path: str             # e.g. "kb/engineers/felicity-farseer.md"
    heading_path: str        # e.g. "Felicity Farseer > Unlock"
    source_url: str | None
    source_tier: int         # 0..3
    source_count: int
    verified: bool
    availability: str        # "live" | "seasonal" | "changed"
    changed_note: str | None
    score: float = 0.0       # cosine similarity; set at retrieval time (copy via dataclasses.replace)

@dataclass
class RetrievalResult:
    query: str
    chunks: list[Chunk]
    max_score: float
    grounded: bool           # max_score >= config.retrieval.tau

@dataclass
class ProfileFact:
    key: str                 # e.g. "rank.combat", "ship.cutter.owned", "balance_cr"
    value: str
    origin: str              # "game-state-json"|"journal"|"screenshot"|"3rd-party"|"manual"
    freshness: str           # ISO date or "unknown"
    verified: bool           # True from logs/game-state; False from manual/vision

@dataclass
class CmdrState:
    name: str
    ranks: dict[str, str] = field(default_factory=dict)   # {"combat":"Expert",...}
    balance_cr: int | None = None
    assets: dict = field(default_factory=dict)            # {"carriers":[...], "ships":[...]}
    goals: list[str] = field(default_factory=list)
    facts: list[ProfileFact] = field(default_factory=list)
```

**ORIGIN_PRIORITY** (highest trust first), defined in `copilot/profile.py`:
```python
ORIGIN_PRIORITY = ["game-state-json", "journal", "screenshot", "3rd-party", "manual"]
```

---

## Function signatures (exact — do not rename across plans)

### copilot/paths.py  (Plan A)
```python
def repo_root() -> Path
def load_config() -> dict                      # parsed config.toml
def kb_dir() -> Path
def embeddings_dir() -> Path
def indexes_dir() -> Path
```

### copilot/atomic.py  (Plan A)
```python
def write_atomic(path: Path, data: str) -> None          # tmp → flush → fsync → os.replace
def write_json_atomic(path: Path, obj) -> None
def read_state() -> dict                                  # STATE.toml
def write_state(state: dict) -> None                      # atomic; stamps updated_at
```

### copilot/ollama_client.py  (Plan A)
```python
def embed(texts: list[str]) -> "np.ndarray"   # shape (len(texts), 1024), float32, L2-normalized; POST /api/embed
def chat_stream(messages: list[dict], model: str | None = None) -> "Iterator[str]"
                                              # POST /api/chat stream=true; yields text deltas with <think>…</think> removed
def vision(image_path: str, prompt: str) -> str   # qwen3-vl:8b; POST /api/chat with images
class OllamaUnavailable(RuntimeError): ...    # raised when localhost:11434 unreachable
```

### copilot/chunker.py  (Plan A)
```python
def chunk_page(path: Path) -> list[Chunk]
    # parse markdown; split on H2/H3; merge/window to 128–512 tokens, 15% overlap;
    # prepend "PageTitle > Heading" breadcrumb to .text; strip YAML frontmatter,
    # [[wikilinks]] (keep alias text), and raw URLs from .text;
    # resolve metadata: page frontmatter defaults + inline `<!-- tier:N src:X -->` overrides;
    # compute chunk_id.
def clean_for_embedding(markdown: str) -> str   # the strip/flatten step (unit-tested directly)
```

### copilot/index.py  (Plan A; Plan D calls upsert)
```python
def build_index(kb_dir: Path) -> int                       # full rebuild; returns chunk count
def upsert_changed(kb_dir: Path) -> dict                   # incremental by content_hash; returns {"added":n,"removed":n,"unchanged":n}
def search(query_vec: "np.ndarray", top_k: int) -> list[tuple[str, float]]   # [(chunk_id, cosine)], sorted desc
def load_manifest() -> dict                                # {chunk_id: {content_hash, kb_path, heading_path, payload}}
def chunk_by_id(chunk_id: str) -> Chunk | None
```
- `embeddings/vectors.npy`: (N, 1024) float32, L2-normalized, row order = `embeddings/chunk_ids.json`.
- `indexes/manifest.json`: `{chunk_id: {"content_hash": str, "kb_path": str, "heading_path": str, "payload": {…Chunk fields except text/score…}}}`.
- content_hash = sha256 of the chunk's raw markdown section.

### copilot/retriever.py  (Plan A; Plans C/D import)
```python
def retrieve(query: str, *, top_k: int | None = None, filters: dict | None = None) -> RetrievalResult
    # embed query → index.search → hydrate Chunks (with .score) → apply filters
    # (e.g. {"verified": True} in verified_only mode) → grounded = max_score >= tau.
    # PURE: no prompt assembly, no profile injection.
```

### copilot/assemble.py  (Plan A)
```python
def build_messages(query: str, result: RetrievalResult, state: CmdrState | None) -> list[dict]
    # system prompt: grounding rules + forced-citation grammar + refusal instruction;
    # profile block (manual facts labeled "(manual, unverified)"); retrieved chunks each
    # prefixed "[<chunk_id>] <text>"; then the user query.
def validate_answer(answer: str, result: RetrievalResult) -> tuple[bool, str]
    # (ok, reason): every factual sentence carries a [chunk_id]; every cited id ∈ result.chunks.
SYSTEM_PROMPT: str   # module constant
```

### copilot/repl.py  (Plan A)
```python
def answer(query: str, state: CmdrState | None) -> str
    # orchestrates: retrieve → if not grounded: REFUSAL → build_messages → chat_stream →
    # validate_answer → if invalid and regen<max_regen: one regen → else REFUSAL.
def main() -> None   # interactive loop; streams to stdout; strips <think>; prints citations.
REFUSAL: str         # "I don't have a verified source for that." (module constant)
```

### copilot/profile.py  (Plan A defines interface + manual source; Plan B adds sources)
```python
from typing import Protocol
class ProfileSource(Protocol):
    @property
    def origin(self) -> str: ...
    def get_facts(self) -> list[ProfileFact]: ...

class ManualProfile:        # Plan A — reads cmdr/duvrazh.md frontmatter+body
    origin = "manual"
    def get_facts(self) -> list[ProfileFact]: ...

def merge_state(sources: list[ProfileSource]) -> CmdrState
    # per fact key, highest ORIGIN_PRIORITY wins; assembles ranks/balance/assets/goals.
def load_cmdr_state() -> CmdrState   # default: discovers available sources, merges.
```

### copilot/data_discovery.py  (Plan B)
```python
def discover_data_sources() -> list[dict]   # scans %USERPROFILE%,Documents,%LOCALAPPDATA%,%APPDATA%,G:\
                                         # writes indexes/data-sources.json (a JSON array of
                                         # {path,type,last_modified,ingest_status}); returns that list
def saved_games_dir() -> Path | None     # %USERPROFILE%\Saved Games\Frontier Developments\Elite Dangerous
```

### copilot/profile_sources.py  (Plan B — NEW file, keeps Plan A's profile.py stable)
```python
class GameStateSource:  origin = "game-state-json"  # Status/Cargo/ShipLocker/FleetCarrier/… JSON
class JournalSource:    origin = "journal"          # Journal.*.log one-shot backfill parse
class ThirdPartySource: origin = "3rd-party"        # EDMC/EDDiscovery/EDEngineer exports if present
def parse_journal(path: Path) -> list[ProfileFact]
def parse_game_state(dir: Path) -> list[ProfileFact]
def available_sources() -> list[ProfileSource]      # those whose data exists on this machine
```
**One sanctioned edit to Plan A's `profile.py`:** `load_cmdr_state()` tries `import copilot.profile_sources` and, if present, prepends `profile_sources.available_sources()` to the source list before `merge_state`. Wrapped in try/except ImportError so Plan A stands alone. This is the ONLY cross-plan file edit; Plan C touches no Plan-A/Plan-B file (only adds `mcp_server.py` + `.mcp.json`).

### copilot/vision_ingest.py  (Plan B)
```python
def ingest_screenshot(image_path: str) -> list[ProfileFact]   # via ollama_client.vision; origin="screenshot"
```

### copilot/mcp_server.py  (Plan C)
```python
# FastMCP server over stdio. Tools:
#   ed_kb_search(query: str, top_k: int = 8) -> list[dict]   # serialized Chunks (retriever.retrieve)
#   ed_kb_answer(query: str) -> dict                          # {answer, citations, grounded}
#   ed_cmdr_state() -> dict                                   # profile.load_cmdr_state()
# Registered in .mcp.json. Imports retriever/assemble/profile — NO retrieval logic re-implemented.
```

---

## Retrieval / verification / acquisition modules (2026-06-15 — council slice)

These shipped after the original A–D plans, via four council-v2 reviews. Signatures
are stable contracts; grounding/trust invariants below are load-bearing.

### copilot/sparse.py — BM25 sparse retrieval (zero new deps)
```python
def tokenize(text: str) -> list[str]                                   # lowercase, punctuation-split; same at build & query
def build_from_corpus(corpus: dict[str, str]) -> SparseIndex           # in-memory BM25+; guards avgdl==0 (no ZeroDivisionError)
def search_index(idx: SparseIndex, query: str, top_k: int) -> list[tuple[str, float]]   # top_k<=0 -> []
def persist(corpus: dict[str, str]) -> None                            # writes embeddings/sparse_index.json; CALL INSIDE index lock
def load_ids() -> list[str]                                            # ids the persisted sparse index knows; never raises
def search(query: str, top_k: int) -> list[tuple[str, float]]          # load+query; [] if no artifact (degrade-to-dense)
```

### copilot/fusion.py — Reciprocal Rank Fusion
```python
def rrf_fuse(dense, sparse, *, k: int = 60, top_k: int | None = None) -> list[tuple[str, float]]   # top_k<=0 -> []
# rerank(query, candidate_ids, *, top_m) is INTENTIONALLY ABSENT while [retrieval].rerank == "off".
```

### copilot/ssrf.py — the single SSRF chokepoint (security-critical)
```python
class SSRFError(ValueError): reason: str   # scheme|no_host|literal_ip_blocked|resolved_ip_blocked|not_allowlisted|resolve_failed|port_blocked
@dataclass(frozen=True)
class GuardConfig: allowlist; allow_any=False; allowed_ports=frozenset({80,443}); allow_private=False; resolver
def is_ip_blocked(ip: str) -> bool                       # private/loopback/link-local/reserved/metadata; fail-closed
def host_is_allowlisted(host, allowlist) -> bool         # exact-or-subdomain suffix; IP literal never allowlisted
def assert_url_safe(url: str, cfg: GuardConfig) -> str   # the ONE guard; checks RESOLVED ip, one hop. allow_*=True only via `is True`.
```

### copilot/acquire.py — hardened fetch primitive (uses ssrf on every hop)
```python
@dataclass(frozen=True)
class FetchResult: url; status; content_type; text(SANITIZED); raw_sha256(pre-sanitize); rendered; redirect_chain   # NO 'verified' field
def load_acquire_config(cfg: dict | None = None) -> AcquireConfig      # secure defaults; allow_*=False unless `is True`
class Fetcher:                                                         # client follow_redirects=False; manual per-hop guard
    def fetch(self, url: str) -> FetchResult                          # retry (SSRFError terminal); streaming body cap; sanitize on return
    def render(self, url: str) -> FetchResult                        # optional Playwright behind guard; PlaywrightUnavailable if absent
```

### copilot/acquire_sources.py — declarative ED source roster
```python
ED_SOURCES: list[EDSource]                       # 9 sources, tiers 0..3, robots/ToS notes; Reddit excluded (Tier-3 only)
def default_allowlist() -> list[str]             # union of all source domains
def source_for_url(url: str) -> EDSource | None  # same host-suffix rule as the SSRF allowlist
```

### copilot/multihop.py — multi-hop decomposition seam (deferred scaffold)
```python
MULTIHOP_ENABLED: bool = False
def decompose(query: str) -> list[str]           # pure; [query] for single-hop; >=2 sub-queries for explicit multi-hop shapes
```

### copilot/verify.py — local council-v2 fact verification
```python
def verify_claim(claim: str, sources: list[str], *, models=None) -> dict   # sources sanitized+fenced; 'verified' needs >= min_sources
def needs_escalation(result: dict) -> bool                                  # low confidence -> escalate to cloud council (manual)
```

### Prior-session modules (also load-bearing, pre-dating this slice)
`copilot/locking.py` (`file_lock` — OS byte-range lock), `copilot/sanitize.py`
(`sanitize_context_text`/`make_nonce`/`fence`), `copilot/eval.py`
(`load_golden`/`retrieval_metrics`/`refusal_calibration`, `python -m copilot.eval`),
`copilot/query_expand.py` (`expand_query`).

### Hybrid retrieval invariants (do not break)
- `index.build_index`/`upsert_changed` build a `{chunk_id: text}` corpus and persist the
  sparse index **inside `_save_index`'s `file_lock`** — dense + sparse are one atomic group.
- `retriever.retrieve` under `fusion="rrf"`: dense (wide `candidate_k`) + `sparse.search`
  (LITERAL query, not the expanded form) → `rrf_fuse` → hydrate in fused order. Under
  `fusion="dense"`: exact legacy path, sparse never called.
- **Grounding/refusal ALWAYS uses the post-filter dense cosine vs τ — never an RRF/BM25
  score.** A high BM25 score cannot launder a false positive past the gate.

---

## chunk_id scheme (one definition, used everywhere)
```python
import hashlib
def make_chunk_id(kb_path: str, heading_path: str) -> str:
    return hashlib.sha256(f"{kb_path}::{heading_path}".encode("utf-8")).hexdigest()[:16]
```
Lives in `copilot/chunker.py`; imported by `index.py`.

---

## Anti-hallucination gate (spec §B) — where each piece lives
- **τ floor:** `retriever.retrieve` sets `grounded` (post-filter dense cosine, never RRF); `repl.answer` refuses if `not grounded`.
- **Forced citation + cited-id-exists:** `assemble.validate_answer`; `repl.answer` regenerates once then refuses.
- **Claim-grounding:** `[copilot].claim_grounding_check` — a cited claim must share content with its chunk, so a confident-wrong answer with a real `[id]` is rejected (anti-fabrication).
- **Multi-hop union:** when `[copilot].multihop=true`, `repl.answer` unions per-sub-query results and runs the SAME `validate_answer` over the union — no second/weakened gate.
- **Acquisition trust boundary:** fetched text is `sanitize.sanitize_context_text`-cleaned before any LLM/KB write; `FetchResult` has no `verified` field; ingested chunks are never auto-verified.
- **Refusal-calibration tests:** `tests/test_gate.py` — empty retrieval AND non-empty-but-below-τ both refuse.

## Idempotency & output (spec §J) — Plan D
- All state writes via `atomic.write_*`. Loop checkpoints `last_completed_phase` after each phase.
- On launch, `wrapper.ps1` reads STATE.toml and resumes at the next phase; content-hash skips (`seen.json`, manifest) make re-runs safe.
- Verbose: every action printed timestamped and `Tee`'d to `journal/daemon.log`; no-new-sources ⇒ switch to deep-analysis (never sleep).

## seen.json (Plan D)  — dedup index
```json
{ "url_sha256": {"first_seen":"<ISO>","content_sha256":"…"} }
```
