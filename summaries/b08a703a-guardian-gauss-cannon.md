---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/guardian_gauss_cannon.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T00:43:20+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Guardian Gauss Cannon — Tier-0 Coriolis extract

Group `ggc`, **hardpoint weapon**, **fixed mount only** (`mount: "F"`), `experimental: true`.
The premier AX anti-Interceptor weapon. **100% thermal** damage (`damagedist {T: 1}`), very high
armour piercing (`piercing: 140`), `requirements.horizons: true` (Guardian Technology Broker
unlock). Two sizes: **class 1 (small, rating D)** and **class 2 (medium, rating B)**. Seeds the
AX-weapon layer of the KB. `availability: live` — AX/Thargoid content is current, accessible (HARD
rule: never present AX as gone).

Key claims (all from the Tier-0 module file):
- **Thermal-only, fixed-mount, charge-fired** AX weapon; range **3000 m**, falloff 1500 m.
- High **distributor draw** and **thermal load** — drains WEP and runs hot. `clip: 1` (single charged
  shot per cycle, then reload).
- Two standard variants + two **pre-engineered reward variants** ("Gauss (HCap + RFire)", `cost: 0`,
  pre-engineered **G1 High Capacity + Rapid Fire**, **not** re-engineerable / grade-changeable /
  experimental-capable).

| Variant | Class | Rating | Dmg/shot | Fire int (s) | Clip/Ammo | Distdraw | Thermload | Power | Mass | Cost (CR) |
|---|---|---|---|---|---|---|---|---|---|---|
| Standard | 1 (S) | D | 22 | 0.83 | 1/80 | 3.8 | 15 | 1.91 | 2 | 167,250 |
| Standard | 2 (M) | B | 38.5 | 0.83 | 1/80 | 7.2 | 25 | 2.61 | 4 | 543,801 |
| HCap+RFire (reward) | 1 (S) | D | 9.6 | 1.15 | 2/200 | 3.8 | 15 | 1.91 | 2 | 0 |
| HCap+RFire (reward) | 2 (M) | B | 18.3 | 1.15 | 2/200 | 7.2 | 25 | 2.61 | 4 | 0 |

Entities: Guardian Gauss Cannon, Guardian Technology Broker, Thargoid Interceptor, AX combat.
Currency signals: experimental AX weapon, Guardian unlock, fixed-only — matches current live roster.
OBSOLETE: NO. Availability per claim: live.
