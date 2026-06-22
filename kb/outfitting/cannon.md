---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/cannon.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-20T21:21:54+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Cannon (Outfitting)

The **Cannon** is the **high-damage, low-rate kinetic primary** of human combat — the alpha-strike
partner to the rapid-fire [[outfitting/multi-cannon]]. Where the Multi-Cannon chips away with a
stream of small rapid rounds, the Cannon fires **big, slow shells**: large per-shot damage, a tiny
clip, a slow rate of fire, and a projectile you must lead. It is the kinetic **burst-damage** option,
and the standard weapon with the **deepest armour piercing**. In the Coriolis data it is group `c`,
file `modules/hardpoints/cannon.json` (internal symbol `Hpt_Cannon_*`). It needs **no unlock** and is
sold at standard outfitting everywhere.

## What it does

- **100% kinetic damage** (`damagedist {K: 1}`) — like the [[outfitting/multi-cannon]] it is the
  **inverse of a laser**: weak vs shields, **strong vs hull**. Bring it to break hulls once a laser
  ([[outfitting/pulse-laser]] / [[outfitting/beam-laser]] / [[outfitting/burst-laser]]) has dropped
  the shields.
- **Big slow shells.** High per-shot damage (Small fixed 22.5 → Huge fixed 82.1) on a **slow fire
  interval** (`fireint` 1.9–2.7 s) and a **small clip** (5–6 rounds) with a 3–4 s reload. This is the
  defining trade vs the Multi-Cannon: punch-per-shot over rate-of-fire.
- **Projectile, must lead.** Shot speed **750–1200 m/s** — *slower* than the Multi-Cannon's 1600 m/s,
  so the shells take real time to arrive. Lead moving targets generously.
- **No damage falloff inside its range.** Uniquely among the primaries, the Cannon's `falloff` equals
  its `range` at every size (3000 / 3500 / 4000 / 4500 m), so it deals **full damage all the way out
  to maximum range** — the Multi-Cannon, by contrast, starts losing damage at 2000 m.
- **Highest kinetic piercing**: 35 → 90 by size, well above the Multi-Cannon's 22 → 68. The Cannon is
  the best standard weapon at punching through a target's **armour hardness**.
- **Ammo-fed.** 100–120-round reserve; runs dry eventually (unlike a laser), but the small clip and
  slow fire mean ammo lasts a long time. Heat (`thermload`) is moderate — warmer per shot than a
  Multi-Cannon, far cooler than a beam.
- Available in **fixed, gimballed and turret** mounts across **Small, Medium and Large**, plus
  **fixed and gimballed Huge** — there is **no Huge turret** Cannon (same family shape as the lasers
  and the Multi-Cannon).

## Variants and stats

Per-shot damage with fire interval (`fireint`, seconds between shots). Two DPS columns: **Burst DPS**
= `damage ÷ fireint` (output while the clip lasts) and **Sust. DPS** = the reload-inclusive figure
`damage × clip ÷ (clip × fireint + reload)` — the small clip and 3–4 s reload pull sustained output
well below the burst rate. All variants: kinetic, full damage to max range (no falloff degradation).

| Size | Mount | Rating | Dmg/shot | Burst DPS | Sust. DPS | Fireint (s) | Clip | Reload (s) | Shotspeed | Range (m) | Power (MW) | Thermload | Piercing | Mass (t) | Cost (CR) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 Small | Fixed | D | 22.5 | 11.3 | 9.0 | 2.00 | 6 | 3 | 1200 | 3000 | 0.34 | 1.4 | 35 | 2 | 21,100 |
| 1 Small | Gimbal | E | 16.0 | 8.3 | 5.9 | 1.92 | 5 | 4 | 1000 | 3000 | 0.38 | 1.3 | 35 | 2 | 42,200 |
| 1 Small | Turret | F | 12.75 | 5.5 | 4.1 | 2.31 | 5 | 4 | 1000 | 3000 | 0.32 | 0.7 | 35 | 2 | 506,400 |
| 2 Medium | Fixed | D | 36.5 | 16.8 | 13.7 | 2.17 | 6 | 3 | 1051 | 3500 | 0.49 | 2.1 | 50 | 4 | 168,430 |
| 2 Medium | Gimbal | D | 24.5 | 11.8 | 8.5 | 2.08 | 5 | 4 | 875 | 3500 | 0.54 | 1.9 | 50 | 4 | 337,600 |
| 2 Medium | Turret | E | 19.77 | 7.9 | 6.0 | 2.50 | 5 | 4 | 875 | 3500 | 0.45 | 1.0 | 50 | 4 | 4,051,200 |
| 3 Large | Fixed | C | 54.94 | 23.1 | 19.1 | 2.38 | 6 | 3 | 959 | 4000 | 0.67 | 3.2 | 70 | 8 | 675,200 |
| 3 Large | Gimbal | C | 37.39 | 16.5 | 12.2 | 2.27 | 5 | 4 | 800 | 4000 | 0.75 | 2.9 | 70 | 8 | 1,350,400 |
| 3 Large | Turret | D | 30.4 | 11.2 | 8.6 | 2.72 | 5 | 4 | 800 | 4000 | 0.64 | 1.6 | 70 | 8 | 16,204,800 |
| 4 Huge | Fixed | B | 82.1 | 31.2 | 26.2 | 2.63 | 6 | 3 | 900 | 4500 | 0.92 | 4.8 | 90 | 16 | 2,700,800 |
| 4 Huge | Gimbal | B | 56.58 | 22.6 | 17.2 | 2.50 | 5 | 4 | 750 | 4500 | 1.03 | 4.4 | 90 | 16 | 5,401,600 |

