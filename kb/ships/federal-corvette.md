---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/federal_corvette.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T02:21:19+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Federal Corvette

The Federal Corvette is **Core Dynamics' large-pad combat flagship** — a heavy gunship and one of
the game's premier anti-Xeno (AX) platforms. It is the **first ship in this KB to mount Huge
(class-4) hardpoints, and it carries two of them**, backed by a **class-8 Power Plant and class-8
Power Distributor** that sustain the heaviest weapon loadout in the game. It is the big-hull step up
from the medium [[ships/alliance-challenger|Alliance Challenger]] / [[ships/krait-mk-ii|Krait Mk II]]
AX line. Purchase is **rank-gated**: it requires Federal Navy rank **Rear Admiral**.

## Overview

- **Manufacturer:** Core Dynamics
- **Size class:** 3 (Large landing pad — needs a large-pad starport)
- **Role:** Heavy combat flagship / anti-Xeno (AX) large-pad gunship
- **Hull cost:** 183,156,068 CR (hull only)
- **Retail cost:** 187,969,450 CR (with stock modules)
- **Crew seats:** 4 · **Ship-Launched Fighter bay** present
- **Requires:** Federal Navy rank **Rear Admiral** (Coriolis `requirements.federationRank: 12`)

## Hull Stats

Source: Coriolis-data ship definition `federal_corvette` (edID 128049369).

- **Hull mass:** 900 t
- **Top speed:** 200 m/s · **Boost:** 260 m/s (agile for a large-pad combat hull)
- **Base shield strength:** 555 MJ
- **Base armour:** 370 · **Hull hardness:** 70 (the highest of any KB ship — excellent against
  armour penetration)
- **Heat capacity:** 333
- **Mass lock factor:** 24 (very high — strongly mass-locks targets, denying their FSD escape)
- **Manoeuvrability (deg/s):** pitch 28 · roll 75 · yaw 8
- **Reserve fuel:** 1.13 t

## Slot Layout

- **Core internals:** Power Plant **8**, Thrusters **7**, Frame Shift Drive **6**,
  Life Support **5**, Power Distributor **8**, Sensors **8**, Fuel Tank **5**. The **class-8 Power
  Plant + class-8 Power Distributor** are the Corvette's signature — they feed and sustain a full
  bank of energy weapons that lighter hulls cannot power.
- **Hardpoints:** **2 × Huge + 1 × Large + 2 × Medium + 2 × Small** (seven weapon mounts). The two
  **Huge (class-4)** mounts are unique among current KB ships and define its raw firepower.
- **Utility mounts:** 8 (room for a deep stack of shield boosters plus chaff, heat sinks and
  point defence).
- **Optional internals:** sizes **7, 7, 7, 6, 6, 5, 5, 4, 4, 3, 1** (eleven regular optionals) plus
  **two class-5 Military slots** plus a reserved class-1 **Planetary Approach Suite**.

### Military slots — bigger, but fewer

The Corvette's **two class-5 Military slots** are **larger** than the Alliance trio's class-4 slots
but **fewer in number** (two vs three). They accept the same reinforcement set (per the Coriolis
data: mahr, hr, scb, mrp, gsrp, gmrp, ghrp):

- [[outfitting/hull-reinforcement]] — standard, **Meta-Alloy** (caustic resist, the AX pick), and
  **Guardian** Hull Reinforcement.
- [[outfitting/module-reinforcement]] — standard and Guardian Module Reinforcement.
- [[outfitting/shield-cell-bank]] — active shield recharge.
- [[outfitting/guardian-shield-reinforcement]] — flat +MJ shield reinforcement.

Bulkheads give **no caustic resistance** (`causres 0` on every grade), so for AX work fit a
Meta-Alloy Hull Reinforcement for caustic protection.

## The Rank Gate

The Corvette cannot be bought until the commander reaches **Rear Admiral** in the Federal Navy
ranking — earned by running Federal-aligned missions and Navy promotion missions. This is the Federal
counterpart to the [[ships/imperial-cutter|Imperial Cutter]]'s **Duke** rank gate (the
[[ships/anaconda|Anaconda]] needs no rank at all). Plan the rank grind before committing to a
Corvette build.

## AX Build Notes — the large-pad gunship

The Corvette is the reference **large-pad** anti-Xeno platform — where the medium Chieftain/
Challenger/Krait line carries the AX kit, the Corvette carries far more of it:

- **AX weapons** on its seven hardpoints (including **two Huge** mounts): the kinetic
  [[outfitting/ax-multi-cannon]] and [[outfitting/ax-multi-cannon-enhanced|Enhanced]] version, the
  Guardian [[outfitting/guardian-gauss-cannon]] / [[outfitting/guardian-plasma-charger]] /
  [[outfitting/guardian-shard-cannon]] trio, the explosive [[outfitting/ax-missile-rack]] family,
  and the anti-swarm [[outfitting/remote-release-flak-launcher]] /
  [[outfitting/remote-release-flechette-launcher]]. The class-8 Power Distributor is what lets the
  Corvette run multiple high-draw Guardian weapons at once.
- **AX utilities** on its eight utility mounts: the [[outfitting/xeno-scanner]] (mandatory to
  target Interceptor hearts), the [[outfitting/shutdown-field-neutraliser]] (negates the EMP pulse),
  and the [[outfitting/caustic-sink-launcher]] (purges caustic DoT) — with mounts to spare for
  shield boosters. Add an optional-internal [[outfitting/decontamination-limpet-controller]] for
  sustained caustic removal.
- **AX defence** in the two class-5 Military slots and the deep optional bank.

AX combat zones, Spire sites and Titan wrecks all remain **live** — the Corvette is a current,
top-tier choice for all of them.

## Versus the medium AX hulls

- **Federal Corvette** — the **large-pad heavyweight**: two Huge hardpoints, class-8 PP/PD, 555 MJ
  base shield, hardness 70, eight utility mounts. Needs a large pad, ≈183 M CR, and the Rear Admiral
  rank gate. The firepower ceiling far exceeds any medium hull.
- **[[ships/alliance-challenger|Alliance Challenger]]** / **[[ships/krait-mk-ii|Krait Mk II]]** — the
  **medium-pad** AX brawlers: cheaper, dock anywhere, three Military slots (Challenger) or three
  Large hardpoints (Krait), but far less raw firepower and shield. Pick a medium when pad access and
  cost matter more than the Corvette's ceiling.
- **[[ships/federal-dropship]]** / **[[ships/federal-gunship]]** — the Corvette's own **medium-pad
  Federal stablemates** (Core Dynamics, rank-gated). The Dropship is the cheap base brawler
  (Midshipman gate); the Gunship is the heavy fighter-bay top variant (Ensign gate, seven mounts,
  three Military slots). Both are far cheaper, lower-gated medium steps below the large-pad Corvette.

## Acquisition

Sold at large stations carrying a shipyard, **once Rear Admiral rank is reached**. Engineer the FSD
for jump range at [[engineers/felicity-farseer]] (Increased Range). Check Spansh
(`spansh.co.uk/stations`) for nearest stock.

[[trunk]]
