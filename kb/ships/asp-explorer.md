---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/asp.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T03:10:00+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Asp Explorer

The Asp Explorer is a **medium-class long-range explorer** by **Lakon Spaceways** — the
classic, affordable mid-game exploration ship. A light 280 t hull, a class-5 Frame Shift
Drive, a generous spread of optional internals and a no-rank-gate price have made it the
default first "proper" explorer for a generation of commanders. Its modern, lighter
stablemate is the [[ships/mandalay]]; the Asp trades a little jump range for far more
internal room and a much cheaper hull.

## Overview

- **Manufacturer:** Lakon Spaceways
- **Size class:** 2 (Medium landing pad — docks at outposts and all larger ports)
- **Role:** Long-range exploration (also light multirole / passenger)
- **Rank requirement:** none — credits only (no `requirements` block in the Coriolis data)
- **Hull cost:** 6,145,793 CR (hull only)
- **Retail cost:** 6,661,154 CR (with stock modules)
- **Crew seats:** 2

## Hull Stats

Source: Coriolis-data ship definition `asp` (edID 128049303, eddbID 3).

- **Hull mass:** 280 t (light — directly boosts jump range)
- **Top speed:** 250 m/s · **Boost:** 340 m/s
- **Base shield strength:** 140 MJ
- **Base armour:** 210 · **Hull hardness:** 52 (low — not a combat hull)
- **Heat capacity:** 272
- **Mass lock factor:** 11
- **Manoeuvrability (deg/s):** pitch 38 · roll 100 · yaw 10 (a fast roll for an explorer)
- **Reserve fuel:** 0.63 t

## Slot Layout

- **Core internals:** Power Plant **5**, Thrusters **5**, Frame Shift Drive **5**,
  Life Support **4**, Power Distributor **4**, Sensors **5**, Fuel Tank **5**. The class-5
  [[outfitting/frame-shift-drive]] on a light 280 t hull is what gives the Asp its long jump
  range; the modest class-4 Power Distributor marks it as an explorer, not a gunship.
- **Hardpoints:** 2 × Medium + 4 × Small (six weapon mounts — enough to fight clear of an
  interdiction, but no Large or Huge slots).
- **Utility mounts:** 4 (heat sinks, shield boosters, a Detailed Surface Scanner kit).
- **Optional internals:** sizes 6, 5, 3, 3, 3, 2, 2, 1 (eight slots) plus a reserved class-1
  **Planetary Approach Suite** (planet-landing and SRV capable). The class-6 slot takes a
  large [[outfitting/fuel-scoop]] or a [[outfitting/guardian-fsd-booster]]; remaining slots
  cover an AFMU, SRV hangar, shields and a Detailed Surface Scanner.
- **Military slots:** none.

Bulkheads carry `causres 0` on every grade, so for any AX detour fit a Meta-Alloy
[[outfitting/hull-reinforcement]] package for caustic resistance.

## Asp Explorer vs the explorer line

Both the Asp and the [[ships/mandalay]] are medium-pad explorers with a class-5 FSD. The **Asp
Explorer** is the cheaper, older classic: heavier (280 t vs 230 t) so a little less range, but
with eight optional internals and a very low entry price (~6.1 M CR hull). The newer Mandalay is
lighter and nimbler with class-leading jump range, at roughly triple the hull cost. Pick the Asp
as an affordable, roomy first explorer; the Mandalay when you want maximum range. For an even
cheaper **small-pad** option, the [[ships/diamondback-explorer]] is the coldest-running of the
three (ideal for tight fuel-scooping) but carries shallower internals and a single seat.

On the same Asp airframe is the cheaper budget sibling, the [[ships/asp-scout]] — lighter (150 t)
and a touch nimbler, but with a smaller class-4 FSD, shallower internals (seven optionals, top
class-5) and fewer mounts (4 vs 6). The Scout is the cut-down economy version; for exploration the
Explorer's bigger drive and deeper internals win, so the Scout is rarely the better buy here.

## Build notes

A standard exploration fit pairs an engineered class-5 FSD with a class-6 fuel scoop, an
AFMU, an SRV hangar and a Detailed Surface Scanner. Engineer the FSD (Increased Range) at
[[engineers/felicity-farseer]] and add a [[outfitting/guardian-fsd-booster]] to push the
jump range toward the top of the explorer class.

## Acquisition

Sold at large stations carrying a shipyard; as a long-standing Lakon hull it is very widely
stocked. Check Spansh (`spansh.co.uk/stations`) for the nearest source, then engineer the
FSD at Farseer Inc in [[locations/deciat]].

[[trunk]]
