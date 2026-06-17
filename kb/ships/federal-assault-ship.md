---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/federal_assault_ship.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T04:59:43Z
source_count: 1
verified: false
availability: live
changed_note:
---

# Federal Assault Ship

The Federal Assault Ship is **Core Dynamics' speed-and-agility variant of the Federal medium combat
line** — the middle hull of the trio (base [[ships/federal-dropship]] → **Assault Ship** → heavy
[[ships/federal-gunship]]). Where its siblings are 580 t tanks, the Assault Ship is a **lighter 480 t
skirmisher**: the **fastest and most manoeuvrable** of the three, and the only one carrying **two Large
hardpoints**. It trades mount count and internal depth for pace and big-calibre punch. Buying one
requires the Federal Navy rank **Chief Petty Officer**.

## Overview

- **Manufacturer:** Core Dynamics
- **Size class:** 2 (Medium landing pad — docks at medium and large ports, including outposts)
- **Role:** Speed/agility medium combat hull; rank-gated assault skirmisher
- **Rank requirement:** Federal Navy rank **Chief Petty Officer** (Coriolis `requirements.federationRank: 5`)
  — between the [[ships/federal-dropship]]'s Midshipman (3) and the [[ships/federal-gunship]]'s Ensign (7).
- **Hull cost:** 19,111,109 CR (hull only)
- **Retail cost:** 19,814,210 CR (with stock modules)
- **Crew seats:** 2 (pilot + one multicrew seat) · **no Ship-Launched Fighter bay**

## Hull Stats

Source: Coriolis-data ship definition `federal_assault_ship` (edID 128672145, eddbID 8).

- **Hull mass:** 480 t — **100 t lighter than both Federal-medium siblings** (each 580 t). The Assault
  Ship is NOT the same airframe mass as the Dropship/Gunship; the reduced mass is the basis of its
  speed and agility edge.
- **Top speed:** 210 m/s · **Boost:** 350 m/s — the **fastest of the Federal medium trio** (Dropship
  180/300, Gunship 170/280).
- **Base shield strength:** 200 MJ · **Base armour:** 300 — ties the Dropship; below the Gunship's
  250/350. The Assault Ship is the brawler, not the tank.
- **Hull hardness:** 60 (same across the trio).
- **Heat capacity:** 286 — the **lowest of the three** (Dropship 331, Gunship 325); it runs hotter, so
  manage heat under sustained fire.
- **Mass lock factor:** 14
- **Manoeuvrability (deg/s):** pitch 38 · roll 90 · yaw 19 — the **most agile of the Federal mediums**
  (Dropship 30/80/14, Gunship 25/80/18). The defining trait of the variant.
- **Reserve fuel:** 0.72 t

## Slot Layout

- **Core internals:** Power Plant **6**, Thrusters **6**, Frame Shift Drive **5**, Life Support **5**,
  Power Distributor **6**, Sensors **4**, Fuel Tank **4** — an **identical core layout to the
  [[ships/federal-dropship]]** (the Gunship steps the distributor up to class-7 and sensors to class-5
  to feed its larger weapon bank).
- **Hardpoints:** **2 × Large + 2 × Medium** (four weapon mounts) — **fewer mounts than either sibling**
  (Dropship 5, Gunship 7), BUT the only Federal medium with **two Large** hardpoints (the Dropship and
  Gunship each carry a single Large). The Assault Ship trades mount count for bigger-calibre slots.
- **Utility mounts:** 4 (shield boosters, chaff, heat sinks, point defence).
- **Optional internals:** sizes 5, 5, 4, 3, 2, 2, 1 (seven regular slots, top two class-5) plus a
  reserved class-1 **Planetary Approach Suite** — between the Dropship's eight and the Gunship's six.
- **Military slots:** **two class-4** (see below).

### Military slots

The Assault Ship's **two class-4 Military slots** match the [[ships/federal-dropship]]'s count (the
[[ships/federal-gunship]] adds a third). Per the Coriolis data both accept the same reinforcement set
(mahr, hr, scb, mrp, gsrp, gmrp, ghrp):

- [[outfitting/hull-reinforcement]] — standard, **Meta-Alloy** (caustic resist, the AX pick), and
  **Guardian** Hull Reinforcement.
- [[outfitting/module-reinforcement]] — standard and Guardian Module Reinforcement.
- [[outfitting/shield-cell-bank]] — active shield recharge.
- [[outfitting/guardian-shield-reinforcement]] — flat +MJ shield reinforcement.

Bulkheads carry **no caustic resistance** (`causres 0` on every grade), so for AX work fit a
Meta-Alloy Hull Reinforcement.

## The Federal medium combat line

The Assault Ship is the **speed/agility middle variant** of Core Dynamics' three medium gunships — all
class-2 (medium pad), all rank-gated, but **NOT all the same mass** (the Assault Ship is 480 t; its
siblings are 580 t):

- **[[ships/federal-dropship]]** — the base variant: **Midshipman** gate, 580 t, 1 Large + 4 Medium
  (5 mounts), two class-4 Military slots, eight regular optionals, **no fighter bay**, ~13.5 M CR.
- **Federal Assault Ship** (this page) — the speed/agility variant: **Chief Petty Officer** gate, the
  lightest at **480 t**, fastest (210/350) and most agile, **2 Large + 2 Medium** (4 mounts — fewest,
  but the only two-Large layout), two class-4 Military slots, seven regular optionals, **no fighter
  bay**, ~19.1 M CR.
- **[[ships/federal-gunship]]** — the heavy top variant: **Ensign** gate, 580 t, 1 Large + 4 Medium +
  2 Small (7 mounts — the most), **three** class-4 Military slots, a class-7 Power Distributor and a
  Ship-Launched Fighter bay; slowest (170/280) and priciest (~34.8 M CR), six regular optionals.

Where the [[ships/federal-corvette]] is the **large-pad** Federal flagship (two Huge hardpoints,
class-8 PP/PD, Rear Admiral gate), the Dropship/Assault Ship/Gunship are the **medium-pad** Federal
combat hulls — the Federal counterpart to the Alliance medium AX trio ([[ships/alliance-chieftain]] /
[[ships/alliance-challenger]] / [[ships/alliance-crusader]]).

## Build notes

The Assault Ship is the **agile gunfighter** of the Federal mediums. Its lighter mass and best-in-trio
turn rate let it hold an angle the tankier siblings cannot, and the two Large hardpoints put real
broadside weight behind a four-mount loadout — pair gimballed or fixed Large weapons with two Medium
support guns. Stack a bi-weave shield with boosters in the four utility slots and fill the two class-4
Military slots with Hull/Module Reinforcement for survivability without killing the agility. Watch the
lower heat capacity (286) under sustained fire — keep a heat sink in a utility slot. AX combat zones,
Spire sites and Titan wrecks remain **live**, so a Meta-Alloy HRP plus AX weapons makes it a nimble
rank-gated AX medium, though the [[ships/alliance-chieftain]] line is still the lighter, faster AX
pick. Engineer the FSD at [[engineers/felicity-farseer]] for jump range if you want it to self-deploy.

## Acquisition

Sold at shipyards in Federal space (and many others), **once Federal Navy rank Chief Petty Officer is
reached** (`federationRank` 5) — a deeper grind than the Dropship's Midshipman, but short of the
Gunship's Ensign. It needs a **Medium** pad (or larger), so it docks at outposts the large-pad Corvette
cannot. Check Spansh (`spansh.co.uk/stations`) for the nearest source.

[[trunk]]
