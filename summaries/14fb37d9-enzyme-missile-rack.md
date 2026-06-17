---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/enzyme_missile_rack.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T01:20:16+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Enzyme Missile Rack (tbem) — Coriolis Tier-0 summary

Group `tbem`, file `hardpoints/enzyme_missile_rack.json`, symbol `Hpt_CausticMissile_Fixed_Medium`.
The **caustic/enzyme** AX missile — internally a "Caustic Missile". Degrades Thargoid hull over time
via a caustic damage-over-time effect (the headline mechanic; the stat block's `damage` field is only
the small direct-impact value). AX/Thargoid content → `availability: live`.

## Key claims (parsed directly from JSON)

- **Explosive damage class** `damagedist {E:1}`, but the low `damage: 5` reflects only direct impact —
  the weapon's purpose is the **caustic enzyme DoT** that eats Thargoid hull over time (DoT magnitude
  is NOT in the Coriolis stat block; do not invent a number).
- **`experimental: true`**.
- **Class 2 (Medium), Fixed ONLY** — no Turret, no Small, no Large.
- **Base variant** (id xt): rating B, dmg 5, clip 8, ammo 64, reload 5, fireint 2.0, piercing 60,
  shotspeed 750, thermload 1.5, power 1.20, mass 4, integrity 51, cost 480,501.
- **Pre-engineered reward variant** (id 5Z) "**Caust Enzyme (High Cap)**": G5 High Capacity blueprint,
  `reengineerable: false`, `gradeChangeable: false`, `canApplyExperimental: false`, availability **CG**
  (Community Goal reward). Stored stat block lists clip 7 / ammo 40 pre-blueprint.

availability=live, obsolete=NO. claims=5. Tier-0 structured, no LLM.
