---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/ax_missile_rack_enhanced.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T01:20:16+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Enhanced AX Missile Rack (Outfitting)

The **Enhanced AX Missile Rack** is the upgraded (`v2`) version of the standard
[[outfitting/ax-missile-rack|AX Missile Rack]] — the **explosive** dumbfire leg of anti-Xeno (AX)
weaponry, tuned to hurt Thargoid biology alongside the kinetic
[[outfitting/ax-multi-cannon|AX Multi-Cannon]]. In the Coriolis data it is group `axmre`, file
`hardpoints/ax_missile_rack_enhanced.json` (symbol `Hpt_ATDumbfireMissile_*_v2`), flagged
`experimental: true`. AX/Thargoid content remains `availability: live` — never present it as gone.

## What's "enhanced" — the differences from the base AX Missile Rack

The Enhanced line keeps the base weapon's identity (AX + explosive, dumbfire, burst-fire ammo) but
improves the two things that matter against fast Thargoid targets:

- **Higher per-missile damage.** Fixed mounts hit for **77** (base 64); the Medium turret rises to
  **64** (base 50). The Large turret stays at 64.
- **Faster missiles.** Shot speed jumps to **1250 m/s** (base 750 m/s, ~1.67×), so missiles lead a
  weaving Interceptor far more reliably.
- **Slightly higher power draw.** 1.30 MW Medium (base 1.20), 1.72 / 1.85 MW Large (base 1.62 / 1.75).
- **Lower nominal ratings.** The `v2` forms sit at D/E (Medium) and B/D (Large) versus the base line's
  B/A — the upgrade trades rating-efficiency for raw output, not module quality.

Everything else mirrors the base weapon: `damagedist {X:1, E:1}` (AX + explosive split), **dumbfire
only** (`missile: "D"`, no seeking variant), piercing 60, fire interval 2.0 s, reload 5 s, ammo 64
(Medium) / 128 (Large), clip 8 / 12. Mounts are **Fixed + Turret**; sizes **Medium (2) and Large (3)**
only. Note the Coriolis file **omits the `falloff`/range field** the base line carried (base falloff
10000 m).

## Variants and stats

All four are `experimental: true`, dumbfire (`missile: "D"`), piercing 60, fireint 2.0 s, reload 5 s,
shot speed 1250 m/s:

| Coriolis id | Size | Mount | Rating | Dmg | Ammo | Clip | Power (MW) | Thermload | Distdraw | Mass (t) | Cost (CR) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4S | 2 Medium | Fixed | D | 77 | 64 | 8 | 1.30 | 2.4 | 0.14 | 4 | 681,534 |
| 4T | 2 Medium | Turret | E | 64 | 64 | 8 | 1.30 | 1.5 | 0.08 | 4 | 2,666,286 |
| 4U | 3 Large | Fixed | B | 77 | 128 | 12 | 1.72 | 3.6 | 0.24 | 8 | 1,703,835 |
| 4V | 3 Large | Turret | D | 64 | 128 | 12 | 1.85 | 1.9 | 0.14 | 8 | 5,347,534 |

integrity 51 (Medium) / 64 (Large). Fixed hits for the full 77; the turrets trade down to 64 for
hands-off tracking and cost ~3–4× the matching fixed. Unlike the base line, **there are no
pre-engineered reward variants** in the Enhanced file — these are the plain upgraded forms.

## How to fit

- Drops into any **Medium or Large hardpoint**. Pair the explosive Enhanced AX Missile Rack with the
  kinetic [[outfitting/ax-multi-cannon-enhanced|Enhanced AX Multi-Cannon]] (or base
  [[outfitting/ax-multi-cannon|AX MC]]) so you cover both AX damage profiles.
- Best used in bursts against Interceptor hearts and exposed Scouts; the faster missiles make the
  dumbfire easier to land. Conserve the limited ammo and rearm between fights.
- Bring a [[outfitting/heat-sink-launcher]] for the AX fight (caustic clouds, silent running).

## Where to get it

The Enhanced AX Missile Rack is an upgraded AX weapon obtained via the **Human Tech Broker** (the
AX-weapon broker line), not a Guardian Structure unlock. The base
[[outfitting/ax-missile-rack|AX Missile Rack]] remains the no-unlock entry weapon.

## Related AX weapons

- [[outfitting/ax-missile-rack]] — the base explosive AX missile this upgrades.
- [[outfitting/ax-multi-cannon]] / [[outfitting/ax-multi-cannon-enhanced]] — the kinetic AX leg.
- [[outfitting/enzyme-missile-rack]] — the caustic/enzyme AX missile.
- [[outfitting/guardian-gauss-cannon]], [[outfitting/guardian-plasma-charger]],
  [[outfitting/guardian-shard-cannon]] — the Guardian AX trio.
- [[outfitting/remote-release-flak-launcher]] / [[outfitting/remote-release-flechette-launcher]] —
  anti-swarm support.

[[trunk]]
