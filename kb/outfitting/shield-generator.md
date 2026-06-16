---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/shield_generator.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T01:04:59+00:00
source_count: 3
verified: true
availability: live
changed_note:
---

# Shield Generator (Outfitting)

The **Shield Generator** is a **core internal** module that projects a regenerating energy
shield around the hull — your first line of defence, absorbing damage before it reaches armour
and modules. Every combat, trading, and most exploration builds carry one. This page covers the
three generator lines from the Tier-0 Coriolis module data: the **standard** Shield Generator
(group `sg`), the **Bi-Weave** Shield Generator (group `bsg`), and the Powerplay **Prismatic**
Shield Generator (group `psg`). Reinforced generators are a separate module (see *Related shield
modules* below).

## How shield strength works — it's a multiplier, not a fixed MJ

A shield generator does **not** have a fixed shield value in megajoules. Instead each module
stores **multipliers** that are applied to the host ship's own base shield value, scaled by how
heavy the hull is relative to the module's mass band:

- `optmass` — the hull mass at which you get the module's `optmul` multiplier.
- `minmass` / `maxmass` — the light and heavy ends of the band.
- `maxmul` — the **highest** multiplier, reached at or below `minmass` (light ships shield best).
- `minmul` — the **lowest** multiplier, reached at or above `maxmass`.
- A hull **heavier than `maxmass` cannot mount that class** — the shield falls below `minmul`
  and effectively won't form. Always fit a class whose `maxmass` exceeds your loaded hull mass.

So **MJ = ship base shield × interpolated multiplier**: a light ship near `minmass` gets up to
`maxmul`; at `optmass` you get exactly `optmul`; toward `maxmass` it falls toward `minmul`. This
is why the same generator gives wildly different MJ on different hulls, and why the headline
"660 MJ" kind of number is always ship-specific, never a property of the module alone.

Resistances are uniform across all three lines: **explosive +0.5, kinetic +0.4, thermal −0.2**
(shields naturally resist explosive/kinetic, are weak to thermal). Distributor draw 0.6.

## Standard Shield Generator (group `sg`)

Ratings run E→A. **Rating sets the multiplier:** A `optmul` 1.2, B 1.1, C 1.0, D 0.9, E 0.8.
Higher rating = more shield (and more power draw, mass, cost). **Class 1 has no B rating** — only
E/D/C/A exist at size 1.

