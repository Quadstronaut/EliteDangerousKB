---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/alliance_challenger.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T02:09:29+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Alliance Challenger

The Alliance Challenger is a **medium-class combat ship** built by **Lakon Spaceways** for the
Alliance — the **tankiest** of the Alliance trio and the heavier sibling of the
[[ships/alliance-chieftain|Alliance Chieftain]]. It trades the Chieftain's agility for more
hull, more shield and a deeper optional-internal bank, while keeping the same defining feature:
**three class-4 Military slots** for stacking anti-Xeno (AX) reinforcement. Requires **Horizons**.

## Overview

- **Manufacturer:** Lakon Spaceways (Alliance-aligned)
- **Size class:** 2 (Medium landing pad — docks at outposts and all larger ports)
- **Role:** Combat / anti-Xeno (AX) heavy brawler
- **Hull cost:** 29,569,804 CR (hull only)
- **Retail cost:** 30,472,252 CR (with stock modules)
- **Crew seats:** 2 (pilot + one multicrew seat; **no Ship-Launched Fighter bay**)
- **Requires:** Horizons

## Hull Stats

Source: Coriolis-data ship definition `alliance_challenger` (edID 128816588).

- **Hull mass:** 450 t
- **Top speed:** 204 m/s · **Boost:** 310 m/s
- **Base shield strength:** 220 MJ
- **Base armour:** 300 · **Hull hardness:** 65 (high — resists armour penetration well)
- **Heat capacity:** 316
- **Mass lock factor:** 13
- **Manoeuvrability (deg/s):** pitch 32 · roll 90 · yaw 16
- **Reserve fuel:** 0.77 t

## Slot Layout

- **Core internals:** Power Plant **6**, Thrusters **6**, Frame Shift Drive **5**,
  Life Support **5**, Power Distributor **6**, Sensors **4**, Fuel Tank **4**
  (same core layout as the Chieftain).
- **Hardpoints:** **1 × Large + 3 × Medium + 3 × Small** (seven weapon mounts).
- **Utility mounts:** 4.
- **Optional internals:** sizes **6, 6, 3, 3, 2, 2, 1** plus **three class-4 Military slots** plus a
  reserved class-1 **Planetary Approach Suite** (planet-landing and SRV capable).

### Military slots — the Alliance AX trait

Like the Chieftain, the Challenger carries **three class-4 Military slots** that accept only
reinforcement/defence modules (not cargo, fuel or utility kit). Eligible modules per the Coriolis
data:

- [[outfitting/hull-reinforcement]] — standard, **Meta-Alloy** (caustic resist, the AX pick), and
  **Guardian** Hull Reinforcement variants.
- [[outfitting/module-reinforcement]] — standard and Guardian Module Reinforcement.
- [[outfitting/shield-cell-bank]] — active shield recharge.
- [[outfitting/guardian-shield-reinforcement]] — flat +MJ shield reinforcement.

Stacking the defence trio in the Military slots — without spending cargo/utility internals — is
why the Alliance hulls tank Thargoid damage so well. Bulkheads give **no caustic resistance**
(`causres 0` on every grade: Lightweight/Reinforced/Military/Mirrored/Reactive), so fit a
Meta-Alloy Hull Reinforcement for AX caustic protection.

## AX Build Notes — the hull these modules go on

The Challenger is the reference **heavy** medium-pad anti-Xeno platform. Its seven hardpoints carry
the AX weapon line, its four utility mounts carry the AX survival kit, and its Military slots stack
the defence trio:

- **AX weapons** on the 1 L + 3 M + 3 S hardpoints: the kinetic [[outfitting/ax-multi-cannon]]
  (and the [[outfitting/ax-multi-cannon-enhanced|Enhanced]] gimballed version), the Guardian
  [[outfitting/guardian-gauss-cannon]] / [[outfitting/guardian-plasma-charger]] /
  [[outfitting/guardian-shard-cannon]] trio, the explosive [[outfitting/ax-missile-rack]] family,
  and the anti-swarm [[outfitting/remote-release-flak-launcher]] /
  [[outfitting/remote-release-flechette-launcher]]. With only one Large mount, the Challenger
  leans on its **three Medium mounts** rather than big-gun firepower.
- **AX utilities** on the 4 utility mounts: the [[outfitting/xeno-scanner]] (mandatory to target
  Interceptor hearts), the [[outfitting/shutdown-field-neutraliser]] (negates the EMP pulse), and
  the [[outfitting/caustic-sink-launcher]] (purges caustic DoT). Add an optional-internal
  [[outfitting/decontamination-limpet-controller]] for sustained caustic removal.
- **AX defence** in the Military slots: see the list above.

AX combat zones, Spire sites and Titan wrecks all remain **live** — the Challenger is a current,
relevant choice for all of them.

## Versus the Alliance Chieftain

Both are class-2 medium-pad Alliance AX hulls with three Military slots, the same core-slot
layout and the same hull hardness (**65**); pick by playstyle:

- **Alliance Challenger** — the **tank**: heavier (hull mass 450 vs 400), more armour (300 vs 280),
  more shield (220 vs 200), more heat capacity (316 vs 289), and a deeper optional bank (seven
  regular optionals including **two class-6** slots vs the Chieftain's six). It also has **more
  weapon mounts overall** (7: 1 L + 3 M + 3 S) but **fewer Large** (1 vs the Chieftain's 2). Costs
  more (≈29.6 M vs ≈18.6 M CR hull).
- **[[ships/alliance-chieftain|Alliance Chieftain]]** — the **brawler**: lighter and far more
  agile (roll 92 / pitch 39 vs 90 / 32), faster (230 / 330 vs 204 / 310), and cheaper, with two
  Large hardpoints for bigger guns. Pick it when turn rate and big-gun punch beat raw durability.

> The third Alliance sibling is the [[ships/alliance-crusader|Alliance Crusader]] — the
> multicrew/fighter-bay variant (crew 4, the only Alliance medium with a Ship-Launched Fighter bay),
> at the cost of being the slowest and least agile of the trio.

## Acquisition

Sold at large stations carrying a shipyard. Engineer the FSD for jump range at
[[engineers/felicity-farseer]] (Increased Range). Check Spansh (`spansh.co.uk/stations`) for
nearest stock.

[[trunk]]
