---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/refinery.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T00:44:44+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Refinery (Outfitting)

The **Refinery** is an **optional internal** module that converts the raw mineral fragments
scooped by your [[outfitting/mining-tools]] (via [[outfitting/limpet-controllers]] Collector
limpets) into refined, sellable commodities. Without a refinery you cannot process what you
mine. Group `rf`. Stats below are from the Tier-0 Coriolis module definitions.

The refinery is **massless** (0 t — no mass field in the module data), so fitting a bigger one
costs only a slot and power, never jump range.

## How bins work

Each refinery has a number of **bins** (hoppers). A bin holds the partial fragments of **one**
mineral type while it accumulates toward a full unit. More bins = more **different** ores you
can refine concurrently without discarding partial materials. In a mixed-content rock, too few
bins forces you to vent partial fragments — so high-value multi-mineral mining wants more bins.

- **Max bins by class (A-rated):** C1 4 · C2 6 · C3 8 · C4 10.
- Bins rise with **both** class and rating; rating also sets power draw and cost.

## Refinery stats (class / rating)

| Class | Rating | Bins | Power (MW) | Cost (CR) |
|---|---|---|---|---|
| 1 | E | 1 | 0.14 | 6,000 |
| 1 | D | 1 | 0.18 | 18,000 |
| 1 | C | 2 | 0.23 | 54,000 |
| 1 | B | 3 | 0.28 | 162,000 |
| 1 | A | 4 | 0.32 | 486,000 |
| 2 | E | 2 | 0.17 | 12,600 |
| 2 | D | 3 | 0.22 | 37,800 |
| 2 | C | 4 | 0.28 | 113,400 |
| 2 | B | 5 | 0.34 | 340,200 |
| 2 | A | 6 | 0.39 | 1,020,600 |
| 3 | E | 3 | 0.2 | 26,460 |
| 3 | D | 4 | 0.27 | 79,380 |
| 3 | C | 6 | 0.34 | 238,140 |
| 3 | B | 7 | 0.41 | 714,420 |
| 3 | A | 8 | 0.48 | 2,143,260 |
| 4 | E | 4 | 0.25 | 55,566 |
| 4 | D | 5 | 0.33 | 166,698 |
| 4 | C | 7 | 0.41 | 500,094 |
| 4 | B | 9 | 0.49 | 1,500,282 |
| 4 | A | 10 | 0.57 | 4,500,846 |

## Choosing a refinery

- **Bins are the whole point** — pick the rating/class that gives the bin count you need for
  the rock types you mine. Core/laser miners chasing several minerals at once want 8–10 bins.
- **It's massless and class 1–4 only**, so even a top A-rated unit barely dents your build —
  fit the largest your spare slots allow.
- Sits at the **end** of the mining loop: [[outfitting/mining-tools]] free fragments →
  [[outfitting/limpet-controllers]] Collector limpets scoop them → Refinery processes them.
  The [[ships/type-11-prospector]] is the natural hull for the full kit.

[[trunk]]
