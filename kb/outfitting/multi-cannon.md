---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/multi_cannon.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-20T21:07:38+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Multi-Cannon (Outfitting)

The **Multi-Cannon** is the **baseline rapid-fire KINETIC primary** of human combat — the
hull-killing partner to the shield-stripping [[outfitting/pulse-laser]]. A laser drops a target's
shields; the Multi-Cannon chews through the **hull** underneath. It is cheap, runs cool, sips power
and carries a large ammo reserve, which is why a **laser + multi-cannon** loadout is the classic
all-purpose human-combat fit. In the Coriolis data it is group `mc`, file
`modules/hardpoints/multi_cannon.json` (internal symbol `Hpt_MultiCannon_*`). It needs **no unlock**
and is sold at standard outfitting everywhere.

This is the **standard human-combat** multi-cannon — distinct from the anti-Thargoid
[[outfitting/ax-multi-cannon]] (the "AT"/AX variant deals anti-Xeno damage and is for Thargoid
targets; this one is the all-purpose kinetic gun for human ships).

## What it does

- **100% kinetic damage** (`damagedist {K: 1}`) — the exact **inverse of a laser**: weak vs shields,
  **strong vs hull**. Bring it to finish hulls once a laser has dropped the shields.
- **Rapid-fire automatic gun.** High rate of fire with per-shot damage; the sustained
  **DPS = damage × rounds-per-shot ÷ fire interval**. (The Huge variants fire **2 rounds per shot**,
  reflected in their DPS.)
- **Runs cool and power-cheap.** Heat (`thermload` 0.04–0.51) and weapon-capacitor draw (`distdraw`
  0.03–0.37) are tiny — trivial to fit and run, leaving headroom for shields and utilities. This is
  the opposite of the hot, hungry [[outfitting/beam-laser]].
- **Ammo-comfortable.** Clip 90–100 with a huge **2100-round reserve** and a 4–5 s reload — long
  engagements without rearming (but it CAN run dry, unlike a laser).
- **Projectile, not hitscan.** Shot speed **1600 m/s**, so you must **lead** moving targets — lasers
  hit instantly, the multi-cannon's rounds take time to arrive.
- **Range 4000 m**, with damage falloff from **2000 m** — longer reach than the 3000 m lasers.
- Available in **fixed, gimballed and turret** mounts across **Small, Medium and Large**, plus
  **fixed and gimballed Huge** — there is **no Huge turret** Multi-Cannon (same family shape as the
  [[outfitting/beam-laser]]).
- **Piercing 22 → 68** by size — slightly higher penetration than the equivalent Pulse Laser.

## Variants and stats

Per-shot damage with fire interval (`fireint`, seconds between shots): **DPS = damage ×
rounds-per-shot ÷ fireint**. All variants: kinetic, range 4000 m, falloff from 2000 m, shot
speed 1600 m/s, ammo reserve 2100.

| Size | Mount | Rating | Dmg/shot | DPS | Fireint (s) | Clip | Power (MW) | Thermload | Distdraw | Piercing | Mass (t) | Cost (CR) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 Small | Fixed | F | 1.12 | 8.6 | 0.13 | 100 | 0.28 | 0.09 | 0.06 | 22 | 2 | 9,500 |
| 1 Small | Gimbal | G | 0.82 | 6.8 | 0.12 | 90 | 0.37 | 0.10 | 0.07 | 22 | 2 | 14,250 |
| 1 Small | Turret | G | 0.56 | 4.0 | 0.14 | 90 | 0.26 | 0.04 | 0.03 | 22 | 2 | 81,600 |
| 2 Medium | Fixed | E | 2.19 | 15.6 | 0.14 | 100 | 0.46 | 0.18 | 0.11 | 37 | 4 | 38,000 |
| 2 Medium | Gimbal | F | 1.64 | 12.6 | 0.13 | 90 | 0.64 | 0.20 | 0.14 | 37 | 4 | 57,000 |
| 2 Medium | Turret | F | 1.17 | 7.3 | 0.16 | 90 | 0.50 | 0.09 | 0.06 | 37 | 4 | 1,292,800 |
| 3 Large | Fixed | C | 3.925 | 23.1 | 0.17 | 100 | 0.64 | 0.28 | 0.18 | 54 | 8 | 140,400 |
| 3 Large | Gimbal | C | 2.84 | 18.9 | 0.15 | 90 | 0.97 | 0.34 | 0.25 | 54 | 8 | 578,436 |
| 3 Large | Turret | E | 2.2 | 11.6 | 0.19 | 90 | 0.86 | 0.20 | 0.16 | 54 | 8 | 3,794,600 |
| 4 Huge | Fixed | A | 4.625 ×2 | 28.0 | 0.33 | 100 | 0.73 | 0.39 | 0.24 | 68 | 16 | 1,177,600 |
| 4 Huge | Gimbal | A | 3.46 ×2 | 23.3 | 0.297 | 90 | 1.22 | 0.51 | 0.37 | 68 | 16 | 6,377,600 |

