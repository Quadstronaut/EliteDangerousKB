---
source_url: https://www.edsm.net/api-v1/system?systemName=Deciat&showId=1&showCoordinates=1&showInformation=1&showPrimaryStar=1
source_type: edsm
source_tier: 0
captured_at: 2026-06-04T07:54:43Z
source_count: 2
verified: true
availability: live
changed_note:
---

# Deciat

Deciat is an Independent system best known as the home of engineer
[[engineers/felicity-farseer]] — the standard first FSD-range unlock. Its scoopable
primary star makes it an easy fuel stop on the way in.

## System Overview

- **Allegiance:** Independent
- **Government:** Feudal
- **Security:** High
- **Economy:** Industrial (secondary: Refinery)
- **Reserve level:** Major
- **Population:** ~31.8 million

## Astrometrics

- **id64:** `6681123623626` (EDSM id 1547)
- **Galactic coordinates:** x = 122.625, y = -0.8125, z = -47.28125
- **Primary star:** Deciat — **K (Yellow-Orange) Star**, **scoopable** (refuel here)

## Points of Interest

- **Farseer Inc.** — engineer [[engineers/felicity-farseer]]'s workshop, a planetary surface
  port on **Deciat 6a** (0.21g moon), `marketId 128676487` (EDSM station id 10). Requires a
  Planetary Approach Suite to land. This is the reason most commanders visit Deciat: the
  first-tier Increased FSD Range blueprint.

## Station Services — Farseer Inc market

Corroborated by the EDSM `stations/market` endpoint (2026-06-15), which returns the same
system id64 (`6681123623626`), confirming Farseer Inc's identity.

- **Sell-only market.** Every commodity lists `buyPrice 0` / `stock 0` — Farseer Inc supplies
  **no commodities** to players; it only carries player **sell demand**.
- **You cannot buy Meta-Alloys at Farseer Inc** (`demand 0`, `stock 0`). To unlock
  [[engineers/felicity-farseer]] you must *bring* Meta-Alloys sourced elsewhere — the
  **Witch Head Science Centre** asteroid base in [[locations/hip-23759]], or Thargoid Barnacle
  sites (Canonn's barnacle map).
- Highest sell-demand commodities at capture: Cobalt (~12,283), Pyrophyllite (~9,987),
  Haematite (~6,695), Lithium (~6,624). Useful as an opportunistic sell stop, not a supply run.

[[trunk]]
