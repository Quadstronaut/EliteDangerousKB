---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/enzyme_missile_rack.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T01:20:16+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Enzyme Missile Rack (Outfitting)

The **Enzyme Missile Rack** is the **caustic** anti-Xeno (AX) missile — internally a "Caustic Missile"
(symbol `Hpt_CausticMissile_Fixed_Medium`). Its job is not the small direct hit but the **enzyme
caustic damage-over-time** it inflicts: missiles coat a Thargoid in a corrosive enzyme that **degrades
its hull over time**, distinct from the burst damage of the [[outfitting/ax-missile-rack|AX Missile
Rack]]. In the Coriolis data it is group `tbem`, file `hardpoints/enzyme_missile_rack.json`, flagged
`experimental: true`. AX/Thargoid content remains `availability: live` — never present it as gone.

## What it does

- **Caustic enzyme DoT is the point.** The stat block's `damage: 5` is only the direct-impact value;
  the weapon's purpose is the lingering caustic effect that eats Thargoid hull over time. The Coriolis
  data does **not** carry the DoT magnitude, so no per-second figure is asserted here.
- **Explosive damage class** `damagedist {E:1}` for the impact component.
- **Fixed Medium only.** Class 2, Fixed mount — **no Turret, no Small, no Large**. The narrowest
  mount options of the AX missile family.
- **Burst-fire ammo.** clip 8, ammo 64, reload 5 s, fire interval 2.0 s, shot speed 750 m/s,
  piercing 60. Low heat (thermload 1.5), power 1.20 MW.

## Variants and stats

| Coriolis id | Size | Mount | Rating | Dmg | Ammo | Clip | Power (MW) | Thermload | Mass (t) | Cost (CR) |
|---|---|---|---|---|---|---|---|---|---|---|
| xt | 2 Medium | Fixed | B | 5 | 64 | 8 | 1.20 | 1.5 | 4 | 480,501 |

integrity 51, distdraw 0.08, breachmin 0.8 / breachmax 1, all `experimental: true`.

### Pre-engineered reward variant — "Caust Enzyme (High Cap)"

A second fixed form (Coriolis id 5Z) ships pre-engineered with the **Grade 5 High Capacity** blueprint.
It is **not re-engineerable**, **not grade-changeable**, and `canApplyExperimental` is **false** —
a locked loadout. Its `availability` is **CG** (Community Goal reward). (The stored stat block lists
clip 7 / ammo 40 before the blueprint is applied in-game.)

## How to fit

- Takes a **Medium hardpoint, fixed only** — you must hold aim on the target. Best applied to a
  Thargoid Interceptor whose hull you want to soften with the caustic stack while your main guns work
  the hearts.
- Caustic stacking rewards **sustained application**, so the burst-fire clip and low heat let you keep
  refreshing the effect.
- Pair with the kinetic [[outfitting/ax-multi-cannon|AX Multi-Cannon]] /
  [[outfitting/ax-multi-cannon-enhanced|Enhanced AX MC]] and the explosive
  [[outfitting/ax-missile-rack|AX Missile Rack]] / [[outfitting/ax-missile-rack-enhanced|Enhanced]].
  Bring a [[outfitting/heat-sink-launcher]] for the AX fight.

## Where to get it

The Enzyme Missile Rack is an AX weapon from the **anti-Xeno war-effort supply chain** / **Human Tech
Broker**, not a Guardian Structure unlock. The locked "Caust Enzyme (High Cap)" variant comes from a
Community Goal reward.

## Related AX weapons

- [[outfitting/ax-missile-rack]] / [[outfitting/ax-missile-rack-enhanced]] — the explosive AX missiles.
- [[outfitting/ax-multi-cannon]] / [[outfitting/ax-multi-cannon-enhanced]] — the kinetic AX leg.
- [[outfitting/guardian-gauss-cannon]], [[outfitting/guardian-plasma-charger]],
  [[outfitting/guardian-shard-cannon]] — the Guardian AX trio.
- [[outfitting/remote-release-flak-launcher]] / [[outfitting/remote-release-flechette-launcher]] —
  anti-swarm support.

[[trunk]]
