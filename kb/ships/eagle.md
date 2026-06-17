---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/eagle.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T03:59:18Z
source_count: 1
verified: false
availability: live
changed_note:
---

# Eagle Mk II

The Eagle Mk II is **Core Dynamics' cheap, ultra-agile small-pad fighter** — the natural "first real
fighter" step up from the free [[ships/sidewinder]]. It is built around one idea: turn. With a
**roll rate of 120 deg/s — the nimblest of any ship paged in this KB** — and the highest pitch rate
in the roster, the Eagle dances around far heavier ships, but it pays for that agility with the
**lowest base armour in the KB** (40) and a shallow class-2 power core. As the second-cheapest hull
paged here, it is the rookie's affordable dogfighter.

## Overview

- **Manufacturer:** Core Dynamics
- **Size class:** 1 (Small landing pad — docks anywhere, including outposts and planetary ports)
- **Role:** Light combat / fighter (dogfighting, cheap bounty hunting, fast interceptor)
- **Rank requirement:** none — credits only (no `requirements` block in the Coriolis data)
- **Hull cost:** 10,947 CR (hull only — the second-cheapest hull in the KB, above only the Sidewinder)
- **Retail cost:** 44,800 CR (with stock modules)
- **Crew seats:** 1

## Hull Stats

Source: Coriolis-data ship definition `eagle` (edID 128049255, eddbID 7).

- **Hull mass:** 50 t (ties the [[ships/viper-mk-iii]]; heavier than the Sidewinder's 25 t and the
  [[ships/adder]]'s 35 t).
- **Top speed:** 240 m/s · **Boost:** 350 m/s
- **Base shield strength:** 60 MJ
- **Base armour:** 40 — the **lowest base armour of any hull in the KB** (under the Sidewinder's 60).
  The Eagle is a glass cannon: it survives by not being hit.
- **Hull hardness:** 28 (low)
- **Heat capacity:** 165 (low)
- **Mass lock factor:** 6
- **Manoeuvrability (deg/s):** pitch **50** · **roll 120** · yaw 18. The roll rate of 120 is the
  **highest (nimblest) of any ship paged in this KB**, exceeding the prior joint record held by the
  [[ships/sidewinder]] and [[ships/vulture]] at 110. Its pitch of 50 is likewise the highest in the
  roster — the Eagle out-turns everything paged here.
- **Reserve fuel:** 0.34 t (tiny — short legs)

## Slot Layout

- **Core internals:** Power Plant **2**, Thrusters **3**, Frame Shift Drive **3**, Life Support **1**,
  Power Distributor **2**, Sensors **2**, Fuel Tank **2**. The class-3 Thrusters on a 50 t hull are
  what drive the class-leading roll and pitch; the class-2 Power Plant and Distributor are the limiting
  factors on weapon and shield loadout.
- **Hardpoints:** 3 × Small (three weapon mounts) — the Eagle's signature triple-small armament, one
  more mount than the Sidewinder's two.
- **Utility mounts:** 1 (room for a single chaff launcher, heat sink, or shield booster — fewer than
  most combat hulls).
- **Optional internals:** sizes 3, 2, 1, 1, 1, 1 (six regular slots, top class-3) plus **one class-2
  Military slot** and a reserved class-1 **Planetary Approach Suite**.
- **Military slots:** one (class 2) — eligible for a Meta-Alloy Hull Reinforcement, Hull/Module
  Reinforcement, Shield Cell Bank or Guardian reinforcement package. Notable on so cheap and small a
  hull.

Bulkheads carry `causres 0` on every grade.

## The rookie small-pad fighter line

- **vs [[ships/sidewinder]]:** the Eagle is the dedicated-fighter step up from the free starter —
  three Small mounts instead of two, a far better roll (120 vs 110) and pitch, plus a Military slot,
  for ~45 k CR. The trade is thinner armour (40 vs 60) and one fewer utility mount.
- **vs [[ships/viper-mk-iii]]:** the Viper Mk III is the faster, tankier small-pad combat starter
  (320/400 speed, 2 Medium + 2 Small mounts, class-3 core and Military slot) for roughly twice the
  retail. The Eagle counters with unmatched agility (roll 120 vs 90) at a fraction of the cost — pick
  the Eagle to out-turn, the Viper to out-run and out-gun.
- **vs [[ships/vulture]]:** the Vulture is the heavy end of the small-pad fighter spectrum — two Large
  hardpoints and a 240 MJ shield — but the Eagle now out-rolls even it (120 vs 110) for a tiny
  fraction of the price. Eagle = featherweight skirmisher; Vulture = small-pad heavyweight.

## Build notes

The Eagle is an agility platform: lean into the turn rate and accept the thin hull. Three gimballed
small weapons (multi-cannons or pulse lasers) plus a small bi-weave shield keep it cheap to rebuy and
hard to track. Use the single utility mount for a chaff launcher to defeat gimballed return fire, and
the class-2 Military slot for a hull or module reinforcement to offset the low base armour. Power and
distributor are the constraints — keep weapon and shield draw inside the class-2 budget or set power
priorities. As with the Sidewinder, the Eagle is cheap enough that its value is in being expendable
while you learn to dogfight.

## Acquisition

Stocked at most shipyards; no rank or permit requirement, credits only. Its low price and small pad
make it available very early in a commander's progression.

[[trunk]]
