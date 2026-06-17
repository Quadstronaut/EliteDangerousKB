---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/ax_multi_cannon_enhanced.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T01:09:03+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Enhanced AX Multi-Cannon (Coriolis axmce) — parsed summary

Coriolis group `axmce`, symbol `Hpt_ATMultiCannon_*` (V2 / Gimbal). All variants `experimental: true`.
`damagedist {X:1, K:1}` = AX + kinetic split (same as base AX MC). Common to every variant:
ammo 2100, range 4000 m, falloff 2000 m, reload 4 s, **shotspeed 4000 m/s** (2.5× the base AX MC's
1600), breachmax 0.5.

## Key differences vs base AX Multi-Cannon
- **Adds GIMBAL (G) mounts** — base line is Fixed + Turret only; Enhanced is Fixed + Gimbal + Turret.
- **2.5× projectile speed** (4000 vs 1600 m/s) — far easier to land at range on strafing Thargoids.
- Classes **Medium (2) + Large (3) only** — **NO Small** mount (corrects the earlier KB guess).
- Pre-engineered reward variants carry G5 **Overcharged + Auto-Loader**.

## Standard variants
| id | Size | Mount | Rating | Dmg | Clip | Power | Thermload | Piercing | Distdraw | Mass | Cost |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4W | 2 Med | Fixed | D | 3.9 | 100 | 0.48 | 0.18 | 17 | 0.11 | 4 | 455,077 |
| 4X | 2 Med | Gimbal | E | 3.7 | 100 | 0.46 | 0.18 | 17 | 0.11 | 4 | 1,197,644 |
| 4Y | 2 Med | Turret | E | 2.0 | 90 | 0.52 | 0.10 | 17 | 0.06 | 4 | 2,193,297 |
| 4Z | 3 Lrg | Fixed | B | 7.3 | 100 | 0.69 | 0.28 | 33 | 0.18 | 8 | 1,360,322 |
| 5A | 3 Lrg | Gimbal | C | 6.3 | 100 | 0.64 | 0.28 | 33 | 0.18 | 8 | 2,390,460 |
| 5B | 3 Lrg | Turret | D | 3.9 | 90 | 0.69 | 0.10 | 33 | 0.06 | 8 | 4,588,709 |

fireint: 0.14 (Med F/G), 0.16 (Med/Lrg Turret), 0.17 (Lrg F/G). integrity 51 (Med) / 64 (Lrg).

## Pre-engineered "AX MC (OC, Auto-Load)" (Gimbal, reward variants)
- **5y** Med Gimbal E: dmg 2.4, power 0.805, cost 1,197,644.
- **5z** Lrg Gimbal C: dmg 4.065, power 1.12, cost 2,390,460.
- Both: preEngineered G5 `Weapon_Overcharged` + experimental `special_auto_loader`;
  `reengineerable:false`, `gradeChangeable:false`, `canApplyExperimental:true`.

## Currency / availability
AX content is **live**. No obsolete claims. source_count 1, verified false.
