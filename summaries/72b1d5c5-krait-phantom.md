---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/krait_phantom.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T02:09:29+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Krait Phantom — Coriolis hull data (Tier 0)

Structured JSON parsed directly (no LLM). Key: `krait_phantom`, edID 128839281, eddbID 37.

## Identity
- **Name:** Krait Phantom
- **Manufacturer:** Faulcon DeLacy
- **Class:** 2 → **medium landing pad**
- **Requires:** no `requirements` block in Coriolis data (no Horizons gate recorded)
- **Hull cost:** 35,741,519 CR / retail 37,472,252 CR

## Flight / defence properties
- hullMass **270 t** (light — 50 t under the Krait Mk II's 320)
- speed **250** m/s / boost **350** m/s (minthrust 64, boostEnergy 13, boostInt 4.5)
- heatCapacity **300**, masslock **14**
- baseShieldStrength **200 MJ**, baseArmour **180**, **hardness 55**
- pitch 26, roll 90, yaw 10 (manoeuvrability)
- crew **2**, reserveFuelCapacity 0.63
- **No fighter hangar** (`fighterHangars` absent) — explorer-leaning

## Slots
- **Core (standard [7,6,5,4,7,6,5]):** PP7 · Thr6 · FSD5 · LS4 · PD7 · Sen6 · FT5 (identical core to the Krait Mk II)
- **Hardpoints (array [3,3,2,2,0,0,0,0]):** 2× Large + 2× Medium = **4 weapon mounts** + **4 utility mounts** (the four class-0 zeros)
- **Optional internals:** 6, 5, 5, 5, 3, 3, 3, 2, 1 (nine regular) + class-1 Planetary Approach Suite
- **NO Military slots** (key contrast vs the Alliance hulls; matches the Krait Mk II)
- **Bulkheads causres 0 on ALL grades** — no caustic resistance from hull; fit Meta-Alloy HRP for AX.

## Claims (current truth, availability: live)
1. The Krait Phantom is a Faulcon DeLacy medium-pad (class 2) multirole/explorer hull; hull cost 35,741,519 CR.
2. It is the **lighter, explorer-leaning sibling of the Krait Mk II**: hullMass 270 (vs 320), faster (250/350 vs 240/330), no fighter bay, crew 2 (vs 3) — for longer jump range.
3. It carries **4 weapon mounts (2L+2M)** + 4 utilities and **nine optional internals**; no Military slots.

## Corrections vs queue speculation
- The Phantom does **NOT** have "an extra/larger optional internal" than the Mk II. Both carry **nine** optional slots; the Mk II's top end is actually *bigger* (two class-6 vs the Phantom's one class-6). The Phantom's longer range comes from **lower hull mass (270 vs 320)** and dropping the fighter bay, not from larger internals.
- crew **2** (vs Mk II's 3) — confirmed.
- fighter hangar **absent** — confirmed.
- Hardpoints **2L+2M (4 mounts)** — leaner than the Mk II's 3L+2M (5 mounts), confirmed.

obsolete=NO
