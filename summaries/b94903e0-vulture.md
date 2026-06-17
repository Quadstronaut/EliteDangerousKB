---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/vulture.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T00:00:00+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Vulture — Coriolis summary

Tier-0 structured parse (no LLM). Coriolis key `vulture`, edID 128049309, eddbID 23.

## Key claims (all availability: live)

- **Manufacturer:** Core Dynamics. **Size class 1 = SMALL pad.**
- **Hull mass 230 t**; speed 210 / boost 340; reserve fuel 0.57 t.
- **Base shield 240 MJ** (high for a small hull — a shield-tanky brawler); **base armour 160**;
  **hull hardness 55**; **mass lock 10**; heat capacity 237.
- **Manoeuvrability:** pitch 42 · **roll 110** · yaw 17. **Roll 110 is the highest (nimblest) of any
  ship paged in this KB** (above the Cobra Mk III's 100).
- **Crew seats: 2.**
- **Core internals (standard [4,5,4,3,5,4,3]):** Power Plant 4, Thrusters 5, Frame Shift Drive 4,
  Life Support 3, Power Distributor 5, Sensors 4, Fuel Tank 3. **The class-4 Power Plant is the
  famous bottleneck** — two Large hardpoints plus thrusters and shields strain a class-4 generator.
- **Hardpoints [3,3,0,0,0,0]:** **2 × Large = 2 weapon mounts** + **4 utility**. Two Large hardpoints
  on a size-1 hull is the Vulture's signature: an enormous firepower-to-size ratio.
- **Optional internals:** sizes 5,4,2,1,1,1,1 (**seven regular slots**, top class 5) + **one class-5
  Military slot** (eligible mahr/hr/scb/mrp/gsrp/gmrp/ghrp) + a reserved class-1 Planetary Approach
  Suite.
- **Costs:** hull 4,692,214 CR / retail 4,925,615 CR.
- Bulkheads carry `causres 0` on every grade.

## Queue-guess corrections (recorded)
- Queue guessed "likely NO Military" — **WRONG: the Vulture has one class-5 Military slot.**
- Queue framed "the small PP/PD" as the bottleneck — **the Power Distributor is class 5 (large for the
  hull); the real bottleneck is the class-4 Power Plant.** Two Large mounts confirmed.

## Currency signals / availability
- `availability: live`. Standard Core Dynamics hull, no rank gate (no `requirements` block).

## OBSOLETE: NO
