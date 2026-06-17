---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/anaconda.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T02:30:00+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Anaconda

The Anaconda is **Faulcon DeLacy's large-pad do-everything flagship** — the classic jack-of-all-trades
that does combat, deep-space exploration and hauling all to a high standard, and a long-standing
anti-Xeno (AX) platform. It mounts **one Huge (class-4) hardpoint** (vs the
[[ships/federal-corvette|Federal Corvette]]'s two) but has the **most weapon mounts of the large-pad
trinity (eight)**, the **deepest optional bank**, and — uniquely among the large combat ships — **no
rank gate**: anyone with the credits can buy one. It also carries the **best stock jump range** of
the trinity thanks to its relatively light 400 t hull.

## Overview

- **Manufacturer:** Faulcon DeLacy (NOT Lakon)
- **Size class:** 3 (Large landing pad — needs a large-pad starport)
- **Role:** Multirole flagship — combat / exploration / hauling / large-pad AX
- **Hull cost:** 142,456,440 CR (hull only)
- **Retail cost:** 146,969,451 CR (with stock modules)
- **Crew seats:** 4 · **Ship-Launched Fighter bay** present
- **Requires:** nothing — **no rank gate** (no `requirements` block in the Coriolis data; credits only)

## Hull Stats

Source: Coriolis-data ship definition `anaconda` (edID 128049363).

- **Hull mass:** 400 t (light for a large-pad hull — the basis of its jump range)
- **Top speed:** 180 m/s · **Boost:** 240 m/s (slow — it is not an agile dogfighter)
- **Base shield strength:** 350 MJ
- **Base armour:** 525 (**the highest base armour of any KB ship**)
- **Hull hardness:** 65
- **Heat capacity:** 334
- **Mass lock factor:** 23 (high)
- **Manoeuvrability (deg/s):** pitch 25 · roll 60 · yaw 10 (sluggish — large hull, low roll)
- **Reserve fuel:** 1.07 t

## Slot Layout

- **Core internals:** Power Plant **8**, Thrusters 7, Frame Shift Drive 6, Life Support 5,
  Power Distributor **8**, Sensors **8**, Fuel Tank 5. The **class-8 Power Plant + class-8 Power
  Distributor** make it a genuine combat hull that can power and sustain a heavy energy-weapon bank.
  (Coriolis lists Sensors at class 8 — recorded verbatim per Tier-0 trust; flag for corroboration.)
- **Hardpoints:** **1 × Huge + 3 × Large + 2 × Medium + 2 × Small** (eight weapon mounts — the most
  of the large-pad trinity, though only one Huge vs the Corvette's two).
- **Utility mounts:** 8 (the reference 8-utility hull — room for a deep shield-booster stack plus
  chaff, heat sinks and point defence).
- **Optional internals:** sizes **7, 6, 6, 6, 5, 5, 5, 4, 4, 4, 2, 1** (twelve regular optionals)
  plus **one class-5 Military slot** plus a reserved class-1 **Planetary Approach Suite**.

### Military slot — one, class 5

Unlike the Corvette (two class-5 Military slots) and the Alliance AX trio (three class-4), the
Anaconda has **a single class-5 Military slot**. It accepts the same reinforcement set (per the
Coriolis data: mahr, hr, scb, mrp, gsrp, gmrp, ghrp):

- [[outfitting/hull-reinforcement]] — standard, **Meta-Alloy** (caustic resist, the AX pick), and
  **Guardian** Hull Reinforcement.
- [[outfitting/module-reinforcement]] — standard and Guardian Module Reinforcement.
- [[outfitting/shield-cell-bank]] — active shield recharge.
- [[outfitting/guardian-shield-reinforcement]] — flat +MJ shield reinforcement.

Bulkheads give **no caustic resistance** (`causres 0` on every grade), so for AX work fit a
Meta-Alloy Hull Reinforcement for caustic protection.

## No rank gate — and the best jump range

The Anaconda's defining advantages over its large-pad rivals are practical: it requires **no Navy
rank** (the Corvette needs Federal Rear Admiral, the Cutter needs Imperial Duke), and its light
400 t hull gives it the **longest stock jump range** of the three. Engineered for range, the Anaconda
was for years the default long-range explorer and remains an excellent one. That same light hull is
why it is the cheapest of the trinity to buy outright.

## AX Build Notes — the no-gate large-pad platform

The Anaconda is a current, top-tier large-pad anti-Xeno platform — the AX choice for commanders who
have not (or do not want to) grind a Navy rank:

- **AX weapons** across its eight hardpoints (including one Huge): the kinetic
  [[outfitting/ax-multi-cannon]] and [[outfitting/ax-multi-cannon-enhanced|Enhanced]] version, the
  Guardian [[outfitting/guardian-gauss-cannon]] / [[outfitting/guardian-plasma-charger]] /
  [[outfitting/guardian-shard-cannon]] trio, the explosive [[outfitting/ax-missile-rack]] family,
  and the anti-swarm [[outfitting/remote-release-flak-launcher]] /
  [[outfitting/remote-release-flechette-launcher]]. The class-8 Power Distributor powers multiple
  high-draw Guardian weapons at once.
- **AX utilities** on its eight utility mounts: the [[outfitting/xeno-scanner]] (mandatory to target
  Interceptor hearts), the [[outfitting/shutdown-field-neutraliser]] (negates the EMP pulse), and the
  [[outfitting/caustic-sink-launcher]] (purges caustic DoT) — with mounts to spare for shield
  boosters. Add an optional-internal [[outfitting/decontamination-limpet-controller]] for sustained
  caustic removal.
- **AX defence** in the class-5 Military slot and the deep twelve-slot optional bank.

AX combat zones, Spire sites and Titan wrecks all remain **live** — the Anaconda is a current choice
for all of them.

## The large-pad trinity

- **Anaconda** — the **no-gate jack-of-all-trades**: one Huge + most total mounts (eight), deepest
  optionals (twelve), best jump range, lightest/cheapest hull, **no rank gate**. Slow and not agile;
  one Military slot only. The flexible generalist.
- **[[ships/federal-corvette|Federal Corvette]]** — the **firepower king**: two Huge hardpoints,
  highest hardness (70), more agile, two class-5 Military slots. Gated behind Federal **Rear Admiral**.
  Pick it for raw combat ceiling.
- **[[ships/imperial-cutter|Imperial Cutter]]** — the **shield-tank/trader**: highest base shield
  (600 MJ), two class-8 optionals (massive cargo), but least agile and only one Huge. Gated behind
  Imperial **Duke**.

## Acquisition

Sold at large stations carrying a shipyard — **no rank required**. Engineer the FSD for jump range at
[[engineers/felicity-farseer]] (Increased Range). Check Spansh (`spansh.co.uk/stations`) for nearest
stock.

[[trunk]]
