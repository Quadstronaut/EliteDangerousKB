---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/anaconda.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17
source_count: 1
verified: false
availability: live
changed_note:
---

# Anaconda — Coriolis Tier-0 extract

- **Manufacturer: Faulcon DeLacy** (NOT Lakon — queue guess was wrong). edID 128049363, eddbID 2.
- **class 3 → LARGE pad.** NO `requirements` block → **no rank gate** (just credits), unlike Corvette (Rear Admiral) / Cutter (Duke).
- hullMass 400, speed 180 / boost 240 (slow), baseShield 350, **baseArmour 525 (highest armour in KB)**, hardness 65, heatCapacity 334, masslock 23, crew 4, fighterHangars TRUE.
- Agility: pitch 25 / roll 60 / yaw 10 (sluggish — large hull). reserveFuel 1.07.
- hullCost 142,456,440 / retailCost 146,969,451.

## Core internals (standard slots [8,7,6,5,8,8,5])
PP **8**, Thrusters 7, FSD 6, LifeSupport 5, PowerDistributor **8**, Sensors **8**, FuelTank 5.
(Class-8 PP + class-8 PD = combat-capable signature. Sensors recorded at class 8 verbatim per Tier-0 trust — flag for corroboration.)

## Hardpoints (array [4,3,3,3,2,2,1,1, +8 zeros])
- **1 Huge (class 4)** + 3 Large (class 3) + 2 Medium (class 2) + 2 Small (class 1) = **EIGHT weapon mounts** (most mounts of the large-pad trinity).
- **8 utility mounts** (the 8 trailing zeros — matches Corvette's 8; Anaconda is the reference 8-utility hull).
- QUEUE CONFIRMED: ONE Huge mount (vs Corvette's two); 8 utility.

## Optional internals (internal array)
7,6,6,6,5,5,5,4,4,4,2,1 = **TWELVE regular optionals** + **ONE class-5 Military slot** (eligible mahr/hr/scb/mrp/gsrp/gmrp/ghrp) + class-1 PlanetaryApproachSuite.
- QUEUE CORRECTION: Anaconda has **1 Military slot (class 5)**, not 0 and not Corvette's 2.

## Bulkheads
causres **0 on ALL grades** (no caustic resistance from hull → fit Meta-Alloy HRP for AX). Lightweight/Reinforced/Military Grade Composite/Mirrored Surface/Reactive Surface, hullboost 0.8→2.5.

claims: ~12 | availability=live | obsolete=NO
