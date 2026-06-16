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

# Shield Booster (Coriolis `sb`)

**Utility-mount** module (not internal). Coriolis path is `hardpoints/shield_booster.json`,
export key `sb`. All variants are **class 0** (size 0, the utility slot) and `passive: 1` —
always-on, no activation. Adds a flat percentage to the ship's total shield strength.

## Key claims (parsed directly from Tier-0 JSON)

- **Five ratings E→A, all class 0.** Rating sets the boost: `shieldboost` E +4%, D +8%, C +12%,
  B +16%, A +20% (the fraction added to total shield MJ).
- **Boosts are multiplicative-stacking with diminishing returns in-game** — Coriolis stores the
  raw per-module figure; multiple boosters do not add linearly once several are fitted (game
  applies stacking falloff). The JSON only carries the single-module value.
- **Base module gives no resistances:** `explres`/`kinres`/`thermres` all 0 — resistance comes
  only from engineering (e.g. Resistance Augmented blueprint). The booster scales the *strength*
  of whatever shield you already have.
- **Mass/power climb with rating:** E 0.5t / 0.2 MW → A 3.5t / 1.2 MW.
- **Cheap:** E 10,000 CR → A 281,000 CR.

| Rating | Shield Boost | Mass (t) | Power (MW) | Integrity | Cost (CR) |
|---|---|---|---|---|---|
| E | +4% | 0.5 | 0.2 | 25 | 10,000 |
| D | +8% | 1.0 | 0.5 | 35 | 23,000 |
| C | +12% | 2.0 | 0.7 | 40 | 53,000 |
| B | +16% | 3.0 | 1.0 | 45 | 122,000 |
| A | +20% | 3.5 | 1.2 | 48 | 281,000 |

availability: live. obsolete: NO. Destination: new page kb/outfitting/shield-booster.md;
pairs with kb/outfitting/shield-generator.md.
