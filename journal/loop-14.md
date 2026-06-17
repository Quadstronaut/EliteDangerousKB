# Loop 14 — Guardian AX outfitting layer + heat management

Mode: search · 3 Tier-0 Coriolis sources, all `availability: live`, no discards, no escalations.

## What changed
- **MERGE** `kb/outfitting/hull-reinforcement.md` — added **Guardian Hull Reinforcement Package**
  (`ghrp`) as a full H2 + table. Powered (C1 D 0.56 MW → C5 D 1.46 MW); causres 5% flat (more than
  Meta-Alloy's 3%) + thermres 2%; highest raw HP of all three HRP lines (C5 488/450 vs std 390/360
  vs MA 351/324). Guardian Tech Broker unlock. source_count 2→3, stays verified **true**.
- **MERGE** `kb/outfitting/module-reinforcement.md` — added **Guardian Module Reinforcement Package**
  (`gmrp`) as a full H2 + table. Powered; same protection fractions as standard MRP (D 0.60 / E 0.30,
  independent Tier-0 corroboration of the mechanic) → source_count 1→2, verified false→**true**.
  ~10% larger integrity pools + Thargoid disruption resistance.
- **NEW** `kb/outfitting/heat-sink-launcher.md` (`hs`) — utility C0/I, passive, single size. clip 1 +
  ammo 3, duration 10 s, fireint 5 s, mass 1.3 t. Sirius variant (id 5W): 0.65 t, cost 0, pre-eng G1
  Expanded Heat Sink Capacity, not re-engineerable. source_count 1, verified false. Forward-linked
  from `shield-cell-bank.md`.

## Verify (local council, qwen3-coder:30b)
- hull-reinforcement → verified, confidence 1.0, escalate false.
- module-reinforcement → verified, confidence 1.0, escalate false.
- heat-sink-launcher → skipped (source_count 1, no conflict).

## Path notes
Queue slugs `guardian_hull_reinforcement.json` / `guardian_module_reinforcement.json` both 404'd
(missing `_package` suffix). Resolved via `modules/index.js`:
`ghrp=internal/guardian_hull_reinforcement_package.json`,
`gmrp=internal/guardian_module_reinforcement_package.json`.

## Follow-ons queued (paths pre-confirmed via index.js)
Guardian Shield Reinforcement (`gsrp`), Guardian Gauss Cannon (`ggc`, seeds AX weapons),
Guardian FSD Booster (`gfsb`).
