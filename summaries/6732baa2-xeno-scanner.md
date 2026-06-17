---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/xeno_scanner.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T01:41:39+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Xeno Scanner (Coriolis Tier-0)

Utility scanner that identifies the Thargoid **type** and reveals its **subsystems / weak points**,
making AX targeting effective (you cannot meaningfully target a Thargoid's vulnerable hearts
without a scan). Class-0 utility mount. **availability: live.** Three variants in the data.

## Variants

| id | name | symbol | rating | range | power | mass | integrity | cost |
|----|------|--------|--------|-------|-------|------|-----------|------|
| xs | Xeno Scanner | `Hpt_XenoScanner_Basic_Tiny` | E | 500 m | 0.2 MW | 1.3 t | 56 | 365,698 cr |
| 3y | Enhanced Xeno Scanner | `Hpt_XenoScannerMk2_Basic_Tiny` | C | 2000 m | 0.8 MW | 1.3 t | 56 | 745,948 cr |
| 4B | Pulse Wave Xeno Scanner | `Hpt_XenoScanner_Advanced_Tiny` | C | 1000 m | 1.0 MW | 3 t | 100 | 850,000 cr |

## Shared constants

- **class:** 0 (utility) · **scantime:** 10 s · **scan angle:** 23° · **boot:** 2 s (all variants)

## Notes

- **Range is the key differentiator.** Base 500 m is dangerously short (you must hold scan inside
  a Thargoid's reach); Enhanced (Mk2) quadruples it to 2000 m, the practical default. Pulse Wave
  sits at 1000 m but is heavier (3 t) with double integrity (100) and the highest power (1.0 MW).
- Cross-links: AX weapon family ([[outfitting/ax-multi-cannon]], [[outfitting/guardian-gauss-cannon]]),
  and the AX-utility siblings [[outfitting/shutdown-field-neutraliser]] / [[outfitting/caustic-sink-launcher]].
- Where: Human Tech Broker (Enhanced/Pulse Wave higher tiers).

Claims: (1) three variants base/Enhanced(Mk2)/Pulse Wave; (2) ranges 500/2000/1000 m respectively;
(3) shared scantime 10s, angle 23°, boot 2s, class 0; (4) Pulse Wave mass 3t / integrity 100 vs
others 1.3t/56. availability=live, obsolete=NO.
