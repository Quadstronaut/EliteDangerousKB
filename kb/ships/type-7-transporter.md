---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/type_7_transport.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T05:39:14+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Type-7 Transporter

The Type-7 Transporter is **Lakon Spaceways' cheap large-pad dedicated freighter** — a deep
cargo hauler that sits in price below the [[ships/type-9-heavy]] but well above the medium-pad
[[ships/type-6-transporter]]. Its defining trait is a **gotcha**: despite being an affordable,
lightly-armed bulk hauler that commanders often expect to be the medium-pad "middle" of the
Lakon Type line, the Type-7 actually **requires a large landing pad** and so cannot dock at
outposts. At a hull cost of 16,783,094 CR it is **the cheapest large-pad hull in the KB** —
the most affordable way onto a large pad — but that large pad limits where it can dock.

## Overview

- **Manufacturer:** Lakon Spaceways
- **Size class:** 3 (**Large** landing pad — requires a large pad; **cannot** dock at outposts)
- **Role:** Budget large-pad cargo hauler (bulk trade, mission running, colonisation supply)
- **Rank requirement:** none — credits only (no `requirements` block in the Coriolis data)
- **Hull cost:** 16,783,094 CR (hull only — **the cheapest large-pad hull in the KB**, undercutting
  the [[ships/imperial-clipper]] at 21,116,895 CR)
- **Retail cost:** 17,472,252 CR (with stock modules)
- **Crew seats:** 1

## Hull Stats

Source: Coriolis-data ship definition `type_7_transport` (edID 128049297, eddbID 20).

- **Hull mass:** 350 t
- **Top speed:** 180 m/s · **Boost:** 300 m/s (slow — plan approaches and avoid interdiction)
- **Base shield strength:** 155 MJ
- **Base armour:** 340 · **Hull hardness:** 54 — noticeably tougher than the medium-pad
  [[ships/type-6-transporter]] (180 armour / hardness 35); the Type-7 can soak more before its
  shields drop, though it is still a freighter, not a brawler.
- **Heat capacity:** 226
- **Mass lock factor:** 10
- **Manoeuvrability (deg/s):** pitch 22 · roll 60 · yaw 22 (ponderous — it turns slowly)
- **Reserve fuel:** 0.52 t

## Slot Layout

- **Core internals:** Power Plant **5**, Thrusters **5**, Frame Shift Drive **5**, Life Support
  **4**, Power Distributor **4**, Sensors **3**, Fuel Tank **5**. A class-5 FSD on a 350 t hull
  gives workable (not spectacular) laden range.
- **Hardpoints:** **4 × Small** (four weapon mounts) — token armament only; the Type-7 cannot
  fight and relies on running rather than shooting.
- **Utility mounts:** 4 (room for shield boosters, chaff, heat sink and point defence).
- **Optional internals:** sizes 6, 6, 6, 5, 5, 5, 3, 3, 2, 1 (ten regular slots, **top three
  class-6**) plus a reserved class-1 **Planetary Approach Suite** (planet-landing and SRV
  capable). The three class-6 plus three class-5 slots carry the Type-7's cargo — deep capacity
  for the price, short of the [[ships/type-9-heavy]]'s twin class-8 racks.
- **Military slots:** none.

Bulkheads carry `causres 0` on every grade.

## The Lakon freight ladder

- **vs [[ships/type-6-transporter]]:** the Type-6 is the cheap **medium-pad** rung (866 k CR,
  docks at outposts). The Type-7 steps up to far deeper optionals (three class-6 vs the Type-6's
  top two class-5) and a tougher hull, but jumps to a **large pad** — a real downgrade in docking
  convenience. Move up to the Type-7 only when you can use large pads and want more cargo than the
  Type-6 carries.
- **vs [[ships/type-9-heavy]]:** the Type-9 is the classic large-pad **bulk** hauler — twin
  class-8 optionals for roughly an order of magnitude more cargo, a fighter bay and crew 4, but it
  costs ~72 M CR (over 4× the Type-7's hull). The Type-7 is the **budget large-pad freighter**
  beneath it: a fraction of the price and cargo, the ship you fly while saving for a Type-9.
- **vs [[ships/imperial-clipper]]:** the Clipper is the next-cheapest large-pad hull (21.1 M) but
  a fast multirole, not a freighter — far quicker (300/380) with bigger-calibre mounts and shallower
  cargo. The Type-7 trades all of that pace for cheaper, deeper cargo on the same pad class.

## Build notes

Fit the Type-7 as a single-purpose bulk hauler: fill the ten optionals with cargo racks (the three
class-6 slots first), add a shield generator, and engineer the class-5 FSD at
[[engineers/felicity-farseer]] (Increased Range) to offset the heavy laden mass — a Frame Shift
Drive (SCO) helps slow in-system transit. The four Small hardpoints and modest 155 MJ shield mean
it cannot fight; rely on a high-wake escape, a shield booster in a utility slot and route planning
to dodge interdiction. With no Military slot, any hull reinforcement competes with cargo, so keep
it lean. Remember the large-pad requirement when planning routes — it locks you out of outpost-only
markets the medium-pad Type-6 can still reach.

## Acquisition

Sold at stations carrying a shipyard; no rank or permit requirement, credits only. Confirmed in the
shipyard stock list at **Garay Terminal** in [[locations/deciat]]. Requires a large landing pad.
Check Spansh (`spansh.co.uk/stations`) for the nearest source.

[[trunk]]
