---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/module_reinforcement_package.json
source_urls: ["https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/module_reinforcement_package.json", "https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/guardian_module_reinforcement_package.json"]
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T21:23:50+00:00
source_count: 2
verified: true
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
- **Draws no power.** There is no `power` field — like an HRP, the standard MRP is a passive module
  with zero power draw, so it costs only a slot and mass. (The Guardian variant below *is* powered.)

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

## Guardian Module Reinforcement — the powered AX variant

The **Guardian Module Reinforcement Package** (Coriolis group `gmrp`, file
`internal/guardian_module_reinforcement_package.json`) is the AX sibling of the standard MRP. It is a
**Guardian module** (unlocked at a **Guardian Technology Broker**) and, unlike the standard MRP, it
is **powered**. Its description adds that it "has resistances to Thargoid specific disruption
technology."

What it brings, confirmed by its own Tier-0 module file:

- **Same protection fractions as the standard MRP**: D absorbs **60%**, E absorbs **30%** of
  penetrating module damage — identical to the unpowered version (an independent Tier-0 confirmation
  of the protection mechanic).
- **Larger integrity pools** than the standard MRP at the same class/rating (≈10% more): e.g. C5
  gives 385/424 (D/E) vs the standard 350/385.
- **Resistance to Thargoid disruption technology** — caustic/field effects the standard MRP does
  nothing against. This is the reason to fit it for AX work.
- **Powered** (C1 D 0.34 MW → C5 D 0.88 MW), where the standard MRP draws none — budget for it.
- Same shape otherwise: **classes 1–5, ratings E and D only**. From class 2 up D is half the mass of
  E; D = higher absorption (60%) for ~3× the cost of E (30%).

| Class | Rating | Module Protection | Integrity (pool) | Mass (t) | Power (MW) | Cost (CR) |
|---|---|---|---|---|---|---|
| 1 | E | 30% | 85 | 2 | 0.27 | 10,000 |
| 1 | D | 60% | 77 | 1 | 0.34 | 30,000 |
| 2 | E | 30% | 127 | 4 | 0.41 | 24,000 |
| 2 | D | 60% | 116 | 2 | 0.47 | 72,000 |
| 3 | E | 30% | 187 | 8 | 0.54 | 57,600 |
| 3 | D | 60% | 171 | 4 | 0.61 | 172,800 |
| 4 | E | 30% | 286 | 16 | 0.68 | 138,240 |
| 4 | D | 60% | 259 | 8 | 0.74 | 414,720 |
| 5 | E | 30% | 424 | 32 | 0.81 | 331,778 |
| 5 | D | 60% | 385 | 16 | 0.88 | 995,330 |

AX/Thargoid content — Spire sites, Titan wrecks, AX combat zones, interceptor encounters — remains
fully `availability: live`, so the Guardian MRP's Thargoid-disruption resistance is current, relevant
outfitting. It pairs with the Guardian Hull Reinforcement Package
([[outfitting/hull-reinforcement]]) and the Guardian Shield Reinforcement Package
([[outfitting/guardian-shield-reinforcement]]) on a dedicated AX hull — together the three form the
**Guardian defensive trio**: modules → hull → shields.

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
including **Garay Terminal** in [[locations/deciat]]. The standard MRP has no unlock requirement; the
**Guardian** variant requires a Guardian Technology Broker unlock.

[[trunk]]
