---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/hauler.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T04:12:55Z
source_count: 1
verified: false
availability: live
changed_note:
---

# Hauler

The Hauler is **Zorgon Peterson's tiny, ultra-cheap small-pad freighter** — the dedicated
cargo-and-jump counterpart to the multipurpose [[ships/adder]] and the free [[ships/sidewinder]]. It
is the **lightest hull in the KB** at just 14 t, and that featherweight mass (not a big drive) is the
source of its famous engineered jump range: a fully-stripped, A-rated Hauler is one of the longest-legged
small ships in the game. With a single Small hardpoint it is no fighter — its whole identity is doing
the cheapest possible cargo run, or being the cheap rookie explorer.

## Overview

- **Manufacturer:** Zorgon Peterson
- **Size class:** 1 (Small landing pad — docks anywhere, including outposts and planetary ports)
- **Role:** Dedicated light freight / budget long-range jumper (cargo running, cheap exploration, courier)
- **Rank requirement:** none — credits only (no `requirements` block in the Coriolis data)
- **Hull cost:** 30,308 CR (hull only — the third-cheapest hull in the KB, above the
  [[ships/sidewinder]] and [[ships/eagle]])
- **Retail cost:** 52,720 CR (with stock modules)
- **Crew seats:** 1

## Hull Stats

Source: Coriolis-data ship definition `hauler` (edID 128049261, eddbID 12).

- **Hull mass:** 14 t — the **lightest hull in the KB**, undercutting the previous lightest, the
  [[ships/sidewinder]]'s 25 t, by a wide margin. This ultra-low mass is the foundation of the Hauler's
  long jump range.
- **Top speed:** 200 m/s · **Boost:** 300 m/s — slow; among the lowest base speeds in the KB (the
  Hauler is built to jump and carry, not to race).
- **Base shield strength:** 50 MJ
- **Base armour:** 100 — surprisingly tough for so tiny a hull (more than the [[ships/eagle]]'s 40 or
  the Sidewinder's 60), though on only 14 t of mass it is still fragile in absolute terms.
- **Hull hardness:** 20 (low — ties the Sidewinder)
- **Heat capacity:** 123 — the **lowest heat capacity of any hull paged in this KB** (below the
  Sidewinder's 140). The Hauler runs hot, so manage heat when fuel-scooping or running silent.
- **Mass lock factor:** 6
- **Manoeuvrability (deg/s):** pitch 36 · roll 100 · yaw 14 (agile enough; roll 100 ties the
  [[ships/adder]] and [[ships/cobra-mk-iii]], short of the [[ships/eagle]]'s class-leading 120).
- **Reserve fuel:** 0.25 t (tiny)

## Slot Layout

- **Core internals:** Power Plant **2**, Thrusters **2**, Frame Shift Drive **2**, Life Support **1**,
  Power Distributor **1**, Sensors **1**, Fuel Tank **2**. A minimal class-2-capped core — the same
  shallow core as the [[ships/sidewinder]] but with a **bigger class-2 Fuel Tank** (vs the Sidewinder's
  class-1). The FSD is only class-2; the Hauler's range comes from its 14 t hull mass, not a large drive.
- **Hardpoints:** 1 × Small (a single weapon mount) — the smallest armament of any ship paged here.
- **Utility mounts:** 2 (room for a shield booster, heat sink, chaff, or point defence).
- **Optional internals:** sizes 3, 3, 2, 1, 1, 1 (six regular slots, **top two class-3**) plus a
  reserved class-1 **Planetary Approach Suite**. **No Military slot.** The two class-3 optionals (vs
  the Sidewinder's top class-2) give the Hauler its cargo-and-fuel bias — bigger racks or fuel tanks
  than the starter hull.
- **Military slots:** none.

Bulkheads carry `causres 0` on every grade.

## The budget freight tier

- **vs [[ships/sidewinder]]:** the Hauler is the dedicated-cargo step beyond the free starter — lighter
  (14 vs 25 t), with bigger top optionals (two class-3 vs class-2) and a bigger fuel tank for longer
  legs. The Sidewinder is the cheaper (4,588 vs 30,308 CR hull) general-purpose baseline with two
  weapon mounts; the Hauler drops a hardpoint to specialise in carrying and jumping.
- **vs [[ships/adder]]:** the [[ships/adder]] is the multipurpose budget hull — three weapon mounts
  (1 Medium + 2 Small), seven optionals, two crew seats and a class-3 FSD/fuel-tank package. The Hauler
  is the **purer freighter/jumper**: lighter (14 vs 35 t) and cheaper, but with only one Small mount,
  six optionals and a smaller class-2 core. Pick the Adder for flexibility, the Hauler for the absolute
  cheapest cargo run or the lightest possible jump platform.
- **vs [[ships/type-8-transporter]]:** the Type-8 is the proper medium-pad dedicated hauler — vastly
  more cargo capacity for serious trade. The Hauler is the tiny small-pad entry rung beneath it, for
  early-game cargo missions and outpost-only routes a medium pad cannot reach.

## Build notes

The Hauler rewards single-purpose fits. **For cargo:** fill the six optionals with cargo racks, fit a
basic shield, and run light. **For range:** strip everything non-essential, fit an A-rated class-2 FSD,
a fuel scoop and the smallest viable life support — the 14 t hull then jumps far out of proportion to
its price, making the Hauler a classic cheap first explorer or a long-range taxi. The single Small
hardpoint and class-1 Power Distributor mean it cannot fight; rely on speed, silent running and not
being seen. With no Military slot, any hull reinforcement competes with cargo, so keep the role focused.

## Acquisition

Stocked at most shipyards; no rank or permit requirement, credits only. Its very low price and small
pad make it one of the most accessible hulls in the game for a commander moving into cargo or
exploration beyond the Sidewinder.

[[trunk]]
