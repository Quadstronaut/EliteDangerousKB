---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/imperial_cutter.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17
source_count: 1
verified: false
availability: live
changed_note:
---

# Imperial Cutter — Coriolis Tier-0 extract

- **Manufacturer: Gutamaya.** edID 128049375, eddbID 26.
- **class 3 → LARGE pad.** `requirements.empireRank 12` → **Imperial Navy rank DUKE** gate (queue guess CONFIRMED — the Imperial counterpart to the Corvette's Rear Admiral).
- **hullMass 1100 (heaviest hull in KB)**, speed 200 / boost 320, **baseShield 600 (highest shield in KB)**, baseArmour 400, hardness 70, heatCapacity 327, **masslock 27 (highest in KB)**, crew 4, fighterHangars TRUE.
- Agility: pitch 18 / roll 45 / yaw 8 (**least agile in KB** — the shield-tank trade). reserveFuel 1.16.
- hullCost 200,493,413 / retailCost 208,969,451.

## Core internals (standard slots [8,8,7,7,7,7,6])
PP **8**, Thrusters **8**, FSD 7, LifeSupport 7, PowerDistributor 7, Sensors 7, FuelTank 6.
(First KB ship with a **class-8 Thruster** slot — needed to move the 1100t hull. Big core all round.)

## Hardpoints (array [4,3,3,2,2,2,2, +8 zeros])
- **1 Huge (class 4)** + 2 Large (class 3) + 4 Medium (class 2) = **SEVEN weapon mounts**. **NO Small mounts.**
- **8 utility mounts** (the 8 trailing zeros).
- QUEUE CORRECTION: 1 Huge + 2 Large + 4 Medium (queue guessed "1 Huge + Large/Medium/Small" — there are **no Small** hardpoints).

## Optional internals (internal array)
8,8,6,6,6,5,5,4,3,1 = **TEN regular optionals** (incl **TWO class-8** — the huge cargo/shield capacity) + **TWO class-5 Military slots** (eligible mahr/hr/scb/mrp/gsrp/gmrp/ghrp) + class-1 PlanetaryApproachSuite.
- 2 class-5 Military slots = SAME as Corvette; two class-8 optionals (vs Corvette's top class-7).

## Bulkheads
causres **0 on ALL grades** (no caustic resistance from hull → fit Meta-Alloy HRP for AX). Lightweight/Reinforced/Military Grade/Mirrored/Reactive, hullboost 0.8→2.5.

claims: ~12 | availability=live | obsolete=NO
