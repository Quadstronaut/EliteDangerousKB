---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/shutdown_field_neutraliser.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T01:41:39+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Shutdown Field Neutraliser (Coriolis Tier-0)

Counters the Thargoid **EMP shutdown-field pulse** — the field a Thargoid Interceptor emits that
disables ship systems (drives, weapons, etc.) mid-fight. Activating the neutraliser before/within
the pulse keeps your ship online. Class-0 utility mount. **availability: live.** Two variants.

## Variants

| id | name | symbol | rating | range | power | activepower | mass | integrity | cost |
|----|------|--------|--------|-------|-------|-------------|------|-----------|------|
| Sn | Shutdown Field Neutraliser | `Hpt_AntiUnknownShutdown_Tiny` | F | 3000 m | 0.2 MW | 0.25 MW | 1.3 t | 35 | 63,000 cr |
| 4E | Thargoid Pulse Neutraliser | `Hpt_AntiUnknownShutdown_Tiny_V2` | E | 0 m | 0.4 MW | 0.33 MW | 3 t | 70 | 150,000 cr |

## Shared constants

- **class:** 0 (utility) · **cooldown:** 10 s · **duration:** 1 · **passive:** 1 (draws power only on activation)

## Notes

- Base (Sn) rating **F**, range **3000 m**. The V2 "Thargoid Pulse Neutraliser" is rating E, heavier
  (3 t), double integrity (70), and carries `range: 0` in the data — recorded verbatim; do not invent a
  numeric reach for it.
- `activepower` (0.25 / 0.33 MW) is the draw while the neutraliser pulse is active, distinct from the
  passive `power` field.
- AX-utility sibling of [[outfitting/xeno-scanner]] and [[outfitting/caustic-sink-launcher]]; pairs with
  the AX weapon line ([[outfitting/ax-multi-cannon]], [[outfitting/guardian-gauss-cannon]]).
- Where: Human Tech Broker / AX war-effort supply.

Claims: (1) two variants base (Sn, rating F) + Thargoid Pulse Neutraliser V2 (4E, rating E);
(2) base range 3000m, V2 range 0 in data; (3) cooldown 10, duration 1, class 0, passive; (4) activepower
0.25/0.33 MW distinct from passive power 0.2/0.4 MW. availability=live, obsolete=NO.
