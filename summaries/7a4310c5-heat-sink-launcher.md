---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/heat_sink_launcher.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16
source_count: 1
verified: false
availability: live
changed_note:
---

# Heat Sink Launcher (hs) — Coriolis Tier-0

Utility mount, **class 0 (tiny utility slot), rating I**, **passive** (no power
toggle hit; consumes 0.2 MW when fitted). Single size — no class/rating ladder.
Ejects a heat sink that rapidly dumps accumulated heat, dropping ship
temperature for a short window (and briefly masking the ship's heat signature —
the explorer / silent-running staple).

## Key claims
- **Standard Heat Sink Launcher** (id 02): mass 1.3 t, power 0.2 MW, cost 3,500 cr,
  integrity 20.
- Capacity: **clip 1 + ammo (reserve) 3** — one sink ready, three held in
  reserve. ammocost 25 cr/sink. reload 10 s.
- Each sink: **duration 10 s** of cooling, **fireint 5.0 s** minimum between
  launches. distdraw 2, drain 100, eps 0.4.
- **Heat Sink Launcher (Sirius)** variant (id 5W): mass **0.65 t** (half weight),
  cost 0 (Powerplay/reward acquisition), **pre-engineered Grade 1 "Expanded Heat
  Sink Capacity"** (blueprint Misc_HeatSinkCapacity) — more sinks per fit. NOT
  re-engineerable, NOT grade-changeable, no experimental effect.

## Build context
Directly supports: Shield Cell Bank use (SCBs spike heat — vent it with a sink),
silent-running / low-heat exploration, and AX/Thargoid caustic-cloud cooling.
Pairs with the SCB page's heat-management note.

availability: live. obsolete: NO.
