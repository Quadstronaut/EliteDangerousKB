---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/module_reinforcement_package.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T21:07:24+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Module Reinforcement Package (Outfitting)

The **Module Reinforcement Package** (MRP) is an **optional internal** module that protects your
ship's **modules** from damage that penetrates the hull. It is the third leg of the defensive tank
stack: shields absorb first, [[outfitting/hull-reinforcement]] hardens the armour beneath them, and
MRPs shield the modules inside the hull from being shot out. In the Coriolis data it is group `mrp`,
file `internal/module_reinforcement_package.json`.

## What it does

- **Protects modules, not hull.** When weapons fire (or collision damage) gets through the hull,
  individual modules — drives, power plant, weapons, life support — start taking damage and can be
  knocked offline or destroyed. An MRP intercepts a share of that module damage.
- **Two stats define it.** `protection` is the **fraction of incoming module damage the MRP
  absorbs**, and `integrity` is the **size of its damage pool** — how much it can soak before it is
  used up. Once the pool is depleted the MRP stops absorbing.
- **Draws no power.** There is no `power` field — like an HRP, an MRP is a passive module with zero
  power draw, so it costs only a slot and mass.

## The E vs D trade

MRPs come in **classes 1–5** with only **two ratings, E and D** (no A/B/C), and the two ratings sit
at opposite ends of a capacity-vs-absorption trade (straight from the in-game description):

- **E — "high damage capacity but low absorption."** Absorbs **30%** of module damage but has the
  **larger integrity pool**, so it soaks a small slice of many hits over a long time. Heavier and
  cheaper.
- **D — "low damage capacity but high absorption."** Absorbs **60%** of module damage but has the
  **smaller pool**, so it blocks a big slice of damage but runs out sooner. **Half the mass** of the
  E variant and roughly **3× the cost**.

Fit **D** when mass/jump-range matters or you expect short, intense bursts of incoming fire; **E**
when you want a cheaper, longer-lasting buffer against sustained chip damage.

## Classes and ratings

| Class | Rating | Module Protection | Integrity (pool) | Mass (t) | Cost (CR) |
|---|---|---|---|---|---|
| 1 | E | 30% | 77 | 2 | 5,000 |
| 1 | D | 60% | 70 | 1 | 15,000 |
| 2 | E | 30% | 115 | 4 | 12,000 |
| 2 | D | 60% | 105 | 2 | 36,000 |
| 3 | E | 30% | 170 | 8 | 28,000 |
| 3 | D | 60% | 155 | 4 | 84,000 |
| 4 | E | 30% | 260 | 16 | 65,000 |
| 4 | D | 60% | 235 | 8 | 195,000 |
| 5 | E | 30% | 385 | 32 | 150,000 |
| 5 | D | 60% | 350 | 16 | 450,000 |

Higher classes take a bigger optional-internal slot, weigh more, and carry a larger integrity pool.
**Stacking multiple MRPs raises total module protection, but with diminishing returns toward a cap**
(like resistances) — you cannot make modules immune by filling every slot with MRPs.

## How to fit

- MRPs go in **optional internal** slots, competing with cargo racks, fuel tanks,
  [[outfitting/shield-cell-bank]]s, and flat-armour [[outfitting/hull-reinforcement]] — a full tank
  build juggles all of these against cargo/utility capacity.
- They matter most on hulls that expect to **lose shields and brawl on hull** (heavy combat ships,
  AX hulls), where keeping drives, power plant, and weapons alive decides the fight.
- They pair with **military-grade bulkheads** and HRPs (hull layer) on a complete survivability
  build: HRPs keep the hull HP up, MRPs keep the modules inside it working.
- Engineer them (e.g. for more integrity at lower mass) on dedicated combat hulls; raw MRPs are the
  baseline.

## Where to get them

Module Reinforcement Packages are common optional-internal stock at most large outfitting stations,
including **Garay Terminal** in [[locations/deciat]]. No Powerplay or unlock requirement.

[[trunk]]
