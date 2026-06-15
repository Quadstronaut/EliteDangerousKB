---
source_url: https://www.edsm.net/api-system-v1/stations?systemName=HIP%2023759
source_type: edsm
source_tier: 0
captured_at: 2026-06-15T20:39:00Z
source_count: 1
verified: false
availability: live
changed_note:
---

# HIP 23759 — station inventory (EDSM)

EDSM stations endpoint for HIP 23759. Corroborates the system-level facts on
`kb/locations/hip-23759.md` and inventories the system's permanent infrastructure.

## Key claims (current truth)
- **87 stations** total — overwhelmingly **Fleet Carriers** (transient) and **Odyssey
  Settlements** (Agriculture / Tourism / Extraction).
- Permanent, non-carrier infrastructure:
  - **Witch Head Science Centre** — **Asteroid base**, Service economy, has market (no
    outfitting/shipyard), controlling faction **Xeno Research Group**, ~2,423 ls, body 9 a.
  - **Columbi's Haven** — **Outpost**, Tourism economy, **no market**, The Allied Commission
    (Alliance), ~2,423 ls, body 9 a.
- Dominant controlling faction across settlements: **Xeno Research Group** (Independent,
  Corporate) — matches the system-level controlling faction on the KB page. Also present:
  The Allied Commission (Alliance) and Witch Head Troop (Independent, Dictatorship).
- **No "Coles Point" station exists** — the queue target's station name was wrong.

## Named entities
- System: HIP 23759 (id64 22793921684, EDSM id 21364)
- Stations: Witch Head Science Centre (Asteroid base), Columbi's Haven (Outpost)
- Factions: Xeno Research Group, The Allied Commission, Witch Head Troop

## Availability
- `live` — all listed infrastructure is current.

## Signals
- OBSOLETE: NO
- currency: live (station list is BGS-current; carriers are transient).
- per-claim availability: station inventory = live.
