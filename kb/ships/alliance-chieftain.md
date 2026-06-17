---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/alliance_chieftain.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T02:00:10+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Alliance Chieftain

The Alliance Chieftain is a **medium-class combat ship** built by **Lakon Spaceways** for the
Alliance. It is the iconic medium-pad **anti-Xeno (AX) brawler**: agile, tough, and — uniquely
among medium hulls — fitted with **three Military internal slots** that take only reinforcement
and defence modules. That combination of high hull hardness, a strong roll rate, and stacked
reinforcement makes it the platform of choice for carrying the KB's AX weapon and utility line
into Thargoid combat. Requires **Horizons**. Its tankier, slower sibling is the
[[ships/alliance-challenger|Alliance Challenger]].

## Overview

- **Manufacturer:** Lakon Spaceways (Alliance-aligned)
- **Size class:** 2 (Medium landing pad — docks at outposts and all larger ports)
- **Role:** Combat / anti-Xeno (AX) multirole brawler
- **Hull cost:** 18,612,476 CR (hull only)
- **Retail cost:** 19,382,252 CR (with stock modules)
- **Crew seats:** 2 (pilot + one multicrew seat; **no Ship-Launched Fighter bay**)
- **Requires:** Horizons

## Hull Stats

Source: Coriolis-data ship definition `alliance_chieftain` (edID 128816574).

- **Hull mass:** 400 t
- **Top speed:** 230 m/s · **Boost:** 330 m/s
- **Base shield strength:** 200 MJ
- **Base armour:** 280 · **Hull hardness:** 65 (high — resists armour penetration well)
- **Heat capacity:** 289
- **Mass lock factor:** 13
- **Manoeuvrability (deg/s):** pitch 39 · **roll 92** (very agile) · yaw 16
- **Reserve fuel:** 0.77 t

## Slot Layout

- **Core internals:** Power Plant **6**, Thrusters **6**, Frame Shift Drive **5**,
  Life Support **5**, Power Distributor **6**, Sensors **4**, Fuel Tank **4**.
  The class-6 power distributor sustains energy weapons, boosting and shield cells under load.
- **Hardpoints:** **2 × Large + 1 × Medium + 3 × Small** (six weapon mounts).
- **Utility mounts:** 4.
- **Optional internals:** sizes **6, 5, 4, 2, 2, 1** plus **three class-4 Military slots** plus a
  reserved class-1 **Planetary Approach Suite** (planet-landing and SRV capable).

### Military slots — the Chieftain's defining trait

The three class-4 **Military slots** accept only reinforcement/defence modules (not cargo, fuel,
or utility kit). Eligible modules per the Coriolis data:

- [[outfitting/hull-reinforcement]] — standard, **Meta-Alloy** (caustic resist, the AX pick), and
  **Guardian** Hull Reinforcement variants.
- [[outfitting/module-reinforcement]] — standard and Guardian Module Reinforcement.
- [[outfitting/shield-cell-bank]] — active shield recharge.
- [[outfitting/guardian-shield-reinforcement]] — flat +MJ shield reinforcement.

Stacking these in the Military slots (without sacrificing cargo/utility internals) is why the
Chieftain tanks Thargoid damage so well. Bulkheads give **no caustic resistance** (`causres 0` on
every grade), so fit a Meta-Alloy Hull Reinforcement for AX caustic protection.

## AX Build Notes — the hull these modules go on

The Chieftain is the reference medium-pad **anti-Xeno** platform. Its six hardpoints carry the
AX weapon line, its four utility mounts carry the AX survival kit, and its Military slots stack
the defence trio:

- **AX weapons** on the 2 L + 1 M + 3 S hardpoints: the kinetic [[outfitting/ax-multi-cannon]]
  (and the [[outfitting/ax-multi-cannon-enhanced|Enhanced]] gimballed version), the Guardian
  [[outfitting/guardian-gauss-cannon]] / [[outfitting/guardian-plasma-charger]] /
  [[outfitting/guardian-shard-cannon]] trio, the explosive [[outfitting/ax-missile-rack]] family,
  and the anti-swarm [[outfitting/remote-release-flak-launcher]] /
  [[outfitting/remote-release-flechette-launcher]].
- **AX utilities** on the 4 utility mounts: the [[outfitting/xeno-scanner]] (mandatory to target
  Interceptor hearts), the [[outfitting/shutdown-field-neutraliser]] (negates the EMP pulse), and
  the [[outfitting/caustic-sink-launcher]] (purges caustic DoT). Add an optional-internal
  [[outfitting/decontamination-limpet-controller]] for sustained caustic removal.
- **AX defence** in the Military slots: see the list above.

AX combat zones, Spire sites and Titan wrecks all remain **live** — the Chieftain is a current,
relevant choice for all of them.

## Versus the Krait Mk II

The other popular medium-pad AX hull is the [[ships/krait-mk-ii]]. The Chieftain trades raw
firepower and cargo for **survivability and agility**: it has fewer/smaller hardpoints
(2 L + 1 M + 3 S vs the Krait's 3 L + 2 M) and smaller optional internals, but **higher hull
hardness (65 vs 55)**, three dedicated **Military reinforcement slots** (the Krait has none), and
a far better roll rate (92 vs 90, with much stronger pitch/yaw). Pick the Chieftain to out-tank
and out-turn in a dogfight; pick the Krait for more guns, a fighter bay and multirole flexibility.

## Acquisition

Sold at large stations carrying a shipyard. Engineer the FSD for jump range at
[[engineers/felicity-farseer]] (Increased Range). Check Spansh (`spansh.co.uk/stations`) for
nearest stock.

[[trunk]]