(Stats are base, unengineered, from the Coriolis-data definition. Huge `Dmg/shot` shown as per-round
× 2 rounds/shot; DPS accounts for both rounds — the Huge fixed's **28.0 DPS is the highest of any
multi-cannon**.)

Within each size the mount choice is the classic kinetic trade:

- **Fixed** — highest DPS, lowest cost, but you must aim and lead. The damage choice for skilled pilots.
- **Gimbal** — auto-tracks within a cone for a modest DPS cut; the all-round default and the easiest
  way to keep a projectile gun on a strafing target.
- **Turret** — fully auto-tracking, lowest DPS, and far the **most expensive** (the Medium turret
  costs ~34× the Medium fixed). Good on multicrew or trader hulls that want hands-off point defence.

## Multi-cannon vs laser — the combo

The Multi-Cannon and a laser are designed to be run **together**, because each covers the other's
weakness:

- A **laser** ([[outfitting/pulse-laser]] / [[outfitting/beam-laser]]) is 100% thermal — it strips
  **shields** fast but bounces off hull.
- The **Multi-Cannon** is 100% kinetic — it barely scratches shields but **shreds hull**.
- Standard human-combat doctrine: **lasers drop the shields, multi-cannons kill the ship.** The MC's
  low heat, low power draw and big ammo reserve make it cheap to keep firing while the lasers do the
  hot, hungry work.

Compared with the [[outfitting/ax-multi-cannon]]: same kinetic, ammo-fed, cool-running character, but
the AX variant adds anti-Xeno damage (and exists only in Medium/Large) for Thargoid targets. Use this
standard Multi-Cannon against **human** ships; use the AX one against **Thargoids**.

## Specials (notes only)

- **Enforcer** (`Hpt_MultiCannon_Fixed_Small_Strong`: Small fixed, 2.9 dmg/shot → ~12.6 DPS, clip 60,
  ammo 1000, piercing 30, range 4500) flagged `powerplay` — a **Powerplay pledge reward under Pranav
  Antal** (Powerplay 2.0; old PP1 guides stale). Harder-hitting, longer-range, smaller-clip kinetic.
- **Pre-engineered Community Goal Multi-Cannon** ("MC (HCap+RFire+Phase)": Medium fixed, clip 294,
  ammo 4706) — pre-engineered Grade-5 **High Capacity + Rapid Fire + Phasing Sequence** (rounds pass
  partly through shields). A one-time **Community Goal** reward (`availability: CG`); existing owners
  keep it, but it is not freely purchasable. Listed for completeness, not as a standard fit.

## How to fit

- Drops into **any hardpoint** of the matching size, fixed/gimbal/turret. Because it is so cool and
  power-cheap, it mixes freely with shields, lasers and utilities on almost any build.
- The standard pairing is **lasers + multi-cannons** (see above). Match calibres to your hardpoints —
  bigger mounts give much higher DPS but cost power-distributor headroom on reload.
- Watch the **ammo**: unlike a laser the MC runs dry. Carry enough reserve (or an engineered High
  Capacity blueprint) for long fights; a [[outfitting/heat-sink-launcher]] is rarely needed for the
  MC's own (negligible) heat.

## Where to get them

Sold at **standard outfitting** at any station with a weapons stock — **no unlock, no Tech Broker,
no Guardian or rank requirement**. Universal availability and very low cost at the small calibres.

## Related weapons

- [[outfitting/pulse-laser]] / [[outfitting/beam-laser]] — the thermal laser partners: lasers strip
  shields, the Multi-Cannon kills hull.
- [[outfitting/ax-multi-cannon]] — the anti-Thargoid (AX) cousin: same kinetic, ammo-fed character
  but adds anti-Xeno damage for Thargoid targets (Medium/Large only).

[[trunk]]
