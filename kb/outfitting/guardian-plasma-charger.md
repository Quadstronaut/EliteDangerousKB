---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/guardian_plasma_charger.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T00:59:46+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Guardian Plasma Charger (Outfitting)

The **Guardian Plasma Charger** is the **charge-up AX (anti-Xeno) plasma weapon** — hold the trigger
to spin up a plasma orb, release to fire a burst that deals pure **absolute** damage. It is the third
member of the Guardian AX-weapon trio alongside the [[outfitting/guardian-gauss-cannon]] and the
[[outfitting/guardian-shard-cannon]]. In the Coriolis data it is group `gpc`, file
`hardpoints/guardian_plasma_charger.json` (internal symbol `Hpt_Guardian_PlasmaLauncher_*`), flagged
`experimental: true`. AX/Thargoid content remains `availability: live` — never present it as gone.

## What it does

- **100% absolute damage** (`damagedist {A: 1}`). Absolute damage ignores conventional and AX
  resistances entirely, so the Plasma Charger lands consistent damage on Thargoid hearts and hull
  regardless of the target's resistance profile.
- **Charge-fired burst.** The listed `damage` is **per plasma round**; holding the trigger charges
  the weapon and expends up to the full **clip of 15** rounds in a single release, so a fully-charged
  shot delivers a burst (up to ~15× the per-round figure). Short charges fire fewer rounds. Plan WEP
  pips and heat around each release rather than holding fire down.
- **Fixed and turret mounts** (`mount: "F"` / `"T"`) in **Small (class 1), Medium (class 2) and
  Large (class 3)** — a fuller mount ladder than the fixed-only Gauss.
- **High armour piercing** (65 → 95 by size) with a meaningful **breach** chance to damage modules
  behind armour.
- **Ammo 200, reload 3 s, fire interval 0.2 s, shot speed 1200 m/s, falloff 1000 m.** Range is
  3000 m at Small/Large and 3500 m at Medium.

The cost of fielding it is a **high distributor draw** (`distdraw` 0.68 → 2.6) that empties the WEP
capacitor quickly. Pair it with a strong power distributor; its thermal load is modest (4.2 → 6.4),
much lower than the [[outfitting/guardian-gauss-cannon]], so heat is less of a constraint — but still
keep a [[outfitting/heat-sink-launcher]] for AX combat in general.

## Variants and stats

Standard forms, by size and mount (all `experimental: true`, clip 15 / ammo 200 / reload 3 s /
fire int 0.2 s / shot speed 1200):

| Size | Mount | Rating | Dmg/round | Distdraw | Power (MW) | Thermload | Piercing | Range (m) | Mass (t) | Cost (CR) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 Small | Fixed | D | 3 | 0.68 | 1.40 | 4.2 | 65 | 3000 | 2 | 176,500 |
| 1 Small | Turret | F | 2 | 0.80 | 1.60 | 5.0 | 65 | 3000 | 2 | 484,050 |
| 2 Medium | Fixed | B | 5 | 1.25 | 2.13 | 5.2 | 80 | 3500 | 4 | 567,761 |
| 2 Medium | Turret | E | 4 | 1.40 | 2.01 | 5.8 | 80 | 3500 | 4 | 1,659,200 |
| 3 Large | Fixed | C | 7 | 2.42 | 3.10 | 6.2 | 95 | 3000 | 8 | 1,423,301 |
| 3 Large | Turret | D | 6 | 2.60 | 2.53 | 6.4 | 95 | 3000 | 8 | 5,495,200 |

### Pre-engineered reward variant

A cost-**0** reward variant **"Plasma Charger (OC+Foc)"** exists in **Small Fixed (D)** and
**Medium Fixed (B)** forms. It comes **pre-engineered with Grade 1 Overcharged + Focused** and is
**locked**: not re-engineerable, grade cannot be changed, and no experimental effect can be applied.
Otherwise its base stats match the standard fixed module of the same size.

## How to fit

- Goes in a **hardpoint of the matching size** (Small/Medium/Large), fixed or turret. Fixed rewards
  aim with the highest damage; turret eases tracking at the cost of per-shot damage and higher cost.
- **Feed the distributor.** The high WEP draw rewards a high-rating power distributor; charge-and-
  release timing should track your WEP capacitor, not just the trigger.
- Used against **Thargoid Interceptors and Scouts**, at AX combat zones, Spire sites and Titan
  wrecks — all `availability: live`.

## Where to get them

The Guardian Plasma Charger is a **Guardian Technology Broker** unlock: gather Guardian blueprint
fragments and materials at a Guardian Structure site (see Canonn's Guardian site map), then unlock at
a station with a Tech Broker. The cost-0 pre-engineered "OC+Foc" variants are reward modules, not
standard stock.

## Related AX weapons

The Guardian AX-weapon trio: [[outfitting/guardian-gauss-cannon]] (fixed, charge-fired, thermal,
anti-Interceptor specialist), [[outfitting/guardian-shard-cannon]] (close-range thermal shard burst),
and this Plasma Charger (absolute-damage charge burst). The non-Guardian
[[outfitting/ax-multi-cannon]] is the standard kinetic AX workhorse that needs no Guardian unlock.

[[trunk]]
