---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/pulse_laser.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-20T20:56:25+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Pulse Laser (Outfitting)

The **Pulse Laser** is the **baseline primary weapon of human combat** — the cheap, low-power,
efficient thermal staple that nearly every ship can mount and run without straining its power
plant or distributor. It is the first gun most commanders ever fire and the reference point all
other weapons are measured against. In the Coriolis data it is group `pl`, file
`modules/hardpoints/pulse_laser.json` (internal symbol `Hpt_PulseLaser_*`). Unlike the AX and
Guardian weapons it needs **no unlock** and is sold at standard outfitting everywhere.

## What it does

- **100% thermal damage** (`damagedist {T: 1}`) — like all lasers it is **strong vs shields,
  weak vs hull**. Pair it with a kinetic or absolute weapon (multi-cannon, cannon, plasma) to
  finish hulls once shields are down.
- **Discrete pulsed shots**, not a continuous beam. Each pulse draws a small amount of WEP
  capacitor (`distdraw`) and adds a little heat (`thermload`) — both far lower than a Beam or
  Burst Laser, which is the Pulse's whole identity: the **coolest, most power-efficient laser**.
- **Range 3000 m**, with damage falloff beginning at **500 m** — effective up close, tapering off
  past medium range.
- Available in **fixed, gimballed and turret** mounts across **Small, Medium and Large**, plus
  **fixed and gimballed Huge** (there is **no Huge turret** Pulse Laser).
- The trade vs its laser siblings: a Pulse Laser does **less raw DPS than a Burst or
  [[outfitting/beam-laser|Beam Laser]]** but runs cooler and sips less power, so it is the easy,
  sustainable choice — especially on power-starved or beginner builds.

## Variants and stats

Per-shot damage and fire interval (`fireint`, seconds between shots) give the sustained
**DPS = damage ÷ fire interval**. All variants: thermal, range 3000 m, falloff from 500 m.

| Size | Mount | Rating | Dmg/shot | DPS | Power (MW) | Thermload | Distdraw | Piercing | Mass (t) | Cost (CR) |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 Small | Fixed | F | 2.05 | 7.9 | 0.39 | 0.33 | 0.30 | 20 | 2 | 2,200 |
| 1 Small | Gimbal | G | 1.56 | 6.2 | 0.39 | 0.31 | 0.31 | 20 | 2 | 6,600 |
| 1 Small | Turret | G | 1.19 | 4.0 | 0.38 | 0.19 | 0.19 | 20 | 2 | 26,000 |
| 2 Medium | Fixed | E | 3.50 | 12.1 | 0.60 | 0.56 | 0.50 | 35 | 4 | 17,600 |
| 2 Medium | Gimbal | F | 2.68 | 9.6 | 0.60 | 0.54 | 0.54 | 35 | 4 | 35,400 |
| 2 Medium | Turret | F | 2.05 | 6.2 | 0.58 | 0.33 | 0.33 | 35 | 4 | 132,800 |
| 3 Large | Fixed | D | 5.98 | 18.1 | 0.90 | 0.96 | 0.86 | 52 | 8 | 70,400 |
| 3 Large | Gimbal | E | 4.58 | 14.8 | 0.92 | 0.92 | 0.92 | 52 | 8 | 140,600 |
| 3 Large | Turret | F | 3.50 | 9.5 | 0.89 | 0.56 | 0.56 | 52 | 8 | 400,400 |
| 4 Huge | Fixed | A | 10.24 | 27.0 | 1.33 | 1.64 | 1.48 | 65 | 16 | 177,600 |
| 4 Huge | Gimbal | A | 7.82 | 21.7 | 1.37 | 1.56 | 1.56 | 65 | 16 | 877,600 |

(Stats are base, unengineered, from the Coriolis-data definition.)

Within each size the mount choice is the classic laser trade:

- **Fixed** — highest per-shot damage and DPS, lowest cost, but you must aim. The damage choice
  for skilled pilots.
- **Gimbal** — auto-tracks within a cone for a modest damage cut; the all-round default.
- **Turret** — fully auto-tracking and the easiest to use, but the lowest DPS and by far the
  **most expensive** (the Medium turret costs ~7.5× the Medium fixed). Good on multicrew or
  trader hulls that want hands-off point defence.

Piercing rises with size (20 → 65), so larger Pulse Lasers also bypass more of a target's armour
hardness.

## Powerplay variant — Pulse Disruptor

A special **Pulse Disruptor** exists (`Hpt_PulseLaser_Fixed_Medium_Disruptor`: Medium fixed,
2.8 dmg/shot, thermload 1.0, rating E) flagged `powerplay`. It is a **Powerplay pledge reward**
under **Felicia Winters** and adds a module-malfunction effect on hit. It is acquired through
**Powerplay 2.0** (the system was reworked in 2024 — old Powerplay 1 acquisition guides are
stale, so follow current PP2 pledge mechanics). The standard Pulse Lasers above need no pledge.

## How to fit

- Drops into **any hardpoint** of the matching size, fixed/gimbal/turret. Because it is so cool
  and power-cheap, it mixes freely with shields, other weapons and utilities on almost any build —
  it is the safe default when a hull is short on power or distributor capacity.
- A common **starter loadout** is all Pulse Lasers (cheap, forgiving, low heat) before graduating
  to higher-DPS [[outfitting/multi-cannon|multi-cannons]], Burst/[[outfitting/beam-laser|Beam]]
  Lasers or specialised weapons. Lasers strip shields; bring a kinetic or absolute weapon for hulls.
- Manage heat with a [[outfitting/heat-sink-launcher]] only if you stack many high-output weapons;
  a Pulse-Laser-only build rarely needs it.

## Where to get them

Sold at **standard outfitting** at any station with a weapons stock — **no unlock, no Tech Broker,
no Guardian or rank requirement**. This universal availability and low cost is why the Pulse Laser
is the baseline every other primary weapon is compared against.

## Related weapons

- [[outfitting/beam-laser]] — the continuous, higher-DPS thermal sibling that runs hotter and
  hungrier (efficiency vs sustained DPS; same 100% thermal damage).
- [[outfitting/multi-cannon]] — the standard kinetic partner: the Pulse strips shields, the
  multi-cannon chews the hull underneath.
- [[outfitting/ax-multi-cannon]] — the standard AX kinetic workhorse (for Thargoid targets;
  contrast: the Pulse Laser is the all-purpose **human-combat** baseline, weak against Thargoids).
- The Guardian AX trio [[outfitting/guardian-gauss-cannon]], [[outfitting/guardian-plasma-charger]],
  [[outfitting/guardian-shard-cannon]] — specialised anti-Xeno weapons, not human-combat staples.

[[trunk]]
