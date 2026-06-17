---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/nanite_torpedo_pylon.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T01:32:40+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Nanite Torpedo Pylon (ntp) — Coriolis Tier-0 summary

Group `ntp`, file `hardpoints/nanite_torpedo_pylon.json`, symbol `Hpt_ATVentDisruptorPylon_Fixed_*`.
The **seeking** anti-Thargoid torpedo and the LAST open weapon in the AX missile/torpedo family.
AX/Thargoid content → `availability: live`.

## Key claims (parsed directly from JSON)

- **Seeking torpedo** (`missile: "S"`) — distinct from the dumbfire [[outfitting/ax-missile-rack|AX Missile Rack]]
  (`missile: "D"`) and Enhanced variant. A guided torpedo, not a fire-and-forget dumbfire.
- **Explosive damage type, ZERO listed direct damage**: `damagedist {E:1}` but `damage: 0`. The Coriolis
  data records no numeric hull damage — the torpedo's effect is its **nanite payload** (the symbol
  `ATVentDisruptorPylon` = "AX Vent Disruptor"), which disrupts Thargoid caustic-venting behaviour. The
  payload's in-game magnitude is NOT in the Coriolis data and is not invented here.
- **2 variants only, both Fixed mount, rating I, single-shot clip (`clip: 1`):**
  - 4Q — **Medium** (class 2), ammo **64**, power 0.4, mass 3, integrity 50, cost 843,170, symbol `Hpt_ATVentDisruptorPylon_Fixed_Medium`
  - 4R — **Large** (class 3), ammo **125**, power 0.7, mass 5, integrity 80, cost 1,627,419, symbol `Hpt_ATVentDisruptorPylon_Fixed_Large`
- Constants across both: `fireint 2.0`, `reload 3`, `shotspeed 1000`, `thermload 35` (high — torpedo-class heat),
  `breachdmg 0`, `distdraw 0`.
- **No Small, no Turret mount, no pre-engineered reward variants** — Medium + Large, Fixed only.

## Place in the AX weapon family

- Completes the AX missile/torpedo line: dumbfire [[outfitting/ax-missile-rack|AX Missile Rack]] (`axmr`) →
  [[outfitting/ax-missile-rack-enhanced|Enhanced AX Missile Rack]] (`axmre`) → caustic
  [[outfitting/enzyme-missile-rack|Enzyme Missile Rack]] (`tbem`) → **seeking Nanite Torpedo Pylon (`ntp`)**.
- Like the other AX missiles, sourced from the Human Tech Broker / AX war-effort supply (no Guardian unlock).

availability=live, obsolete=NO. claims=5. Tier-0 structured, no LLM.
