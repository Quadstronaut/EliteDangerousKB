---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/fer_de_lance.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17
source_count: 1
verified: false
availability: live
changed_note:
---

# Fer-de-Lance — Coriolis ship data (Tier-0)

Structured Coriolis JSON, parsed directly (no LLM). Coriolis key `fer_de_lance`
(filename `ships/fer_de_lance.json`, resolved first try). edID 128049351, eddbID 11.

## Identity / class
- name: Fer-de-Lance; manufacturer: **Zorgon Peterson**; class **2 (MEDIUM pad)**.
- **NO requirements block in data → NO rank gate** (credits only).
- hullCost 51,242,363 / retailCost 51,567,040.

## Flight / hull
- hullMass 250; speed 260 / boost 350; masslock 12.
- baseShieldStrength **300 (high for a medium)**; baseArmour 225; **hardness 70 (high — combat hull)**.
- heatCapacity **224 (LOW — runs hot)**; reserveFuelCapacity 0.67; crew 2.
- pitch 38 / roll 90 / yaw 12.
- bulkheads causres 0 on ALL grades.

## Core (standard) — [6,5,4,4,6,4,3]
PP6 · Thr5 · **FSD4 (weak jump)** · LS4 · **PD6 (large — feeds energy weapons)** · Sen4 · **FT3 (small tank)**.
The signature trade: a class-6 Power Distributor for sustained weapon fire, paid for
with a class-4 FSD (poor range) and class-3 fuel tank (short legs).

## Hardpoints — [4,2,2,2,2, +6 zeros]
**1 Huge (class-4) + 4 Medium = 5 weapon mounts** + **6 utility mounts**.
First-class combat layout: one Huge slot on a medium hull, no Small/Large.

## Optionals (internal) — [5,4,4,2,1,1] + class-1 PAS
SIX optional internals only (one class-5, two class-4, one class-2, two class-1)
+ class-1 Planetary Approach Suite. **NO Military slots.** Shallow internals are
the cost of the combat focus (limited cargo/utility room).

## Claims (for synthesis)
1. Fer-de-Lance is a Zorgon Peterson class-2 medium-pad ship, no rank gate, hull 51,242,363 CR. [availability: live]
2. Carries **1 Huge (class-4) hardpoint** + 4 Medium = 5 mounts on a medium hull; 6 utility. [live]
3. hardness 70, baseShield 300, heatCapacity 224 (low) — a hard-hitting, hot-running combat hull. [live]
4. Core: PP6 Thr5 FSD4 LS4 PD6 Sen4 FT3 — strong PD, weak FSD/fuel tank tradeoff. [live]
5. 6 optionals (top class-5), no Military slots — shallow internals. [live]

obsolete: NO
