---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/burst_laser.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-20T21:21:54+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Burst Laser (Outfitting)

The **Burst Laser** is the **middle laser** of human combat's primary trio — between the cool,
efficient [[outfitting/pulse-laser]] and the hot, continuous [[outfitting/beam-laser]]. It fires a
short **burst of three pulses** per trigger pull, then pauses before the next burst: **mid heat, mid
power draw, mid sustained DPS** — more damage than a Pulse, cooler and cheaper to run than a Beam. In
the Coriolis data it is group `ul`, file `modules/hardpoints/burst_laser.json` (internal symbol
`Hpt_PulseLaserBurst_*`). Like the other standard lasers it needs **no unlock** and is sold at
standard outfitting everywhere.

## What it does

- **100% thermal damage** (`damagedist {T: 1}`) — like all lasers it is **strong vs shields, weak vs
  hull**. Pair it with a kinetic or absolute weapon ([[outfitting/multi-cannon|multi-cannon]],
  [[outfitting/cannon|cannon]], plasma) to finish hulls once shields are down.
- **Burst-fire, not single pulses or a continuous beam.** Each trigger pull fires a **burst of 3
  pulses** in rapid succession (`burst: 3`, intra-burst rate `burstrof`), then waits the inter-burst
  interval (`fireint`) before the next burst. This staccato delivery is the Burst Laser's whole
  identity — it bridges the Pulse's discrete single shots and the Beam's unbroken stream.
- **Range 3000 m**, with damage falloff beginning at **500 m** — same effective band as the Pulse.
  As a hitscan weapon it hits instantly, no projectile lead required.
- **No ammo** — capacitor-limited, never reloaded (you run out of WEP charge, not bullets).
- Available in **fixed, gimballed and turret** mounts across **Small, Medium and Large**, plus
  **fixed and gimballed Huge** — there is **no Huge turret** Burst Laser (same family shape as the
  [[outfitting/pulse-laser]] and [[outfitting/beam-laser]]).

## How sustained DPS works (the burst gap)

The Burst Laser's sustained DPS **cannot** be read as `damage ÷ fireint` — that ignores the three
pulses fired inside each burst. Each cycle delivers `burst × damage` over a time of
`(burst − 1)/burstrof + fireint` seconds (the spacing of the pulses within the burst, plus the gap to
the next burst). So:

> **DPS = (damage × burst) ÷ ((burst − 1)/burstrof + fireint)**

(Worked example, Small fixed: 1.72 × 3 ÷ (2/15 + 0.5) = 5.16 ÷ 0.633 = **8.15 DPS**.) Note the gap
lives in the **`fireint`** field — there is no separate `burstint` field in the data.

## Variants and stats

All variants fire `burst` = 3 pulses per trigger. DPS below folds in the inter-burst gap by the
formula above. Heat/s and WEP/s are the **sustained** drains (per-pulse `thermload`/`distdraw` ×
effective rounds-per-second). All variants: thermal, range 3000 m, falloff from 500 m.

| Size | Mount | Rating | Dmg/shot | DPS | Power (MW) | Heat/s | WEP/s | Piercing | Mass (t) | Cost (CR) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 Small | Fixed | F | 1.72 | 8.1 | 0.65 | 1.80 | 1.18 | 20 | 2 | 4,400 |
| 1 Small | Gimbal | G | 1.22 | 6.4 | 0.64 | 1.80 | 1.27 | 20 | 2 | 8,600 |
| 1 Small | Turret | G | 0.87 | 4.2 | 0.60 | 0.91 | 0.67 | 20 | 2 | 52,800 |
| 2 Medium | Fixed | E | 3.53 | 13.0 | 1.05 | 2.88 | 1.85 | 35 | 4 | 23,000 |
| 2 Medium | Gimbal | F | 2.45 | 10.3 | 1.04 | 2.82 | 2.06 | 35 | 4 | 48,500 |
| 2 Medium | Turret | F | 1.72 | 6.8 | 0.98 | 1.49 | 1.10 | 35 | 4 | 162,800 |
| 3 Large | Fixed | D | 7.73 | 20.8 | 1.66 | 4.57 | 2.98 | 52 | 8 | 140,400 |
| 3 Large | Gimbal | E | 5.16 | 16.6 | 1.65 | 4.57 | 3.31 | 52 | 8 | 281,600 |
| 3 Large | Turret | E | 3.53 | 11.0 | 1.57 | 2.43 | 1.75 | 52 | 8 | 800,400 |
| 4 Huge | Fixed | E | 20.61 | 32.3 | 2.58 | 7.09 | 4.66 | 65 | 16 | 281,600 |
| 4 Huge | Gimbal | E | 12.09 | 25.9 | 2.59 | 7.14 | 5.16 | 65 | 16 | 1,245,600 |

