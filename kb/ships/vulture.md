---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/vulture.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T00:00:00+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Vulture

The Vulture is **Core Dynamics' small-pad heavy fighter** — the iconic "two big guns on a small
hull" brawler. It mounts **two Large hardpoints on a size-1 airframe**, an enormous
firepower-to-size ratio, and backs them with a high base shield and a class-leading roll rate (now second only to the [[ships/eagle]]
Mk II). The price is the Vulture's defining weakness: a **class-4 Power Plant** that struggles to feed
two Large weapons alongside thrusters and shields, making power management (or an engineered power
plant) essential. It is the small-pad companion to the medium-pad combat king
[[ships/fer-de-lance]].

## Overview

- **Manufacturer:** Core Dynamics
- **Size class:** 1 (Small landing pad — docks anywhere, including small outposts)
- **Role:** Dedicated combat (bounty hunting, Conflict Zones, anti-pirate patrol)
- **Rank requirement:** none — credits only (no `requirements` block in the Coriolis data)
- **Hull cost:** 4,692,214 CR (hull only)
- **Retail cost:** 4,925,615 CR (with stock modules)
- **Crew seats:** 2

## Hull Stats

Source: Coriolis-data ship definition `vulture` (edID 128049309, eddbID 23).

- **Hull mass:** 230 t
- **Top speed:** 210 m/s · **Boost:** 340 m/s (slow cruise, but boosts hard and turns superbly)
- **Base shield strength:** 240 MJ (high for a small hull — a shield-tanky brawler)
- **Base armour:** 160 · **Hull hardness:** 55
- **Heat capacity:** 237
- **Mass lock factor:** 10
- **Manoeuvrability (deg/s):** pitch 42 · **roll 110** · yaw 17. The roll rate of 110 is the
  **second-highest of any ship paged in this KB**, tied with the featherweight starter
  [[ships/sidewinder]] and behind only the [[ships/eagle]] Mk II (roll 120) — but the Vulture pairs
  that roll with real firepower, out-rolling almost everything to keep its fixed Large mounts on target.
- **Reserve fuel:** 0.57 t

## Slot Layout

- **Core internals:** Power Plant **4**, Thrusters **5**, Frame Shift Drive **4**,
  Life Support **3**, Power Distributor **5**, Sensors **4**, Fuel Tank **3**. **The class-4 Power
  Plant is the Vulture's famous bottleneck** — two Large hardpoints plus thrusters and shields can
  exceed its output, so power priorities or an Overcharged power plant are part of every serious
  build. (The Power Distributor is a healthy class 5, so the constraint is generation, not the
  distributor.)
- **Hardpoints:** 2 × Large (two weapon mounts). Two Large slots on a small hull is the Vulture's
  signature — concentrated firepower that punches far above its size.
- **Utility mounts:** 4 (shield boosters, chaff, heat sinks, point defence).
- **Optional internals:** sizes 5, 4, 2, 1, 1, 1, 1 (seven regular slots, top class 5) plus **one
  class-5 Military slot** and a reserved class-1 **Planetary Approach Suite**. The Military slot
  takes a [[outfitting/hull-reinforcement]], [[outfitting/module-reinforcement]] or
  [[outfitting/shield-cell-bank]] without spending a normal optional.
- **Military slots:** one (class 5).

Bulkheads carry `causres 0` on every grade.

## Vulture vs other combat hulls

- **vs [[ships/fer-de-lance]]:** the Fer-de-Lance is the medium-pad step up — one Huge (class-4)
  hardpoint, a larger class-6 Power Distributor and far more shield, but it needs a medium pad and
  costs ~10×. The Vulture delivers two Large mounts and best-in-KB agility on a small pad for a
  fraction of the price; the FDL trades agility for raw mount size and sustained energy draw.
- **vs the cheap small-pad fighters [[ships/viper-mk-iii]] and [[ships/diamondback-scout]]:** both
  are far cheaper, lighter entry combat hulls with four smaller mounts (2 Medium + 2 Small) rather
  than the Vulture's two Large. The Viper is the fast interceptor (320/400, thin armour, a Military
  slot); the Scout is the cool-running recon fighter. The Vulture is the step up in firepower and
  shield once you can afford ~4.9 M CR and solve its power budget.
- **As a small-pad brawler** it sits alongside the other Core Dynamics combat lineage and the
  large-pad [[ships/federal-corvette]] as the entry rung of dedicated heavy combat — outturning
  bigger ships while two Large weapons do the work, provided you solve the power budget.

## Build notes

The textbook fit is two Large gimballed or fixed weapons (pulse/burst lasers for low draw, or a
multi-cannon pair to spare the distributor), a strong shield with boosters, and an Overcharged or
Low-Emissions power plant to relieve the class-4 generator. Engineer the Power Distributor at
[[engineers/the-dweller]] to sustain energy-weapon fire, and prioritise modules carefully so a
hardpoint deployment never browns out. Heat capacity is moderate, so carry a
[[outfitting/heat-sink-launcher]] if running energy weapons hard.

## Acquisition

Sold at stations carrying a shipyard; as a Core Dynamics combat hull it is widely stocked and,
being small-pad, can be based out of outposts. Check Spansh (`spansh.co.uk/stations`) for the
nearest source.

[[trunk]]
