---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/ax_missile_rack_enhanced.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T01:20:16+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Enhanced AX Missile Rack (axmre) — Coriolis Tier-0 summary

Group `axmre`, file `hardpoints/ax_missile_rack_enhanced.json`, symbol `Hpt_ATDumbfireMissile_*_v2`.
The upgraded (`v2`) version of the base [[outfitting/ax-missile-rack|AX Missile Rack]] (`axmr`). All
variants `experimental: true`. AX/Thargoid content → `availability: live`.

## Key claims (parsed directly from JSON)

- **AX + explosive** damage split `damagedist {X:1, E:1}` — same profile as the base AX Missile Rack.
- **Dumbfire only** (`missile: "D"`) — no seeking variant, same as base.
- **4 standard variants**, all Fixed/Turret, Medium (class 2) + Large (class 3), `experimental: true`:
  - 4S — Medium Fixed, rating **D**, dmg **77**, ammo 64, clip 8, power 1.30, thermload 2.4, distdraw 0.14, cost 681,534
  - 4T — Medium Turret, rating **E**, dmg **64**, ammo 64, clip 8, power 1.30, thermload 1.5, distdraw 0.08, cost 2,666,286
  - 4U — Large Fixed, rating **B**, dmg **77**, ammo 128, clip 12, power 1.72, thermload 3.6, distdraw 0.24, cost 1,703,835
  - 4V — Large Turret, rating **D**, dmg **64**, ammo 128, clip 12, power 1.85, thermload 1.9, distdraw 0.14, cost 5,347,534
- Constants: piercing 60, fireint 2.0, reload 5, **shotspeed 1250**, mass 4 (Med) / 8 (Lrg), integrity 51 (Med) / 64 (Lrg).
- **No pre-engineered reward variants** in this file (the base axmr had two: "AX MRack (HCap+RFire)").

## Diffs vs base AX Missile Rack (the "enhanced")

- **Higher damage**: Fixed 77 (base 64); Medium Turret 64 (base 50); Large Turret 64 (base 64, same).
- **Faster missiles**: shotspeed **1250** vs base **750** (~1.67×) → easier leading, better hit rate.
- **Slightly higher power**: 1.30 MW Medium (base 1.20), 1.72/1.85 MW Large (base 1.62/1.75).
- **Lower nominal ratings** (Fixed Med D vs base B; etc.) — the `v2` trades rating-efficiency for output.
- The enhanced file **omits the `falloff`/range field** the base carried (base falloff 10000 m).

availability=live, obsolete=NO. claims=6. Tier-0 structured, no LLM.
