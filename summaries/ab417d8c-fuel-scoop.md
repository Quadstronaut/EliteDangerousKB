---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/fuel_scoop.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T00:32:57+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Fuel Scoop (Coriolis module def)

Optional internal. Refuels the ship from the corona of a scoopable star (KGBFOAM main-sequence
types) while flying through it in supercruise. **Massless** (0 t) — costs only an internal slot
and power. Group `fs`.

Key claims (from Coriolis JSON):
- Classes **1–8**, ratings **E–A**. No mass on any variant.
- **Scoop rate** (the only stat that matters) rises with class AND rating. A-rated is always the
  fastest in its class. Sample rates: 1A 42 · 3A 176 · 5A 577 · 6A 878 · 7A 1245 · 8A 1680.
- Power draw rises with class/rating (8A draws 1.12 MW); A-rated draws the most.
- Cost scales steeply (5A ≈ 9.07M CR, 6A ≈ 28.76M CR, 8A ≈ 289M CR).
- Pick the largest class your spare optional slot allows, then A-rate it for fastest refuelling.

availability: live. obsolete: NO.
