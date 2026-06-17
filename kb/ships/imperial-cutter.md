---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/imperial_cutter.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T02:30:30+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Imperial Cutter

The Imperial Cutter is **Gutamaya's large-pad flagship** — the Imperial counterpart to the
[[ships/federal-corvette|Federal Corvette]] and the third member of the large-pad combat trinity. It
is the game's premier **shield-tank and bulk trader**: it carries the **highest base shield in this
KB (600 MJ)** and **two class-8 optional internals** for enormous cargo or shield capacity, but pays
for it with the **least agility of any KB ship** and only **one Huge hardpoint** (vs the Corvette's
two). Purchase is **rank-gated** behind Imperial Navy rank **Duke**.

## Overview

- **Manufacturer:** Gutamaya
- **Size class:** 3 (Large landing pad — needs a large-pad starport)
- **Role:** Shield-tank combat flagship / heavy trader / large-pad AX
- **Hull cost:** 200,493,413 CR (hull only — the priciest of the trinity)
- **Retail cost:** 208,969,451 CR (with stock modules)
- **Crew seats:** 4 · **Ship-Launched Fighter bay** present
- **Requires:** Imperial Navy rank **Duke** (Coriolis `requirements.empireRank: 12`)

## Hull Stats

Source: Coriolis-data ship definition `imperial_cutter` (edID 128049375).

- **Hull mass:** 1100 t (**the heaviest hull in this KB**)
- **Top speed:** 200 m/s · **Boost:** 320 m/s (good straight-line speed despite the mass)
- **Base shield strength:** 600 MJ (**the highest base shield of any KB ship** — the shield-tank trait)
- **Base armour:** 400
- **Hull hardness:** 70 (tied with the Corvette for highest in KB)
- **Heat capacity:** 327
- **Mass lock factor:** 27 (**the highest in KB** — very strong FSD denial)
- **Manoeuvrability (deg/s):** pitch 18 · roll 45 · yaw 8 (**the least agile ship in the KB** — turns
  poorly; the cost of its size and shield)
- **Reserve fuel:** 1.16 t

## Slot Layout

- **Core internals:** Power Plant **8**, Thrusters **8**, Frame Shift Drive 7, Life Support 7,
  Power Distributor 7, Sensors 7, Fuel Tank 6. The **class-8 Thruster** slot is a KB first — needed
  to move the 1100 t hull — and the big core all round supports the heavy shield/weapon loadout.
- **Hardpoints:** **1 × Huge + 2 × Large + 4 × Medium** (seven weapon mounts). **No Small mounts.**
  One Huge (vs the Corvette's two) is why the Cutter trails it in raw forward firepower.
- **Utility mounts:** 8 (deep shield-booster stack plus chaff, heat sinks, point defence).
- **Optional internals:** sizes **8, 8, 6, 6, 6, 5, 5, 4, 3, 1** (ten regular optionals, **two of them
  class-8**) plus **two class-5 Military slots** plus a reserved class-1 **Planetary Approach Suite**.
  The two class-8 optionals are what give the Cutter its enormous cargo (as a trader) or shield-cell /
  reinforcement capacity (as a tank).

### Military slots — two, class 5

The Cutter's **two class-5 Military slots** match the Corvette's. They accept the same reinforcement
set (per the Coriolis data: mahr, hr, scb, mrp, gsrp, gmrp, ghrp):

- [[outfitting/hull-reinforcement]] — standard, **Meta-Alloy** (caustic resist, the AX pick), and
  **Guardian** Hull Reinforcement.
- [[outfitting/module-reinforcement]] — standard and Guardian Module Reinforcement.
- [[outfitting/shield-cell-bank]] — active shield recharge.
- [[outfitting/guardian-shield-reinforcement]] — flat +MJ shield reinforcement.

Bulkheads give **no caustic resistance** (`causres 0` on every grade), so for AX work fit a
Meta-Alloy Hull Reinforcement for caustic protection.

## The Rank Gate

The Cutter cannot be bought until the commander reaches **Duke** in the Imperial Navy ranking — earned
by running Imperial-aligned missions and Navy promotion missions. This is the Imperial counterpart to
the Corvette's **Rear Admiral** gate (the Anaconda, by contrast, needs no rank). Plan the rank grind
before committing to a Cutter build.

## AX Build Notes — the large-pad shield tank

The Cutter is a current large-pad anti-Xeno platform that leans on its huge shield rather than raw
forward firepower:

- **AX weapons** across its seven hardpoints (one Huge): the kinetic [[outfitting/ax-multi-cannon]]
  and [[outfitting/ax-multi-cannon-enhanced|Enhanced]] version, the Guardian
  [[outfitting/guardian-gauss-cannon]] / [[outfitting/guardian-plasma-charger]] /
  [[outfitting/guardian-shard-cannon]] trio, the explosive [[outfitting/ax-missile-rack]] family, and
  the anti-swarm [[outfitting/remote-release-flak-launcher]] /
  [[outfitting/remote-release-flechette-launcher]].
- **AX utilities** on its eight utility mounts: the [[outfitting/xeno-scanner]] (mandatory to target
  Interceptor hearts), the [[outfitting/shutdown-field-neutraliser]] (negates the EMP pulse), and the
  [[outfitting/caustic-sink-launcher]] (purges caustic DoT). Add an optional-internal
  [[outfitting/decontamination-limpet-controller]] for sustained caustic removal.
- **AX defence** in the two class-5 Military slots, the two class-8 optionals (a deep
  [[outfitting/shield-cell-bank]] bank), and the rest of the optional bank.

AX combat zones, Spire sites and Titan wrecks all remain **live** — the Cutter is a current,
top-tier shield-tank choice for all of them.

## The large-pad trinity

- **Imperial Cutter** — the **shield-tank/trader**: highest base shield (600 MJ), two class-8
  optionals (massive cargo / cell-bank capacity), highest mass lock. Least agile of all KB ships; one
  Huge mount, no Small mounts. Gated behind Imperial **Duke**. Pick it for survivability and cargo.
- **[[ships/federal-corvette|Federal Corvette]]** — the **firepower king**: two Huge hardpoints, more
  agile, same two class-5 Military slots, hardness 70. Gated behind Federal **Rear Admiral**. Pick it
  for raw combat ceiling.
- **[[ships/anaconda|Anaconda]]** — the **no-gate jack-of-all-trades**: one Huge but eight total
  mounts, deepest optionals, best jump range, lightest/cheapest hull, **no rank gate**. Pick it for
  flexibility without grinding a Navy rank.

## Acquisition

Sold at large stations carrying a shipyard, **once Duke rank is reached**. Engineer the FSD for jump
range at [[engineers/felicity-farseer]] (Increased Range). Check Spansh (`spansh.co.uk/stations`) for
nearest stock.

[[trunk]]
