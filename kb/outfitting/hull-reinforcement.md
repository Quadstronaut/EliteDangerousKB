---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/hull_reinforcement_package.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T01:04:59+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Hull Reinforcement Package (Outfitting)

The **Hull Reinforcement Package** (HRP) is an **optional internal** module that adds flat armour
hit points plus small damage resistances to the ship's hull. It is the armour-layer counterpart
to the shield layer's [[outfitting/shield-booster]]: where a booster scales your shields, an HRP
hardens the hull underneath them — the last thing standing once shields drop. In the Coriolis
data it is group `hr`, file `internal/hull_reinforcement_package.json`.

## What it does

- **Flat HP, not a percentage.** `hullreinforcement` adds a fixed number of armour HP to the
  hull, independent of the ship's size — so on a small light hull an HRP is a large *relative*
  boost, and on a heavy hull it is a smaller relative one.
- **Small resistances** to explosive, kinetic, and thermal damage, scaling by class
  (+0.5% per class step). These stack with the ship's bulkhead resistances.
- HP and resist apply to the **armour layer**, so an HRP keeps helping after shields collapse —
  which is exactly when raw hull tank matters.

## Classes and ratings

HRPs come in **classes 1–5** with only **two ratings, E and D** (no A/B/C). The **D variant adds
more HP at half the mass of the E variant**, but costs roughly 3× as much. Fit **D** when you can
afford it or when mass/jump-range matters; **E** to save credits on a budget build.

| Class | Rating | Hull HP | Resist (exp/kin/therm) | Mass (t) | Cost (CR) |
|---|---|---|---|---|---|
| 1 | E | 80 | +0.5% | 2 | 5,000 |
| 1 | D | 110 | +0.5% | 1 | 15,000 |
| 2 | E | 150 | +1.0% | 4 | 12,000 |
| 2 | D | 190 | +1.0% | 2 | 36,000 |
| 3 | E | 230 | +1.5% | 8 | 28,000 |
| 3 | D | 260 | +1.5% | 4 | 84,000 |
| 4 | E | 300 | +2.0% | 16 | 65,000 |
| 4 | D | 330 | +2.0% | 8 | 195,000 |
| 5 | E | 360 | +2.5% | 32 | 150,000 |
| 5 | D | 390 | +2.5% | 16 | 450,000 |

Higher classes take a bigger optional-internal slot and weigh more, but give more HP. Stacking
multiple HRPs is additive on HP (no diminishing-returns falloff like shield boosters have), so
heavy-armour builds simply fill several optional slots with the largest HRPs the slots allow.

## No caustic resistance — that's a different module

The standard HRP's `causres` (caustic resistance) is **0**. It gives **no protection against
Thargoid caustic damage**. For AX/Thargoid builds that need caustic resistance, the separate
**Meta-Alloy Hull Reinforcement Package** (Coriolis `mahr`) is the module to fit instead — it
trades some of the flat stats for caustic protection. AX content (Spire sites, Titan wrecks,
AX combat zones) remains fully `availability: live`.

## How to fit

- HRPs go in **optional internal** slots, competing with cargo racks, shield cell banks, fuel
  tanks, and the like — so a heavy-armour build sacrifices cargo/utility capacity for survivability.
- They pair with high-grade **military-grade bulkheads** (the ship's base armour) and
  **Module Reinforcement Packages** (which protect modules rather than hull) on a full tank build.
- On a layered defensive build: [[outfitting/shield-generator]] + [[outfitting/shield-booster]]
  carry the shield layer, HRPs carry the armour layer beneath.
- Engineer them (Heavy Duty for more HP, or the resist-focused blueprints) for serious combat
  hulls; raw HRPs are the baseline.

## Where to get them

Hull Reinforcement Packages are common optional-internal stock at most large outfitting stations,
including **Garay Terminal** in [[locations/deciat]]. No unlock requirement.

[[trunk]]
