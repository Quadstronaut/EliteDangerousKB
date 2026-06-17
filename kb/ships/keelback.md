---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/keelback.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T04:39:15Z
source_count: 1
verified: false
availability: live
changed_note:
---

# Keelback

The Keelback is **Lakon Spaceways' armed, fighter-capable variant of the [[ships/type-6-transporter]]
airframe** — the budget "trader that can fight back." It shares the Type-6's cheap medium-pad freighter
base, but trades some cargo depth for real teeth: a heavier hull, **2 Medium + 2 Small hardpoints**, and
a **Ship-Launched Fighter bay**. At a hull cost of 2,946,463 CR it is the **cheapest fighter-bay-capable
hull in the KB** — the classic cheapest way into flying an SLF — and the **second-cheapest medium-pad
hull in the KB**, behind only its Type-6 sibling.

## Overview

- **Manufacturer:** Lakon Spaceways
- **Size class:** 2 (Medium landing pad — docks at outposts and all larger ports)
- **Role:** Budget combat-trader / SLF carrier (armed hauling, low-cost fighter-bay platform, light AX)
- **Rank requirement:** none — credits only (no `requirements` block in the Coriolis data)
- **Hull cost:** 2,946,463 CR (hull only — **second-cheapest medium-pad hull in the KB**, behind the
  [[ships/type-6-transporter]]'s 866,622)
- **Retail cost:** 3,126,154 CR (with stock modules)
- **Crew seats:** 2 (pilot + one — covers a Ship-Launched Fighter pilot or multicrew seat)
- **Fighter bay capable:** yes (`fighterHangars: true`)

## Hull Stats

Source: Coriolis-data ship definition `keelback` (edID 128672269, eddbID 27).

- **Hull mass:** 180 t — heavier than the [[ships/type-6-transporter]]'s 155 t (the combat-tank trade).
- **Top speed:** 200 m/s · **Boost:** 300 m/s — slower than the Type-6's 220/350; the extra mass and
  armour cost it pace.
- **Base shield strength:** 135 MJ — meaningfully stronger than the Type-6's 90 MJ.
- **Base armour:** 270 — far tougher than the Type-6's 180 (a hull built to take some return fire).
- **Hull hardness:** 45 — above the Type-6's 35.
- **Heat capacity:** 215
- **Mass lock factor:** 8
- **Manoeuvrability (deg/s):** pitch 27 · roll 100 · yaw 15.
- **Reserve fuel:** 0.39 t

## Slot Layout

- **Core internals:** Power Plant **4**, Thrusters **4**, Frame Shift Drive **4**, Life Support **1**,
  Power Distributor **3**, Sensors **2**, Fuel Tank **4**. The class-4 FSD with a class-4 fuel tank keeps
  a useful jump range, and the class-4 power plant feeds the bigger hardpoints and the fighter bay.
- **Hardpoints:** **2 × Medium + 2 × Small** (four weapon mounts) — a real upgrade over the
  [[ships/type-6-transporter]]'s two Small mounts. Enough to fight back, escort, or run light AX.
- **Utility mounts:** 3 (shield booster, chaff, heat sink or point defence).
- **Optional internals:** sizes 5, 5, 4, 3, 2, 2, 1 (seven regular slots, **top two class-5**) plus a
  reserved class-1 **Planetary Approach Suite**. **No Military slot.** One of the class-5-capable
  optionals can hold a Ship-Launched Fighter bay.
- **Military slots:** none.

Bulkheads carry `causres 0` on every grade (fit a Meta-Alloy Hull Reinforcement for any AX detour).

## The Type-6 airframe pair

- **vs [[ships/type-6-transporter]]:** these two share Lakon's medium-pad airframe and split by
  philosophy. The **Type-6** is the pure freighter — lighter (155 t), faster (220/350), with eight
  cargo-biased optionals (top two class-5) but only **2 Small mounts and no fighter bay** — the cheapest
  medium-pad hull in the KB. The **Keelback** is the combat variant — heavier and slower, with one fewer
  optional (seven), but **2 Medium + 2 Small mounts, a Ship-Launched Fighter bay, and roughly double the
  shield/armour**. Fly the Type-6 to move cargo cheaply; fly the Keelback when you want a hauler that can
  shoot back or carry a fighter.
- **vs [[ships/hauler]]:** the small-pad bottom rung of the budget freight ladder — a tiny 14 t
  single-Small hull. The Keelback sits well above it: a medium pad, four weapon mounts and an SLF bay.

## The cheapest fighter bay

The Keelback's standout trait is `fighterHangars: true` on so cheap a hull. Every other fighter-bay ship
in the KB costs far more — the next cheapest is the [[ships/alliance-crusader]] at ~22.1 M CR, then large
hulls like the [[ships/anaconda]], [[ships/federal-corvette]] and [[ships/imperial-cutter]]. That makes
the Keelback the **cheapest entry point to flying a Ship-Launched Fighter**, long its real-world
reputation: a ~3 M-credit ship that lets a wingman (NPC or multicrew) launch a second gun platform.

## Build notes

Fit the Keelback as an armed escort-hauler or a budget SLF platform. Put a fighter bay in a class-5
optional, fill the rest with cargo racks or a shield/hull mix, and arm the 2 Medium mounts with gimballed
multi-cannons or lasers backed by the 2 Small. Engineer the class-4 FSD at [[engineers/felicity-farseer]]
(Increased Range) for trade legs. With no Military slot, hull reinforcement competes with cargo, so lean
on the 135 MJ shield and a utility-slot shield booster. For light AX work fit a Meta-Alloy Hull
Reinforcement (bulkheads carry no caustic resistance).

## Acquisition

Sold at most stations carrying a shipyard; no rank or permit requirement, credits only. Its medium pad
and low price make it the most accessible fighter-bay ship in the game. Check Spansh
(`spansh.co.uk/stations`) for the nearest source.

[[trunk]]