(Stats are base, unengineered, from the Coriolis-data definition.)

Within each size the mount choice is the classic kinetic trade:

- **Fixed** — highest per-shot damage and DPS, lowest cost, **6-round clip** (vs 5 for gimbal/turret)
  and the fastest 3 s reload, but you must aim and lead. The damage choice for skilled pilots.
- **Gimbal** — auto-tracks within a cone for a damage cut; easier to keep a slow shell on a strafing
  target.
- **Turret** — fully auto-tracking, lowest DPS, and far the **most expensive** (the Large turret
  costs ~24× the Large fixed). Good on multicrew or trader hulls that want hands-off point defence.

## Cannon vs Multi-Cannon — the two kinetics

Both are 100% kinetic hull-killers, but they play very differently:

- **Multi-Cannon** = rapid chip damage. Small per-shot hits, very high rate of fire, a big clip
  (90–100) and a fast 1600 m/s projectile. Forgiving, sustained, ammo-rich.
- **Cannon** = slow alpha strikes. Huge per-shot shells, a tiny clip (5–6), a slow 1.9–2.7 s fire
  interval and a slower projectile you must lead. Punishing to land but devastating per hit.
- **Per-second DPS is similar** at the same mount (e.g. Large fixed: Cannon 23.1 burst vs Multi-Cannon
  23.1), but the Cannon concentrates it into far fewer, far harder shots, and adds **much higher
  piercing** (Large 70 vs 54; Huge 90 vs 68) plus **no range falloff**. That makes the Cannon the
  better pick against **heavily armoured, hardened targets** and at **long range**, while the
  Multi-Cannon is easier to keep on target and better against fast, weaving ships.
- Both want a **laser** to strip shields first — kinetics barely scratch shields.

## Powerplay variant — Concord Cannon (note only)

A special **Concord Cannon** exists (`Hpt_Cannon_Gimbal_Medium_Burst`: Gimbal Medium, **burst-firing**
— `burst` 3, `burstrof` 4 — 14.63 dmg/shot, clip 9, ammo 300, shot speed 1300, piercing 42) flagged
`powerplay`. It is a **Powerplay 2.0 pledge reward** that turns the cannon into a 3-round burst weapon
with a larger clip and faster shells (old Powerplay 1 guides are stale; follow current PP2 pledge
mechanics). The standard Cannons above need no pledge.

## How to fit

- Drops into **any hardpoint** of the matching size, fixed/gimbal/turret. The fixed mounts give the
  best damage and the extra clip round; gimbals trade damage for tracking.
- Standard pairing: a **laser** ([[outfitting/pulse-laser]] / [[outfitting/burst-laser]] /
  [[outfitting/beam-laser]]) to drop shields, then Cannons to **smash the hull** — especially good
  against big, hardened targets where the Cannon's piercing and per-shot punch shine.
- Mind the **clip and reload**: the Cannon's true output is the sustained (reload-inclusive) DPS, so
  pick your shots — it rewards landing hits, not spraying. An engineered High Capacity blueprint eases
  the small magazine.

## Where to get them

Sold at **standard outfitting** at any station with a weapons stock — **no unlock, no Tech Broker, no
Guardian or rank requirement**. Universal availability; cost climbs very steeply for the turret and
larger variants.

## Related weapons

- [[outfitting/multi-cannon]] — the rapid-fire kinetic sibling: the Cannon trades rate of fire and
  clip size for far bigger per-shot punch, higher piercing and no range falloff.
- [[outfitting/pulse-laser]] / [[outfitting/burst-laser]] / [[outfitting/beam-laser]] — the thermal
  laser partners: lasers strip shields, the Cannon kills hull.
- [[outfitting/ax-multi-cannon]] — the anti-Thargoid kinetic workhorse (contrast: the Cannon is a
  human-combat weapon, not anti-Xeno).

[[trunk]]
