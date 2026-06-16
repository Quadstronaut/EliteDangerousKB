---
source_url: https://www.edsm.net/api-v1/system?systemName=Deciat&showId=1&showCoordinates=1&showInformation=1&showPrimaryStar=1
source_urls: ["https://www.edsm.net/api-v1/system?systemName=Deciat&showId=1&showCoordinates=1&showInformation=1&showPrimaryStar=1", "https://www.edsm.net/api-system-v1/stations?systemName=Deciat", "https://www.edsm.net/api-system-v1/stations/market?systemName=Deciat&stationName=Farseer%20Inc", "https://www.edsm.net/api-system-v1/stations/shipyard?marketId=3229756160", "https://www.edsm.net/api-system-v1/stations/outfitting?marketId=3229756160"]
source_type: edsm
source_tier: 0
captured_at: 2026-06-15T23:48:53Z
source_count: 4
verified: false
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

## Station Services — large-pad & outfit ports

From the EDSM `api-system-v1/stations` endpoint (2026-06-15), same system id64
(`6681123623626`). Deciat holds 59 permanent ports (transient fleet carriers excluded). Pad size
follows station type: Coriolis/Orbis/Ocellus **Starports carry Large pads**; **Outposts** top out
at Medium.

- **Garay Terminal** — **Coriolis Starport (Large pad)**, ~2042 ls from arrival (orbits Deciat 6),
  `marketId 3229756160`. The system's **only large-pad orbital port** and the de-facto
  **restock / outfit / shipyard hub** for commanders visiting Felicity Farseer. Carries
  **Market + Shipyard + Outfitting** plus Universal Cartographics, Tuning, Missions, Bartender,
  Pioneer Supplies, Vista Genomics, and active System Colonisation contribution. Controlling
  faction Ryders of the Void (Industrial/Refinery).
- **Matteucci Dock** — Outpost (Medium pad), ~2042 ls (Deciat 6). Market + Outfitting, **no shipyard**.
- **Carson Hub** — Outpost (Medium pad), ~2042 ls (Deciat 6). Market + Outfitting, **no shipyard**.
- **Kirtley Vision** — Planetary Outpost, ~62 ls (Deciat 4). Market + Outfitting — the closest
  outfitting if you want to skip the 2042-ls cruise out to Garay (requires Planetary Approach Suite).
- **Hasse Point** — Planetary Outpost, ~62 ls (Deciat 4). Outfitting only, **no market**.
- **Orbital Construction Site: Penrose Vista** — a Trailblazers colonisation construction site at
  0 ls, accepting colonisation contributions.

### Garay Terminal — shipyard stock

Corroborated by the EDSM `api-system-v1/stations/shipyard` endpoint (`marketId 3229756160`,
2026-06-15), a third independent endpoint confirming Garay Terminal carries a **Shipyard**. It
stocks **17 hulls** for direct purchase:

Sidewinder, Eagle, Hauler, Adder, Viper Mk III, Cobra Mk III, Type-6 Transporter,
Type-7 Transporter, Asp Explorer, Type-9 Heavy, Viper Mk IV, Keelback, Krait Mk II,
Type-8 Transporter, Cobra Mk V, Panther Clipper Mk II, Type-11 Prospector.

- The list includes the recent hulls **Type-8 Transporter**, **[[ships/cobra-mk-v|Cobra Mk V]]**,
  **Panther Clipper Mk II**, and **Type-11 Prospector**, so the stock reflects the current
  (post-2024) ship roster.
- Largest hulls available: **Type-9 Heavy** and **Panther Clipper Mk II** — fitting for the
  system's only large-pad orbital starport.
- Shipyard inventories rotate with the market; treat this as "ships commonly stocked here,"
  not a frozen guarantee.

### Garay Terminal — outfitting stock

<!-- ESCALATION: confidence=0.75 verdict=conflict — cloud council required -->
Corroborated by the EDSM `api-system-v1/stations/outfitting` endpoint (`marketId 3229756160`,
2026-06-15), a fourth independent endpoint confirming Garay Terminal carries **Outfitting**. It
lists **653 module SKUs** across **107 module families** — a comprehensive large-port catalogue.

- **Full core internals to Class 8:** Power Plant, Thrusters, Power Distributor, Life Support,
  Sensors and Fuel Scoop all reach Class 8; **Shield Generator** and **Bi-Weave Shield Generator**
  reach Class 8; Shield Cell Bank reaches Class 8.
- **Frame Shift Drive to Class 7 — standard *and* Frame Shift Drive (SCO)** are both stocked. You
  can buy a base FSD (or the supercruise-overcharge variant) here and take it straight to
  [[engineers/felicity-farseer]] for the Increased Range blueprint without leaving the system.
- Support/utility kit: Refinery (→4), all limpet controllers (Collector / Prospector /
  Fuel-Transfer / Hatch-Breaker / Repair / Recon, →7), Auto Field-Maintenance Unit (→8),
  Planetary Vehicle Hangar (SRV bays to size 6).
- Weapons are stocked but capped around **Class 4** (lasers, cannons, multi-cannons, fragment
  cannons, missile/torpedo racks) — small/medium loadouts, no large/huge hardpoint weapons.
- **No Guardian modules** are sold (FSD Booster, hybrid power plant, module/shield reinforcement) —
  expected, since Guardian tech is unlocked at Guardian ruins / Tech Brokers, never on a market.

**Outfitting/shipyard takeaway:** [[engineers/felicity-farseer]]'s own Farseer Inc base is a
medium-pad planetary outpost with a sell-only market and no shipyard. For a **large pad**, a
**ship purchase**, or a full **outfitting** run, dock at **Garay Terminal** (~2042 ls) — the only
large orbital starport in-system, and a one-stop shop to buy a hull, fit an FSD, and engineer it
at Farseer Inc.

[[trunk]]