(Stats are base, unengineered, from the Coriolis-data definition. DPS and the per-second heat/WEP
figures are computed from the burst-fire fields as described above.)

Within each size the mount choice is the classic laser trade:

- **Fixed** — highest per-shot damage and DPS, lowest cost, but you must aim. The damage choice for
  skilled pilots.
- **Gimbal** — auto-tracks within a cone for a modest DPS cut; the all-round default.
- **Turret** — fully auto-tracking and the easiest to use, but the lowest DPS and far the **most
  expensive** (the Medium turret costs ~7× the Medium fixed). Good on multicrew or trader hulls that
  want hands-off point defence.

Piercing rises with size (20 → 65), so larger Burst Lasers also bypass more of a target's armour
hardness.

## The laser trio — Pulse < Burst < Beam

The three standard thermal lasers share 100% thermal damage, the same mounts and sizes, and the same
no-unlock availability. They differ on **sustained DPS vs running cost**, and the Burst sits squarely
in the middle:

- **Sustained DPS** climbs Pulse → Burst → Beam at every size. Small fixed: Pulse **7.9** < Burst
  **8.1** < Beam **9.8**. Large fixed: **18.1** < **20.8** < **25.78**. Huge fixed: **27.0** < **32.3**
  < **41.38**.
- **Heat and WEP draw** climb the same order. Large fixed heat/s: Pulse **0.96** < Burst **4.57** <
  Beam **7.2**; WEP/s: **0.86** < **2.98** < **5.1**.
- **Rule of thumb**: the [[outfitting/pulse-laser]] is the cool, power-cheap, beginner-safe baseline;
  the [[outfitting/beam-laser]] is the fastest shield-stripper but cooks the ship and drains the
  distributor; the **Burst Laser is the compromise** — meaningfully more DPS than a Pulse for a
  moderate heat/power bill, without the Beam's punishing demands. A good step up once a build has a
  little distributor and heat headroom but not enough for beams.

## Powerplay variant — Cytoscrambler (note only)

A special **Cytoscrambler** Burst Laser exists (`Hpt_PulseLaserBurst_Fixed_Small_Scatter`: Small
fixed, `burst` 8, `burstrof` 20, 3.6 dmg/shot, `jitter` 1.7, **piercing 1**, range 1000) flagged
`powerplay`. It is a **Powerplay pledge reward under Archon Delaine** — a short-range, high-spread
**scatter** burst that shreds shields up close but has almost no piercing (poor vs hull). It is
acquired through **Powerplay 2.0** (the system was reworked in 2024 — old Powerplay 1 acquisition
guides are stale, so follow current PP2 pledge mechanics). The standard Burst Lasers above need no
pledge.

## How to fit

- Drops into **any hardpoint** of the matching size, fixed/gimbal/turret. Its mid heat and power draw
  make it an easy upgrade over a [[outfitting/pulse-laser]] when the build can spare a little
  distributor and thermal headroom, without committing to the [[outfitting/beam-laser]]'s demands.
- Standard pairing: Burst Lasers to **strip shields**, then a kinetic gun
  ([[outfitting/multi-cannon|multi-cannon]] or [[outfitting/cannon|cannon]]) to **kill the hull**.
  Lasers are weak vs hull; never run an all-laser build against tanky targets.
- A [[outfitting/heat-sink-launcher]] helps if you stack several Bursts or mix in beams; a single
  Burst rarely needs one.

## Where to get them

Sold at **standard outfitting** at any station with a weapons stock — **no unlock, no Tech Broker, no
Guardian or rank requirement**. Universal availability; cost climbs steeply for the larger and turret
variants.

## Related weapons

- [[outfitting/pulse-laser]] — the cool, efficient, lower-DPS baseline thermal laser; the Burst is the
  next step up (more DPS, more heat).
- [[outfitting/beam-laser]] — the continuous, highest-DPS thermal laser that runs hottest and
  hungriest; the Burst sits below it on both DPS and running cost.
- [[outfitting/multi-cannon]] / [[outfitting/cannon]] — the kinetic partners: lasers strip shields,
  the kinetic guns kill hull.
- [[outfitting/ax-multi-cannon]] — the anti-Thargoid kinetic workhorse (contrast: the Burst Laser is
  a human-combat thermal weapon, weak against Thargoids).

[[trunk]]
