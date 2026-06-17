---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/keelback.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T04:39:15Z
source_count: 1
verified: false
availability: live
changed_note: null
---

# Keelback (Coriolis Tier-0 ship data)

Structured Coriolis ship JSON, parsed directly (no LLM). Key `keelback`,
file `ships/keelback.json` (resolved first try, 3118 bytes, no 404).

## Identity
- **Name:** Keelback · **Manufacturer:** Lakon · **edID** 128672269 · **eddbID** 27
- **Size class:** 2 (MEDIUM landing pad) — same airframe family as the [[ships/type-6-transporter]]
- **Rank gate:** NONE (no `requirements` block — credits only)
- **Hull cost:** 2,946,463 CR · **Retail:** 3,126,154 CR

## Key claims (current truth)
- **Combat variant of the Type-6 airframe.** The Keelback is Lakon's armed, fighter-capable
  sibling of the [[ships/type-6-transporter]] freighter: same medium-pad base, but it trades
  cargo depth for guns, a Ship-Launched Fighter bay, and tougher hull.
- **`fighterHangars: true`** — it can equip a Ship-Launched Fighter (SLF) bay. At 2,946,463 CR
  it is the **cheapest fighter-bay-capable hull in the KB** (next cheapest with a bay is the
  [[ships/alliance-crusader]] at ~22.1 M CR). Real-world: the famous "cheapest SLF carrier."
- **2nd-cheapest medium-pad (class-2) hull in the KB**, behind only its Type-6 sibling
  (866,622 CR). The Type-6 keeps the "cheapest medium-pad" title.
- Hardpoints **[2,2,1,1,0,0,0] = 2 Medium + 2 Small = 4 weapon mounts + 3 utility** — a real
  upgrade over the Type-6's 2 Small (the "trader that can fight back").
- Heavier and slower than the Type-6 (the combat-tank trade): hullMass 180 vs 155,
  speed 200/300 vs 220/350, but baseShield 135 vs 90, baseArmour 270 vs 180, hardness 45 vs 35.

## Stats
- speed 200 / boost 300 · hullMass 180 · masslock 8 · crew 2
- baseShield 135 · baseArmour 270 · hardness 45 · heatCapacity 215
- pitch 27 / roll 100 / yaw 15 · reserveFuelCapacity 0.39
- Core standard **[4,4,4,1,3,2,4]**: PP4 Thr4 FSD4 LS1 PD3 Sen2 FT4 (class-4 FSD + class-4 fuel tank)
- Internals **[5,5,4,3,2,2,1, PAS-c1]** = SEVEN regular (top two class-5) + class-1 Planetary
  Approach Suite. **NO Military slot.** (One fewer regular internal than the Type-6's eight.)
- Bulkheads `causres 0` on every grade (mahr fit needed for AX work).

## Availability
- **availability: live** — current ship, buyable now, no rank gate. Not obsolete.

## Obsolete? NO.
