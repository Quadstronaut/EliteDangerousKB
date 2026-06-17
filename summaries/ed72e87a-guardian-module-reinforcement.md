---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/guardian_module_reinforcement_package.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16
source_count: 1
verified: false
availability: live
changed_note:
---

# Guardian Module Reinforcement Package (gmrp) — Coriolis Tier-0

Powered optional internal. Classes 1–5, ratings **D & E only**.
Requires the **Guardian Technology Broker** unlock (Guardian module).
ukDiscript: "Powered module that protects a ship's modules from any weapons fire
penetrating the hull. It utilises its own damage capacity to absorb a proportion
of the damage applied to modules, eventually burning out when its capacity
reaches zero. This version is based on Guardian research and has resistances to
Thargoid specific disruption technology."

## Key claims
- **Powered** — unlike the standard Module Reinforcement Package (0 power),
  Guardian MRP draws power (C1 D 0.34 MW → C5 D 0.88 MW).
- **Same protection fractions as standard MRP**: D 0.60, E 0.30 (fraction of
  penetrating module damage absorbed). `integrity` = absorption pool that burns
  out at zero.
- The Guardian edge: **resistance to Thargoid-specific disruption technology**
  (caustic/field effects) on top of conventional module protection — the AX
  sibling of the standard MRP.
- Rating split (symbol Class2 = D, Class1 = E): **D = higher absorb (0.60) at
  half mass for ~3× cost; E = lower absorb (0.30), double mass, cheaper, slightly
  larger integrity pool.**

## Full table (class · rating · protection · integrity · mass · power · cost)
- C1: D 0.60 / 77 / 1 t / 0.34 MW / 30,000 cr · E 0.30 / 85 / 2 t / 0.27 MW / 10,000 cr
- C2: D 0.60 / 116 / 2 t / 0.47 MW / 72,000 cr · E 0.30 / 127 / 4 t / 0.41 MW / 24,000 cr
- C3: D 0.60 / 171 / 4 t / 0.61 MW / 172,800 cr · E 0.30 / 187 / 8 t / 0.54 MW / 57,600 cr
- C4: D 0.60 / 259 / 8 t / 0.74 MW / 414,720 cr · E 0.30 / 286 / 16 t / 0.68 MW / 138,240 cr
- C5: D 0.60 / 385 / 16 t / 0.88 MW / 995,330 cr · E 0.30 / 424 / 32 t / 0.81 MW / 331,778 cr

availability: live — Guardian tech is currently accessible; this is the AX module
protection layer. obsolete: NO.
