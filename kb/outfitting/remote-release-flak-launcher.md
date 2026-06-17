---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/remote_release_flak_launcher.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T01:09:03+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Remote Release Flak Launcher (Outfitting)

The **Remote Release Flak Launcher** is the **anti-swarm support weapon** of AX combat: it fires a
flak shell that you **remote-detonate** at a chosen distance, bursting into shrapnel that clears
Thargoid **Swarm clouds** and packs of **Scouts**. In the Coriolis data it is group `rfl`, file
`hardpoints/remote_release_flak_launcher.json` (symbol `Hpt_FlakMortar_*`). AX/Thargoid content
remains `availability: live` — never present it as gone.

## What it does

- **100% explosive area burst** (`damagedist {E:1}`). It is not a single-target heart-cracker — its
  job is to detonate a flak cloud among the Thargoid swarm/scout cluster and wipe many small targets
  at once.
- **Remote detonation.** "Remote release" means you trigger the burst manually at range rather than on
  impact — let the shell drift into the swarm, then detonate for maximum coverage.
- **Single-shot loading.** Clip 1, reload 2 s, fire interval 2.0 s, ammo 32 — fire-and-detonate
  cadence, not a stream. Damage 34 per burst, **piercing 60**.
- **Huge effective range.** `falloff` is **100000 m** with shot speed 550 m/s — reach is not the
  limiter; timing the detonation is.
- **Moderate heat.** thermload 3.6, power 1.20 MW, distdraw 0.24.

## Variants and stats

Both forms are **class 2 (Medium) only**, rating B, ammo 32, clip 1, reload 2 s, fireint 2.0 s,
damage 34, piercing 60, falloff 100000 m, shot speed 550 m/s, power 1.20 MW, mass 4 t, integrity 51:

| Size | Mount | Rating | Dmg | Ammo | Clip | Power (MW) | Cost (CR) |
|---|---|---|---|---|---|---|---|
| 2 Medium | Fixed | B | 34 | 32 | 1 | 1.20 | 261,800 |
| 2 Medium | Turret | B | 34 | 32 | 1 | 1.20 | 1,259,200 |

There is **no Small or Large** Flak Launcher and **no pre-engineered variant** in this line — just the
Medium fixed and turret. The turret tracks for you (and costs ~5× the fixed); the fixed is cheaper and
lets you aim the detonation point precisely.

## Flak vs Flechette — the two remote-detonation anti-swarm weapons

The Flak Launcher's kinetic sibling is the
[[outfitting/remote-release-flechette-launcher|Remote Release Flechette Launcher]] (`tbrfl`). Both are
single-shot, remote-detonation, Medium-only (same mass 4, power 1.20, shotspeed 550, fireint 2.0,
reload 2, clip 1, thermload 3.6) — they differ in damage type and profile:

- **Flak** — **explosive** (`E:1`), dmg 34, ammo 32, piercing 60. Fewer, harder bursts.
- **Flechette** — **kinetic** (`K:1`), dmg 13, ammo **72**, piercing 80/70, **breachdmg 6.5**. More
  detonations, higher penetration, module-breach pressure.

## How to fit

- Takes a **Medium hardpoint** (it is a hardpoint weapon, not a utility slot — don't confuse it with
  Point Defence). On a multi-hardpoint AX ship, give up one Medium mount to it.
- **Essential against Scout swarms and Interceptor-summoned Swarm clouds** — without flak, the swarm
  chips your hull and drops heat sinks/shields. One Flak Launcher dramatically eases those phases.
- Pair with your main AX guns — kinetic [[outfitting/ax-multi-cannon|AX Multi-Cannon]] /
  [[outfitting/ax-multi-cannon-enhanced|Enhanced AX MC]], the explosive
  [[outfitting/ax-missile-rack|AX Missile Rack]] / [[outfitting/ax-missile-rack-enhanced|Enhanced]],
  the caustic [[outfitting/enzyme-missile-rack|Enzyme Missile Rack]], or the Guardian trio
  ([[outfitting/guardian-gauss-cannon|Gauss]], [[outfitting/guardian-plasma-charger|Plasma Charger]],
  [[outfitting/guardian-shard-cannon|Shard Cannon]]) — and a [[outfitting/heat-sink-launcher]].

## Where to get it

Sold through the **anti-Xeno war-effort supply chain** (rescue megaships and stations in/near former
Thargoid space). No Guardian unlock required.

## Related AX weapons

- [[outfitting/remote-release-flechette-launcher]] — the kinetic anti-swarm sibling.
- [[outfitting/ax-multi-cannon]] / [[outfitting/ax-multi-cannon-enhanced]] — kinetic AX.
- [[outfitting/ax-missile-rack]] / [[outfitting/ax-missile-rack-enhanced]] — explosive AX missiles.
- [[outfitting/enzyme-missile-rack]] — caustic/enzyme AX missile.
- [[outfitting/guardian-gauss-cannon]], [[outfitting/guardian-plasma-charger]],
  [[outfitting/guardian-shard-cannon]] — the Guardian AX trio.

[[trunk]]
