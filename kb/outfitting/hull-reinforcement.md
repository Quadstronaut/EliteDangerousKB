---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/hull_reinforcement_package.json
source_urls: ["https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/hull_reinforcement_package.json", "https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/meta_alloy_hull_reinforcement_package.json", "https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/guardian_hull_reinforcement_package.json"]
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T21:23:50+00:00
source_count: 3
verified: true
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

## Meta-Alloy Hull Reinforcement — the caustic-resistant variant

The standard HRP's `causres` (caustic resistance) is **0**: it gives **no protection against
Thargoid caustic damage**. The separate **Meta-Alloy Hull Reinforcement Package** (Coriolis group
`mahr`, file `internal/meta_alloy_hull_reinforcement_package.json`) is the variant to fit for AX work
— it is **a** caustic-resistant HRP (see Guardian below for the other).

What it trades, confirmed by its own Tier-0 module file:

- **Caustic resistance `causres` = 3%, flat** across every class and rating — the whole reason to fit
  it. (Standard HRP = 0.)
- **No conventional resistances**: its `explres` / `kinres` / `thermres` are all **0**, where a
  standard HRP gives +0.5%/class. You give up exp/kin/therm hardening to get caustic.
- **Slightly less raw armour HP** than the standard HRP at the same class/rating (e.g. C5 gives
  324/351 HP vs the standard 360/390).
- Same shape otherwise: **classes 1–5, ratings E and D only, no power draw**. From class 2 up the D
  variant is half the mass of E (at class 1 both weigh 2 t).

| Class | Rating | Hull HP | Caustic res | exp/kin/therm res | Mass (t) | Cost (CR) |
|---|---|---|---|---|---|---|
| 1 | E | 72 | +3% | 0 | 2 | 7,501 |
| 1 | D | 99 | +3% | 0 | 2 | 22,501 |
| 2 | E | 135 | +3% | 0 | 4 | 18,000 |
| 2 | D | 171 | +3% | 0 | 2 | 54,000 |
| 3 | E | 207 | +3% | 0 | 8 | 42,000 |
| 3 | D | 234 | +3% | 0 | 4 | 126,000 |
| 4 | E | 270 | +3% | 0 | 16 | 97,501 |
| 4 | D | 297 | +3% | 0 | 8 | 292,501 |
| 5 | E | 324 | +3% | 0 | 32 | 225,001 |
| 5 | D | 351 | +3% | 0 | 16 | 675,001 |

## Guardian Hull Reinforcement — the powered AX hull layer

The **Guardian Hull Reinforcement Package** (Coriolis group `ghrp`, file
`internal/guardian_hull_reinforcement_package.json`) is the premium anti-Thargoid hull layer. It is
a **Guardian module** — unlocked at a **Guardian Technology Broker** — and unlike every other HRP it
is **powered**. Its description: "Powered module that increases the ship's hull integrity and
resistance to Thargoid, caustic and thermic damage."

What it brings, confirmed by its own Tier-0 module file:

- **The most raw armour HP of any HRP line.** C5 gives **488/450** HP (D/E) vs the standard HRP's
  390/360 and Meta-Alloy's 351/324 — Guardian wins raw HP at every class.
- **Caustic resistance `causres` = 5%, flat** across all classes/ratings — *more* than Meta-Alloy's
  3% — **plus** a small **thermal resistance `thermres` = 2%**. `explres`/`kinres` are 0 (no
  explosive/kinetic hardening), same as Meta-Alloy.
- **Powered.** It draws power (C1 D 0.56 MW → C5 D 1.46 MW) where the standard and Meta-Alloy HRPs
  draw none — budget for it on the power plant.
- Same shape otherwise: **classes 1–5, ratings E and D only**. From class 2 up D is half the mass of
  E and adds more HP for a higher cost.

| Class | Rating | Hull HP | Caustic res | Thermal res | Mass (t) | Power (MW) | Cost (CR) |
|---|---|---|---|---|---|---|---|
| 1 | E | 100 | +5% | +2% | 2 | 0.45 | 10,000 |
| 1 | D | 138 | +5% | +2% | 1 | 0.56 | 30,000 |
| 2 | E | 188 | +5% | +2% | 4 | 0.68 | 24,000 |
| 2 | D | 238 | +5% | +2% | 2 | 0.79 | 72,000 |
| 3 | E | 288 | +5% | +2% | 8 | 0.90 | 57,600 |
| 3 | D | 325 | +5% | +2% | 4 | 1.01 | 172,800 |
| 4 | E | 375 | +5% | +2% | 16 | 1.13 | 138,240 |
| 4 | D | 413 | +5% | +2% | 8 | 1.24 | 414,720 |
| 5 | E | 450 | +5% | +2% | 32 | 1.35 | 331,778 |
| 5 | D | 488 | +5% | +2% | 16 | 1.46 | 995,330 |

AX/Thargoid content — Spire sites, Titan wrecks, AX combat zones, interceptor encounters — remains
fully `availability: live`, so caustic resistance is current, relevant outfitting. AX builds
typically **mix** Meta-Alloy and Guardian HRPs (for caustic res) with standard HRPs, since stacking
pushes resistances toward a cap; Guardian HRPs lead on raw HP and resist but cost a slot's worth of
power, so power-starved hulls lean on the unpowered Meta-Alloy variant.

## How to fit

- HRPs go in **optional internal** slots, competing with cargo racks, shield cell banks, fuel
  tanks, and the like — so a heavy-armour build sacrifices cargo/utility capacity for survivability.
- They pair with high-grade **military-grade bulkheads** (the ship's base armour) and
  [[outfitting/module-reinforcement|Module Reinforcement Packages]] (which protect modules rather
  than hull) on a full tank build.
- On a layered defensive build: [[outfitting/shield-generator]] + [[outfitting/shield-booster]]
  carry the shield layer, HRPs carry the armour layer beneath.
- Engineer them (Heavy Duty for more HP, or the resist-focused blueprints) for serious combat
  hulls; raw HRPs are the baseline.

## Where to get them

Hull Reinforcement Packages are common optional-internal stock at most large outfitting stations,
including **Garay Terminal** in [[locations/deciat]]. No unlock requirement for the standard and
Meta-Alloy variants; the **Guardian** variant requires a Guardian Technology Broker unlock.

[[trunk]]
