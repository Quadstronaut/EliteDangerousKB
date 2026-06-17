---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/orca.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T05:26:00+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Orca

The Orca is **Saud Kruger's fast large-pad luxury passenger liner** — the middle rung of the
Saud Kruger trio ([[ships/dolphin]] → Orca → [[ships/beluga-liner]]). Like the Dolphin it is built
to carry people in style rather than cargo or guns — it can fit **Luxury-class passenger cabins**
(the Saud Kruger `luxuryCabins` signature) — but its calling card is **speed**: at **300 m/s base /
380 m/s boost** it is one of the fastest large hulls in the game, tying the [[ships/imperial-clipper]]
for the fastest large-pad speed in the KB. A class-6 thruster on a light 290 t hull is what makes a
liner this quick. Despite the mid-liner billing it needs a **Large landing pad** (size class 3) — it
cannot use the outposts the small-pad Dolphin can — and it buys with **credits only, no rank gate**.

## Overview

- **Manufacturer:** Saud Kruger
- **Size class:** 3 (Large landing pad only — large orbital and planetary ports)
- **Role:** Fast luxury passenger transport (tourism, luxury and economy passenger missions)
- **Rank requirement:** none — credits only. The Coriolis data has **no `requirements` block at
  all** (not even the `horizons` flag the Dolphin and Beluga carry).
- **Hull cost:** 47,800,723 CR (hull only)
- **Retail cost:** 48,539,887 CR (with stock modules)
- **Crew seats:** 2

## Hull Stats

Source: Coriolis-data ship definition `orca` (edID 128049327, eddbID 16).

- **Hull mass:** 290 t — light for a large hull, which (with the big thruster) is the source of its speed.
- **Top speed:** 300 m/s · **Boost:** 380 m/s — exceptionally fast for a large-pad ship; **ties the
  [[ships/imperial-clipper]] for the fastest large-pad speed in the KB**, and far quicker than the
  other large hulls ([[ships/imperial-cutter]] 200/320, [[ships/anaconda]] 180/240,
  [[ships/federal-corvette]] 200/260, [[ships/beluga-liner]] 200/280).
- **Base shield strength:** 220 MJ · **Base armour:** 220 · **Hull hardness:** 55 (modest — a fast
  liner, not a warship).
- **Heat capacity:** 262, **Mass lock factor:** 16, **Reserve fuel:** 0.79 t.
- **Manoeuvrability (deg/s):** pitch 25 · roll 55 · yaw 18 — slow, lazy roll typical of a big liner;
  it is fast in a straight line, not nimble.

## Slot Layout

- **Core internals:** Power Plant **5**, Thrusters **6**, Frame Shift Drive **5**, Life Support **6**,
  Power Distributor **5**, Sensors **4**, Fuel Tank **5**. The **class-6 thrusters** on a light 290 t
  hull deliver the class-leading speed; the **class-6 Life Support** slot is oversized (a Saud Kruger
  liner trait, even larger on the Beluga).
- **Hardpoints:** **1 × Large + 2 × Medium** (three weapon mounts) plus 4 utility mounts — token
  armament for self-defence, more than the Dolphin's 2 Small but still not a liner's main job.
- **Optional internals:** sizes 6, 5, 5, 5, 4, 3, 2, 2, 1 (nine regular slots, **top class-6**) plus a
  reserved class-1 **Planetary Approach Suite**. Deep, large internals are the point — fill them with
  **passenger cabins** (Economy/Business/First/Luxury), a shield and a fuel scoop.
- **Military slots:** none.

Bulkheads carry `causres 0` on every grade.

## Orca in the passenger-liner line

- **vs [[ships/dolphin]]:** the Dolphin is the **small-pad** entry liner (140 t, cheap, docks at
  outposts). The Orca is the large-pad step up — much bigger, far more expensive, faster (300/380 vs
  250/350), with deeper class-6 internals for more (and bigger) cabins. The trade is the **Large pad
  requirement**: the Orca cannot use the outposts the Dolphin can.
- **vs [[ships/beluga-liner]]:** both are **large-pad** Saud Kruger liners, and this is the real choice
  in the trio. The **Orca** is the light (290 t), fast (300/380), cheaper hull with nine optionals; the
  **Beluga Liner** is the heavy (950 t), slow (200/280), pricey flagship with twelve optionals (the most
  cabin capacity), a fighter bay, crew 4 and a class-8 life-support slot. Pick the Orca for **speed and
  cost**, the Beluga for **maximum passengers**.

## vs the [[ships/imperial-clipper]]

The Orca and the Imperial Clipper share the **same 300/380 speed** — the joint-fastest large-pad ships
in the KB — and both are light large hulls (Orca 290 t, Clipper 400 t). They differ in role: the Clipper
is a Baron-rank-gated **combat multirole** (2 Large + 2 Medium hardpoints, class-7 optionals), while the
Orca is a no-gate **passenger liner** (token 1 Large + 2 Medium guns, cabin-focused internals). Same pace,
opposite purpose.

## Build notes

The standard fit is a stack of passenger cabins (mix the classes to match the mission's seats), a
Bi-Weave shield, a fuel scoop and a Detailed Surface Scanner for sightseeing tours. Engineer dirty-drive
thrusters to lean into the Orca's natural speed — fast transit means more passenger runs completed per
hour, and the light hull holds a good jump range. With no Military slot, any hull reinforcement comes out
of the nine regular optionals, so most builds lean on the shield and pace rather than armour.

## Acquisition

Sold at stations carrying a shipyard; it needs a **Large landing pad** (no outposts) and buys with
**credits only — no rank gate**. Check Spansh (`spansh.co.uk/stations`) for the nearest source.

[[trunk]]
