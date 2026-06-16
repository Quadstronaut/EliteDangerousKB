---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/prospector_limpet_controllers.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T00:44:44+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

<!-- second source: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/collector_limpet_controllers.json (Collector section) -->

# Limpet Controllers (Outfitting)

**Limpet Controllers** are **optional internal** modules that command single-use drones
(*limpets*) carried as cargo. Each controller type commands one job; this page covers the two
**mining** controllers — **Prospector** and **Collector** — that the mining loop depends on.
(Other controllers exist for fuel transfer, hatch-breaking, repair, decontamination, recon,
research and rescue; those are not mining tools and are out of scope here.) Stats below are
from the Tier-0 Coriolis module definitions.

Two rules of thumb decide your fit:
- **Class** sets how many limpets the controller runs **at once** — bigger slot, more drones.
- **Rating** (A best) sets range, lifetime, power draw and cost; mass varies non-linearly.

Pair these with the [[outfitting/mining-tools]] that free the fragments and the
[[outfitting/refinery]] that converts them. The [[ships/type-11-prospector]] carries a
dedicated limpet-only bay sized for exactly this loadout.

## Prospector Limpet Controller

Fires **Prospector Limpets** that attach to an asteroid and report its full mineral
composition, and apply a **yield bonus** to that rock — so you mine the right asteroids and
get more from each. Group `pc`. One prospector per rock; class decides how many you can have
in flight simultaneously.

- **Mount:** Optional Internal. Classes **1, 3, 5, 7**; ratings A–E.
- **Simultaneous limpets:** C1 = 1, C3 = 2, C5 = 4, C7 = 8.
- **Longest reach (A-rated):** C1 7 km · C3 7.7 km · C5 9.1 km · C7 11.9 km.

| Class | Rating | Max limpets | Range (km) | Mass (t) | Power (MW) | Cost (CR) |
|---|---|---|---|---|---|---|
| 1 | E | 1 | 3 | 1.3 | 0.18 | 600 |
| 1 | D | 1 | 4 | 0.5 | 0.14 | 1,200 |
| 1 | C | 1 | 5 | 1.3 | 0.23 | 2,400 |
| 1 | B | 1 | 6 | 2 | 0.32 | 4,800 |
| 1 | A | 1 | 7 | 1.3 | 0.28 | 9,600 |
| 3 | E | 2 | 3.3 | 5 | 0.27 | 5,400 |
| 3 | D | 2 | 4.4 | 2 | 0.2 | 10,800 |
| 3 | C | 2 | 5.5 | 5 | 0.34 | 21,600 |
| 3 | B | 2 | 6.6 | 8 | 0.48 | 43,200 |
| 3 | A | 2 | 7.7 | 5 | 0.41 | 86,400 |
| 5 | E | 4 | 3.9 | 20 | 0.4 | 48,600 |
| 5 | D | 4 | 5.2 | 8 | 0.3 | 97,200 |
| 5 | C | 4 | 6.5 | 20 | 0.5 | 194,400 |
| 5 | B | 4 | 7.8 | 32 | 0.97 | 388,800 |
| 5 | A | 4 | 9.1 | 20 | 0.6 | 777,600 |
| 7 | E | 8 | 5.1 | 80 | 0.55 | 437,400 |
| 7 | D | 8 | 6.8 | 32 | 0.41 | 874,800 |
| 7 | C | 8 | 8.5 | 80 | 0.69 | 1,749,600 |
| 7 | B | 8 | 10.2 | 128 | 0.97 | 3,499,200 |
| 7 | A | 8 | 11.9 | 80 | 0.83 | 6,998,400 |

## Collector Limpet Controller

Fires **Collector Limpets** — autonomous drones that scoop freed mineral fragments (and
floating cargo canisters) and ferry them to your cargo hold, so you keep mining instead of
manually flying to each chunk. Group `cc`. Run several at once to clear fragments before they
drift off.

- **Mount:** Optional Internal. Classes **1, 3, 5, 7**; ratings A–E.
- **Simultaneous limpets:** C1 = 1, C3 = 2, C5 = 3, C7 = 4.
- **Limpet lifetime** (`time`, seconds): A 720 (longest) · D 600 · C 510 · B 420 · E 300.
  A-rated limpets live longest, so they make more round-trips before expiring — the standard
  pick for sustained mining.

| Class | Rating | Max limpets | Lifetime (s) | Range (km) | Mass (t) | Power (MW) | Cost (CR) |
|---|---|---|---|---|---|---|---|
| 1 | E | 1 | 300 | 0.8 | 0.5 | 0.14 | 600 |
| 1 | D | 1 | 600 | 0.6 | 0.5 | 0.18 | 1,200 |
| 1 | C | 1 | 510 | 1 | 1.3 | 0.23 | 2,400 |
| 1 | B | 1 | 420 | 1.4 | 2 | 0.28 | 4,800 |
| 1 | A | 1 | 720 | 1.2 | 2 | 0.32 | 9,600 |
| 3 | E | 2 | 300 | 0.88 | 2 | 0.2 | 5,400 |
| 3 | D | 2 | 600 | 0.66 | 2 | 0.27 | 10,800 |
| 3 | C | 2 | 510 | 1.1 | 5 | 0.34 | 21,600 |
| 3 | B | 2 | 420 | 1.54 | 8 | 0.41 | 43,200 |
| 3 | A | 2 | 720 | 1.32 | 8 | 0.48 | 86,400 |
| 5 | E | 3 | 300 | 1.04 | 8 | 0.3 | 48,600 |
| 5 | D | 3 | 600 | 0.78 | 8 | 0.4 | 97,200 |
| 5 | C | 3 | 510 | 1.3 | 20 | 0.5 | 194,400 |
| 5 | B | 3 | 420 | 1.82 | 32 | 0.6 | 388,800 |
| 5 | A | 3 | 720 | 1.56 | 32 | 0.7 | 777,600 |
| 7 | E | 4 | 300 | 1.36 | 32 | 0.41 | 437,400 |
| 7 | D | 4 | 600 | 1.02 | 32 | 0.55 | 874,800 |
| 7 | C | 4 | 510 | 1.7 | 80 | 0.69 | 1,749,600 |
| 7 | B | 4 | 420 | 2.38 | 128 | 0.83 | 3,499,200 |
| 7 | A | 4 | 720 | 2.04 | 128 | 0.97 | 6,998,400 |

## Choosing controllers for a miner

- **One Prospector controller is usually enough** — you only prospect one rock at a time, so a
  small class (C1/C3) A-rated gives good range cheaply.
- **Favour Collector class** — clearing fragments fast is the bottleneck, so spend your larger
  optional slots on a high-class Collector controller (C7 A runs 4 long-lived limpets).
- **Carry enough limpet cargo** — each limpet is one cargo unit consumed on use; bring plenty.
- See [[outfitting/mining-tools]] for the extraction tools and [[outfitting/refinery]] for the
  final processing stage. The [[ships/type-11-prospector]] is the natural hull for this kit.

[[trunk]]
