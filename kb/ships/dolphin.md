---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/dolphin.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T05:12:08+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Dolphin

The Dolphin is **Saud Kruger's small-pad luxury passenger liner** — the entry rung of the
Saud Kruger trio (Dolphin → [[ships/orca]] → [[ships/beluga-liner]]) and the first ship from that
manufacturer in the KB. It is purpose-built to carry people, not cargo or guns: it can fit
**Luxury-class passenger cabins** (the Saud Kruger signature), packs nine optional internal slots
to fill with them, and has only token armament. A class-5 thruster and class-4 fuel tank on a light
140 t hull give it surprisingly good pace and range for a budget liner, which is why it is the
classic first ship for sightseeing and luxury passenger missions.

## Overview

- **Manufacturer:** Saud Kruger
- **Size class:** 1 (Small landing pad — docks anywhere, including outposts)
- **Role:** Passenger transport (tourism, luxury and economy passenger missions)
- **Rank requirement:** none — credits only (no `federationRank`/`empireRank` requirement). The
  Coriolis data carries a `requirements.horizons: true` flag (a game-version tag, not a gate).
- **Hull cost:** 1,117,906 CR (hull only)
- **Retail cost:** 1,337,323 CR (with stock modules)
- **Crew seats:** 1

## Hull Stats

Source: Coriolis-data ship definition `dolphin` (edID 128049291, eddbID 31).

- **Hull mass:** 140 t
- **Top speed:** 250 m/s · **Boost:** 350 m/s — decent for a liner, off a class-5 thruster.
- **Base shield strength:** 110 MJ · **Base armour:** 110 · **Hull hardness:** 35 (light and
  lightly protected — a liner, not a fighter)
- **Heat capacity:** 165, **Mass lock factor:** 9, **Reserve fuel:** 0.5 t. (The Dolphin's
  reputation for "cool" long jumps on passenger runs is about its low thermal load in flight; the
  heat-capacity buffer stat itself is a modest 165.)
- **Manoeuvrability (deg/s):** pitch 30 · roll 100 · yaw 20 (notably agile in yaw for a
  passenger hull)

## Slot Layout

- **Core internals:** Power Plant **4**, Thrusters **5**, Frame Shift Drive **4**,
  Life Support **4**, Power Distributor **3**, Sensors **3**, Fuel Tank **4**. The **class-5
  thrusters** (large for a 140 t hull) deliver the pace, and a **class-4 fuel tank** plus light
  mass give a respectable jump range; the small class-3 Power Distributor confirms it is no fighter.
- **Hardpoints:** 2 × Small (two weapon mounts only) plus 3 utility mounts — barely armed, as
  expected of a liner.
- **Optional internals:** sizes 5, 4, 4, 3, 2, 2, 2, 1, 1 (nine slots) plus a reserved class-1
  **Planetary Approach Suite**. Deep internals (top class-5) are the whole point — fill them with
  **passenger cabins**, including Luxury-class (`luxuryCabins: true`), plus a shield and a fuel
  scoop for long tourist runs.
- **Military slots:** none.

Bulkheads carry `causres 0` on every grade.

## Dolphin in the passenger-liner line

- **vs [[ships/orca]] and [[ships/beluga-liner]]:** the Dolphin is the **small** entry point of
  the Saud Kruger luxury trio — cheapest, lightest, and small-pad (it docks at outposts the
  large-pad Orca and Beluga cannot reach). The Orca is the fast mid-tier **large-pad** liner
  (300/380, light 290 t) and the Beluga the large-pad flagship with the most cabin space — both, like
  the Dolphin, are large-pad ships. All three share the luxury-cabin capability; the Dolphin is where
  it starts.
- **vs cargo haulers like the [[ships/type-6-transporter]]:** both are cheap, light Lakon/Saud
  Kruger small-to-medium utility hulls with token weapons, but the Type-6 fills its bays with
  **cargo racks** while the Dolphin fills its (luxury-capable) bays with **passenger cabins**. Pick
  by mission board — freight vs passengers.

## Build notes

The standard fit is a stack of passenger cabins (mix Economy/Business/First/Luxury to match the
mission's seats), a Bi-Weave shield, a fuel scoop for the long legs, and a Detailed Surface Scanner
if running sightseeing tours. Keep mass down to preserve jump range — passenger runs are paid by
distance and time, and the Dolphin's light hull is its advantage.

## Acquisition

Sold at stations carrying a shipyard; cheap and widely stocked. Check Spansh
(`spansh.co.uk/stations`) for the nearest. A common first purchase for commanders moving into
passenger missions.

[[trunk]]
