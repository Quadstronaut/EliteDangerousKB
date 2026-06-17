---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/alliance_crusader.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T02:21:19+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Alliance Crusader

The Alliance Crusader is a **medium-class combat ship** built by **Lakon Spaceways** for the
Alliance — the **multicrew / Ship-Launched Fighter** member of the Alliance trio, completing the set
alongside the agile [[ships/alliance-chieftain|Alliance Chieftain]] and the tanky
[[ships/alliance-challenger|Alliance Challenger]]. It is the **only Alliance medium with a fighter
hangar**, seats a **full four-person crew**, and keeps the trio's defining trait: **three class-4
Military slots** for stacking anti-Xeno (AX) reinforcement. The cost is mobility — it is the
**slowest and least agile** of the three. Requires **Horizons**.

## Overview

- **Manufacturer:** Lakon Spaceways (Alliance-aligned)
- **Size class:** 2 (Medium landing pad — docks at outposts and all larger ports)
- **Role:** Combat / anti-Xeno (AX) multicrew platform with a fighter bay
- **Hull cost:** 22,096,565 CR (hull only)
- **Retail cost:** 22,866,341 CR (with stock modules)
- **Crew seats:** 4 (pilot + multicrew; **Ship-Launched Fighter bay** present)
- **Requires:** Horizons

## Hull Stats

Source: Coriolis-data ship definition `alliance_crusader` (edID 128816581).

- **Hull mass:** 500 t (heaviest of the Alliance trio)
- **Top speed:** 180 m/s · **Boost:** 300 m/s (slowest of the trio)
- **Base shield strength:** 200 MJ
- **Base armour:** 300 · **Hull hardness:** 65 (high — resists armour penetration well)
- **Heat capacity:** 316
- **Mass lock factor:** 13
- **Manoeuvrability (deg/s):** pitch 32 · roll 80 · yaw 16 (least agile of the trio)
- **Reserve fuel:** 0.77 t

## Slot Layout

- **Core internals:** Power Plant **6**, Thrusters **6**, Frame Shift Drive **5**,
  Life Support **5**, Power Distributor **6**, Sensors **4**, Fuel Tank **4**
  (identical core layout to the Chieftain and Challenger).
- **Hardpoints:** **1 × Large + 2 × Medium + 3 × Small** (six weapon mounts).
- **Utility mounts:** 4.
- **Optional internals:** sizes **6, 5, 3, 3, 2, 2, 1** plus **three class-4 Military slots** plus a
  reserved class-1 **Planetary Approach Suite** (planet-landing and SRV capable).

### Military slots — the Alliance AX trait

Like both siblings, the Crusader carries **three class-4 Military slots** that accept only
reinforcement/defence modules (not cargo, fuel or utility kit). Eligible modules per the Coriolis
data:

- [[outfitting/hull-reinforcement]] — standard, **Meta-Alloy** (caustic resist, the AX pick), and
  **Guardian** Hull Reinforcement variants.
- [[outfitting/module-reinforcement]] — standard and Guardian Module Reinforcement.
- [[outfitting/shield-cell-bank]] — active shield recharge.
- [[outfitting/guardian-shield-reinforcement]] — flat +MJ shield reinforcement.

Stacking the defence trio in the Military slots — without spending cargo/utility internals — is why
the Alliance hulls tank Thargoid damage so well. Bulkheads give **no caustic resistance**
(`causres 0` on every grade: Lightweight/Reinforced/Military/Mirrored/Reactive), so fit a Meta-Alloy
Hull Reinforcement for AX caustic protection.

## The Fighter Bay — what sets the Crusader apart

The Crusader is the **only Alliance medium hull with a Ship-Launched Fighter bay**
(`fighterHangars: true`) and a **four-seat crew**. That makes it the trio's natural **multicrew**
ship: a hired or wing-mate NPC/CMDR can fly a deployed fighter while the pilot focuses fire, doubling
the effective gun count against a Thargoid Interceptor. In exchange it is the slowest (180 m/s vs the
Chieftain's 230) and least manoeuvrable (roll 80 vs 92) of the three, and carries the fewest total
weapon mounts (six vs the Challenger's seven). Note that for a cheaper way into *just* a fighter bay,
the [[ships/keelback]] (~3 M CR) is the cheapest fighter-bay-capable hull in the KB — the Crusader is the
cheapest with the full AX/multicrew package, not the cheapest SLF carrier overall.

## AX Build Notes — the hull these modules go on

The Crusader is the **multicrew** medium-pad anti-Xeno platform. Its six hardpoints carry the AX
weapon line, its four utility mounts carry the AX survival kit, its Military slots stack the defence
trio, and its fighter bay adds a second gun:

- **AX weapons** on the 1 L + 2 M + 3 S hardpoints: the kinetic [[outfitting/ax-multi-cannon]]
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

AX combat zones, Spire sites and Titan wrecks all remain **live** — the Crusader is a current,
relevant choice for all of them.

## Versus the Chieftain and Challenger

All three are class-2 medium-pad Alliance AX hulls with the same core-slot layout, the same hull
hardness (**65**) and **three class-4 Military slots**; pick by playstyle:

- **Alliance Crusader** — the **multicrew gunship**: the only one with a **fighter bay** and a
  **four-seat crew**, with a deep optional bank (seven regular optionals incl. one class-6 and one
  class-5). The trade-off is speed and agility — it is the slowest (180/300) and least nimble
  (roll 80). Six weapon mounts (1 L + 2 M + 3 S). Hull ≈22.1 M CR.
- **[[ships/alliance-challenger|Alliance Challenger]]** — the **tank**: most hull/shield and the
  deepest optional bank (two class-6 slots), seven weapon mounts (1 L + 3 M + 3 S) but no fighter
  bay (crew 2). Hull ≈29.6 M CR.
- **[[ships/alliance-chieftain|Alliance Chieftain]]** — the **brawler**: lightest and most agile
  (roll 92), fastest (230/330), cheapest (≈18.6 M CR), and the only one with **two Large**
  hardpoints for big-gun punch. No fighter bay (crew 2).

For a step up to a **large-pad** AX platform with far more firepower, see the
[[ships/federal-corvette|Federal Corvette]].

## Acquisition

Sold at large stations carrying a shipyard. Engineer the FSD for jump range at
[[engineers/felicity-farseer]] (Increased Range). Check Spansh (`spansh.co.uk/stations`) for nearest
stock.

[[trunk]]
