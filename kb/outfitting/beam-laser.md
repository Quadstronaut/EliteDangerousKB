---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/beam_laser.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-20T21:07:38+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Beam Laser (Outfitting)

The **Beam Laser** is the **continuous-fire, highest-sustained-DPS thermal laser** — the hot,
hungry sibling of the [[outfitting/pulse-laser]]. Where the Pulse fires discrete pulses cheaply and
coolly, the Beam pours out an **unbroken beam** for the most sustained thermal damage of the laser
family, at a steep **heat and power** cost. In the Coriolis data it is group `bl`, file
`modules/hardpoints/beam_laser.json` (internal symbol `Hpt_BeamLaser_*`). Like the Pulse it needs
**no unlock** and is sold at standard outfitting everywhere.

## What it does

- **100% thermal damage** (`damagedist {T: 1}`) — like all lasers it is **strong vs shields, weak
  vs hull**. The Beam is the fastest shield-stripper in the laser family; pair it with a kinetic or
  absolute weapon ([[outfitting/multi-cannon|multi-cannon]], cannon, plasma) to finish hulls.
- **Continuous beam, not pulsed.** The Beam deals damage every instant the trigger is held, so the
  Coriolis `damage` field IS the **per-second figure (DPS)** — there is no fire interval to divide
  by. `thermload` and `distdraw` are likewise **per-second** drains.
- **Runs hot and hungry — its defining trait.** Both heat (`thermload`) and weapon-capacitor draw
  (`distdraw`) are far higher than the Pulse: a Large fixed Beam dumps 7.2 heat/s and 5.1 WEP/s,
  versus the Large fixed Pulse's 0.96 and 0.86. The Beam will **overheat a hull and drain the WEP
  capacitor** quickly if you hold the trigger — it rewards short, disciplined bursts and a strong
  distributor.
- **No ammo** — capacitor-limited, never reloaded (you run out of WEP charge, not bullets).
- **Range 3000 m**, with damage falloff beginning at **600 m** — slightly longer effective band than
  the Pulse (falloff 500 m), but the same 3000 m hard cap. As a hitscan weapon it hits instantly,
  no projectile lead required.
- Available in **fixed, gimballed and turret** mounts across **Small, Medium and Large**, plus
  **fixed and gimballed Huge** — there is **no Huge turret** Beam Laser (same family shape as the
  Pulse).

## Variants and stats

For a continuous beam, the listed **DPS = the `damage` field directly** (no per-shot conversion).
Thermload and distdraw shown are per-second. All variants: thermal, range 3000 m, falloff from 600 m.

| Size | Mount | Rating | DPS | Power (MW) | Thermload/s | Distdraw/s | Piercing | Mass (t) | Cost (CR) |
|---|---|---|---|---|---|---|---|---|---|
| 1 Small | Fixed | E | 9.8 | 0.62 | 3.5 | 1.94 | 18 | 2 | 37,430 |
| 1 Small | Gimbal | E | 7.66 | 0.60 | 3.6 | 2.11 | 18 | 2 | 74,650 |
| 1 Small | Turret | F | 5.4 | 0.57 | 2.4 | 1.32 | 18 | 2 | 500,000 |
| 2 Medium | Fixed | D | 15.96 | 1.01 | 5.1 | 3.16 | 35 | 4 | 299,520 |
| 2 Medium | Gimbal | D | 12.52 | 1.00 | 5.3 | 3.44 | 35 | 4 | 500,600 |
| 2 Medium | Turret | E | 8.82 | 0.93 | 3.5 | 2.16 | 35 | 4 | 2,099,900 |
| 3 Large | Fixed | C | 25.78 | 1.62 | 7.2 | 5.10 | 50 | 8 | 1,177,600 |
| 3 Large | Gimbal | C | 20.28 | 1.60 | 7.6 | 5.58 | 50 | 8 | 2,396,160 |
| 3 Large | Turret | D | 14.34 | 1.51 | 5.1 | 3.51 | 50 | 8 | 19,399,600 |
| 4 Huge | Fixed | A | 41.38 | 2.61 | 9.9 | 8.19 | 60 | 16 | 2,396,160 |
| 4 Huge | Gimbal | A | 32.68 | 2.57 | 10.6 | 8.99 | 60 | 16 | 8,746,160 |

