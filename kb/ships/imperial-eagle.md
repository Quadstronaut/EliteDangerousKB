---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/imperial_eagle.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T04:12:55Z
source_count: 1
verified: false
availability: live
changed_note:
---

# Imperial Eagle

The Imperial Eagle is **Gutamaya's Imperial refinement of the [[ships/eagle]] Mk II** — the same
small-pad airframe, rebuilt as a faster, better-shielded, harder-hitting skirmisher. Where the base
Eagle is Core Dynamics' bargain dogfighter, the Imperial Eagle trades a little of that raw agility
for a Medium hardpoint, a bigger power plant, a stronger shield and a higher boost speed. The sibling
pairing mirrors the [[ships/viper-mk-iii]]/[[ships/viper-mk-iv]] and the Diamondback Scout/Explorer
split: same chassis, two tuning philosophies.

## Overview

- **Manufacturer:** Gutamaya (an Imperial ship — but, unusually for the marque, **no rank gate**)
- **Size class:** 1 (Small landing pad — docks anywhere, including outposts and planetary ports)
- **Role:** Light combat / fast interceptor (dogfighting, bounty hunting, an upgraded Eagle)
- **Rank requirement:** none — credits only (no `requirements` block in the Coriolis data; the
  Imperial Eagle is one of the few Gutamaya hulls buyable without an Empire rank)
- **Hull cost:** 73,023 CR (hull only)
- **Retail cost:** 110,830 CR (with stock modules)
- **Crew seats:** 1

## Hull Stats

Source: Coriolis-data ship definition `imperial_eagle` (edID 128672138, eddbID 15).

- **Hull mass:** 50 t (ties the base [[ships/eagle]] and the [[ships/viper-mk-iii]]).
- **Top speed:** 300 m/s · **Boost:** 400 m/s — **faster than the base Eagle** (240/350); the boost of
  400 matches the fastest small-pad hulls in the KB ([[ships/cobra-mk-iii]], Viper Mk III).
- **Base shield strength:** 80 MJ — **higher than the base Eagle's 60**.
- **Base armour:** 60 — higher than the base Eagle's 40 (which remains the KB's lowest). The Imperial
  Eagle is still a light hull, but less of a glass cannon than its Core Dynamics cousin.
- **Hull hardness:** 28 (low — same as the base Eagle)
- **Heat capacity:** 163 (low)
- **Mass lock factor:** 6
- **Manoeuvrability (deg/s):** pitch 40 · **roll 100** · yaw 15. Agile, but **short of the base
  Eagle's class-leading pitch 50 / roll 120** — the base Eagle keeps the nimblest-roll record in the
  KB. The Imperial Eagle's roll of 100 sits in the next tier (ties the [[ships/cobra-mk-iii]] and
  [[ships/adder]]).
- **Reserve fuel:** 0.37 t (tiny — short legs)

## Slot Layout

- **Core internals:** Power Plant **3**, Thrusters **3**, Frame Shift Drive **3**, Life Support **1**,
  Power Distributor **2**, Sensors **2**, Fuel Tank **2**. The defining difference from the base Eagle
  is the **class-3 Power Plant** (vs the base Eagle's class-2) — more power headroom to feed the larger
  Medium weapon and the stronger shield. The rest of the core matches the base Eagle.
- **Hardpoints:** 1 × Medium + 2 × Small (three weapon mounts) — the same three-mount count as the
  base Eagle's triple-Small, but with **one mount upgraded to Medium** for a meaningful firepower bump.
- **Utility mounts:** 1 (a single chaff launcher, heat sink, or shield booster — same as the base Eagle).
- **Optional internals:** sizes 3, 2, 1, 1, 1, 1 (six regular slots, top class-3) plus **one class-2
  Military slot** and a reserved class-1 **Planetary Approach Suite** — identical internal layout to
  the base Eagle.
- **Military slots:** one (class 2) — eligible for a Meta-Alloy Hull Reinforcement, Hull/Module
  Reinforcement, Shield Cell Bank or Guardian reinforcement package.

Bulkheads carry `causres 0` on every grade.

## The Eagle pair

- **vs [[ships/eagle]] (Mk II):** same 50 t airframe, two philosophies. The **base Eagle** is the
  cheaper (10,947 vs 73,023 CR hull) pure agility platform — class-leading roll 120 / pitch 50 and
  three Small mounts. The **Imperial Eagle** is the upgraded fighter: faster (300/400 vs 240/350),
  better-shielded (80 vs 60 MJ), tougher (armour 60 vs 40), with a **Medium hardpoint** and a bigger
  class-3 power plant — at the cost of some turn rate (roll 100 vs 120) and ~7× the hull price. Pick the
  base Eagle to out-turn; pick the Imperial Eagle to hit harder and run faster.
- **vs [[ships/viper-mk-iii]]:** the Viper Mk III is the other fast small-pad combat starter — the same
  320/400-class speed and a heavier 2 Medium + 2 Small armament with a class-3 Military slot, for a
  higher price. The Imperial Eagle is the lighter, single-Medium alternative with a stronger shield but
  fewer mounts.
- **vs [[ships/sidewinder]]:** the Imperial Eagle is a serious step up from the free starter — far more
  speed, shield, firepower and a Military slot — but costs ~110 k CR retail against the Sidewinder's
  effectively-free hull.

## Build notes

The Imperial Eagle is the Eagle for commanders who want the agility of the chassis but a little more
punch and survivability. Mount a gimballed Medium weapon (multi-cannon or pulse laser) as the primary
with two Small gimballed weapons in support, a small bi-weave shield, and use the single utility mount
for a chaff launcher. The class-3 Power Plant gives more headroom than the base Eagle, so weapon and
shield draw are less of a constraint — but the Power Distributor is still only class-2, so keep
sustained fire modest. Fit the class-2 Military slot with a hull or module reinforcement to offset the
light armour. Like the base Eagle, it rewards an aggressive, turn-fighting style.

## Acquisition

Stocked at Imperial shipyards (and many others); **no rank or permit requirement** despite the Gutamaya
badge — credits only. Its small pad and modest price make it an accessible early-to-mid upgrade.

[[trunk]]
