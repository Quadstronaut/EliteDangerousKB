---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/guardian_fsd_booster.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T00:43:20+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Guardian FSD Booster — Tier-0 Coriolis extract

Group `gfsb`, optional internal, **classes 1–5**, single rating **H** (Guardian). Guardian module
(Guardian Technology Broker unlock) — **powered**. Adds a **flat LY bonus** (`jumpboost`) to every
jump; stacks additively on top of the FSD, does **not** replace it. `integrity` constant **32**,
`mass` constant **1.3 t** across all classes. Description (verbatim): "Used to boost the output of
Frame Shift Drives, but at the cost of overall fuel efficiency." `availability: live`.

This Tier-0 file **independently corroborates** the existing [[mechanics/frame-shift-drive]] claim
that the booster adds **+10.5 LY at class 5**.

Key claims (all from the Tier-0 module file):
- **Flat jump-range addition**, biggest at class 5 (+10.5 LY); same flat bonus regardless of hull, so
  light ships gain the most *relative* range.
- One module per class size (no E/D/A ladder — rating is always `H`).
- Power scales with class; mass is a constant 1.3 t.

| Class | Jump boost (LY) | Power (MW) | Mass (t) | Cost (CR) |
|---|---|---|---|---|
| 1 | +4.00 | 0.75 | 1.3 | 405,022 |
| 2 | +6.00 | 0.98 | 1.3 | 810,521 |
| 3 | +7.75 | 1.27 | 1.3 | 1,620,431 |
| 4 | +9.25 | 1.65 | 1.3 | 3,245,013 |
| 5 | +10.50 | 2.14 | 1.3 | 6,483,101 |

Entities: Guardian FSD Booster, Frame Shift Drive, Guardian Technology Broker, jump range (LY).
Currency signals: Guardian module, flat-boost-by-class — matches current live roster.
OBSOLETE: NO. Availability per claim: live.
