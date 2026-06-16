---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/bi_weave_shield_generator.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T00:54:21+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Bi-Weave Shield Generator — Tier-0 parse

Group `bsg` (symbol `..._Class3_Fast`). The "fast-recharge" alternative shield generator:
trades peak shield strength for much higher regeneration. Classes 1–8.

Key claims (from Coriolis module data):
- **C-rating only** — there is exactly one variant per class (no E/D/B/A line). Each is the
  `Int_ShieldGenerator_SizeN_Class3_Fast` module.
- `optmul` **0.9** at every class (vs a standard A-rated 1.2), so raw MJ is lower than an
  A-rated standard shield of the same class. minmul→maxmul 0.4→1.4.
- **Regen is the selling point:** base `regen` 1.8 MJ/s for C1–4, 2.2 (C5), 3.2 (C6), 4.4 (C7),
  5.8 (C8) — roughly 1.8–2.4× a standard generator's regen. `brokenregen` (recovery from
  collapse) 2.4 → 14.4 by class, far faster than standard (1.6 → 9.6).
- Same optmass band as the standard generator per class (C1 25 t … C8 1800 t) and identical
  resistances (explosive +0.5, kinetic +0.4, thermal −0.2; distdraw 0.6).
- Power draw matches the standard C-rated unit of the same class (C8 4 MW). Cheaper than
  top A-rated standard (C8 27.1M vs 162.6M CR).

availability: live. obsolete: NO.
