---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/federal_gunship.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T04:51:20Z
source_count: 1
verified: false
availability: live
changed_note:
---

# Federal Gunship

The Federal Gunship is **Core Dynamics' heavy, fighter-bay medium gunship** — the up-armed top
variant of the [[ships/federal-dropship]] airframe and the most heavily armed of the Federal medium
combat line. It keeps the Dropship's 580 t hull but adds firepower, defence and a **Ship-Launched
Fighter bay**: a **1 Large + 4 Medium + 2 Small** seven-mount loadout (the most weapon mounts of any
Federal medium), **three class-4 Military slots**, a **class-7 Power Distributor** to feed them, and
heavier shield and armour. It is the slowest of the three and the most rank-gated — purchase requires
Federal Navy rank **Ensign**.

## Overview

- **Manufacturer:** Core Dynamics
- **Size class:** 2 (Medium landing pad — docks at medium and large ports, including outposts)
- **Role:** Heavy medium gunship with a Ship-Launched Fighter bay; rank-gated brawler
- **Rank requirement:** Federal Navy rank **Ensign** (Coriolis `requirements.federationRank: 7`) —
  higher than the [[ships/federal-dropship]]'s Midshipman (3).
- **Hull cost:** 34,814,912 CR (hull only)
- **Retail cost:** 35,814,210 CR (with stock modules)
- **Crew seats:** 2 (pilot + one multicrew seat) · **Ship-Launched Fighter bay present**

## Hull Stats

Source: Coriolis-data ship definition `federal_gunship` (edID 128672152, eddbID 10).

- **Hull mass:** 580 t — the same airframe as the [[ships/federal-dropship]]; heavy and sluggish.
- **Top speed:** 170 m/s · **Boost:** 280 m/s — the **slowest of the Federal mediums** (the Dropship
  manages 180/300). It fights by tanking, not by chasing.
- **Base shield strength:** 250 MJ · **Base armour:** 350 — both higher than the Dropship's 200/300;
  the Gunship is the tankier sibling.
- **Hull hardness:** 60
- **Heat capacity:** 325
- **Mass lock factor:** 14
- **Manoeuvrability (deg/s):** pitch 25 · roll 80 · yaw 18 — ponderous in pitch, the airframe's mass
  showing.
- **Reserve fuel:** 0.82 t

## Slot Layout

- **Core internals:** Power Plant **6**, Thrusters **6**, Frame Shift Drive **5**, Life Support **5**,
  Power Distributor **7**, Sensors **5**, Fuel Tank **4**. The **class-7 Power Distributor** (vs the
  Dropship's PD6) is the upgrade that sustains the larger weapon bank.
- **Hardpoints:** **1 × Large + 4 × Medium + 2 × Small** (seven weapon mounts) — the **most weapon
  mounts of any Federal medium** (the Dropship has five; the two extra Small mounts are the Gunship's
  addition).
- **Utility mounts:** 4 (shield boosters, chaff, heat sinks, point defence).
- **Optional internals:** sizes 6, 6, 2, 2, 1 (six regular slots, top two class-6) plus a reserved
  class-1 **Planetary Approach Suite**. Note the Gunship trades internal depth — only **six** regular
  optionals vs the Dropship's eight — for its extra Military slot and the fighter bay.
- **Military slots:** **three class-4** (see below).

### Military slots

The Gunship's **three class-4 Military slots** are one more than the [[ships/federal-dropship]]'s two
— the deepest dedicated reinforcement bank of the Federal medium line. Per the Coriolis data all three
accept the same set (mahr, hr, scb, mrp, gsrp, gmrp, ghrp):

- [[outfitting/hull-reinforcement]] — standard, **Meta-Alloy** (caustic resist, the AX pick), and
  **Guardian** Hull Reinforcement.
- [[outfitting/module-reinforcement]] — standard and Guardian Module Reinforcement.
- [[outfitting/shield-cell-bank]] — active shield recharge.
- [[outfitting/guardian-shield-reinforcement]] — flat +MJ shield reinforcement.

Bulkheads carry **no caustic resistance** (`causres 0` on every grade), so for AX work fit a
Meta-Alloy Hull Reinforcement.

## The Federal medium combat line

The Gunship is the **heavy top variant** of Core Dynamics' three medium gunships — all class-2
(medium pad), all 580 t, all rank-gated:

- **[[ships/federal-dropship]]** — the base variant: Midshipman gate, 1 Large + 4 Medium (5 mounts),
  two class-4 Military slots, **no fighter bay**, eight regular optionals, ~13.5 M CR.
- **[[ships/federal-assault-ship]]** — the speed/agility mid-trio variant (not yet paged).
- **Federal Gunship** (this page) — the heavy top variant: **Ensign** gate, 1 Large + 4 Medium +
  2 Small (7 mounts), **three** class-4 Military slots, class-7 PD, **a fighter bay**, but slower
  (170/280) and far pricier (~34.8 M CR), with only six regular optionals.

Where the [[ships/federal-corvette]] is the **large-pad** Federal flagship (two Huge hardpoints,
class-8 PP/PD, Rear Admiral gate), the Gunship is the heaviest **medium-pad** Federal combat hull —
the Federal counterpart to the multicrew [[ships/alliance-crusader]] (the only fighter-bay hull of
the Alliance medium AX trio with [[ships/alliance-chieftain]] / [[ships/alliance-challenger]]).

## Build notes

The Gunship is a **medium-pad gun platform**. With seven hardpoints and a class-7 distributor it can
run a heavier, more varied weapon mix than the Dropship — pair fixed big-hitters in the Large/Medium
mounts with the two Small mounts for utility weapons or extra multi-cannons. Fill the three class-4
Military slots with Hull/Module Reinforcement for a deep tank, run a bi-weave shield with boosters in
the four utility slots, and deploy the Ship-Launched Fighter to split enemy fire. AX combat zones,
Spire sites and Titan wrecks remain **live** — fit a Meta-Alloy HRP plus AX weapons and the Gunship
becomes a durable rank-gated AX medium, trading the [[ships/alliance-chieftain]]'s agility for raw
mount count and a fighter bay. The shallow six-slot optional bank is the trade-off: cargo/range builds
favour the Dropship or the Alliance hulls.

## Acquisition

Sold at shipyards in Federal space (and many others), **once Federal Navy rank Ensign is reached**
(`federationRank` 7) — a deeper grind than the Dropship's Midshipman. It needs a **Medium** pad (or
larger), so it docks at outposts the large-pad Corvette cannot. Check Spansh
(`spansh.co.uk/stations`) for the nearest source.

[[trunk]]
