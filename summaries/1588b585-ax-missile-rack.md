---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/ax_missile_rack.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T01:09:03+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# AX Missile Rack (Coriolis axmr) — parsed summary

Coriolis group `axmr`, symbol `Hpt_ATDumbfireMissile_*`. All variants `experimental: true`,
`missile: "D"` = **dumbfire only** (no seeking variant in this file — corrects the queue note's
"dumbfire/seeking"). `damagedist {X:1, E:1}` = **AX + explosive** split — the explosive leg of the
AX kinetic/explosive mix (pairs with the kinetic [[outfitting/ax-multi-cannon]]).

Common: piercing 60 (high), falloff **10000 m** (full damage out to 10 km), shotspeed 750 m/s,
fireint 2.0 s, reload 5 s, breachdmg 0.1.

## Standard variants
| id | Size | Mount | Rating | Dmg | Ammo | Clip | Power | Thermload | Distdraw | Mass | Cost |
|---|---|---|---|---|---|---|---|---|---|---|---|
| x4 | 2 Med | Fixed | B | 64 | 64 | 8 | 1.20 | 2.4 | 0.14 | 4 | 540,900 |
| x5 | 2 Med | Turret | B | 50 | 64 | 8 | 1.20 | 1.5 | 0.08 | 4 | 2,022,700 |
| x6 | 3 Lrg | Fixed | A | 64 | 128 | 12 | 1.62 | 3.6 | 0.24 | 8 | 1,352,250 |
| x7 | 3 Lrg | Turret | A | 64 | 128 | 12 | 1.75 | 1.9 | 0.14 | 8 | 4,056,750 |

Mounts Fixed + Turret; classes Medium (2) + Large (3). Fixed Medium and both Large = 64 dmg/missile;
Medium turret trades to 50. integrity 51 (Med) / 64 (Lrg).

## Pre-engineered "AX MRack (HCap+RFire)" (Fixed, reward variants)
- **5w** Med Fixed E: dmg 71.5, ammo 64, clip 8, fireint 3.045, reload 7.85, power 1.20, mass 4.25,
  cost 540,900.
- **5x** Lrg Fixed C: dmg 71.5, ammo 128, clip 12, fireint 3.045, reload 7.85, power 1.62, mass 8.5,
  **cost 0** (reward variant).
- Both: preEngineered G5 `Weapon_HighCapacity` + `Weapon_RapidFire`; `reengineerable:false`,
  `gradeChangeable:false`, `canApplyExperimental:false`.

## Currency / availability
AX content is **live**. No obsolete claims. Enhanced variant `axmre` noted as follow-on.
source_count 1, verified false.
