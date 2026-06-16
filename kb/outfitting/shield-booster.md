---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/shield_booster.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T01:04:59+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Shield Booster (Outfitting)

The **Shield Booster** is a **utility-mount** module that increases your ship's total shield
strength by a flat percentage. It is the standard companion to a [[outfitting/shield-generator]]
on any combat or PvP-survivable build — a generator sets the base shield pool, boosters scale it
up. In the Coriolis data it lives under `hardpoints/shield_booster.json` (export key `sb`), and
every variant is **class 0** (the utility slot) and **passive** (always on, no toggle).

## What it does

A booster multiplies your *total* shield MJ by its `shieldboost` figure. Because shields already
combine the generator multiplier with the hull's base value, a booster stacks on top of that
result. Boosters are the cheapest, most slot-efficient way to grow a shield buffer — utility
mounts are plentiful and the modules are light.

**Diminishing returns:** the game applies a stacking falloff once several boosters are fitted, so
each additional booster adds less than the last. The Coriolis JSON only stores the single-module
value (the table below); it does not model the multi-booster falloff. In practice 4–6 boosters is
the usual ceiling before the marginal gain stops being worth the power and utility slots.

**No innate resistance:** the base module's `explres`/`kinres`/`thermres` are all 0 — a stock
booster only scales shield *strength*. Resistances come from engineering the booster (e.g. the
Resistance Augmented blueprint), which is why engineered boosters are a staple of serious combat
builds.

## Ratings (all class 0 / utility)

Rating sets the boost percentage; higher ratings cost more mass, power, and credits.

| Rating | Shield Boost | Mass (t) | Power (MW) | Integrity | Cost (CR) |
|---|---|---|---|---|---|
| E | +4% | 0.5 | 0.2 | 25 | 10,000 |
| D | +8% | 1.0 | 0.5 | 35 | 23,000 |
| C | +12% | 2.0 | 0.7 | 40 | 53,000 |
| B | +16% | 3.0 | 1.0 | 45 | 122,000 |
| A | +20% | 3.5 | 1.2 | 48 | 281,000 |

A-rated (+20%) is the default pick for combat builds where the utility slot and power budget can
spare it; the lighter D/C ratings suit weight-sensitive or power-starved hulls.

## How to fit

- Boosters go in **utility mounts**, the same small slots that take chaff, heat sinks, and point
  defence — so a shield-heavy build competes with those for slots.
- They do nothing without a [[outfitting/shield-generator]] running; on a hull flying shieldless
  they are dead weight and power draw.
- On a defensive build they pair with flat-armour [[outfitting/hull-reinforcement]] (which boosts
  the *hull* layer) — boosters scale the shield layer, HRPs scale the armour layer underneath.
- Engineer them (Resistance Augmented / Heavy Duty) for the real gains; raw boosters are a
  starting point.

## Where to get them

Shield boosters are common outfitting stock at most large stations with an Outfitting service,
including **Garay Terminal** in [[locations/deciat]]. No Powerplay or unlock requirement.

[[trunk]]
