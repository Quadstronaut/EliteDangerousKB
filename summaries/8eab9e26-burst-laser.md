---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/burst_laser.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-20T21:21:54+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Burst Laser — Coriolis module data (summary)

Group `ul`, file `modules/hardpoints/burst_laser.json`, internal symbol `Hpt_PulseLaserBurst_*`.
The **middle laser** of the primary trio: fires a short **burst of 3 pulses** per trigger pull,
then a gap. 100% thermal (`damagedist {T:1}`) — strong vs shields, weak vs hull. Range 3000 m,
falloff from 500 m (Huge fixed special 600 m). Standard variants: 11 (Small/Medium/Large
Fixed/Gimbal/Turret + Huge Fixed/Gimbal) — **no Huge turret**, same family shape as Pulse/Beam.

## Burst mechanic (key claims)

- Every standard variant has `burst: 3` (rounds per burst) and `burstrof` (intra-burst rate,
  rounds/sec). **The inter-burst gap is the `fireint` field** — NOT a `burstint` field (the queue
  guessed `burstint`; the data has none, the cycle interval lives in `fireint`).
- **Sustained DPS folds in the gap**: one cycle = (burst−1)/burstrof + fireint seconds, delivering
  burst×damage. So `DPS = damage × burst ÷ ((burst−1)/burstrof + fireint)`. This is NOT damage/fireint.
  (Cross-checked: Small fixed = 1.72×3 ÷ (2/15+0.5) = 8.15, matches EDSY; Huge fixed = 32.26.)
- Computed standard DPS (per mount, S→Huge fixed): F 8.1 / G 6.4 / T 4.2 (S); 13.0 / 10.3 / 6.8 (M);
  20.8 / 16.6 / 11.0 (L); Huge F 32.3 / G 25.9.
- **Mid heat, mid WEP draw** — sits between Pulse (cool) and Beam (hot). Large fixed: heat ~4.6/s,
  WEP ~3.0/s (vs Pulse 0.96/0.86, Beam 7.2/5.1). Trio order on DPS and heat both: Pulse < Burst < Beam.
- Piercing 20 → 65 by size. No ammo (capacitor-limited, like all lasers).

## Special (note only, not a page)

- **Cytoscrambler** (`Cyto`, Archon Delaine `powerplay`): Small fixed scatter burst — burst 8,
  burstrof 20, damage 3.6, jitter 1.7, **piercing 1**, range 1000. A short-range, high-spread
  shield-shredder, acquired via Powerplay 2.0. One-line note only.

availability: live. obsolete: NO. claims: 5+. KEEP.
