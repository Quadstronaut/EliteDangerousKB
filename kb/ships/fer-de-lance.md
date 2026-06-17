---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/fer_de_lance.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T03:11:00+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Fer-de-Lance

The Fer-de-Lance is the **premier medium-class combat ship** by **Zorgon Peterson** — the
classic "glass cannon" of the medium pad. It is the smallest hull in the game to mount a
**Huge (class-4) hardpoint**, backed by a large class-6 Power Distributor for sustained
energy-weapon fire and a high shield for its size. It pays for that firepower with a weak
Frame Shift Drive, a small fuel tank, and shallow optional internals — the Fer-de-Lance is
built to fight in a chosen system, not to roam. Compared with the multirole
[[ships/python]] (three Large hardpoints, deep internals) it concentrates damage into one
big mount and out-turns it.

## Overview

- **Manufacturer:** Zorgon Peterson
- **Size class:** 2 (Medium landing pad — docks at outposts and all larger ports)
- **Role:** Dedicated combat (bounty hunting, PvP, Conflict Zones)
- **Rank requirement:** none — credits only (no `requirements` block in the Coriolis data)
- **Hull cost:** 51,242,363 CR (hull only)
- **Retail cost:** 51,567,040 CR (with stock modules)
- **Crew seats:** 2

## Hull Stats

Source: Coriolis-data ship definition `fer_de_lance` (edID 128049351, eddbID 11).

- **Hull mass:** 250 t
- **Top speed:** 260 m/s · **Boost:** 350 m/s
- **Base shield strength:** 300 MJ (high for a medium hull)
- **Base armour:** 225 · **Hull hardness:** 70 (high — a true combat hull)
- **Heat capacity:** 224 (low — the Fer-de-Lance runs hot; manage with heat sinks)
- **Mass lock factor:** 12
- **Manoeuvrability (deg/s):** pitch 38 · roll 90 · yaw 12
- **Reserve fuel:** 0.67 t

## Slot Layout

- **Core internals:** Power Plant **6**, Thrusters **5**, Frame Shift Drive **4**,
  Life Support **4**, Power Distributor **6**, Sensors **4**, Fuel Tank **3**. The signature
  trade is a class-6 Power Distributor (feeds sustained beam/pulse/multi-cannon fire) paid for
  with a class-4 [[outfitting/frame-shift-drive]] (poor jump range) and a class-3 fuel tank
  (short legs).
- **Hardpoints:** 1 × Huge (class-4) + 4 × Medium (five weapon mounts). The lone Huge slot on
  a medium hull is the Fer-de-Lance's defining feature.
- **Utility mounts:** 6 (generous — room for shield boosters, heat sinks, chaff and point
  defence together).
- **Optional internals:** sizes 5, 4, 4, 2, 1, 1 (six slots) plus a reserved class-1
  **Planetary Approach Suite**. Shallow internals (top slot only class-5) are the cost of the
  combat focus — limited cargo, and shield/utility space is tight.
- **Military slots:** none.

Bulkheads carry `causres 0` on every grade. The low heat capacity makes a
[[outfitting/heat-sink-launcher]] near-mandatory on a Huge energy build.

## Fer-de-Lance vs other medium combat hulls

- **vs [[ships/python]]:** the Python spreads firepower across three Large hardpoints and
  carries far deeper optional internals (ten slots, three class-6) for a multirole/trader
  build. The Fer-de-Lance concentrates damage into one Huge mount, turns harder, and shields
  better, but jumps poorly and carries little. Python = versatile heavy mounts; FDL = focused
  burst and agility.
- **vs [[ships/krait-mk-ii]]:** the Krait Mk II is the multirole medium combatant (three Large
  mounts, an SLF bay, deeper internals); the Fer-de-Lance is the pure duellist with the single
  Huge slot and best-in-class agility for its size.
- **vs [[ships/vulture]]:** the Vulture is the small-pad expression of the same firepower-to-size
  philosophy — two Large hardpoints and the nimblest roll in the KB on a size-1 hull, at a
  fraction of the cost, but power-starved by a class-4 plant and far lower shield. The
  Fer-de-Lance is the medium-pad step up: one Huge mount, a class-6 distributor and much more
  shield, in exchange for a medium pad and a far higher price.

## Build notes

The textbook fit is a Huge fixed or gimballed energy weapon (beam, plasma, or multi-cannon)
with the four Medium mounts as support, a Bi-Weave or engineered prismatic shield, and heat
sinks for the low heat capacity. Engineer the Power Distributor (at [[engineers/the-dweller]])
and weapons (at Tod "The Blaster" McQuinn) to sustain the Huge slot's draw.

## Acquisition

Sold at large stations carrying a shipyard. Check Spansh (`spansh.co.uk/stations`) for the
nearest stock. As a high-value combat hull it is most common around higher-population systems.

[[trunk]]
