---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/module_reinforcement_package.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T21:07:24+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Module Reinforcement Package (Coriolis) — summary

Tier-0 Coriolis module file, group `mrp`, `internal/module_reinforcement_package.json`. Parsed directly.

## Key claims (from structured fields)

- **Optional internal** module that protects *modules* (not hull) from weapons fire that penetrates
  the hull. The third leg of the tank stack: shields → hull (HRP) → modules (MRP).
- **No `power` field → draws no power** (passive, like HRP).
- **Classes 1–5, ratings E and D only** (no A/B/C).
- **`protection`** = fraction of incoming module damage diverted to the MRP's pool: **E = 0.30
  (30%)**, **D = 0.60 (60%)**.
- **`integrity`** = the MRP's damage-capacity pool (how much it can soak before depleting).
- **Trade per the in-game description**: E = "high damage capacity but low absorption" (more
  integrity, 30% absorb, heavier, cheaper); D = "low damage capacity but high absorption" (less
  integrity, 60% absorb, half the mass, ~3× the cost).
- Stacking multiple MRPs raises total module protection but follows diminishing returns toward a cap
  (like resistances) — not unbounded.
- Mass/integrity/cost by class: C1 E 77 HP/2 t/5,000 cr → C5 E 385 HP/32 t/150,000 cr (D = lighter,
  higher absorb, costlier).

## Availability

`availability: live` — current optional-internal module. obsolete=NO.
