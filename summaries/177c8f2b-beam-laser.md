---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/beam_laser.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-20T21:07:38+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Beam Laser — Coriolis summary

Group `bl`, file `modules/hardpoints/beam_laser.json`, symbol `Hpt_BeamLaser_*`. The
**continuous-fire, highest-sustained-DPS thermal laser** — the hot, hungry sibling of the
[[outfitting/pulse-laser]]. Standard primary, no unlock, `availability: live`.

## Key claims (parsed directly — no LLM)

- **100% thermal** (`damagedist {T: 1}`) on every variant → strong vs shields, weak vs hull.
- **Continuous beam**: the `damage` field IS the per-second figure (DPS), not per-shot — there is
  no `fireint`. `thermload` and `distdraw` are likewise per-second. Do NOT divide by a fire interval.
- **Runs hot and hungry**: far higher `thermload` (2.4–10.6) and `distdraw` (WEP draw 1.32–8.99)
  than the Pulse — this heat/power cost is the Beam's whole identity. No ammo (capacitor-limited).
- **Range 3000 m**, falloff from **600 m** (Pulse falls off from 500 m).
- 11 standard variants: **fixed/gimbal/turret × Small/Medium/Large + fixed/gimbal Huge** — there is
  **no Huge turret** beam laser (same family shape as the Pulse).
- **Piercing 18 → 60** by size. Mass 2/4/8/16 t by class 1/2/3/4.

### Standard variants (DPS = `damage`, continuous)

| Size | Mount | Rating | DPS | Power (MW) | Thermload/s | Distdraw/s | Piercing | Mass (t) | Cost (CR) |
|---|---|---|---|---|---|---|---|---|---|
| 1 Small | Fixed | E | 9.8 | 0.62 | 3.5 | 1.94 | 18 | 2 | 37,430 |
| 1 Small | Gimbal | E | 7.66 | 0.60 | 3.6 | 2.11 | 18 | 2 | 74,650 |
| 1 Small | Turret | F | 5.4 | 0.57 | 2.4 | 1.32 | 18 | 2 | 500,000 |
| 2 Medium | Fixed | D | 15.96 | 1.01 | 5.1 | 3.16 | 35 | 4 | 299,520 |
| 2 Medium | Gimbal | D | 12.52 | 1.00 | 5.3 | 3.44 | 35 | 4 | 500,600 |
| 2 Medium | Turret | E | 8.82 | 0.93 | 3.5 | 2.16 | 35 | 4 | 2,099,900 |
| 3 Large | Fixed | C | 25.78 | 1.62 | 7.2 | 5.10 | 50 | 8 | 1,177,600 |
| 3 Large | Gimbal | C | 20.28 | 1.60 | 7.6 | 5.58 | 50 | 8 | 2,396,160 |
| 3 Large | Turret | D | 14.34 | 1.51 | 5.1 | 3.51 | 50 | 8 | 19,399,600 |
| 4 Huge | Fixed | A | 41.38 | 2.61 | 9.9 | 8.19 | 60 | 16 | 2,396,160 |
| 4 Huge | Gimbal | A | 32.68 | 2.57 | 10.6 | 8.99 | 60 | 16 | 8,746,160 |

### Powerplay special (note only — not a page)

- **Retributor** (`Hpt_BeamLaser_Fixed_Small_Heat`, Small fixed, DPS 4.9, thermload 2.7 — lower heat)
  flagged `powerplay`, pledge reward under **Edmund Mahon**. Acquired via **Powerplay 2.0** (PP1
  guides stale). Standard beams need no pledge.

## Availability / obsolescence

availability=**live**, obsolete=**NO**. Current standard weapon. 1 source (Tier-0 Coriolis),
verified:false (single source).
