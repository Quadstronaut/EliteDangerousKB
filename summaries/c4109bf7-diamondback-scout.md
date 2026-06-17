---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/diamondback_scout.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17
source_count: 1
verified: false
availability: live
changed_note:
---

# Diamondback Scout (Coriolis ship data)

Tier-0 Coriolis JSON. Top-level key is `diamondback` (file `diamondback_scout.json`) — note the
key/file mismatch vs the Explorer's `diamondback_explorer`.

## Identity
- name: Diamondback Scout (DBS); edID 128671217, eddbID 6
- manufacturer: Lakon
- class: 1 (SMALL landing pad)
- NO `requirements` block → no rank/permit gate (credits only)
- crew: 1 (single-seat, like the DBX)
- hull cost 463,926 CR / retail 564,329 CR (cheap)

## Hull / flight
- hullMass 170 (lighter than DBX 260)
- speed 280 / boost 380
- baseShieldStrength 120; baseArmour 120 (symmetrical)
- hardness 40 (low); masslock 8
- heatCapacity 346 — very high; 2nd only to the DBX sibling (351) in the KB → confirms the
  Diamondback cool-running family trait
- pitch 42 / roll 100 / yaw 15; reserveFuelCapacity 0.49

## Slots
- standard [4,4,4,2,3,2,4] = PP4 Thr4 FSD4 LS2 PD3 Sen2 FT4 (class-4 FSD = modest range vs the
  DBX's class-5 — the scout is the cheap fighter, the explorer is the ranged one)
- hardpoints [2,2,1,1,0,0,0,0] = 2 Medium + 2 Small = 4 weapon mounts + 4 utility
- internal: 3,3,3,2,1,1 = SIX optional internals (top class-3) + class-1 PlanetaryApproachSuite.
  NO Military slot (contrast the Viper Mk III, which has one).
- bulkheads: causres 0 on all grades

## Claims
1. Diamondback Scout is a Lakon class-1 (small-pad) ship, no rank gate, hull 463,926 CR. [availability: live]
2. hullMass 170, speed 280/boost 380, heatCapacity 346 (cool-running). [availability: live]
3. 2 Medium + 2 Small hardpoints + 4 utility; six optionals (top class-3); NO Military slot. [availability: live]

obsolete: NO
