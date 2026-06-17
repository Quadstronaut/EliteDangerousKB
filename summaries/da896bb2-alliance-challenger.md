---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/alliance_challenger.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T02:09:29+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Alliance Challenger — Coriolis hull data (Tier 0)

Structured JSON parsed directly (no LLM). Key: `alliance_challenger`, edID 128816588, eddbID 34.

## Identity
- **Name:** Alliance Challenger
- **Manufacturer:** Lakon (Alliance military hull line)
- **Class:** 2 → **medium landing pad**
- **Requires:** Horizons (`requirements.horizons: true`)
- **Hull cost:** 29,569,804 CR / retail 30,472,252 CR

## Flight / defence properties
- hullMass **450 t**
- speed **204** m/s / boost **310** m/s (minthrust 65, boostEnergy 19, boostInt 6)
- heatCapacity **316**, masslock **13**
- baseShieldStrength **220 MJ**, baseArmour **300**, **hardness 65**
- pitch 32, roll 90, yaw 16 (manoeuvrability)
- crew **2**, reserveFuelCapacity 0.77
- **No fighter hangar** (`fighterHangars` absent)

## Slots
- **Core (standard [6,6,5,5,6,4,4]):** PP6 · Thr6 · FSD5 · LS5 · PD6 · Sen4 · FT4
- **Hardpoints (array [3,2,2,2,1,1,1,0,0,0,0]):** 1× Large + 3× Medium + 3× Small = **7 weapon mounts** + **4 utility mounts** (the four class-0 zeros)
- **Optional internals:** 6, 6, 3, 3, 2, 2, 1 (seven regular) + **THREE class-4 Military slots** + class-1 Planetary Approach Suite
- Military-slot eligible modules: `mahr, hr, scb, mrp, gsrp, gmrp, ghrp` (Meta-Alloy/std HRP, SCB, MRP, Guardian shield/module/hull reinforcement)
- **Bulkheads causres 0 on ALL grades** (Lightweight/Reinforced/Military/Mirrored/Reactive) — no caustic resistance from hull; fit Meta-Alloy HRP for AX.

## Claims (current truth, availability: live)
1. The Alliance Challenger is a Lakon/Alliance medium-pad (class 2) combat hull requiring Horizons; hull cost 29,569,804 CR.
2. It is the **tankiest** of the Alliance trio: hullMass 450, baseArmour 300, baseShieldStrength 220, heatCapacity 316 — all higher than the Chieftain's (400 / 280 / 200 / 289).
3. It carries **7 weapon mounts (1L+3M+3S)** + 4 utilities, and **three class-4 Military slots** for AX-defence reinforcement.

## Corrections vs queue speculation
- Military slots = **3**, NOT "more than the Chieftain's 3" — both Alliance hulls carry exactly three class-4 Military slots.
- hardness = **65**, NOT higher than the Chieftain — identical (both 65).
- Hardpoint count IS higher (7 vs Chieftain's 6), but via **fewer Large** (1L vs 2L) traded for **more Medium** (3M vs 1M).

obsolete=NO
