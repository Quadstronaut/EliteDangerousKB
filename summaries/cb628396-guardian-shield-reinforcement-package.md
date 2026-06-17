---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/guardian_shield_reinforcement_package.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T00:43:20+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Guardian Shield Reinforcement Package — Tier-0 Coriolis extract

Group `gsrp`, optional internal, **classes 1–5**, ratings **E and D only**. Guardian module
(Guardian Technology Broker unlock) — **powered**. Adds a **flat MJ amount** (`shieldaddition`)
to total shield strength; `integrity` is a constant **36** across the line. Completes the Guardian
defensive trio: Guardian Hull Reinforcement (`ghrp`) + Guardian Module Reinforcement (`gmrp`) +
**Guardian Shield Reinforcement (`gsrp`)**. The shield-layer analogue of the Hull Reinforcement
Package (flat HP). `availability: live` — Guardian content is current, accessible outfitting.

Key claims (all from the Tier-0 module file):
- **Flat shield boost**, not a multiplier. D rating > E rating in `shieldaddition`, at half the mass,
  for more power and ~3× the cost — same E/D trade pattern as standard HRP/MRP.
- C1 E adds **44 MJ** → C5 D adds **215 MJ**.
- Powered: C1 E **0.35 MW** → C5 D **1.26 MW**.

| Class | Rating | Shield add (MJ) | Power (MW) | Mass (t) | Cost (CR) |
|---|---|---|---|---|---|
| 1 | E | 44 | 0.35 | 2 | 10,000 |
| 1 | D | 61 | 0.46 | 1 | 30,000 |
| 2 | E | 83 | 0.56 | 4 | 24,000 |
| 2 | D | 105 | 0.67 | 2 | 72,000 |
| 3 | E | 127 | 0.74 | 8 | 57,600 |
| 3 | D | 143 | 0.84 | 4 | 172,800 |
| 4 | E | 165 | 0.95 | 16 | 138,240 |
| 4 | D | 182 | 1.05 | 8 | 414,720 |
| 5 | E | 198 | 1.16 | 32 | 331,778 |
| 5 | D | 215 | 1.26 | 16 | 995,330 |

Entities: Guardian Shield Reinforcement Package, Guardian Technology Broker, shield strength (MJ).
Currency signals: classes 1–5, E/D ratings, powered — matches current live module roster.
OBSOLETE: NO. Availability per claim: live.