| Class | Rating | Opt Mass (t) | Optmul | Min→Max Mul | Regen | Broken Regen | Power (MW) | Integrity | Cost (CR) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | E | 25 | 0.8 | 0.3→1.3 | 1 | 1.6 | 0.72 | 32 | 300 |
| 1 | D | 25 | 0.9 | 0.4→1.4 | 1 | 1.6 | 0.96 | 24 | 1,240 |
| 1 | C | 25 | 1.0 | 0.5→1.5 | 1 | 1.6 | 1.2 | 40 | 5,140 |
| 1 | A | 25 | 1.2 | 0.7→1.7 | 1 | 1.6 | 1.68 | 48 | 88,075 |
| 2 | E | 55 | 0.8 | 0.3→1.3 | 1 | 1.6 | 0.9 | 41 | 1,978 |
| 2 | D | 55 | 0.9 | 0.4→1.4 | 1 | 1.6 | 1.2 | 31 | 5,934 |
| 2 | C | 55 | 1.0 | 0.5→1.5 | 1 | 1.6 | 1.5 | 51 | 17,803 |
| 2 | B | 55 | 1.1 | 0.6→1.6 | 1 | 1.6 | 1.8 | 71 | 53,408 |
| 2 | A | 55 | 1.2 | 0.7→1.7 | 1 | 1.6 | 2.1 | 61 | 160,224 |
| 3 | E | 165 | 0.8 | 0.3→1.3 | 1 | 1.87 | 1.08 | 51 | 6,271 |
| 3 | D | 165 | 0.9 | 0.4→1.4 | 1 | 1.87 | 1.44 | 38 | 18,812 |
| 3 | C | 165 | 1.0 | 0.5→1.5 | 1 | 1.87 | 1.8 | 64 | 56,435 |
| 3 | B | 165 | 1.1 | 0.6→1.6 | 1 | 1.87 | 2.16 | 90 | 169,304 |
| 3 | A | 165 | 1.2 | 0.7→1.7 | 1 | 1.87 | 2.52 | 77 | 507,912 |
| 4 | E | 285 | 0.8 | 0.3→1.3 | 1 | 2.53 | 1.32 | 64 | 19,878 |
| 4 | D | 285 | 0.9 | 0.4→1.4 | 1 | 2.53 | 1.76 | 48 | 59,633 |
| 4 | C | 285 | 1.0 | 0.5→1.5 | 1 | 2.53 | 2.2 | 80 | 178,898 |
| 4 | B | 285 | 1.1 | 0.6→1.6 | 1 | 2.53 | 2.64 | 112 | 536,693 |
| 4 | A | 285 | 1.2 | 0.7→1.7 | 1 | 2.53 | 3.08 | 96 | 1,610,080 |
| 5 | E | 405 | 0.8 | 0.3→1.3 | 1 | 3.75 | 1.56 | 77 | 63,012 |
| 5 | D | 405 | 0.9 | 0.4→1.4 | 1 | 3.75 | 2.08 | 58 | 189,035 |
| 5 | C | 405 | 1.0 | 0.5→1.5 | 1 | 3.75 | 2.6 | 96 | 567,106 |
| 5 | B | 405 | 1.1 | 0.6→1.6 | 1 | 3.75 | 3.12 | 134 | 1,701,318 |
| 5 | A | 405 | 1.2 | 0.7→1.7 | 1 | 3.75 | 3.64 | 115 | 5,103,953 |
| 6 | E | 540 | 0.8 | 0.3→1.3 | 1.3 | 5.33 | 1.86 | 90 | 199,747 |
| 6 | D | 540 | 0.9 | 0.4→1.4 | 1.3 | 5.33 | 2.48 | 68 | 599,242 |
| 6 | C | 540 | 1.0 | 0.5→1.5 | 1.3 | 5.33 | 3.1 | 113 | 1,797,726 |
| 6 | B | 540 | 1.1 | 0.6→1.6 | 1.3 | 5.33 | 3.72 | 158 | 5,393,177 |
| 6 | A | 540 | 1.2 | 0.7→1.7 | 1.3 | 5.33 | 4.34 | 136 | 16,179,531 |
| 7 | E | 1,060 | 0.8 | 0.3→1.3 | 1.8 | 7.33 | 2.1 | 105 | 633,199 |
| 7 | D | 1,060 | 0.9 | 0.4→1.4 | 1.8 | 7.33 | 2.8 | 79 | 1,899,597 |
| 7 | C | 1,060 | 1.0 | 0.5→1.5 | 1.8 | 7.33 | 3.5 | 131 | 5,698,790 |
| 7 | B | 1,060 | 1.1 | 0.6→1.6 | 1.8 | 7.33 | 4.2 | 183 | 17,096,371 |
| 7 | A | 1,060 | 1.2 | 0.7→1.7 | 1.8 | 7.33 | 4.9 | 157 | 51,289,112 |
| 8 | E | 1,800 | 0.8 | 0.3→1.3 | 2.4 | 9.6 | 2.4 | 120 | 2,007,241 |
| 8 | D | 1,800 | 0.9 | 0.4→1.4 | 2.4 | 9.6 | 3.2 | 90 | 6,021,722 |
| 8 | C | 1,800 | 1.0 | 0.5→1.5 | 2.4 | 9.6 | 4 | 150 | 18,065,165 |
| 8 | B | 1,800 | 1.1 | 0.6→1.6 | 2.4 | 9.6 | 4.8 | 210 | 54,195,495 |
| 8 | A | 1,800 | 1.2 | 0.7→1.7 | 2.4 | 9.6 | 5.6 | 180 | 162,586,486 |

`regen` is the steady recharge rate (MJ/s) while the shield is up but not full; `brokenregen`
is the (slower) rate after the shield has collapsed and is rebuilding. Both depend only on
class, not rating.

## Bi-Weave Shield Generator (group `bsg`)

The Bi-Weave trades peak strength for a **much faster recharge**. There is **one variant per
class, always C-rated** (internally `Class3_Fast`). Its `optmul` is **0.9** — below an A-rated
standard (1.2) and equal to a D-rated standard — so raw MJ is lower. What you buy is regen:
roughly **1.8–2.4× the standard generator's recharge**, and a far faster recovery after a
collapse. In prolonged fights where the shield keeps cycling, a Bi-Weave can effectively tank
more total damage than a higher-MJ standard shield that recharges slowly.

| Class | Opt Mass (t) | Optmul | Min→Max Mul | Regen | Broken Regen | Power (MW) | Integrity | Cost (CR) |
|---|---|---|---|---|---|---|---|---|
| 1 | 25 | 0.9 | 0.4→1.4 | 1.8 | 2.4 | 1.2 | 40 | 7,713 |
| 2 | 55 | 0.9 | 0.4→1.4 | 1.8 | 2.4 | 1.5 | 51 | 26,705 |
| 3 | 165 | 0.9 | 0.4→1.4 | 1.8 | 2.8 | 1.8 | 64 | 84,653 |
| 4 | 285 | 0.9 | 0.4→1.4 | 1.8 | 3.8 | 2.2 | 80 | 268,347 |
| 5 | 405 | 0.9 | 0.4→1.4 | 2.2 | 5.6 | 2.6 | 96 | 850,659 |
| 6 | 540 | 0.9 | 0.4→1.4 | 3.2 | 8 | 3.1 | 113 | 2,696,589 |
| 7 | 1,060 | 0.9 | 0.4→1.4 | 4.4 | 11 | 3.5 | 131 | 8,548,185 |
| 8 | 1,800 | 0.9 | 0.4→1.4 | 5.8 | 14.4 | 4 | 150 | 27,097,748 |

