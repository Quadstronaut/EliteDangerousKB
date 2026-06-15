---
source_url: https://www.edsm.net/api-system-v1/stations/market?systemName=HIP%2023759&stationName=Witch%20Head%20Science%20Centre
source_type: edsm
source_tier: 0
captured_at: 2026-06-15T20:40:00Z
source_count: 1
verified: false
availability: live
changed_note:
---

# HIP 23759 — Witch Head Science Centre market (Meta-Alloys confirmation)

EDSM commodity-market endpoint for the **Witch Head Science Centre** (Asteroid base) in HIP 23759.
Used to corroborate the Meta-Alloys claim on `kb/locations/hip-23759.md`.

## Key claims (current truth)
- The Witch Head Science Centre lists **Meta-Alloys** on its commodity market:
  `buyPrice = 148,408 cr`, `sellPrice = 148,400 cr`, **`stock = 0` / `stockBracket = 0`** at capture.
  → Meta-Alloys ARE a listed buyable commodity here, but stock is BGS-dependent and was empty at
  capture time — confirm live stock before a buying run.
- Also lists **Platinum Alloy** (`buyPrice = 11,842 cr`, stock 0).
- Market carries **351 commodities** total (Service-economy asteroid base).
- This is the system's only permanent asteroid-base market; the queue's hypothesised
  "Coles Point" station **does not exist** in HIP 23759.

## Named entities
- Station: Witch Head Science Centre (Asteroid base, marketId 128753743)
- System: HIP 23759 (id64 22793921684)
- Commodity: Meta-Alloys

## Availability
- `live` — the station and its market are current, accessible infrastructure.

## Signals
- OBSOLETE: NO
- currency: market data is BGS-live; stock fluctuates.
- per-claim availability: Meta-Alloys listing = live (stock = changed/seasonal via BGS).
