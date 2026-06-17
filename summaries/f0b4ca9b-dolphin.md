---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/dolphin.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T05:12:08+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Dolphin (Coriolis ship definition)

Tier-0 structured extract, parsed directly (no LLM). Key `dolphin` (edID 128049291, eddbID 31).

## Key claims

- **Manufacturer:** Saud Kruger — the **first Saud Kruger hull in the KB** (opens the
  Dolphin → [[ships/orca]] → [[ships/beluga-liner]] luxury-liner line). **Size class 1**
  (small landing pad).
- **No rank gate** — no `federationRank`/`empireRank` requirement; credits only (hull
  1,117,906 CR / retail 1,337,323 CR). The data carries a `requirements.horizons: true` flag
  (game-version tag, not a rank/credit gate).
- **`luxuryCabins: true`** — the Dolphin can fit Luxury-class passenger cabins, the Saud Kruger
  signature; the smallest/cheapest luxury-cabin-capable hull.
- **Top speed 250 m/s · boost 350 m/s.** Hull mass 140 t. **Base shield 110 MJ · base armour
  110 · hardness 35** (light, lightly protected — a liner, not a fighter).
- **Heat capacity 165**, mass lock 9, crew 1, reserve fuel 0.5 t. (The Dolphin's in-game
  "cool jumps" reputation is about low thermal load on passenger runs; the heat-capacity buffer
  stat itself is a modest 165.)
- **Manoeuvrability:** pitch 30 · roll 100 · yaw 20 (agile in yaw for a passenger hull).
- **Hardpoints [1,1,0,0,0]:** 2 Small weapon mounts + 3 utility mounts — barely armed.
- **Core standard [4,5,4,4,3,3,4]:** PP4 Thr5 FSD4 LS4 PD3 Sen3 FT4 — class-5 thrusters and a
  class-4 fuel tank give a small liner decent pace and range; small class-3 distributor.
- **Optional internals [5,4,4,3,2,2,2,1,1] + class-1 Planetary Approach Suite:** nine regular
  slots (top class-5) — deep, to fill with passenger cabins; **no Military slot**.
- Bulkheads `causres 0` on every grade.

availability: live. obsolete: NO. Per-claim availability: all live.
