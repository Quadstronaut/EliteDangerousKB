---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/ax_multi_cannon.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T00:59:46+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# AX Multi-Cannon (Outfitting)

The **AX Multi-Cannon** is the **standard, non-Guardian kinetic AX (anti-Xeno) workhorse** — the
everyman weapon against Thargoid Interceptors and Scouts. Unlike the Guardian AX trio it needs **no
Guardian unlock**, making it the usual entry point into AX combat. In the Coriolis data it is group
`axmc`, file `hardpoints/ax_multi_cannon.json` (internal symbol `Hpt_ATMultiCannon_*`, "AT" = the
game's internal anti-Thargoid tag), flagged `experimental: true`. AX/Thargoid content remains
`availability: live` — never present it as gone.

## What it does

- **AX + kinetic damage** (`damagedist {X: 1, K: 1}`) — split between anti-Xeno (X) and conventional
  kinetic (K). The AX component lets it harm Thargoid biology that shrugs off normal weapons.
- **Sustained automatic fire**, not charge-fired: a large **clip (100 fixed / 90 turret)** and a
  huge **ammo reserve of 2100** make it the most ammo-comfortable AX weapon — long engagements
  without rearming.
- **Long range.** `range` 4000 m with `falloff` at 2000 m: usable for poking hearts and Scouts at
  distance, with reduced damage past 2000 m.
- **Very low heat and power.** Thermal load 0.1 → 0.3 and power 0.46 → 0.64 MW — trivial to fit and
  run, leaving headroom for shields and utilities.
- **Fixed and turret mounts** in **Medium (class 2) and Large (class 3) only** — there is **no Small
  AX Multi-Cannon** in this (standard) line.
- **Piercing 17 (Medium) → 33 (Large)** — lower than the Guardian weapons, so it leans on volume of
  fire rather than per-shot penetration. Shot speed 1600 m/s, reload 4 s.

## Variants and stats

Standard forms (all `experimental: true`; ammo 2100 / reload 4 s / range 4000 m / falloff 2000 m /
shot speed 1600):

| Size | Mount | Rating | Dmg | Clip | Distdraw | Power (MW) | Thermload | Piercing | Mass (t) | Cost (CR) |
|---|---|---|---|---|---|---|---|---|---|---|
| 2 Medium | Fixed | E | 3.3 | 100 | 0.11 | 0.46 | 0.2 | 17 | 4 | 379,000 |
| 2 Medium | Turret | F | 1.7 | 90 | 0.06 | 0.50 | 0.1 | 17 | 4 | 1,826,500 |
| 3 Large | Fixed | C | 6.1 | 100 | 0.18 | 0.64 | 0.3 | 33 | 8 | 1,181,500 |
| 3 Large | Turret | E | 3.3 | 90 | 0.06 | 0.64 | 0.1 | 33 | 8 | 3,821,600 |

Fixed mounts deal nearly double a turret's per-shot damage; turrets trade that for tracking and cost
far more. The Large fixed (6.1/shot) is the standard hard hitter of this line.

> **Enhanced variant.** An upgraded **Enhanced AX Multi-Cannon** (Coriolis group `axmce`) exists as a
> separate module with improved stats and **Small** mounts; it is a likely follow-on KB page. This
> page covers the base AX Multi-Cannon only.

## How to fit

- Drops into any **Medium or Large hardpoint**, fixed or turret. Because it is so cool and
  power-cheap, it mixes freely with Guardian weapons and shields on the same hull.
- A typical **beginner AX loadout** stacks several AX Multi-Cannons (no unlock grind) before
  graduating to the Guardian [[outfitting/guardian-gauss-cannon|Gauss]],
  [[outfitting/guardian-plasma-charger|Plasma Charger]] or
  [[outfitting/guardian-shard-cannon|Shard Cannon]].
- Still bring a [[outfitting/heat-sink-launcher]] — not for this weapon's heat (negligible) but for
  the AX fight in general (Thargoid caustic clouds, silent running, EMP recovery).

## Where to get them

The base AX Multi-Cannon is **not a Guardian unlock** — it is sold at stations associated with the
anti-Xeno war effort (rescue megaships and stations in/near former Thargoid space) and via the
standard Tech Broker where stocked. No Guardian Structure visit is required, which is why it is the
common first AX weapon.

[[trunk]]
