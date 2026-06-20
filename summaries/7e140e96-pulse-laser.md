---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/pulse_laser.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-20T20:56:25+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Pulse Laser — Coriolis module summary

Tier-0 Coriolis module definition, group `pl` (file `modules/hardpoints/pulse_laser.json`,
6826 bytes). An ARRAY of variants by mount (Fixed/Gimbal/Turret) × class (1–4). Internal symbol
`Hpt_PulseLaser_*`.

## Key claims (parsed directly, no LLM)

- **Damage type: 100% Thermal** (`damagedist {T: 1}`) on every variant → strong vs shields,
  weak vs hull. Falloff begins at **500 m**, max range **3000 m** on all variants.
- The cheap, low-power, efficient **thermal staple** — the baseline primary human-combat weapon.
- Class 1 = Small, 2 = Medium, 3 = Large, 4 = Huge. **Huge has only Fixed + Gimbal** (no Huge turret).
- Per-shot damage and fire interval (`fireint`, seconds) → sustained DPS = damage / fireint:

| Size | Mount | Rating | Dmg/shot | Fire int (s) | DPS | Power (MW) | Thermload | Distdraw | Mass (t) | Cost (CR) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 Small | Fixed | F | 2.05 | 0.26 | 7.9 | 0.39 | 0.33 | 0.30 | 2 | 2,200 |
| 1 Small | Gimbal | G | 1.56 | 0.25 | 6.2 | 0.39 | 0.31 | 0.31 | 2 | 6,600 |
| 1 Small | Turret | G | 1.19 | 0.30 | 4.0 | 0.38 | 0.19 | 0.19 | 2 | 26,000 |
| 2 Medium | Fixed | E | 3.50 | 0.29 | 12.1 | 0.60 | 0.56 | 0.50 | 4 | 17,600 |
| 2 Medium | Gimbal | F | 2.68 | 0.28 | 9.6 | 0.60 | 0.54 | 0.54 | 4 | 35,400 |
| 2 Medium | Turret | F | 2.05 | 0.33 | 6.2 | 0.58 | 0.33 | 0.33 | 4 | 132,800 |
| 3 Large | Fixed | D | 5.98 | 0.33 | 18.1 | 0.90 | 0.96 | 0.86 | 8 | 70,400 |
| 3 Large | Gimbal | E | 4.58 | 0.31 | 14.8 | 0.92 | 0.92 | 0.92 | 8 | 140,600 |
| 3 Large | Turret | F | 3.50 | 0.37 | 9.5 | 0.89 | 0.56 | 0.56 | 8 | 400,400 |
| 4 Huge | Fixed | A | 10.24 | 0.38 | 27.0 | 1.33 | 1.64 | 1.48 | 16 | 177,600 |
| 4 Huge | Gimbal | A | 7.82 | 0.36 | 21.7 | 1.37 | 1.56 | 1.56 | 16 | 877,600 |

- Piercing: 20 (Small) → 35 (Medium) → 52 (Large) → 65 (Huge).
- Pattern: Fixed = highest per-shot damage; Gimbal trades damage for tracking; Turret lowest
  damage but auto-tracks and costs far more. Pulse > Burst > Beam for efficiency (low heat/draw),
  but lower raw DPS than burst/beam.

## Powerplay variant (one-line note)

- A **Pulse Disruptor** special variant exists (`Hpt_PulseLaser_Fixed_Medium_Disruptor`, Medium
  Fixed, dmg 2.8, thermload 1.0) flagged `powerplay: True`, pledge **Felicia Winters**. It adds a
  module-malfunction effect. Acquired through **Powerplay (now Powerplay 2.0)** — note the system
  was reworked, so old PP1 acquisition guides are stale.

## Currency / availability

- **availability: live** — current Coriolis module data; standard purchasable weapon at outfitting.
- **OBSOLETE: NO.**
