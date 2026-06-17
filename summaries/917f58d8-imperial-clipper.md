---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/imperial_clipper.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T04:39:15Z
source_count: 1
verified: false
availability: live
changed_note: null
---

# Imperial Clipper (Coriolis Tier-0 ship data)

Structured Coriolis ship JSON, parsed directly (no LLM). Key `imperial_clipper`,
file `ships/imperial_clipper.json` (resolved first try, 3220 bytes, no 404).

## Identity
- **Name:** Imperial Clipper · **Manufacturer:** Gutamaya · **edID** 128049315 · **eddbID** 13
- **Size class:** 3 (LARGE landing pad — its signature quirk: large-pad-only despite a mid-size feel)
- **Rank gate:** `empireRank 7` = **BARON** (between the [[ships/imperial-courier]]'s Master/3 and
  the [[ships/imperial-cutter]]'s Duke/12)
- **Hull cost:** 21,116,895 CR · **Retail:** 22,295,860 CR

## Key claims (current truth)
- **Fastest large-pad ship in the KB.** speed **300** / boost **380** — the highest of any
  class-3 hull paged (next-best large-pad boost is the [[ships/imperial-cutter]]'s 320; the
  rest — Anaconda 240, Corvette 260, Type-10 219, Type-9 200, Panther 250 — are far slower).
- **Fast, elegant multirole** that extends the Gutamaya/Imperial line beyond the small-pad pair
  ([[ships/imperial-eagle]] + [[ships/imperial-courier]]) up to a large-pad flagship class.
- Hardpoints **[3,3,2,2,0,0,0,0] = 2 Large + 2 Medium = 4 weapon mounts + 4 utility** —
  **NO Small mounts** (all medium-or-bigger, the Clipper's signature armament shape).
- Requires an **Empire rank (Baron)**, unlike the no-gate [[ships/imperial-eagle]] but like the
  rank-gated Courier/Cutter.

## Stats
- speed 300 / boost 380 · hullMass 400 · masslock 12 · crew 2
- baseShield 180 · baseArmour 270 · hardness 60 · heatCapacity 304
- pitch 40 / roll 80 / yaw 18 · reserveFuelCapacity 0.74
- Core standard **[6,6,5,5,6,5,4]**: PP6 Thr6 FSD5 LS5 PD6 Sen5 FT4
- Internals **[7,6,4,4,3,3,2,2,1, PAS-c1]** = NINE regular (top class-7) + class-1 Planetary
  Approach Suite. **NO Military slot.**
- Bulkheads `causres 0` on every grade.

## Availability
- **availability: live** — current ship, buyable now (with Empire Baron rank). Not obsolete.

## Obsolete? NO.
