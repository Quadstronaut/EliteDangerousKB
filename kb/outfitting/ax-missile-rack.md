---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/ax_missile_rack.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T01:09:03+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# AX Missile Rack (Outfitting)

The **AX Missile Rack** is the **explosive** leg of anti-Xeno (AX) weaponry — high-damage dumbfire
missiles tuned to hurt Thargoid biology, complementing the kinetic
[[outfitting/ax-multi-cannon|AX Multi-Cannon]]. In the Coriolis data it is group `axmr`, file
`hardpoints/ax_missile_rack.json` (symbol `Hpt_ATDumbfireMissile_*`), flagged `experimental: true`.
AX/Thargoid content remains `availability: live` — never present it as gone.

## What it does

- **AX + explosive damage** (`damagedist {X:1, E:1}`) — the AX component harms Thargoid biology; the
  explosive component is the "kinetic/explosive mix" partner to the AX MC's AX+kinetic profile.
- **Dumbfire only.** Every variant is `missile: "D"` (dumbfire) — there is **no seeking variant** in
  this module file. Aim and lead the target yourself; the high projectile range covers the rest.
- **Big per-missile hits.** 64 damage per missile on the Fixed Medium and both Large variants
  (Medium turret 50), with **piercing 60** — far higher penetration than the AX MC's 17/33.
- **Very long reach.** `falloff` is **10000 m**, so missiles deal full damage out to 10 km
  (shot speed 750 m/s, so lead generously at range).
- **Limited ammo.** Fire interval 2.0 s, reload 5 s; ammo 64 (Medium) / 128 (Large), clip 8 / 12 —
  a burst weapon, not a sustained-fire one. Heat is moderate (thermload 1.5–3.6).

## Variants and stats

Standard forms (all `experimental: true`, dumbfire; falloff 10000 m / fireint 2.0 s / reload 5 s /
piercing 60 / shot speed 750):

| Size | Mount | Rating | Dmg | Ammo | Clip | Power (MW) | Thermload | Distdraw | Mass (t) | Cost (CR) |
|---|---|---|---|---|---|---|---|---|---|---|
| 2 Medium | Fixed | B | 64 | 64 | 8 | 1.20 | 2.4 | 0.14 | 4 | 540,900 |
| 2 Medium | Turret | B | 50 | 64 | 8 | 1.20 | 1.5 | 0.08 | 4 | 2,022,700 |
| 3 Large | Fixed | A | 64 | 128 | 12 | 1.62 | 3.6 | 0.24 | 8 | 1,352,250 |
| 3 Large | Turret | A | 64 | 128 | 12 | 1.75 | 1.9 | 0.14 | 8 | 4,056,750 |

Mounts are **Fixed + Turret**; classes **Medium (2) and Large (3)** only (no Small). integrity 51
(Medium) / 64 (Large). Fixed Medium and both Large variants hit for the full 64; the Medium turret
trades down to 50 for tracking and costs ~4× the fixed.

### Pre-engineered reward variants — "AX MRack (HCap+RFire)"

Two fixed forms ship pre-engineered (Coriolis ids 5w / 5x):

| Size | Mount | Rating | Dmg | Ammo | Clip | Fireint | Reload | Power | Cost (CR) |
|---|---|---|---|---|---|---|---|---|---|
| 2 Medium | Fixed | E | 71.5 | 64 | 8 | 3.045 | 7.85 | 1.20 | 540,900 |
| 3 Large | Fixed | C | 71.5 | 128 | 12 | 3.045 | 7.85 | 1.62 | 0 |

Both carry **Grade 5 High Capacity + Rapid Fire** (higher per-missile damage, slower fire interval).
They are **not re-engineerable**, **not grade-changeable**, and `canApplyExperimental` is **false** —
fixed loadouts. The Large variant's **cost 0** marks it as a reward (e.g. Community Goal) module.

## How to fit

- Drops into any **Medium or Large hardpoint**. Pair the explosive AX Missile Rack with the kinetic
  [[outfitting/ax-multi-cannon|AX Multi-Cannon]] (or [[outfitting/ax-multi-cannon-enhanced|Enhanced
  AX MC]]) so you cover both AX damage profiles.
- Best used in bursts against Interceptor hearts and exposed Scouts; conserve the limited ammo and
  rearm between fights.
- Bring a [[outfitting/heat-sink-launcher]] for the AX fight (caustic clouds, silent running).

## Where to get it

AX weapons are obtained from the **anti-Xeno war-effort supply chain** (rescue megaships / stations
in and near former Thargoid space) and the **Human Tech Broker**. No Guardian Structure visit is
required. The Enhanced variant (`axmre`) is a follow-on research target.

## Related AX weapons

- [[outfitting/ax-multi-cannon]] / [[outfitting/ax-multi-cannon-enhanced]] — the kinetic AX leg.
- [[outfitting/guardian-gauss-cannon]], [[outfitting/guardian-plasma-charger]],
  [[outfitting/guardian-shard-cannon]] — the Guardian AX trio.
- [[outfitting/remote-release-flak-launcher]] — anti-swarm flak support.

[[trunk]]
