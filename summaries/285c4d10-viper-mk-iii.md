---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/viper.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17
source_count: 1
verified: false
availability: live
changed_note:
---

# Viper Mk III (Coriolis ship data)

Tier-0 Coriolis JSON. Top-level key `viper` (= the Mk III; the Mk IV is the separate
`viper_mk_iv` key).

## Identity
- name: Viper (Mk III); edID 128049273, eddbID 22
- manufacturer: Faulcon DeLacy
- class: 1 (SMALL landing pad)
- NO `requirements` block → no rank/permit gate (credits only)
- crew: 1
- hull cost 96,733 CR / retail 142,931 CR — CHEAPER than the Cobra Mk III (prior KB "cheapest"
  at hull 208,372 / retail 349,718); the Viper Mk III is now the cheapest hull in the KB.

## Hull / flight
- hullMass 50 — by far the lightest hull in the KB (next is Cobra Mk III 180 / DBS 170)
- speed 320 / boost 400 — signature high top speed (faster base than Cobra Mk III's 280/400)
- baseShieldStrength 105; baseArmour 70 (low — light combat hull)
- hardness 35 (low); masslock 7
- heatCapacity 195 — low, runs hot (contrast the Diamondbacks' 346/351)
- pitch 35 / roll 90 / yaw 15; reserveFuelCapacity 0.41

## Slots
- standard [3,3,3,2,3,3,2] = PP3 Thr3 FSD3 LS2 PD3 Sen3 FT2 (small core, max class-3; tiny
  class-2 fuel tank = short legs)
- hardpoints [2,2,1,1,0,0] = 2 Medium + 2 Small = 4 weapon mounts + 2 utility
- internal: 3,3,2,1,1,1 = SIX optional internals + ONE class-3 Military slot
  (eligible mahr/hr/scb/mrp/gsrp/gmrp/ghrp) + class-1 PlanetaryApproachSuite.
  The Military slot is notable on so cheap/small a hull — lets it carry an AX/combat reinforcement
  module without spending a cargo optional.
- bulkheads: causres 0 on all grades

## Claims
1. Viper Mk III is a Faulcon DeLacy class-1 (small-pad) ship, no rank gate, hull 96,733 CR
   (cheapest hull in the KB). [availability: live]
2. hullMass 50 (lightest in KB), speed 320/boost 400 (signature speed), low armour 70, runs hot
   (heatCapacity 195). [availability: live]
3. 2 Medium + 2 Small hardpoints + 2 utility; six optionals + one class-3 Military slot. [availability: live]

obsolete: NO
