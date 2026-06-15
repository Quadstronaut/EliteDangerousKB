# Loop 3 journal

Mode: search. Target: EDSM `stations/market` for Farseer Inc, Deciat (tier 0).

## Findings

- Farseer Inc (marketId 128676487, station id 10) market is **sell-only**: every commodity
  has `buyPrice 0` / `stock 0`. No commodity supply for players.
- **Meta-Alloys** at Farseer Inc: `demand 0, stock 0` → not buyable and not an active sell
  target. The Farseer unlock requires *delivering* Meta-Alloys sourced elsewhere.
- Corroborated station identity via matching system id64 `6681123623626`.

## Pages updated

- `kb/locations/deciat.md` — added "Station Services — Farseer Inc market"; `source_count` 1→2,
  `verified` false→true.
- `kb/engineers/felicity-farseer.md` — corrected stale "Coles Point" reference to the
  loop-2-verified **Witch Head Science Centre** ([[locations/hip-23759]]); added
  [[locations/deciat]] wikilink; noted Farseer Inc market is sell-only; `source_count` 3→4.

## VERIFY (local council)

- `deciat` — verdict=**verified**, confidence=0.67, escalate=false.
- `felicity-farseer` — verdict=**verified**, confidence=0.95, escalate=false.
- Ollama hiccup: `qwen3-coder:30b` returned HTTP 500 on the first claim's vote; the council
  degraded gracefully (qwen3:8b supported) and still reached a supported verdict. No escalation.

## Discards

None.
