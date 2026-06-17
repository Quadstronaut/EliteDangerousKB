---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/type_6_transporter.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T04:26:26Z
source_count: 1
verified: false
availability: live
changed_note:
---

# Type-6 Transporter

The Type-6 Transporter is **Lakon Spaceways' cheap medium-pad dedicated freighter** — the classic
"first real trader," the next rung up the hauler ladder from the small-pad [[ships/hauler]]. At a hull
cost of just 866,622 CR it is **by far the cheapest medium-pad ship in the KB**, yet it steps up from
the Hauler's small pad to a medium pad and trades into deep, cargo-biased optionals. With only two
Small hardpoints it is no fighter; its whole identity is moving cargo cheaply, with a good jump range
for a budget trader thanks to a class-4 FSD on a light hull.

## Overview

- **Manufacturer:** Lakon Spaceways
- **Size class:** 2 (Medium landing pad — docks at outposts and all larger ports)
- **Role:** Budget medium-pad cargo hauler (early bulk trade, mission running, the first dedicated freighter)
- **Rank requirement:** none — credits only (no `requirements` block in the Coriolis data)
- **Hull cost:** 866,622 CR (hull only — **the cheapest medium-pad hull in the KB**)
- **Retail cost:** 1,045,945 CR (with stock modules)
- **Crew seats:** 1

## Hull Stats

Source: Coriolis-data ship definition `type_6_transporter` (edID 128049285, eddbID 19).

- **Hull mass:** 155 t — light for a medium hull, which (with the class-4 FSD) underpins its decent range.
- **Top speed:** 220 m/s · **Boost:** 350 m/s.
- **Base shield strength:** 90 MJ — weak; the Type-6 is unarmoured-trader fragile and relies on not
  being caught rather than tanking damage.
- **Base armour:** 180 · **Hull hardness:** 35.
- **Heat capacity:** 179
- **Mass lock factor:** 8
- **Manoeuvrability (deg/s):** pitch 30 · roll 100 · yaw 17 (surprisingly nimble roll for a freighter).
- **Reserve fuel:** 0.39 t

## Slot Layout

- **Core internals:** Power Plant **3**, Thrusters **4**, Frame Shift Drive **4**, Life Support **2**,
  Power Distributor **3**, Sensors **2**, Fuel Tank **4**. The **class-4 FSD paired with a class-4 fuel
  tank** on a light 155 t hull is the data behind the Type-6's good-range reputation — long legs for so
  cheap a trader.
- **Hardpoints:** **2 × Small** (two weapon mounts) — barely armed; a pure freighter that cannot fight.
- **Utility mounts:** 3 (room for a shield booster, chaff, heat sink or point defence).
- **Optional internals:** sizes 5, 5, 4, 4, 3, 2, 2, 1 (eight regular slots, **top two class-5**) plus a
  reserved class-1 **Planetary Approach Suite**. The two class-5 optionals carry the Type-6's cargo
  capacity — far deeper than the small-pad [[ships/hauler]]'s top class-3 racks. **No Military slot.**
- **Military slots:** none.

Bulkheads carry `causres 0` on every grade.

## The dedicated-freight ladder

- **vs [[ships/hauler]]:** the Hauler is the small-pad rung beneath the Type-6 — a tiny 14 t hull with
  top class-3 optionals, for the cheapest possible outpost-only cargo runs. The Type-6 is the **medium-pad
  step up**: a medium pad, far deeper class-5 optionals (much more cargo) and a stronger core, for a hull
  price still under a million credits. Move up to the Type-6 once you need real cargo capacity and can use
  medium pads.
- **vs [[ships/type-8-transporter]]:** the Type-8 is the modern top-end medium-pad hauler — a class-7
  plus three class-6 optionals out-haul a Python, with six weapon mounts for self-defence, but it costs
  ~35 M CR. The Type-6 is the budget-entry medium freighter beneath it: a fraction of the price and cargo,
  the ship you fly while saving for a Type-8 (or skipping straight to a [[ships/type-9-heavy]] for bulk).
- **vs [[ships/type-7-transporter]]:** the Type-7 is the next Lakon Type freighter up, but it is a
  **large-pad** hull (the cheapest large-pad hull in the KB at 16.8 M CR) — deeper cargo and a tougher
  hull than the Type-6, but it **cannot dock at outposts**. The Type-6 keeps the medium pad (and outpost
  access); step to the Type-7 only when you can use large pads and want more cargo.
- **vs [[ships/asp-explorer]]:** the next-cheapest medium-pad hull in the KB (~6.1 M), the Asp is the
  roomy multirole/explorer; the Type-6 is the pure-freight budget option roughly 7× cheaper to buy.
- **vs [[ships/keelback]]:** the Keelback is the Type-6's **armed, fighter-capable sibling** on the same
  Lakon airframe — heavier and slower, one fewer optional, but with **2 Medium + 2 Small mounts, a
  Ship-Launched Fighter bay and roughly double the shield/armour**, for ~3 M CR (the second-cheapest
  medium-pad hull, just above the Type-6). Fly the Type-6 to haul cheaply; step to the Keelback when you
  want a trader that can fight back or carry a fighter.

## Build notes

Fit the Type-6 as a single-purpose hauler: fill the eight optionals with cargo racks (the two class-5
slots first), add a basic shield, and engineer the class-4 FSD at [[engineers/felicity-farseer]]
(Increased Range) for trade routes with long jumps — a Frame Shift Drive (SCO) helps in-system transit.
The two Small hardpoints and weak 90 MJ shield mean it cannot fight; rely on a high-wake escape, a
shield booster in a utility slot and route planning to avoid interdiction. With no Military slot, any
hull reinforcement competes with cargo, so keep it lean and lean on speed.

## Acquisition

Sold at most stations carrying a shipyard; no rank or permit requirement, credits only. Its low price
and medium pad make it one of the most accessible real freighters in the game. Check Spansh
(`spansh.co.uk/stations`) for the nearest source.

[[trunk]]
