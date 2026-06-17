---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/ships/beluga.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T05:26:00+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Beluga Liner

The Beluga Liner is **Saud Kruger's flagship large-pad luxury passenger liner** — the top of the
Saud Kruger trio ([[ships/dolphin]] → [[ships/orca]] → Beluga Liner) and the biggest dedicated
people-carrier in the game. It is built around one job: **maximum passengers in maximum comfort**. It
fits **Luxury-class cabins** (the Saud Kruger `luxuryCabins` signature) across **twelve optional
internals** — the deepest of the trio — and is the only one of the three with a **Ship-Launched
Fighter bay** and full **four-seat multicrew**. The trade for all that capacity is bulk: at **950 t**
it is the heaviest of the trio and slow (200/280), and it needs a **Large landing pad**. It buys with
**credits only, no rank gate**.

## Overview

- **Manufacturer:** Saud Kruger
- **Size class:** 3 (Large landing pad only — large orbital and planetary ports)
- **Role:** Flagship luxury passenger transport (high-capacity tourism and luxury passenger missions)
- **Rank requirement:** none — credits only. The Coriolis data carries `requirements.horizons: true`
  (a game-version tag, not a rank gate).
- **Hull cost:** 79,694,761 CR (hull only)
- **Retail cost:** 84,532,764 CR (with stock modules)
- **Crew seats:** 4 (pilot + three multicrew seats — the full complement)

## Hull Stats

Source: Coriolis-data ship definition `beluga` (display name "Beluga Liner"; edID 128049345, eddbID 30).

- **Hull mass:** 950 t — the heaviest of the Saud Kruger trio by far ([[ships/orca]] 290 t,
  [[ships/dolphin]] 140 t), and the source of its sluggish pace.
- **Top speed:** 200 m/s · **Boost:** 280 m/s — slow; a stark contrast to the light Orca's 300/380.
- **Base shield strength:** 280 MJ · **Base armour:** 280 · **Hull hardness:** 60 — the toughest of the
  trio (the big hull carries the most protection), though still a liner, not a warship.
- **Heat capacity:** 283, **Mass lock factor:** 18, **Reserve fuel:** 0.81 t.
- **Manoeuvrability (deg/s):** pitch 25 · roll 60 · yaw 17 — heavy and ponderous, as expected of a
  950 t flagship.

## Slot Layout

- **Core internals:** Power Plant **6**, Thrusters **7**, Frame Shift Drive **7**, Life Support **8**,
  Power Distributor **6**, Sensors **5**, Fuel Tank **7**. The **class-8 Life Support** slot is the
  hull's largest core slot — an oversized Saud Kruger liner trait (the Orca's is class-6) that lets the
  Beluga keep a full passenger complement breathing in an emergency.
- **Hardpoints:** **5 × Medium** (five weapon mounts, no Large/Huge) plus 6 utility mounts — more weapon
  mounts than the Orca's three, but all medium-calibre; still token self-defence rather than a combat fit.
- **Optional internals:** sizes 6, 6, 6, 6, 5, 5, 4, 3, 3, 3, 3, 1 (twelve regular slots, **top four
  class-6** — the deepest internals of the trio) plus a reserved class-1 **Planetary Approach Suite**.
  This is the whole point: the most **passenger-cabin** capacity of any liner in the KB.
- **Fighter bay:** `fighterHangars: true` — the Beluga can carry a **Ship-Launched Fighter** (the only
  liner of the trio that can; the Orca and Dolphin cannot).
- **Military slots:** none.

Bulkheads carry `causres 0` on every grade.

## Beluga in the passenger-liner line

- **vs [[ships/orca]]:** both are **large-pad** Saud Kruger liners — this is the core choice in the trio.
  The **Orca** is light (290 t), fast (300/380) and cheaper, with nine optionals. The **Beluga** is heavy
  (950 t), slow (200/280) and pricier, but carries **twelve optionals** (the most cabins), a **fighter
  bay**, **crew 4** and a **class-8 life-support** slot. Pick the Orca for speed and economy, the Beluga
  for maximum passengers and comfort.
- **vs [[ships/dolphin]]:** the Dolphin is the small-pad entry liner (140 t, cheap, docks at outposts).
  The Beluga is the opposite extreme — the large-pad flagship with roughly seven times the hull mass and
  far more cabin space, but it needs a Large pad and a far larger budget. Same Saud Kruger luxury DNA,
  scaled from rookie run to flagship tour operator.

## Build notes

Fit it as a high-capacity cruise liner: load the twelve optionals with passenger cabins (heavy on
First/Luxury for the best-paying tourist missions), a strong Bi-Weave or prismatic shield, a fuel scoop,
and a Detailed Surface Scanner for sightseeing routes. The class-8 life-support slot is generous — a
mid-grade unit is plenty, freeing budget elsewhere. Engineer the FSD for range to reach distant tourist
beacons in fewer jumps; the 950 t mass means range is precious. The fighter bay is a niche extra — most
luxury builds skip it for another cabin, but it is there if you want an escort fighter on long runs.

## Acquisition

Sold at stations carrying a shipyard; it needs a **Large landing pad** (no outposts) and buys with
**credits only — no rank gate**. The priciest of the Saud Kruger trio. Check Spansh
(`spansh.co.uk/stations`) for the nearest source.

[[trunk]]
