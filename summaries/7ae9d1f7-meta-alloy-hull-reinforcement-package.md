---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/meta_alloy_hull_reinforcement_package.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T21:07:24+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Meta-Alloy Hull Reinforcement Package (Coriolis) — summary

Tier-0 Coriolis module file, group `mahr`, `internal/meta_alloy_hull_reinforcement_package.json`.
Parsed directly. Destination: MERGE H2 into `kb/outfitting/hull-reinforcement.md` (page already
points here for caustic resistance).

## Key claims (from structured fields)

- **Optional internal**, classes 1–5, ratings **E and D only** (no power field → passive, no draw).
- **`hullreinforcement`** (flat armour HP): C1 72/99 → C5 324/351 (E/D). **Slightly less raw HP than
  the standard HRP** (which is C1 80/110 → C5 360/390).
- **`explres` / `kinres` / `thermres` = 0** — gives **NO conventional resistances** (unlike standard
  HRP's +0.5%/class exp/kin/therm).
- **`causres` = 0.03 (3%) FLAT** across every class and rating — this is the **only HRP that grants
  caustic resistance**. Confirms the cross-reference already in hull-reinforcement.md.
- **Mass**: C1 both 2 t; from C2 up, D is half the mass of E (C5 E 32 t / D 16 t).
- **Use case**: AX/Thargoid builds where caustic damage (caustic missiles, caustic clouds,
  proximity to Thargoid wreckage / Titan interiors) eats hull. Trades conventional resists + a
  little raw HP for caustic protection.

## Availability

`availability: live` — current AX-relevant module. AX/Spire/Titan content remains accessible. obsolete=NO.
