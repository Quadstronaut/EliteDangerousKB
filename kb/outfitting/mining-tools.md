---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/mining_laser.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T00:32:57+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Mining Tools (Outfitting)

The mining toolkit is a set of **hardpoint** weapons plus one **utility** scanner used to find,
crack, and harvest asteroids. Modern asteroid mining uses three extraction methods — **surface**
(laser + abrasion), **sub-surface** (displacement missile), and **deep core** (seismic charge) —
all feeding **Collector Limpets** that scoop the freed fragments. Stats below are from the
Tier-0 Coriolis module definitions.

A dedicated miner pairs these tools with a [[outfitting/fuel-scoop]] for range, a Prospector and
Collector Limpet Controller, a Refinery, and ideally the [[ships/type-11-prospector]] hull whose
mining-tool-only hardpoints are sized for exactly this loadout.

## Pulse Wave Analyser (utility — find the rocks)

Prospecting scanner. Emits a pulse that briefly makes asteroids glow by mineral content, so you
can pick valuable rocks out of a ring at a glance before mining. Group `pwa`.

- **Mount:** Utility slot (Class **0**) — does **not** use a hardpoint.
- **Ratings:** A–E, mass 1.3 t, no damage.
- **Power:** A 3.2 · B 1.6 · C 0.8 · D 0.4 · E 0.2 MW.
- **Cost:** A 1,097,095 · B 365,698 · C 121,899 · D 40,633 · E 13,544 CR.
- A-rated gives the strongest sweep and is the standard prospecting pick.

## Mining Laser (surface)

Continuous-beam tool that fractures an asteroid's surface and draws mineral fragments into the
beam. The baseline surface-mining tool. Group `ml`. Energy weapon — no ammo, draws from the
power distributor.

| Variant | Class | Mount | Rating | Damage | Range | Power | Cost (CR) |
|---|---|---|---|---|---|---|---|
| Mining Laser | 1 (Small) | Fixed | D | 2 | 500 m | 0.50 | 6,800 |
| Mining Laser | 1 (Small) | Turret | D | 2 | 500 m | 0.50 | 9,400 |
| Mining Laser | 2 (Medium) | Fixed | D | 4 | 500 m | 0.75 | 22,576 |
| Mining Laser | 2 (Medium) | Turret | D | 4 | 500 m | 0.75 | 32,576 |

- **Mining Lance** — a [[mechanics/powerplay]] module from **Zemina Torval** (pledge reward).
  Class 1 Fixed, range **2000 m** (4× standard), damage 8, power 0.7. The long-reach laser for
  pledged miners.
- **Mining Laser V1** — a pre-engineered reward variant: range 1250 m, pre-rolled Grade-5
  Long Range with Incendiary experimental, cost 0.

## Abrasion Blaster (surface deposits)

Short-burst tool that knocks **surface deposits** (the little mineral lumps stuck to a rock's
outside) loose so Collector Limpets can scoop them. Group `abl`.

| Variant | Class | Mount | Rating | Damage | Range | Power | Cost (CR) |
|---|---|---|---|---|---|---|---|
| Abrasion Blaster | 1 (Small) | Fixed | D | 4 | 1000 m | 0.34 | 9,700 |
| Abrasion Blaster | 1 (Small) | Turret | D | 4 | 1000 m | 0.47 | 27,480 |
| Abr Blast (LR) | 1 (Small) | Fixed | D | 4 | **4180 m** | 0.17 | 9,700 |

Class 1 only. The long-range (LR) variant trades nothing meaningful for a 4× reach.

## Sub-Surface Displacement Missile (sub-surface)

Penetrating missile that detonates **below** the surface to expel sub-surface deposits (the
glowing pockets revealed by the Prospector/analyser). Group `sdm`.

| Variant | Class | Mount | Rating | Range | Ammo | Reload | Power | Cost (CR) |
|---|---|---|---|---|---|---|---|---|
| Sub-Surface Disp. Missile | 1 (Small) | Fixed | B | 3000 m | 32 | 2 s | 0.42 | 12,600 |
| Sub-Surface Disp. Missile | 1 (Small) | Turret | B | 3000 m | 32 | 2 s | 0.42 | 38,750 |
| Sub-Surface Disp. Missile | 2 (Medium) | Fixed | B | 3000 m | 96 | 2 s | 1.01 | 122,170 |
| Sub-Surface Disp. Missile | 2 (Medium) | Turret | B | 3000 m | 96 | 2 s | 0.93 | 381,750 |
| Extraction Missile | 2 (Medium) | Fixed | B | — | 96 | 2 s | 1.00 | 822,091 |

The Class-1 fits a small hardpoint, making sub-surface mining viable on smaller miners.

## Seismic Charge Launcher (deep core)

The deep-core tool. Plant timed charges in an asteroid's fissures, then detonate them at the
correct combined yield to crack the rock open and expose the core. Group `scl`.

| Variant | Class | Mount | Rating | Damage | Range | Ammo | Power | Cost (CR) |
|---|---|---|---|---|---|---|---|---|
| Seismic Charge Launcher | 2 (Medium) | Fixed | B | 15 | 3000 m | 72 | 1.2 | 153,110 |
| Seismic Charge Launcher | 2 (Medium) | Turret | B | 15 | 3000 m | 72 | 1.2 | 445,570 |

Class 2 only — needs a Medium+ hardpoint. Core mining is the highest-value method (void opals,
low-temperature diamonds, alexandrite) and depends on this launcher plus the Pulse Wave Analyser
to locate core-bearing rocks.

## Putting a miner together

- **Find:** Pulse Wave Analyser (utility) + Prospector Limpet Controller.
- **Extract:** Mining Laser (surface) + Abrasion Blaster (surface deposits) + Sub-Surface
  Displacement Missile (sub-surface) + Seismic Charge Launcher (deep core) — fit the ones that
  match the mining you intend to do.
- **Collect & refine:** Collector Limpet Controller + Refinery.
- **Hull:** the [[ships/type-11-prospector]] dedicates four hardpoints to mining tools and carries
  a limpet-only bay, making it the natural home for this loadout.

[[trunk]]
