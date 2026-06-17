---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/guardian_shard_cannon.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T00:59:46+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Guardian Shard Cannon (Outfitting)

The **Guardian Shard Cannon** is the **close-range AX (anti-Xeno) shotgun** — each pull of the
trigger sprays a spread of **12 thermal shards**. It is the highest-sustained-DPS member of the
Guardian AX-weapon trio, alongside the [[outfitting/guardian-gauss-cannon]] and the
[[outfitting/guardian-plasma-charger]]. In the Coriolis data it is group `gsc`, file
`hardpoints/guardian_shard_cannon.json` (internal symbol `Hpt_Guardian_ShardCannon_*`), flagged
`experimental: true`. AX/Thargoid content remains `availability: live` — never present it as gone.

## What it does

- **100% thermal damage** (`damagedist {T: 1}`), like the Gauss cannon — effective against exposed
  Thargoid hearts.
- **Shotgun spread.** Each shot fires **12 shards** (`roundspershot: 12`) with **jitter 5** (a
  cone of spread). The listed `damage` is **per shard**, so a full hit at close range stacks all
  12 — but spread and jitter mean you must be **close** to land them all.
- **Short range.** `range` and `falloff` are both **1700 m**: full damage out to 1700 m, then a hard
  cut-off. This is a brawling weapon, not a poke-from-range tool.
- **Fixed and turret mounts** in **Small (class 1), Medium (class 2) and Large (class 3)**.
- **Very low thermal load** (0.6 → 2.2) — far cooler than Gauss — so it sustains fire well and is
  forgiving on heat. Distributor draw is low at Small but climbs at Large.
- **Clip 5, ammo 180, reload 5 s, fire interval 0.6 s, shot speed 1133 m/s, piercing 30 → 60.**

## Variants and stats

Standard forms, by size and mount (all `experimental: true`; 12 shards/shot, clip 5 / ammo 180 /
reload 5 s / fire int 0.6 s / range 1700 m / jitter 5). "Dmg/shot" is the per-shard figure × 12 at a
full point-blank hit:

| Size | Mount | Rating | Dmg/shard | Dmg/shot (×12) | Distdraw | Power (MW) | Thermload | Piercing | Mass (t) | Cost (CR) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 Small | Fixed | D | 2.0 | 24.0 | 0.42 | 0.87 | 0.7 | 30 | 2 | 151,650 |
| 1 Small | Turret | F | 1.1 | 13.2 | 0.36 | 0.72 | 0.6 | 30 | 2 | 502,000 |
| 2 Medium | Fixed | A | 3.7 | 44.4 | 0.65 | 1.21 | 1.2 | 45 | 4 | 507,761 |
| 2 Medium | Turret | D | 2.4 | 28.8 | 0.57 | 1.16 | 1.1 | 45 | 4 | 1,767,001 |
| 3 Large | Fixed | C | 5.2 | 62.4 | 1.40 | 1.68 | 2.2 | 60 | 8 | 1,461,350 |
| 3 Large | Turret | D | 3.4 | 40.8 | 1.20 | 1.39 | 2.0 | 60 | 8 | 5,865,026 |

### Pre-engineered reward variants

Two cost-**0** reward variants exist (Medium Fixed is rating A — the trio's only base-A weapon):

- **"Shard (OC+Foc+SPen)"** — Small Fixed (D) and Medium Fixed (A). Pre-engineered **Grade 1 Long
  Range + Focused** with the **Super Penetrator** experimental (`special_super_penetrator_cooled`);
  unusually, `canApplyExperimental` is **true** here. Long Range stretches the otherwise short reach.
- **"Shard (Long Range)"** — Medium Fixed (A). Pre-engineered **Grade 5 Long Range** (a Community
  Goal reward, `availability: CG`) and **locked** (not re-engineerable, no grade change, no
  experimental).

## How to fit

- Pick the **largest size your hardpoint allows** — Large fixed is the heavy hitter (62.4/shot at
  point blank). Use it on agile ships that can stay inside 1700 m of an Interceptor.
- The **low heat** makes it the easiest Guardian AX weapon to sustain; still bring a
  [[outfitting/heat-sink-launcher]] for the rest of the AX loadout.
- A common AX build pairs short-range Shard Cannons (sustained thermal) with longer-range
  [[outfitting/guardian-gauss-cannon|Gauss]] or [[outfitting/ax-multi-cannon|AX Multi-Cannons]] for
  flexibility.

## Where to get them

The Guardian Shard Cannon is a **Guardian Technology Broker** unlock: gather Guardian blueprint
fragments and materials at a Guardian Structure site (see Canonn's Guardian site map), then unlock at
a station with a Tech Broker. The cost-0 pre-engineered variants are reward modules, not stock.

## Related AX weapons

The Guardian AX-weapon trio: [[outfitting/guardian-gauss-cannon]] (long-range thermal, anti-
Interceptor specialist), [[outfitting/guardian-plasma-charger]] (absolute-damage charge burst), and
this Shard Cannon (close-range thermal shotgun). The non-Guardian [[outfitting/ax-multi-cannon]] is
the standard kinetic AX workhorse that needs no Guardian unlock.

[[trunk]]
