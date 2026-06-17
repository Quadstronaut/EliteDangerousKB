---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/guardian_fsd_booster.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T00:43:20+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Guardian FSD Booster (Outfitting)

The **Guardian FSD Booster** is an **optional internal** module that adds a **flat bonus to jump
range** (in light-years) to every jump. It does **not** replace the [[outfitting/frame-shift-drive]]
— it **stacks additively** on top of it, so the same booster benefits any FSD. In the Coriolis data
it is group `gfsb`, file `internal/guardian_fsd_booster.json`. It is a **Guardian module** (Guardian
Technology Broker unlock) and, like all Guardian internals, it is **powered**.

This is the single most impactful exploration module after the FSD itself: a class-5 booster adds
**+10.5 LY to every jump**, independently confirming the figure on the mechanics page
[[mechanics/frame-shift-drive]].

## What it does

- **Flat LY, added to each jump.** `jumpboost` is a fixed light-year bonus by class, applied on top
  of the FSD's computed range. Because the bonus is flat, a **light ship gains the most *relative*
  range** — the same +10.5 LY is a bigger percentage on a 30 LY jumper than on a 60 LY one.
- **At the cost of fuel efficiency.** The in-game description reads: "Used to boost the output of
  Frame Shift Drives, but at the cost of overall fuel efficiency." The booster leans on the FSD
  harder per jump.
- **One module per class size.** There is no E/D/A rating ladder — the rating is always `H`
  (Guardian). Pick the **largest class your optional slots allow** for the biggest bonus.
- **Constant mass and integrity.** Every class weighs **1.3 t** and has integrity **32**; only the
  jump bonus, power draw, and cost change with class.

## Classes

| Class | Jump boost (LY) | Power (MW) | Mass (t) | Cost (CR) |
|---|---|---|---|---|
| 1 | +4.00 | 0.75 | 1.3 | 405,022 |
| 2 | +6.00 | 0.98 | 1.3 | 810,521 |
| 3 | +7.75 | 1.27 | 1.3 | 1,620,431 |
| 4 | +9.25 | 1.65 | 1.3 | 3,245,013 |
| 5 | +10.50 | 2.14 | 1.3 | 6,483,101 |

The bonus has **diminishing class-to-class returns** (C1→C2 adds 2.0 LY, but C4→C5 adds only
1.25 LY), while power draw keeps climbing — but explorers almost always fit the **largest class that
fits**, since +10.5 LY per jump compounds enormously over a long route.

## How to fit

- Goes in an **optional internal** slot, competing with fuel tanks, [[outfitting/cargo-rack]]s and
  reinforcement packages. On a dedicated explorer (e.g. the [[ships/mandalay]]) the booster takes a
  large optional slot specifically for the range gain.
- Pairs with an A-rated, engineered [[outfitting/frame-shift-drive]] and a light hull — the booster
  is most valuable when the underlying jump range is already high. See
  [[mechanics/frame-shift-drive]] for jump-range theory and neutron boosting (the booster's flat
  bonus stacks under the neutron multiplier too).
- It is the standard third piece of an exploration drive train: **FSD + Guardian FSD Booster + fuel
  scoop** ([[outfitting/fuel-scoop]]).

## Where to get them

The Guardian FSD Booster is a **Guardian Technology Broker** unlock — collect Guardian blueprint
fragments and materials at a Guardian Structure site (see Canonn's Guardian site map), then unlock at
a station with a Tech Broker. `availability: live`.

[[trunk]]
