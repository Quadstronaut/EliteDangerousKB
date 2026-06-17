---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/federal_dropship.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T04:51:20Z
source_count: 1
verified: false
availability: live
changed_note:
---

# Federal Dropship

The Federal Dropship is **Core Dynamics' base medium combat / troop-transport gunship** — the first
rung of the Federal medium combat line (Dropship → [[ships/federal-assault-ship|Assault Ship]] →
[[ships/federal-gunship|Gunship]]) and, until now, the only medium counterpart in this KB to the
large-pad Federal flagship [[ships/federal-corvette]]. It is a **slow, tanky, rank-gated brawler**:
580 t of hull, a heavy 300-armour shell, **two class-4 Military reinforcement slots**, and a
**1 Large + 4 Medium** hardpoint layout. Buying one requires the Federal Navy rank **Midshipman**.

## Overview

- **Manufacturer:** Core Dynamics
- **Size class:** 2 (Medium landing pad — docks at medium and large ports, including outposts)
- **Role:** Base medium combat / troop gunship; rank-gated tanky brawler
- **Rank requirement:** Federal Navy rank **Midshipman** (Coriolis `requirements.federationRank: 3`)
- **Hull cost:** 13,510,106 CR (hull only)
- **Retail cost:** 14,314,210 CR (with stock modules)
- **Crew seats:** 2 (pilot + one multicrew seat) · **no Ship-Launched Fighter bay**

## Hull Stats

Source: Coriolis-data ship definition `federal_dropship` (edID 128049321, eddbID 9).

- **Hull mass:** 580 t — heavy for a medium hull, the source of its famously sluggish feel.
- **Top speed:** 180 m/s · **Boost:** 300 m/s — slow; the Dropship trades pace for armour.
- **Base shield strength:** 200 MJ · **Base armour:** 300 — a tanky medium, built to soak fire.
- **Hull hardness:** 60 (good penetration resistance for a medium).
- **Heat capacity:** 331
- **Mass lock factor:** 14
- **Manoeuvrability (deg/s):** pitch 30 · roll 80 · yaw 14 — ponderous, in keeping with the mass.
- **Reserve fuel:** 0.83 t

## Slot Layout

- **Core internals:** Power Plant **6**, Thrusters **6**, Frame Shift Drive **5**, Life Support **5**,
  Power Distributor **6**, Sensors **4**, Fuel Tank **4**. A class-6 plant and distributor on a
  medium hull comfortably power the weapon bank.
- **Hardpoints:** **1 × Large + 4 × Medium** (five weapon mounts) — note **only one Large** mount;
  the firepower comes from the quartet of Mediums, not big-calibre slots.
- **Utility mounts:** 4 (shield boosters, chaff, heat sinks, point defence).
- **Optional internals:** sizes 6, 5, 5, 4, 3, 3, 2, 1 (eight regular slots, top class-6) plus a
  reserved class-1 **Planetary Approach Suite**.
- **Military slots:** **two class-4** (see below).

### Military slots

The Dropship's **two class-4 Military slots** are the hallmark of a Federal combat hull (the
[[ships/federal-gunship]] adds a third). Per the Coriolis data both accept the same reinforcement
set (mahr, hr, scb, mrp, gsrp, gmrp, ghrp):

- [[outfitting/hull-reinforcement]] — standard, **Meta-Alloy** (caustic resist, the AX pick), and
  **Guardian** Hull Reinforcement.
- [[outfitting/module-reinforcement]] — standard and Guardian Module Reinforcement.
- [[outfitting/shield-cell-bank]] — active shield recharge.
- [[outfitting/guardian-shield-reinforcement]] — flat +MJ shield reinforcement.

Bulkheads carry **no caustic resistance** (`causres 0` on every grade), so for AX work fit a
Meta-Alloy Hull Reinforcement.

## The Federal medium combat line

The Dropship is the **base airframe** of Core Dynamics' three medium gunships, all class-2 (medium
pad), all 580 t, all rank-gated:

- **Federal Dropship** (this page) — the base variant: **Midshipman** gate, 1 Large + 4 Medium
  (5 mounts), two class-4 Military slots, **no fighter bay**, the cheapest of the three at ~13.5 M CR.
- **[[ships/federal-assault-ship]]** — the speed/agility variant (the mid-trio hull; not yet paged).
- **[[ships/federal-gunship]]** — the heavy top variant: **Ensign** gate, 1 Large + 4 Medium + 2 Small
  (7 mounts — the most of the three), **three** class-4 Military slots, a class-7 Power Distributor,
  and a Ship-Launched Fighter bay; slower (170/280) and far pricier (~34.8 M CR).

Where the [[ships/federal-corvette]] is the **large-pad** Federal flagship (two Huge hardpoints,
class-8 PP/PD, Rear Admiral gate), the Dropship/Gunship are the **medium-pad** Federal combat hulls —
the Federal counterpart to the Alliance medium AX trio ([[ships/alliance-chieftain]] /
[[ships/alliance-challenger]] / [[ships/alliance-crusader]]).

## Build notes

The Dropship is a **budget tank brawler**. Its low speed means it fights by absorbing damage rather
than dodging it: stack a bi-weave shield with boosters in the four utility slots, fill the two class-4
Military slots with Hull/Module Reinforcement, and arm the 1 Large + 4 Medium mounts with gimballed
multi-cannons or pulse lasers. AX combat zones, Spire sites and Titan wrecks remain **live**, so a
Meta-Alloy HRP in a Military slot plus AX weapons turns it into an affordable rank-gated AX medium —
though the [[ships/alliance-chieftain]] line is the more agile AX choice. Engineer the FSD for jump
range at [[engineers/felicity-farseer]] if you want it to self-deploy.

## Acquisition

Sold at shipyards in Federal space (and many others), **once Federal Navy rank Midshipman is
reached** (`federationRank` 3) — earned through Federal-aligned and Navy promotion missions. It needs
a **Medium** pad (or larger), so it docks at outposts the large-pad Corvette cannot. Check Spansh
(`spansh.co.uk/stations`) for the nearest source.

[[trunk]]
