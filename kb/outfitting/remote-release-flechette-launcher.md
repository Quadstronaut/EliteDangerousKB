---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/remote_release_flechette_launcher.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T01:20:16+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Remote Release Flechette Launcher (Outfitting)

The **Remote Release Flechette Launcher** is the **kinetic** anti-swarm support weapon of AX combat —
the sibling of the explosive [[outfitting/remote-release-flak-launcher|Remote Release Flak Launcher]].
It fires a **remote-detonated** flechette round that bursts into a shrapnel cloud, clearing Thargoid
**Swarm clouds** and packs of **Scouts**. In the Coriolis data it is group `tbrfl`, file
`hardpoints/remote_release_flechette_launcher.json` (symbol `Hpt_FlechetteLauncher_*_Medium`).
AX/Thargoid content remains `availability: live` — never present it as gone.

## What it does

- **100% kinetic shrapnel** (`damagedist {K:1}`). Where the flak launcher bursts as explosive area
  damage, the flechette scatters **kinetic** fragments — the same remote-detonation role, a different
  damage type.
- **Remote detonation.** Fire the round toward the swarm, then trigger the burst manually at range for
  maximum coverage rather than waiting for impact.
- **Not flagged experimental.** Unlike the AX missile/multi-cannon lines, the flechette carries no
  `experimental` flag in the Coriolis data.
- **Module-breach on penetration.** `breachdmg 6.5` (breachmin/max 1) — beyond the swarm-clearing
  role, hits that penetrate do meaningful damage to a target's internal modules.
- **High ammo, low per-hit.** Damage 13 per round but ammo **72** (vs the flak launcher's 32); clip 1,
  reload 2 s, fire interval 2.0 s — a fire-and-detonate cadence, not a stream.

## Variants and stats

Both forms are **class 2 (Medium) only**, rating B, damage 13, ammo 72, clip 1, reload 2 s, fireint
2.0 s, shot speed 550 m/s, power 1.20 MW, thermload 3.6, mass 4 t, integrity 51, breachdmg 6.5:

| Coriolis id | Size | Mount | Rating | Dmg | Ammo | Clip | Piercing | Power (MW) | Cost (CR) |
|---|---|---|---|---|---|---|---|---|---|
| xy | 2 Medium | Fixed | B | 13 | 72 | 1 | 80 | 1.20 | 353,761 |
| yF | 2 Medium | Turret | B | 13 | 72 | 1 | 70 | 1.20 | 1,279,200 |

There is **no Small or Large** Flechette Launcher and **no pre-engineered variant** — just the Medium
fixed and turret. The fixed has higher piercing (80 vs 70) and lets you aim the detonation; the turret
tracks for you and costs ~3.6× as much.

## Flechette vs Flak — which anti-swarm weapon

Both are single-shot, remote-detonation Medium-only support weapons (same mass 4, power 1.20,
shotspeed 550, fireint 2.0, reload 2, clip 1, thermload 3.6). They differ in damage type and profile:

- **[[outfitting/remote-release-flechette-launcher|Flechette]]** — **kinetic** (`K:1`), dmg 13,
  ammo **72**, piercing 80/70, **breachdmg 6.5**. More shots, higher penetration, module-breach.
- **[[outfitting/remote-release-flak-launcher|Flak]]** — **explosive** (`E:1`), dmg 34, ammo 32,
  piercing 60. Fewer, harder bursts.

Pick by what the rest of your loadout lacks: flak for a punchier explosive burst, flechette for more
detonations and kinetic/breach pressure. Both fill the same "clear the swarm" slot.

## How to fit

- Takes a **Medium hardpoint** (a hardpoint weapon, not a utility — don't confuse it with Point
  Defence). On a multi-hardpoint AX ship, give up one Medium mount to it.
- Like the flak launcher, it eases the **Scout swarm / Interceptor-summoned Swarm cloud** phases that
  otherwise chip hull and force heat-sink/shield management.
- Pair with your main AX guns — kinetic [[outfitting/ax-multi-cannon|AX Multi-Cannon]] /
  [[outfitting/ax-multi-cannon-enhanced|Enhanced AX MC]], the explosive
  [[outfitting/ax-missile-rack|AX Missile Rack]] / [[outfitting/ax-missile-rack-enhanced|Enhanced]],
  the caustic [[outfitting/enzyme-missile-rack|Enzyme Missile Rack]], or the Guardian trio
  ([[outfitting/guardian-gauss-cannon|Gauss]], [[outfitting/guardian-plasma-charger|Plasma Charger]],
  [[outfitting/guardian-shard-cannon|Shard Cannon]]) — and a [[outfitting/heat-sink-launcher]].

## Where to get it

Sold through the **anti-Xeno war-effort supply chain** (rescue megaships and stations in/near former
Thargoid space) / **Human Tech Broker**. No Guardian unlock required.

## Related AX weapons

- [[outfitting/remote-release-flak-launcher]] — the explosive anti-swarm sibling.
- [[outfitting/ax-multi-cannon]] / [[outfitting/ax-multi-cannon-enhanced]] — kinetic AX.
- [[outfitting/ax-missile-rack]] / [[outfitting/ax-missile-rack-enhanced]] — explosive AX missiles.
- [[outfitting/enzyme-missile-rack]] — caustic/enzyme AX missile.
- [[outfitting/guardian-gauss-cannon]], [[outfitting/guardian-plasma-charger]],
  [[outfitting/guardian-shard-cannon]] — the Guardian AX trio.

[[trunk]]
