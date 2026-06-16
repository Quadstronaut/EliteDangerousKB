---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/cobra_mk_v.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-15T23:59:25+00:00
source_count: 1
verified: false
availability: live
changed_note: ""
---

# Cobra Mk V — hull stats (Coriolis)

Coriolis-data ship definition `cobramkv` (edID 129031229). Faulcon DeLacy small
multi-role ship. Surfaced as current stock at Garay Terminal (Deciat) in Loop 5.

## Hull properties

- **Manufacturer:** Faulcon DeLacy
- **Size class:** 1 (small landing pad)
- **Hull cost:** 1,477,085 cr (hull only) · **Retail (with base modules):** 1,989,461 cr
- **Hull mass:** 150 t
- **Top speed:** 291 m/s · **Boost:** 412 m/s (boost cost 10, 5 boost interval)
- **Base shield strength:** 160 MJ
- **Base armour:** 180 · **Hardness:** 40
- **Heat capacity:** 245
- **Mass lock factor:** 8
- **Crew seats:** 3 (multicrew)
- **Manoeuvrability (deg/s):** pitch 45.61, roll 121.62, yaw 33.45
- **Reserve fuel:** 0.49 t

## Slot layout

- **Core internals** (Coriolis `standard` order):
  Power Plant **4**, Thrusters **4**, Frame Shift Drive **4**, Life Support **3**,
  Power Distributor **4**, Sensors **3**, Fuel Tank **4** (default 4C).
- **Hardpoints:** 3× Medium + 2× Small weapon mounts.
- **Utility mounts:** 4.
- **Optional internals:** sizes 5, 4, 4, 4, 3, 3, 3, 2, 1 (nine slots) plus a
  reserved class-1 Planetary Approach Suite (planet-landing / SRV capable).

## Currency signals

- Cobra Mk V is a current ship (released late 2024); present in live Coriolis-data
  and stocked at Garay Terminal's shipyard. `availability: live`.

## Note on source path

Coriolis ship data lives at `ships/<slug>.json`, NOT the queue's stale
`dist/ships.json` (that path 404s — `dist/index.json` is generated at install
time and not committed to the repo).
