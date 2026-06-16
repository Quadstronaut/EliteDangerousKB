---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/shield_generator.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T00:54:21+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Shield Generator (standard) — Tier-0 parse

Group `sg`. Optional-internal core defence module. Classes 1–8, ratings E/D/C/B/A —
**except Class 1, which has no B rating** (only E/D/C/A exist for size 1).

Key claims (from Coriolis module data):
- Shield strength is a **multiplier** on the ship's base shield, not a fixed MJ value. The
  module stores `optmul` (multiplier at `optmass`), `minmul` (at/above `maxmass`) and `maxmul`
  (at/below `minmass`); actual MJ = ship base shield × interpolated multiplier for that hull's mass.
- A-rated `optmul` is **1.2** at every class; B 1.1, C 1.0, D 0.9, E 0.8. minmul→maxmul widen
  with rating (A 0.7→1.7, E 0.3→1.3).
- `optmass`/`minmass`/`maxmass` scale by class: C1 25/13/63 t … C8 1800/900/4500 t. A ship
  heavier than `maxmass` cannot fit that class (shield collapses below minmul).
- Base `regen` 1 MJ/s for C1–5, rising 1.3 (C6) / 1.8 (C7) / 2.4 (C8); `brokenregen`
  (recharge while shield is down) 1.6 → 9.6 by class. Same value across all ratings of a class.
- Power draw rises with class and rating: C5A 3.64 MW, C8A 5.6 MW.
- Uniform resistances: explosive +0.5, kinetic +0.4, thermal −0.2; distributor draw 0.6.
- Costs: C5A 5.1M CR, C7A 51.3M CR, C8A 162.6M CR.

availability: live. obsolete: NO.