(Stats are base, unengineered, from the Coriolis-data definition.)

Within each size the mount choice is the classic laser trade:

- **Fixed** — highest DPS, lowest cost, but you must aim. The damage choice for skilled pilots.
- **Gimbal** — auto-tracks within a cone for a modest DPS cut; the all-round default.
- **Turret** — fully auto-tracking and the easiest to use, but the lowest DPS and by far the **most
  expensive** (the Large turret costs ~16× the Large fixed). Good on multicrew or trader hulls that
  want hands-off point defence.

Piercing rises with size (18 → 60), so larger Beam Lasers also bypass more of a target's armour
hardness.

## Beam vs Pulse — efficiency vs sustained DPS

Same 100% thermal damage, same mounts and sizes, same no-unlock availability — the difference is
**sustained DPS vs running cost**:

- The Beam does **more DPS** at every size (e.g. Small fixed **9.8** vs the Pulse's 7.9; Large fixed
  **25.78** vs 18.1), and needs **no aiming gaps** — held continuously it strips shields faster.
- But it runs far **hotter and hungrier**: the Large fixed Beam's 7.2 heat/s and 5.1 WEP/s dwarf the
  Pulse's 0.96 and 0.86, so the Beam will cook the ship and empty the distributor if over-held.
- **Rule of thumb**: the [[outfitting/pulse-laser]] is the cool, power-cheap, beginner-safe baseline;
  the Beam is the choice when you have the **power plant, distributor and heat headroom** to convert
  that capacity into the fastest shield-stripping in the laser family. (The Burst Laser sits between
  them — pulsed bursts, mid heat/DPS.)

## Powerplay variant — Retributor

A special **Retributor** Beam Laser exists (`Hpt_BeamLaser_Fixed_Small_Heat`: Small fixed, DPS 4.9,
thermload **2.7** — notably cooler than the standard Small fixed's 3.5) flagged `powerplay`. It is a
**Powerplay pledge reward under Edmund Mahon** and trades raw damage for reduced heat (and applies a
shield-disruption effect). It is acquired through **Powerplay 2.0** (the system was reworked in 2024
— old Powerplay 1 acquisition guides are stale, so follow current PP2 pledge mechanics). The standard
Beam Lasers above need no pledge.

## How to fit

- Drops into **any hardpoint** of the matching size, fixed/gimbal/turret. Because it is heat- and
  power-intensive, budget for it: a strong **Power Distributor** (WEP capacitor + recharge) keeps the
  beam firing, and a [[outfitting/heat-sink-launcher]] dumps the heat spikes — far more relevant here
  than on a Pulse build.
- Common pairing: Beam Lasers to **strip shields fast**, then [[outfitting/multi-cannon|multi-cannons]]
  (cool, ammo-cheap kinetic) to **chew the hull**. Lasers are weak vs hull; never run beams alone.
- On power-starved or beginner hulls the [[outfitting/pulse-laser]] is the safer baseline; step up to
  the Beam once the build has distributor and heat headroom to spare.

## Where to get them

Sold at **standard outfitting** at any station with a weapons stock — **no unlock, no Tech Broker,
no Guardian or rank requirement**. Universal availability; the cost climbs steeply for the larger and
turret variants.

## Related weapons

- [[outfitting/pulse-laser]] — the cool, efficient, lower-DPS baseline thermal laser; the Beam's
  direct sibling (efficiency vs sustained DPS).
- [[outfitting/multi-cannon]] — the kinetic partner: lasers drop shields, the multi-cannon kills hull.
- [[outfitting/ax-multi-cannon]] — the anti-Thargoid kinetic workhorse (contrast: the Beam is a
  human-combat thermal weapon, weak against Thargoids).

[[trunk]]
