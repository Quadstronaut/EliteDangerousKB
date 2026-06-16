---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/fuel_scoop.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T00:32:57+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Fuel Scoop (Outfitting)

The Fuel Scoop is an **optional internal** that refuels the ship for free from the corona of a
scoopable star while you fly through it in supercruise. It is the module that makes long-range
exploration and self-sufficient travel possible. Stats below are from the Tier-0 Coriolis
module definition.

The fuel scoop is **massless** (0 t in every class and rating) — it costs only an internal slot
and some power, never jump range. That makes "fit the biggest scoop your spare slot allows, then
A-rate it" the near-universal rule.

## Scoopable stars

You can only scoop the main-sequence star classes summarised by the mnemonic **KGBFOAM**
(K, G, B, F, O, A, M). Approach in supercruise and skim the corona just outside the exclusion
zone; watch heat. Non-main-sequence stars (white dwarfs, neutron stars, etc.) are **not**
scoopable — they are used for jump-range boosting, not refuelling (see
[[mechanics/frame-shift-drive]]).

## Rating matters more than anything

The only meaningful stat is **scoop rate** (fuel gathered per second). It rises with both class
and rating, and A-rated is always the fastest in its class. A bigger, hotter scoop means shorter
stops at each star on an expedition.

## A-rated module table

| Class | Scoop rate | Power | Cost (CR) |
|---|---|---|---|
| 1A | 42 | 0.32 | 82,270 |
| 2A | 75 | 0.39 | 284,844 |
| 3A | 176 | 0.48 | 902,954 |
| 4A | 342 | 0.57 | 2,862,364 |
| 5A | 577 | 0.70 | 9,073,694 |
| 6A | 878 | 0.83 | 28,763,610 |
| 7A | 1,245 | 0.97 | 91,180,644 |
| 8A | 1,680 | 1.12 | 289,042,641 |

(Each class also comes in B/C/D/E at lower rate, power and cost — e.g. a 5E scoops at 247 vs the
5A's 577. Budget builds drop a rating or two; the scoop never costs mass either way.)

## Build notes

- An explorer wants the **largest class** that fits a spare optional, A-rated, so refuel stops on
  a neutron highway take seconds. The light [[ships/mandalay]] runs a class-6 scoop in its big
  optional bay for exactly this.
- Bulk haulers and miners usually fit a smaller scoop (3A–5A) since cargo and limpets compete for
  the big slots; pair with a [[outfitting/frame-shift-drive]] sized for the hull.

[[trunk]]
