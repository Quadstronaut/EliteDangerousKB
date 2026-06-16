---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/pristmatic_shield_generator.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T01:04:59+00:00
source_count: 1
verified: false
availability: live
changed_note: Prismatic is now an Aisling Duval reward under Powerplay 2.0 (the pledge system was overhauled in 2024); the module itself is unchanged.
---

# Prismatic Shield Generator (Coriolis `psg`)

Core-internal alternative shield generator. **Powerplay reward**, pledged to **Aisling Duval**
(`pp: "Aisling Duval"`, `powerplay: "True"`). Highest shield multiplier of any generator line.
Coriolis filename is the misspelled `internal/pristmatic_shield_generator.json`, export key `psg`.

## Key claims (parsed directly from Tier-0 JSON)

- **A-rating only.** Every class 1–8 ships as a single A-rated variant — no E/D/C/B.
- **Multiplier line (same mechanic as standard generators):** `minmul` 1.0, `optmul` **1.5**,
  `maxmul` 2.0. The 1.5 optmul is higher than a standard A-rated generator (1.2) and far above
  Bi-Weave (0.9) — Prismatic gives the most MJ per slot of any generator.
- **Resistances identical to other generators:** explosive +0.5, kinetic +0.4, thermal −0.2.
  Distributor draw `distdraw` 0.6.
- **Heavy power draw** (the trade-off): class 5 = 5.46 MW vs standard 5A 3.64 MW; class 8 = 8.4 MW.
- **Slow recharge:** `regen` 1.0 MJ/s for classes 1–6, 1.1 at C7, 1.4 at C8; `brokenregen`
  1.2 → 5.4 across the range. Lower regen-per-class than standard, much lower than Bi-Weave.
- **Mass identical to standard generators** (C1 2.5t … C5 40t … C8 320t), so it drops into the
  same core internal slot.
- **Cost is steep:** C1 132,200 CR → C5 7,655,930 CR → C8 243,879,730 CR.

Per-class A-rated table (optmass / minmass→maxmass / power / regen / brokenregen / integrity / cost):

| Class | Opt Mass | Min→Max Mass | Power (MW) | Regen | Broken Regen | Integrity | Cost (CR) |
|---|---|---|---|---|---|---|---|
| 1 | 25 | 13→63 | 2.52 | 1.0 | 1.2 | 48 | 132,200 |
| 2 | 55 | 23→138 | 3.15 | 1.0 | 1.2 | 61 | 240,340 |
| 3 | 165 | 83→413 | 3.78 | 1.0 | 1.3 | 77 | 761,870 |
| 4 | 285 | 143→713 | 4.62 | 1.0 | 1.7 | 96 | 2,415,120 |
| 5 | 405 | 203→1013 | 5.46 | 1.0 | 2.3 | 115 | 7,655,930 |
| 6 | 540 | 270→1350 | 6.51 | 1.0 | 3.2 | 136 | 24,269,300 |
| 7 | 1060 | 530→2650 | 7.35 | 1.1 | 4.2 | 157 | 76,933,670 |
| 8 | 1800 | 900→4500 | 8.4 | 1.4 | 5.4 | 180 | 243,879,730 |

availability: live — Powerplay 2.0 modules remain obtainable by pledging.
obsolete: NO. Destination: merge H2 into kb/outfitting/shield-generator.md.
