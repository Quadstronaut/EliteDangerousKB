---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/type_10_defender.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T02:42:17+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Type-10 Defender

The Type-10 Defender is **Lakon Spaceways' dedicated anti-Xeno (AX) gunship** — a slow, heavily
armoured flying fortress built on the same airframe as the [[ships/type-9-heavy]] bulk hauler but
turned into a weapons platform. It carries the **highest base armour and hull hardness of any KB
ship** and the **most weapon mounts (nine)**, trading agility and Huge-class firepower for raw
durability and a wall of medium/large hardpoints plus eight utility mounts. Like the
[[ships/anaconda]] it has **no rank gate** — credits only. Its defining role is parking in a
Thargoid AX combat zone or over a Spire site and out-tanking everything.

## Overview

- **Manufacturer:** Lakon Spaceways
- **Size class:** 3 (Large landing pad — needs a large-pad starport; cannot dock at outposts)
- **Role:** AX gunship / heavily-armoured combat platform (also a slow large-pad multirole)
- **Hull cost:** 121,334,619 CR (hull only)
- **Retail cost:** 124,755,342 CR (with stock modules)
- **Crew seats:** 4 (multicrew capable) · **Ship-Launched Fighter bay** present
- **Requires:** nothing — **no rank gate** (no `requirements` block in the Coriolis data; credits only)

## Hull Stats

Source: Coriolis-data ship definition `type_10_defender` (edID 128785619).

- **Hull mass:** 1200 t (**the heaviest hull in the KB** — above the Imperial Cutter's 1100 t)
- **Top speed:** 179 m/s · **Boost:** 219 m/s (slow — it is a platform, not a dogfighter)
- **Base shield strength:** 320 MJ (comparatively low — it tanks with hull, not shields)
- **Base armour:** 580 (**the highest base armour of any KB ship**, above the Anaconda's 525)
- **Hull hardness:** 75 (**the highest hardness in the KB**, above the Corvette/Cutter's 70 —
  incoming fire is heavily blunted)
- **Heat capacity:** 335
- **Mass lock factor:** 26 (very high)
- **Manoeuvrability (deg/s):** pitch 20 · roll 20 · yaw 8 (**very sluggish** — identical figures to
  the [[ships/type-9-heavy]], the shared airframe)
- **Reserve fuel:** 0.77 t

## Slot Layout

- **Core internals:** Power Plant **8**, Thrusters **7**, Frame Shift Drive **7**, Life Support 5,
  Power Distributor **7**, Sensors 4, Fuel Tank **6**. The class-8 Power Plant feeds the big weapon
  bank; the class-7 thrusters are needed just to move the 1200 t hull. Sensors are only class 4.
- **Hardpoints:** **4 × Large + 3 × Medium + 2 × Small = nine weapon mounts** — the **most weapon
  mounts of any KB ship**. There is **no Huge hardpoint**: the Type-10 brings firepower through
  *count* and turret coverage rather than a single Huge slot (unlike the
  [[ships/federal-corvette|Corvette]]'s two Huge or the [[ships/anaconda]]/[[ships/imperial-cutter|Cutter]]'s
  one).
- **Utility mounts:** 8 (the reference 8-utility hull — room for the full AX utility kit plus a
  shield-booster/chaff/heat-sink stack).
- **Optional internals:** sizes **8, 7, 6, 5, 4, 4, 3, 3, 2, 1** (ten regular optionals) plus **two
  class-5 Military slots** plus a reserved class-1 **Planetary Approach Suite**.

### Military slots — two, class 5

The Type-10 has **two class-5 Military slots** (the same count as the Corvette and Cutter). Per the
Coriolis data the **first** slot can take **Meta-Alloy Hull Reinforcement** plus the rest of the
reinforcement set; the **second** slot takes the same set **except Meta-Alloy HRP**. They accept:

- [[outfitting/hull-reinforcement]] — standard, **Meta-Alloy** (caustic resist, the AX pick — first
  slot only), and **Guardian** Hull Reinforcement.
- [[outfitting/module-reinforcement]] — standard and Guardian Module Reinforcement.
- [[outfitting/shield-cell-bank]] — active shield recharge.
- [[outfitting/guardian-shield-reinforcement]] — flat +MJ shield reinforcement.

Bulkheads give **no caustic resistance** (`causres 0` on every grade), so for AX work fit a
Meta-Alloy Hull Reinforcement in the eligible Military slot for caustic protection.

## AX Build Notes — the no-gate armour brick

The Type-10 Defender is a current, top-tier large-pad anti-Xeno platform, and the easiest large AX
hull to acquire (no Navy rank required):

- **AX weapons** spread across its nine hardpoints: the kinetic [[outfitting/ax-multi-cannon]] and
  [[outfitting/ax-multi-cannon-enhanced|Enhanced]] version, the Guardian
  [[outfitting/guardian-gauss-cannon]] / [[outfitting/guardian-plasma-charger]] /
  [[outfitting/guardian-shard-cannon]] trio, the explosive [[outfitting/ax-missile-rack]] family, and
  the anti-swarm [[outfitting/remote-release-flak-launcher]] /
  [[outfitting/remote-release-flechette-launcher]]. The nine mounts and high turret count make it
  ideal for a turreted AX loadout that keeps firing while the brick slowly turns.
- **AX utilities** on its eight utility mounts: the [[outfitting/xeno-scanner]] (mandatory to target
  Interceptor hearts), the [[outfitting/shutdown-field-neutraliser]] (negates the EMP pulse) and the
  [[outfitting/caustic-sink-launcher]] (purges caustic DoT) — with mounts to spare for shield
  boosters. Add an optional-internal [[outfitting/decontamination-limpet-controller]] for sustained
  caustic removal.
- **AX defence** in the two class-5 Military slots and the ten-slot optional bank — the Type-10's huge
  armour (580) and hardness (75) make hull-tanking the natural strategy over its modest 320 MJ shield.

AX combat zones, Spire sites and Titan wrecks all remain **live** — the Type-10 is a current choice
for all of them, and a forgiving one thanks to its armour.

## The large-pad trinity — and where the Type-10 fits

The Type-10 sits alongside the large-pad combat trinity as the **dedicated armour platform**:

- **[[ships/federal-corvette|Federal Corvette]]** — firepower king (two Huge, highest agility of the
  large hulls), Federal **Rear Admiral** gate.
- **[[ships/anaconda]]** — no-gate jack-of-all-trades (one Huge, eight total mounts, best jump range).
- **[[ships/imperial-cutter|Imperial Cutter]]** — shield-tank/trader (600 MJ shield, two class-8
  optionals), Imperial **Duke** gate.
- **Type-10 Defender** — the **armour brick**: no Huge but **nine total mounts**, **highest armour
  (580) and hardness (75)** in the KB, heaviest hull (1200 t), two Military slots, **no rank gate**.
  Slowest and least agile of the large combat hulls; low shield (320 MJ). Pick it to out-*tank* a
  fight rather than out-*gun* it.

Compared with its airframe sibling the [[ships/type-9-heavy]] (same sluggish pitch 20 / roll 20 /
yaw 8), the Type-10 swaps the Type-9's twin class-8 cargo optionals for armour, hardpoints and the
class-8 Power Plant — the combat version of the same hull.

## Acquisition

Sold at large stations carrying a shipyard — **no rank required** (Horizons content). Check Spansh
(`spansh.co.uk/stations`) for nearest stock. For AX work, engineer the FSD at
[[engineers/felicity-farseer]] (Increased Range) to offset the heavy hull and fit a Meta-Alloy Hull
Reinforcement in the eligible Military slot.

[[trunk]]
