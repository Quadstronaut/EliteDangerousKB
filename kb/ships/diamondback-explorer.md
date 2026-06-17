---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/diamondback_explorer.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T00:00:00+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Diamondback Explorer

The Diamondback Explorer (DBX) is a **small-class long-range explorer** by **Lakon Spaceways** —
the budget, cold-running entry to serious exploration. Its defining trait is an exceptionally high
heat capacity, which lets it sit close to hot stars while fuel-scooping without overheating, and a
class-5 Frame Shift Drive on a light 260 t hull for long jumps at a very low price. As the only
**small-pad** ship of the explorer line, it completes the trio alongside the medium-pad
[[ships/asp-explorer]] (roomy classic) and [[ships/mandalay]] (modern max-range).

## Overview

- **Manufacturer:** Lakon Spaceways
- **Size class:** 1 (Small landing pad — docks anywhere, including small outposts)
- **Role:** Long-range exploration (cheap entry; famed for cool fuel-scooping)
- **Rank requirement:** none — credits only (no `requirements` block in the Coriolis data)
- **Hull cost:** 1,638,277 CR (hull only)
- **Retail cost:** 1,894,760 CR (with stock modules)
- **Crew seats:** 1 (single-seat — no multicrew co-pilot)

## Hull Stats

Source: Coriolis-data ship definition `diamondback_explorer` (edID 128671831, eddbID 5).

- **Hull mass:** 260 t (light — directly boosts jump range)
- **Top speed:** 260 m/s · **Boost:** 340 m/s
- **Base shield strength:** 150 MJ
- **Base armour:** 150 · **Hull hardness:** 42 (low — not a combat hull)
- **Heat capacity:** 351 — the **highest of any ship paged in this KB**. This is the data behind
  the DBX's famous cool-running reputation: it stays cooler than rivals while fuel-scooping near
  hot stars.
- **Mass lock factor:** 10
- **Manoeuvrability (deg/s):** pitch 35 · roll 90 · yaw 13
- **Reserve fuel:** 0.52 t

## Slot Layout

- **Core internals:** Power Plant **4**, Thrusters **4**, Frame Shift Drive **5**,
  Life Support **3**, Power Distributor **4**, Sensors **3**, Fuel Tank **5**. The class-5
  [[outfitting/frame-shift-drive]] on a light 260 t hull is what gives the DBX its long jump
  range; the modest class-4 Power Distributor marks it as an explorer, not a gunship.
- **Hardpoints:** 1 × Large + 2 × Medium (three weapon mounts). The lone **Large** hardpoint on a
  small hull lets the DBX punch above its size if interdicted — unusual for an explorer.
- **Utility mounts:** 4 (heat sinks, shield boosters, a Detailed Surface Scanner kit).
- **Optional internals:** sizes 4, 4, 3, 3, 2, 2, 1, 1 (eight slots) plus a reserved class-1
  **Planetary Approach Suite** (planet-landing and SRV capable). The top class-4 slots take a
  [[outfitting/fuel-scoop]] or a [[outfitting/guardian-fsd-booster]]; remaining slots cover an
  AFMU, SRV hangar, shields and a Detailed Surface Scanner.
- **Military slots:** none.

Bulkheads carry `causres 0` on every grade, so for any AX detour fit a Meta-Alloy
[[outfitting/hull-reinforcement]] package for caustic resistance.

## Explorer trio: budget vs roomy vs max-range

All three share a class-5 FSD; they differ in pad size, mass and price.

- **Diamondback Explorer — budget / coldest.** The only **small-pad** explorer (260 t). Cheapest
  by far (~1.6 M CR hull) and the coolest-running (heat capacity 351), ideal for tight-orbit fuel
  scooping. Shallower internals (eight slots, top class 4) and a single seat.
- **[[ships/asp-explorer]] — roomy classic.** Medium pad, 280 t, eight optionals topping out at
  class 6, ~6.1 M CR hull. The affordable workhorse with more module room than the DBX.
- **[[ships/mandalay]] — max range.** Medium pad, light 230 t, ten optionals (top class 6), best
  jump range of the three, ~16.5 M CR hull. The modern choice when range is everything.

Pick the DBX for a cheap, cool first explorer that lands on any pad; the Asp for more room at a
modest price; the Mandalay for outright range.

## Build notes

A standard exploration fit pairs an engineered class-5 FSD with a fuel scoop, an AFMU, an SRV
hangar and a Detailed Surface Scanner. Engineer the FSD (Increased Range) at
[[engineers/felicity-farseer]] and add a [[outfitting/guardian-fsd-booster]] to push jump range
toward the top of the explorer class. The high heat capacity makes the DBX forgiving when scooping
aggressively between jumps.

## Acquisition

Sold at stations carrying a shipyard; as a long-standing Lakon hull it is very widely stocked and,
being small-pad, can be based out of outposts. Check Spansh (`spansh.co.uk/stations`) for the
nearest source, then engineer the FSD at Farseer Inc in [[locations/deciat]].

[[trunk]]
