---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/viper_mk_iv.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T03:48:37Z
source_count: 1
verified: false
availability: live
changed_note:
---

# Viper Mk IV

The Viper Mk IV is **Faulcon DeLacy's heavier, tankier small-pad combat ship** — the bulkier
evolution of the fast-attack [[ships/viper-mk-iii]]. Where the Mk III is a featherweight
interceptor built around raw speed, the Mk IV trades that speed for substance: nearly four times
the hull mass, more than double the armour and shield, a bigger core with a real fuel tank, and a
deeper optional bank. It is the multirole-leaning member of the Viper pair — still small-pad and
still cheap by combat-ship standards, but it survives a fight instead of outrunning it.

## Overview

- **Manufacturer:** Faulcon DeLacy
- **Size class:** 1 (Small landing pad — docks anywhere, including outposts and planetary ports)
- **Role:** Multirole combat (bounty hunting, patrol, light Conflict Zones)
- **Rank requirement:** none — credits only (no `requirements` block in the Coriolis data)
- **Hull cost:** 312,797 CR (hull only)
- **Retail cost:** 437,931 CR (with stock modules)
- **Crew seats:** 1

## Hull Stats

Source: Coriolis-data ship definition `viper_mk_iv` (the Mk IV is a separate hull from the
`viper`/Mk III). edID 128672255, eddbID 28.

- **Hull mass:** 190 t — nearly 4× the Viper Mk III's 50 t. The added mass is the basis of its
  tankier, slower character.
- **Top speed:** 270 m/s · **Boost:** 340 m/s — notably slower than the Mk III's 320/400 (the
  speed-for-bulk trade that defines the pair).
- **Base shield strength:** 150 MJ
- **Base armour:** 150 (symmetrical) · **Hull hardness:** 35 — both the shield and armour are well
  above the Mk III's 105/70, so the Mk IV genuinely tanks where the Mk III dodges.
- **Heat capacity:** 209 (slightly higher than the Mk III's 195, still on the warm side)
- **Mass lock factor:** 7
- **Manoeuvrability (deg/s):** pitch 30 · roll 90 · yaw 12 (a touch less nimble than the Mk III)
- **Reserve fuel:** 0.46 t

## Slot Layout

- **Core internals:** Power Plant **4**, Thrusters **4**, Frame Shift Drive **4**,
  Life Support **2**, Power Distributor **3**, Sensors **3**, Fuel Tank **4**. A bigger core than
  the Mk III ([3,3,3,2,3,3,2]) across the board, and crucially a class-4 fuel tank (vs the Mk III's
  class-2) — the Mk IV has noticeably longer legs.
- **Hardpoints:** 2 × Medium + 2 × Small (four weapon mounts) — the same mount layout as the
  [[ships/viper-mk-iii]] and the [[ships/cobra-mk-iii]].
- **Utility mounts:** 2 (chaff, heat sinks, a shield booster or point defence).
- **Optional internals:** sizes 4, 4, 3, 2, 2, 1, 1, 1 (eight slots, top class-4) plus **one
  class-3 Military slot** (eligible Meta-Alloy / standard Hull Reinforcement, Module Reinforcement,
  Shield Cell Bank or a Guardian reinforcement package) and a reserved class-1 **Planetary Approach
  Suite**. The eight optionals (vs the Mk III's six) are the Mk IV's multirole edge — more room for
  cargo, an SCB, or reinforcement.
- **Military slots:** one (class 3).

Bulkheads carry `causres 0` on every grade.

## Viper pair and small-pad siblings

- **vs [[ships/viper-mk-iii]]:** the two Vipers split the same chassis concept in opposite
  directions. The Mk III is the **fast, cheap interceptor** — 50 t, 320/400, thin armour, short
  legs (FT2), six optionals, hull 96,733 CR. The Mk IV is the **tankier multirole** — 190 t,
  270/340, double the shield/armour, a bigger core with a class-4 fuel tank, eight optionals, hull
  312,797 CR. Both keep the 2 Medium + 2 Small mounts, the 2 utility slots and the single class-3
  Military slot; pick speed (Mk III) or staying power and range (Mk IV).
- **vs [[ships/cobra-mk-iii]]:** the same four-mount layout, but the Cobra is the multirole hauler
  (eight optionals, faster boost at 400) and the cheaper hull; the Viper Mk IV brings the class-3
  Military slot and more shield/armour for a combat lean.
- **vs [[ships/vulture]]:** the Vulture is the small-pad firepower king (two Large mounts, 240 MJ
  shield, best-in-KB roll) but costs ~4.9 M CR and is power-constrained. The Viper Mk IV is the far
  cheaper, more flexible four-mount alternative when you want a durable small-pad fighter without
  the Vulture's price or power budget.

## Build notes

The textbook fit is two Medium + two Small weapons (gimballed multi-cannons or pulse/burst lasers
to spare the class-3 distributor), a fast-charging shield, and chaff plus a heat sink in the two
utility mounts. Put a Hull or Module Reinforcement in the class-3 Military slot and the Mk IV tanks
considerably better than the Mk III. Engineer the FSD at [[engineers/felicity-farseer]] to extend
its already-decent range, and Dirty Drive Tuning helps offset the lower base speed.

## Acquisition

Sold at most stations with a shipyard; being small-pad it can be based out of outposts. Check
Spansh (`spansh.co.uk/stations`) for nearest stock.

[[trunk]]
