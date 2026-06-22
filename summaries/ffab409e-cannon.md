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

# Cannon — Coriolis module data (summary)

Group `c`, file `modules/hardpoints/cannon.json`, internal symbol `Hpt_Cannon_*`.
The **high-damage / low-rate kinetic primary** — the alpha-strike partner to the rapid-fire
[[outfitting/multi-cannon]]. 100% kinetic (`damagedist {K:1}`) — weak vs shields, strong vs hull.
Standard variants: 11 (Small/Medium/Large Fixed/Gimbal/Turret + Huge Fixed/Gimbal) — **no Huge
turret**, same family shape as the lasers.

## Key claims

- **Big slow shells, tiny clip.** Per-shot damage is large (Small fixed 22.5 → Huge fixed 82.1),
  `fireint` is slow (1.92–2.72 s), clip is small (5–6), reload 3–4 s. The kinetic burst-damage
  option vs the multi-cannon's sustained chip damage.
- **DPS = damage ÷ fireint** (1 round/shot, no burst on standard variants). Full-clip DPS S→Huge
  fixed: 11.3 / 16.8 / 23.1 / 31.2. **Reload-inclusive sustained DPS** is lower (Small fixed 9.0,
  Medium 13.7, Large 19.1, Huge 26.2) — the small clip + 3–4 s reload bite hard.
- **Projectile, must lead.** Shot speed 750–1200 m/s (slower than the multi-cannon's 1600) — large
  travel time, lead moving targets.
- **No damage falloff within range.** `falloff` == `range` at every size (3000/3500/4000/4500),
  so cannons hold **full damage out to their max range** — unlike the multi-cannon (falloff 2000).
- **Highest kinetic piercing**: 35 → 90 by size (vs multi-cannon 22 → 68) — best standard weapon at
  punching through hardened armour.
- Runs warmer than the multi-cannon (thermload 0.7–4.8/shot) but still moderate. Ammo reserve
  100–120 rounds.

## Special (note only, not a page)

- **Concord Cannon** (Gimbal Medium burst, `powerplay`): burst 3, burstrof 4, damage 14.63, clip 9,
  ammo 300, shotspeed 1300, piercing 42 — a burst-firing Powerplay 2.0 cannon variant. One-line note.

availability: live. obsolete: NO. claims: 6+. KEEP.
