---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/shield_cell_bank.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T21:07:24+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Shield Cell Bank (Coriolis) — summary

Tier-0 Coriolis module file, group `scb`, `internal/shield_cell_bank.json`. Parsed directly (no LLM).

## Key claims (from structured fields)

- **Active-recharge module**: uses pre-charged cells to rapidly restore *active* shields. The
  in-game/Coriolis description states it has **no effect on collapsed (down) shields** — must be
  triggered while shields are still up.
- **Cells per module = `clip` (1) + `ammo` (reserve).** E and B ratings carry the most cells;
  A and C fewer; D fewest. Each cell restores `shieldreinforcement` MJ.
- **`shieldreinforcement`** (MJ restored per cell) rises with class and rating. A-rated = highest
  heal per cell (best burst recovery); B-rated = largest total reservoir (cells × heal).
- **`duration`** = seconds over which a cell delivers its reinforcement (1s @ C1 → 17s @ C8);
  **`spinup`** = 5s before the effect starts (all variants); **`boot`** = 25s power-on delay.
- **`thermload`** = heat spike per activation (170 @ C1 → 800 @ C8). Heavy SCB use overheats the
  ship — pair with heat sinks / low-emissions on serious builds.
- **`power`** draw rises with class/rating (0.41 → 3.36 MW). **`ammocost`** = 300 cr per cell to rearm.
- **Quirk**: Class 8 E has `rechargerating` "C" (all other variants' rechargerating matches rating).
- Repeatedly referenced by `shield-generator.md` — slow-regen generators (esp. Prismatic) lean on SCBs.

## Availability

`availability: live` — current core module, all classes 1–8, ratings E/D/C/B/A. obsolete=NO.
