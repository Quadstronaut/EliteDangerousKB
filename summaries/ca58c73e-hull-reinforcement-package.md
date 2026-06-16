---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/hull_reinforcement_package.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T01:04:59+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Hull Reinforcement Package (Coriolis `hr`)

Optional-internal module, group `hr`, Coriolis path `internal/hull_reinforcement_package.json`.
Adds flat armour HP plus small damage resistances to the ship's hull. The non-Guardian,
non-Meta-Alloy baseline of the "reinforce" family.

## Key claims (parsed directly from Tier-0 JSON)

- **Classes 1–5, ratings E and D only** (no A/B/C). Two variants per class.
- **`hullreinforcement` = flat armour HP added** (not a percentage): C1 80–110 → C5 360–390.
- **D-rating is strictly better HP at half the mass of E**, but ~3× the cost: e.g. C5 E = 360 HP
  / 32 t / 150,000 CR, C5 D = 390 HP / 16 t / 450,000 CR. Fit D when you can afford it, E to
  save credits or when mass is not the constraint.
- **Small flat resistances scale by class:** explosive/kinetic/thermal each +0.5% (C1), +1.0%
  (C2), +1.5% (C3), +2.0% (C4), +2.5% (C5). Identical across the three damage types.
- **`causres` (caustic resistance) is 0** — the standard HRP gives NO caustic protection. That
  is the job of the separate Meta-Alloy Hull Reinforcement Package (`mahr`), relevant to
  Thargoid/AX builds.
- HP and resist are added *before* the ship's own armour resistances, increasing effective hull.

| Class | Rating | Hull HP | Resist (exp/kin/therm) | Mass (t) | Cost (CR) |
|---|---|---|---|---|---|
| 1 | E | 80 | +0.5% | 2 | 5,000 |
| 1 | D | 110 | +0.5% | 1 | 15,000 |
| 2 | E | 150 | +1.0% | 4 | 12,000 |
| 2 | D | 190 | +1.0% | 2 | 36,000 |
| 3 | E | 230 | +1.5% | 8 | 28,000 |
| 3 | D | 260 | +1.5% | 4 | 84,000 |
| 4 | E | 300 | +2.0% | 16 | 65,000 |
| 4 | D | 330 | +2.0% | 8 | 195,000 |
| 5 | E | 360 | +2.5% | 32 | 150,000 |
| 5 | D | 390 | +2.5% | 16 | 450,000 |

availability: live. obsolete: NO. Destination: new page kb/outfitting/hull-reinforcement.md;
completes the defence trio with shield-generator.md + shield-booster.md.
