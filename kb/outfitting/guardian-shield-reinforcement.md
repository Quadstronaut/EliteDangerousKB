---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/guardian_shield_reinforcement_package.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T00:43:20+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Guardian Shield Reinforcement Package (Outfitting)

The **Guardian Shield Reinforcement Package** (GSRP) is an **optional internal** module that adds a
**flat amount of shield strength (MJ)** to a ship's shields. It is the shield-layer counterpart to
the [[outfitting/hull-reinforcement|Hull Reinforcement Package]] (which adds flat *armour* HP): a
GSRP hardens the shield that sits in front of the hull. In the Coriolis data it is group `gsrp`,
file `internal/guardian_shield_reinforcement_package.json`.

It is a **Guardian module** — unlocked at a **Guardian Technology Broker** — and, like all Guardian
internals, it is **powered** (draws MW where conventional reinforcement packages draw none). With
the Guardian Hull Reinforcement (`ghrp`) and the Guardian Module Reinforcement (`gmrp`), it
completes the **Guardian defensive trio**: shields → hull → modules.

## What it does

- **Flat MJ, not a multiplier.** `shieldaddition` adds a fixed number of megajoules to the ship's
  total shield strength, independent of hull mass — so it is a large *relative* boost on a small
  light shield and a smaller relative one on a heavy capital shield. This differs from the
  [[outfitting/shield-booster]] (a *percentage* multiplier) and the
  [[outfitting/shield-cell-bank]] (active recharge): the GSRP is a passive, always-on flat add.
- **Powered.** Every class/rating draws power (C1 E 0.35 MW → C5 D 1.26 MW). Budget for it on the
  power plant — unlike the standard reinforcement packages, which are unpowered.
- **Module integrity** is a constant **36** across the whole line.

## Classes and ratings

GSRPs come in **classes 1–5** with only **two ratings, E and D** (no A/B/C) — the same shape as the
standard and Guardian Hull/Module Reinforcement lines. Within a class the **D variant adds more
shield MJ at half the mass** of the E variant, but draws slightly more power and costs roughly **3×**
as much. Fit **D** when mass/jump-range matters or you can afford it; **E** to save credits.

| Class | Rating | Shield add (MJ) | Power (MW) | Mass (t) | Cost (CR) |
|---|---|---|---|---|---|
| 1 | E | 44 | 0.35 | 2 | 10,000 |
| 1 | D | 61 | 0.46 | 1 | 30,000 |
| 2 | E | 83 | 0.56 | 4 | 24,000 |
| 2 | D | 105 | 0.67 | 2 | 72,000 |
| 3 | E | 127 | 0.74 | 8 | 57,600 |
| 3 | D | 143 | 0.84 | 4 | 172,800 |
| 4 | E | 165 | 0.95 | 16 | 138,240 |
| 4 | D | 182 | 1.05 | 8 | 414,720 |
| 5 | E | 198 | 1.16 | 32 | 331,778 |
| 5 | D | 215 | 1.26 | 16 | 995,330 |

Stacking multiple GSRPs is **additive on shield MJ** (no diminishing-returns falloff like the
shield booster has), so shield-tank builds simply fit several of the largest GSRPs their optional
slots allow — at the cost of slots, mass, and power.

## How to fit

- GSRPs go in **optional internal** slots, competing with cargo racks, [[outfitting/shield-cell-bank]]s,
  fuel tanks, and [[outfitting/hull-reinforcement|HRPs]] — so a shield-heavy build sacrifices cargo
  for raw shield buffer.
- They layer on top of the base [[outfitting/shield-generator]] and the percentage
  [[outfitting/shield-booster]]: generator sets the multiplier, boosters add a percentage, GSRPs add
  flat MJ on top. The three together build the shield pool that Shield Cell Banks then recharge.
- On an **AX/Thargoid** build the Guardian defensive trio works together —
  [[outfitting/hull-reinforcement|Guardian HRP]] for caustic-resistant hull,
  [[outfitting/module-reinforcement|Guardian MRP]] for module protection, and the GSRP for raw shield
  buffer. AX content remains `availability: live`.

## Where to get them

The GSRP is a **Guardian Technology Broker** unlock — collect Guardian blueprint fragments and
materials at a Guardian Structure site (see Canonn's Guardian site map), then unlock at a station
with a Tech Broker. It is not common shipyard stock the way standard reinforcement packages are.

[[trunk]]
