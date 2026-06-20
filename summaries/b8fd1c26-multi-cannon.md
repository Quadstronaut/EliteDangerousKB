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

# Multi-Cannon (standard) — Coriolis summary

Group `mc`, file `modules/hardpoints/multi_cannon.json`, symbol `Hpt_MultiCannon_*`. The
**baseline rapid-fire KINETIC primary** of human combat — the hull-killing partner to the
shield-stripping [[outfitting/pulse-laser]]. Distinct from the anti-Thargoid
[[outfitting/ax-multi-cannon]]. Standard weapon, no unlock, `availability: live`.

## Key claims (parsed directly — no LLM)

- **100% kinetic** (`damagedist {K: 1}`) on every variant → weak vs shields, strong vs hull.
  The exact inverse of a laser — drop shields with a laser, finish hulls with the multi-cannon.
- **Per-shot damage** with `fireint` (seconds between shots): **DPS = damage × roundspershot ÷ fireint**.
  The Huge variants carry `roundspershot: 2` (two rounds per trigger pull) — their DPS already
  accounts for it.
- **Runs cool and efficient**: tiny `thermload` (0.04–0.51) and tiny WEP `distdraw` (0.03–0.37) —
  trivial to fit and run, leaving headroom for shields/utilities. Opposite of the hot/hungry Beam.
- **Ammo-comfortable**: clip 90–100, huge **2100-round reserve**, reload 4–5 s.
- **Projectile, not hitscan**: `shotspeed` 1600 m/s — you must LEAD moving targets (lasers hit instantly).
- **Range 4000 m**, falloff from **2000 m** (longer reach than the 3000 m lasers).
- **QUEUE-GUESS CORRECTION**: the standard Multi-Cannon **DOES have Huge (class-4) variants**
  (Fixed + Gimbal, no Huge turret) — the queue guessed "class 1–3, no Huge", WRONG. Family shape is
  identical to the Beam Laser: S/M/L fixed+gimbal+turret plus Huge fixed+gimbal.
- **Piercing 22 → 68** by size. Mass 2/4/8/16 t by class 1/2/3/4.

### Standard variants

| Size | Mount | Rating | Dmg/shot | DPS | Fireint (s) | Clip / Ammo | Power (MW) | Thermload | Piercing | Mass (t) | Cost (CR) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 Small | Fixed | F | 1.12 | 8.6 | 0.13 | 100 / 2100 | 0.28 | 0.09 | 22 | 2 | 9,500 |
| 1 Small | Gimbal | G | 0.82 | 6.8 | 0.12 | 90 / 2100 | 0.37 | 0.10 | 22 | 2 | 14,250 |
| 1 Small | Turret | G | 0.56 | 4.0 | 0.14 | 90 / 2100 | 0.26 | 0.04 | 22 | 2 | 81,600 |
| 2 Medium | Fixed | E | 2.19 | 15.6 | 0.14 | 100 / 2100 | 0.46 | 0.18 | 37 | 4 | 38,000 |
| 2 Medium | Gimbal | F | 1.64 | 12.6 | 0.13 | 90 / 2100 | 0.64 | 0.20 | 37 | 4 | 57,000 |
| 2 Medium | Turret | F | 1.17 | 7.3 | 0.16 | 90 / 2100 | 0.50 | 0.09 | 37 | 4 | 1,292,800 |
| 3 Large | Fixed | C | 3.925 | 23.1 | 0.17 | 100 / 2100 | 0.64 | 0.28 | 54 | 8 | 140,400 |
| 3 Large | Gimbal | C | 2.84 | 18.9 | 0.15 | 90 / 2100 | 0.97 | 0.34 | 54 | 8 | 578,436 |
| 3 Large | Turret | E | 2.2 | 11.6 | 0.19 | 90 / 2100 | 0.86 | 0.20 | 54 | 8 | 3,794,600 |
| 4 Huge | Fixed | A | 4.625 ×2 | 28.0 | 0.33 | 100 / 2100 | 0.73 | 0.39 | 68 | 16 | 1,177,600 |
| 4 Huge | Gimbal | A | 3.46 ×2 | 23.3 | 0.297 | 90 / 2100 | 1.22 | 0.51 | 68 | 16 | 6,377,600 |

(Huge `Dmg/shot` shown as per-round × 2 rounds/shot; DPS accounts for both rounds.)

### Specials (notes only — not pages)

- **Enforcer** (`Hpt_MultiCannon_Fixed_Small_Strong`, Small fixed, dmg 2.9/shot → DPS ~12.6, clip 60,
  ammo 1000, piercing 30, range 4500) flagged `powerplay`, pledge reward under **Pranav Antal**
  (Powerplay 2.0). Harder-hitting, longer-range, smaller-clip kinetic.
- **Pre-engineered CG Multi-Cannon** ("MC (HCap+RFire+Phase)", Medium fixed, clip 294, ammo 4706):
  pre-engineered Grade-5 High Capacity + Rapid Fire + **Phasing Sequence** experimental (shots pass
  partially through shields). `availability: CG` — a one-time Community Goal reward; existing owners
  keep it, not freely purchasable.

## Availability / obsolescence

availability=**live**, obsolete=**NO**. Current standard weapon. 1 source (Tier-0 Coriolis),
verified:false (single source).
