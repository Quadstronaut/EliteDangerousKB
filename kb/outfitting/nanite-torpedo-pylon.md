---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/nanite_torpedo_pylon.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T01:32:40+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Nanite Torpedo Pylon (Outfitting)

The **Nanite Torpedo Pylon** is the **seeking** anti-Xeno (AX) torpedo launcher and the last weapon in
the AX missile/torpedo family. Internally it is the "AX Vent Disruptor Pylon" (symbol
`Hpt_ATVentDisruptorPylon_Fixed_*`): it fires a guided torpedo carrying a **nanite payload** aimed at
**Thargoid caustic/cooling vents** rather than dealing conventional hull damage. In the Coriolis data
it is group `ntp`, file `hardpoints/nanite_torpedo_pylon.json`. AX/Thargoid content remains
`availability: live` — never present it as gone.

## What it does

- **Seeking torpedo** (`missile: "S"`). Unlike the dumbfire [[outfitting/ax-missile-rack|AX Missile
  Rack]] and [[outfitting/ax-missile-rack-enhanced|Enhanced AX Missile Rack]] (`missile: "D"`), the
  Nanite Torpedo guides to its target after launch.
- **The nanite payload is the point — not direct damage.** The stat block lists `damage: 0` with an
  explosive damage class `damagedist {E:1}`. The weapon does **no** listed direct hull damage; its
  effect is the nanite/vent-disruption payload implied by the `ATVentDisruptorPylon` symbol. The
  Coriolis data does **not** carry the payload's magnitude, so no numeric effect is asserted here.
- **Single-shot pylon.** `clip: 1` — one torpedo is loaded at a time; `reload: 3` s, fire interval
  `2.0` s, shot speed `1000` m/s. High heat per shot (`thermload: 35`), `breachdmg 0`, `distdraw 0`.
- **Fixed only, Medium or Large.** No Small, no Turret — you must hold aim to acquire the lock.

## Variants and stats

| Coriolis id | Size | Mount | Rating | Guidance | Ammo | Clip | Power (MW) | Thermload | Mass (t) | Cost (CR) |
|---|---|---|---|---|---|---|---|---|---|---|
| 4Q | 2 Medium | Fixed | I | Seeking | 64  | 1 | 0.4 | 35 | 3 | 843,170 |
| 4R | 3 Large  | Fixed | I | Seeking | 125 | 1 | 0.7 | 35 | 5 | 1,627,419 |

integrity 50 (Medium) / 80 (Large). Both are rating **I** (the special "no conventional rating"
class shared by torpedo/special weapons). **No pre-engineered reward variants** in this file — just
the two standard sizes.

## How to fit

- Takes a **Medium or Large hardpoint, fixed only**. The Large variant nearly doubles the ammo
  reserve (125 vs 64) for sustained vent work; the Medium fits smaller AX builds.
- Each torpedo is a single loaded round (clip 1) on a 3 s reload, so a fight is a sequence of
  deliberate, aimed launches rather than a stream — match it to the target's exposed-vent windows.
- The high `thermload` (35) per launch means heat spikes; bring a [[outfitting/heat-sink-launcher]]
  as with the rest of the AX kit.

## Where to get it

The Nanite Torpedo Pylon is an AX weapon from the **anti-Xeno war-effort supply chain** / **Human
Tech Broker**, not a Guardian Structure unlock — the same source as the other AX missiles.

## Related AX weapons

- [[outfitting/ax-missile-rack]] / [[outfitting/ax-missile-rack-enhanced]] — the dumbfire explosive AX missiles.
- [[outfitting/enzyme-missile-rack]] — the caustic-DoT AX missile.
- [[outfitting/ax-multi-cannon]] / [[outfitting/ax-multi-cannon-enhanced]] — the kinetic AX leg.
- [[outfitting/guardian-gauss-cannon]], [[outfitting/guardian-plasma-charger]],
  [[outfitting/guardian-shard-cannon]] — the Guardian AX trio.
- [[outfitting/remote-release-flak-launcher]] / [[outfitting/remote-release-flechette-launcher]] —
  anti-swarm support.

[[trunk]]