Opt-mass bands and resistances are identical to the standard generator of the same class, so a
Bi-Weave slots into the same core internal a standard shield would use.

## Prismatic Shield Generator (group `psg`)

The **Prismatic** is a **Powerplay reward** generator, pledged to **Aisling Duval** (still
obtainable under Powerplay 2.0 — the pledge system was overhauled in 2024, the module is
unchanged). It delivers the **highest shield multiplier of any generator**: `optmul` **1.5**
(vs standard A 1.2, Bi-Weave 0.9), with `minmul` 1.0 and `maxmul` 2.0. The trade-offs are a
**much heavier power draw** and a **slow recharge** — `regen` stays at 1.0 MJ/s through class 6
(1.1 at C7, 1.4 at C8), the lowest of the three lines. Every class ships **A-rated only**
(no E/D/C/B). Mass and the opt-mass bands match the standard generator of the same class, so it
drops straight into the same core internal slot. Resistances are the shared exp +0.5 / kin +0.4
/ therm −0.2.

| Class | Opt Mass (t) | Optmul | Min→Max Mul | Regen | Broken Regen | Power (MW) | Integrity | Cost (CR) |
|---|---|---|---|---|---|---|---|---|
| 1 | 25 | 1.5 | 1.0→2.0 | 1.0 | 1.2 | 2.52 | 48 | 132,200 |
| 2 | 55 | 1.5 | 1.0→2.0 | 1.0 | 1.2 | 3.15 | 61 | 240,340 |
| 3 | 165 | 1.5 | 1.0→2.0 | 1.0 | 1.3 | 3.78 | 77 | 761,870 |
| 4 | 285 | 1.5 | 1.0→2.0 | 1.0 | 1.7 | 4.62 | 96 | 2,415,120 |
| 5 | 405 | 1.5 | 1.0→2.0 | 1.0 | 2.3 | 5.46 | 115 | 7,655,930 |
| 6 | 540 | 1.5 | 1.0→2.0 | 1.0 | 3.2 | 6.51 | 136 | 24,269,300 |
| 7 | 1,060 | 1.5 | 1.0→2.0 | 1.1 | 4.2 | 7.35 | 157 | 76,933,670 |
| 8 | 1,800 | 1.5 | 1.0→2.0 | 1.4 | 5.4 | 8.4 | 180 | 243,879,730 |

Compare the class-5 power draw: Prismatic 5.46 MW vs standard 5A 3.64 MW vs Bi-Weave 5C 2.6 MW.
The Prismatic wins on raw buffer but demands a stronger power plant and distributor, and leans
hard on **Shield Cell Banks** to recover because its passive regen is so slow.

## Standard vs Bi-Weave vs Prismatic — which to fit

- **Standard A-rated** — highest non-Powerplay MJ for the slot. Best for builds that boost
  shields with [[outfitting/shield-booster]] and engineering and want a big buffer to soak burst
  damage (PvE bounty hunting, anything relying on shield cell banks to top a large pool).
- **Bi-Weave (C)** — lower MJ but recharges fast and rebuilds quickly after dropping. Favoured
  for sustained fights, ganker-resistant trade/explore hulls, and any build that would rather
  shrug damage off continuously than ride one big pool. Cheaper, too.
- **Prismatic (A, Powerplay)** — the biggest buffer of all (1.5 optmul) but slow to recharge and
  power-hungry. Shines on heavily shield-stacked builds that top up with Shield Cell Banks rather
  than relying on passive regen; requires an Aisling Duval pledge to obtain.
- **Mass matters more than rating gut-feel:** confirm the class `maxmass` exceeds your loaded
  hull mass, then pick the line. A heavy hull may be forced down to a class where it sits near
  `minmul` — engineering (e.g. Reinforced / Thermal Resistant blueprints) is how shield builds
  recover that.

## Related shield modules

- **Prismatic Shield Generator** — now documented above (group `psg`).
- **[[outfitting/shield-booster]]** — utility-mount module that adds a flat % to total shield
  strength; standard companion to any generator on a combat build.
- **Reinforced (Enhanced Low Power) Shield Generator** — lower power draw at the cost of regen.
  A separate module file, not detailed here yet.
- On defensive builds the shield sits alongside flat-armour [[outfitting/hull-reinforcement]].

## Where to buy

Standard and Bi-Weave generators are stocked to **Class 8** at **Garay Terminal** in
[[locations/deciat]] (the large-pad Coriolis starport that serves Felicity Farseer visitors).
The Prismatic is a Powerplay module — obtained by pledging to **Aisling Duval**, not bought from
a station outfitting list.

Shielding pairs with [[outfitting/frame-shift-drive]] and the rest of the core internals; on
defensive builds it sits alongside [[outfitting/hull-reinforcement]] and module reinforcement.
See [[ships/python-mk-ii]], [[ships/panther-clipper-mk-ii]] and other hulls for class-by-hull
slot sizes.

[[trunk]]
