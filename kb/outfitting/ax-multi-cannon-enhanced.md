---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/ax_multi_cannon_enhanced.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T01:09:03+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Enhanced AX Multi-Cannon (Outfitting)

The **Enhanced AX Multi-Cannon** is the upgraded version of the standard
[[outfitting/ax-multi-cannon|AX Multi-Cannon]] — the kinetic anti-Xeno (AX) workhorse against
Thargoid Interceptors and Scouts. In the Coriolis data it is group `axmce`, file
`hardpoints/ax_multi_cannon_enhanced.json` (symbol `Hpt_ATMultiCannon_*`, the `V2` / `Gimbal`
forms), flagged `experimental: true`. AX/Thargoid content remains `availability: live` — never
present it as gone.

## What's "enhanced" — the differences from the base AX Multi-Cannon

The Enhanced line keeps the base weapon's identity (AX + kinetic, big ammo, low heat) but improves
the two things that matter most against fast, strafing Thargoids:

- **Gimbal mounts added.** The base AX Multi-Cannon is **Fixed + Turret only**; the Enhanced line is
  **Fixed + Gimbal + Turret**. Gimballed AX fire auto-tracks the target — a major usability gain in
  AX combat where Interceptors orbit and weave.
- **2.5× projectile speed.** Shot speed jumps to **4000 m/s** (base AX MC is 1600 m/s), so shots land
  far more reliably at the 4 km engagement range — fewer wasted rounds on a moving heart.
- **Slightly higher per-shot damage** on the workhorse mounts (Large fixed 7.3 vs base 6.1).
- **No Small mount.** Like the base line, the Enhanced AX MC is **Medium (class 2) and Large
  (class 3) only**. (Earlier KB notes guessed a Small mount existed — the Coriolis data shows none.)

Everything else mirrors the base weapon: `damagedist {X:1, K:1}` (AX + kinetic split), huge **ammo
2100**, **clip 100** (fixed/gimbal) / **90** (turret), **range 4000 m / falloff 2000 m**, reload 4 s,
very low thermal load (0.10–0.28) and modest power (0.46–0.69 MW).

## Variants and stats

Standard forms (all `experimental: true`; ammo 2100 / reload 4 s / range 4000 m / falloff 2000 m /
shot speed 4000):

| Size | Mount | Rating | Dmg | Clip | Power (MW) | Thermload | Piercing | Distdraw | Mass (t) | Cost (CR) |
|---|---|---|---|---|---|---|---|---|---|---|
| 2 Medium | Fixed | D | 3.9 | 100 | 0.48 | 0.18 | 17 | 0.11 | 4 | 455,077 |
| 2 Medium | Gimbal | E | 3.7 | 100 | 0.46 | 0.18 | 17 | 0.11 | 4 | 1,197,644 |
| 2 Medium | Turret | E | 2.0 | 90 | 0.52 | 0.10 | 17 | 0.06 | 4 | 2,193,297 |
| 3 Large | Fixed | B | 7.3 | 100 | 0.69 | 0.28 | 33 | 0.18 | 8 | 1,360,322 |
| 3 Large | Gimbal | C | 6.3 | 100 | 0.64 | 0.28 | 33 | 0.18 | 8 | 2,390,460 |
| 3 Large | Turret | D | 3.9 | 90 | 0.69 | 0.10 | 33 | 0.06 | 8 | 4,588,709 |

Fire interval is 0.14 s (Medium fixed/gimbal), 0.16 s (turrets) and 0.17 s (Large fixed/gimbal);
integrity 51 (Medium) / 64 (Large). As with the base line, **fixed** hits hardest per shot, **gimbal**
trades a little damage for tracking, and **turret** trades the most for hands-off fire and costs the
most.

### Pre-engineered reward variants — "AX MC (OC, Auto-Load)"

Two gimbal forms ship pre-engineered (Coriolis ids 5y / 5z):

| Size | Mount | Rating | Dmg | Power (MW) | Cost (CR) |
|---|---|---|---|---|---|
| 2 Medium | Gimbal | E | 2.4 | 0.805 | 1,197,644 |
| 3 Large | Gimbal | C | 4.065 | 1.12 | 2,390,460 |

Both carry **Grade 5 Overcharged** plus the **Auto-Loader** experimental (reloads the clip during
fire — excellent for the AX MC's sustained-fire role). They are **not re-engineerable** and **not
grade-changeable**, but `canApplyExperimental` is **true**, so a different experimental can be
swapped in.

## How to fit

- Drops into any **Medium or Large hardpoint**. The gimbal option makes this the friendlier AX MC for
  pilots who struggle to hold fixed convergence on a strafing Interceptor.
- Still pairs naturally with the Guardian AX trio —
  [[outfitting/guardian-gauss-cannon|Gauss]], [[outfitting/guardian-plasma-charger|Plasma Charger]],
  [[outfitting/guardian-shard-cannon|Shard Cannon]] — and with the explosive
  [[outfitting/ax-missile-rack|AX Missile Rack]] for a kinetic+explosive mix.
- Bring a [[outfitting/heat-sink-launcher]] for the AX fight in general (caustic clouds, silent
  running, EMP recovery) — not for this weapon's heat, which is negligible.

## Where to get it

The Enhanced AX Multi-Cannon is an upgraded AX weapon obtained via the **Human Tech Broker** (the
AX-weapon broker line), not a Guardian Structure unlock. The base
[[outfitting/ax-multi-cannon|AX Multi-Cannon]] remains the no-unlock entry weapon.

## Related AX weapons

- [[outfitting/ax-multi-cannon]] — the base kinetic workhorse this upgrades.
- [[outfitting/ax-missile-rack]] — the explosive AX missile leg.
- [[outfitting/guardian-gauss-cannon]], [[outfitting/guardian-plasma-charger]],
  [[outfitting/guardian-shard-cannon]] — the Guardian AX trio.
- [[outfitting/remote-release-flak-launcher]] — anti-swarm flak support.

[[trunk]]
