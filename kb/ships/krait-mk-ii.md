---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/krait_mkii.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T02:00:10+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Krait Mk II

The Krait Mk II is a **medium-class multirole ship** by **Faulcon DeLacy** — one of the most
popular all-rounders in the game and the heavier medium-pad alternative to the
[[ships/alliance-chieftain|Alliance Chieftain]] for anti-Xeno (AX) combat. **Three large
hardpoints**, a full set of generous optional internals, a Ship-Launched Fighter bay and a
three-seat crew make it equally at home in AX combat, bounty hunting, exploration and trade.

## Overview

- **Manufacturer:** Faulcon DeLacy
- **Size class:** 2 (Medium landing pad — docks at outposts and all larger ports)
- **Role:** Multirole (AX combat, bounty hunting, exploration, trade)
- **Hull cost:** 44,160,710 CR (hull only)
- **Retail cost:** 45,814,205 CR (with stock modules)
- **Crew seats:** 3 (pilot + two — covers a Ship-Launched Fighter pilot and a multicrew seat)

## Hull Stats

Source: Coriolis-data ship definition `krait_mkii` (edID 128816567).

- **Hull mass:** 320 t
- **Top speed:** 240 m/s · **Boost:** 330 m/s
- **Base shield strength:** 220 MJ
- **Base armour:** 220 · **Hull hardness:** 55
- **Heat capacity:** 300
- **Mass lock factor:** 16
- **Manoeuvrability (deg/s):** pitch 26 · roll 90 · yaw 10
- **Reserve fuel:** 0.63 t
- **Fighter bay capable:** yes (`fighterHangars: true`)

## Slot Layout

- **Core internals:** Power Plant **7**, Thrusters **6**, Frame Shift Drive **5**,
  Life Support **4**, Power Distributor **7**, Sensors **6**, Fuel Tank **5**.
  The class-7 power plant and class-7 power distributor give it plenty of headroom for energy
  weapons, boosting and a fighter bay.
- **Hardpoints:** **3 × Large + 2 × Medium** (five weapon mounts — heavier punch than the
  Chieftain's 2 L + 1 M + 3 S).
- **Utility mounts:** 4.
- **Optional internals:** sizes **6, 6, 5, 5, 4, 3, 3, 2, 1** plus a reserved class-1
  **Planetary Approach Suite**. **No Military slots** (unlike the Chieftain).

The deep, general-purpose optional bank is the Krait's strength: dual class-6 internals plus a
long tail let it carry shields, hull reinforcement, cargo, an SRV bay and a fighter hangar all at
once. The trade-off versus the Chieftain is the lack of dedicated **Military** reinforcement
slots, so AX defence modules compete with cargo and utility internals.

## AX Build Notes

A common heavy medium-pad AX hull. The three large hardpoints take big AX weapons, the four
utility mounts carry the AX survival kit, and the SLF bay adds a second gun platform:

- **AX weapons** on the 3 L + 2 M hardpoints: the kinetic [[outfitting/ax-multi-cannon]] and its
  [[outfitting/ax-multi-cannon-enhanced|Enhanced]] gimballed version, the Guardian
  [[outfitting/guardian-gauss-cannon]] / [[outfitting/guardian-plasma-charger]] /
  [[outfitting/guardian-shard-cannon]] trio, the explosive [[outfitting/ax-missile-rack]] family,
  and the anti-swarm [[outfitting/remote-release-flak-launcher]] /
  [[outfitting/remote-release-flechette-launcher]].
- **AX utilities** on the 4 utility mounts: [[outfitting/xeno-scanner]] (to target Interceptor
  hearts), [[outfitting/shutdown-field-neutraliser]] (negates the EMP pulse) and
  [[outfitting/caustic-sink-launcher]] (purges caustic DoT). Add an optional-internal
  [[outfitting/decontamination-limpet-controller]] for sustained caustic cleaning.
- **AX defence:** stack [[outfitting/hull-reinforcement]] (use the Meta-Alloy variant for caustic
  resist — bulkheads give `causres 0`), [[outfitting/module-reinforcement]] and
  [[outfitting/shield-cell-bank]] in the general optional slots.

AX combat zones, Spire sites and Titan wrecks all remain **live** — the Krait is a current,
relevant choice for all of them.

## Versus the Alliance Chieftain

Both are class-2 medium-pad AX hulls; pick by playstyle:

- **Krait Mk II** — more firepower (3 L + 2 M hardpoints), bigger and more numerous optional
  internals, a **fighter bay** (`fighterHangars: true`) and a 3-seat crew, plus class-7 power
  plant/distributor. The multirole choice when you want guns, cargo and flexibility. Costs
  far more (≈44 M vs ≈19 M CR hull).
- **[[ships/alliance-chieftain|Alliance Chieftain]]** — tougher and nimbler: higher hull
  hardness (65 vs 55), three dedicated **Military reinforcement slots** the Krait lacks, and a
  much better roll/pitch/yaw. The dedicated AX brawler when survivability and turn rate matter
  more than raw firepower.

## Acquisition

Sold at large stations carrying a shipyard. Engineer the FSD for jump range at
[[engineers/felicity-farseer]] (Increased Range). Check Spansh (`spansh.co.uk/stations`) for
nearest stock.

[[trunk]]
