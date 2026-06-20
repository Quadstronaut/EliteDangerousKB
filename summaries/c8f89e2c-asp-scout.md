---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/asp_scout.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-20T20:56:25+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Asp Scout — Coriolis ship summary

Tier-0 Coriolis ship definition, key `asp_scout` (file `ships/asp_scout.json`, 3062 bytes,
resolved first try — no 404, no index.js probe). edID 128672276, eddbID 24.

## Key claims (parsed directly, no LLM)

- **Asp Scout**, manufacturer **Lakon**, **class 2 = MEDIUM landing pad**.
- **NO `requirements` block → NO rank gate** (credits only).
- Hull cost **3,819,823 CR** / retail **3,961,154 CR** — cheaper than the Asp Explorer
  (hull 6,145,793).
- **hullMass 150 t** — much LIGHTER than the Asp Explorer's 280 t (about half).
- speed **220** / boost **300** (slower than the Explorer's 250/340).
- baseShieldStrength **120**, baseArmour **180**, hardness **52** (same as Explorer), heatCapacity **210**.
- masslock 8, crew 2, reserveFuelCapacity 0.47.
- Manoeuvrability: pitch **40** · roll **110** · yaw **15** (a touch more agile than the Explorer's 38/100/10).
- Core standard slots **[4,4,4,3,4,4,4]** = PP4 Thr4 **FSD4** LS3 PD4 Sen4 FT4 — the
  **FSD is class 4**, one smaller than the Explorer's class-5 (the queue's CHECK confirmed: weaker FSD).
- Hardpoints **[2,2,1,1,0,0]** = **2 Medium + 2 Small = 4 weapon mounts + 2 utility**
  (the Explorer has 2 Medium + 4 Small = 6 mounts + 4 utility — the Scout has fewer).
- Internal **[5,4,3,3,2,2,1] + PAS-c1** = **7 regular optionals (top class-5) + Planetary Approach
  Suite, NO Military slot** (the Explorer has 8 regular, top class-6 — the Scout is shallower).
- Bulkheads `causres 0` on every grade.

## Currency / availability

- **availability: live** — current Coriolis ship definition, flyable, sold without restriction.
- No obsolete mechanics. **OBSOLETE: NO.**

## Verdict vs queue guesses

class-2 medium pad CONFIRMED; no rank gate CONFIRMED; lighter than the Explorer CONFIRMED
(150 vs 280 t); weaker FSD CONFIRMED (class-4 vs class-5); shallower internals + no Military
CONFIRMED (7 vs 8 optionals). Net: the Scout is the cheaper, lighter, shallower budget sibling
on the same Asp airframe — but actually carries FEWER weapon mounts than the Explorer despite
its "combat/recon" billing.
