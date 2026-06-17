---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/heat_sink_launcher.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T21:23:50+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Heat Sink Launcher (Outfitting)

The **Heat Sink Launcher** is a **utility-mount** module that ejects a heat sink — a disposable
block that rapidly absorbs the ship's accumulated heat and is then jettisoned, dumping that heat
overboard. Firing one drops ship temperature for a short window and briefly masks the ship's heat
signature. In the Coriolis data it is group `hs`, file `hardpoints/heat_sink_launcher.json`. It is
the standard answer to any build that spikes its own heat — most directly the
[[outfitting/shield-cell-bank]], whose recharge cycle dumps a large thermal load.

## What it does

- **Vents heat on demand.** A launched sink soaks heat into itself over a **10-second** cooling
  window, then ejects, carrying that heat away. This is the only instant way to shed heat short of
  shutting modules down.
- **Drops your heat signature.** While a sink burns, the ship runs cold — useful for **silent
  running**, slipping past sensors, surviving **AX/Thargoid caustic clouds**, and stopping heat
  damage during overheats.
- **Passive utility.** It is a `passive: 1` module: it sits in a utility slot drawing a small fixed
  0.2 MW and does not need to be deployed like a weapon.

## Stats (single size — class 0, rating I)

Unlike most modules there is no class/rating ladder: the Heat Sink Launcher comes in **one size**,
a **class-0 (tiny) utility mount**, rating **I**.

| Field | Value | Meaning |
|---|---|---|
| Mass | 1.3 t | (Sirius variant 0.65 t) |
| Power | 0.2 MW | fixed draw when fitted |
| Clip | 1 | sinks ready to fire before reload |
| Ammo (reserve) | 3 | spare sinks held |
| Duration | 10 s | cooling window per sink |
| Fire interval | 5.0 s | minimum time between launches |
| Reload | 10 s | time to reload the clip |
| Ammo cost | 25 CR | per sink restocked |
| Integrity | 20 | module hit points |
| Cost | 3,500 CR | base purchase |

With clip 1 + reserve 3 a stock launcher carries **four sinks** before needing a restock; engineer
the **Ammo Capacity** blueprint to carry more.

## The Sirius pre-engineered variant

A second variant, the **Heat Sink Launcher (Sirius)**, is a Powerplay/reward acquisition (purchase
cost 0 CR) that comes **pre-engineered with Grade 1 "Expanded Heat Sink Capacity"** (blueprint
`Misc_HeatSinkCapacity`) — it carries more sinks per fit and weighs only **0.65 t**. It is
**not re-engineerable**, its grade **cannot be changed**, and it **cannot take an experimental
effect** — a fixed, drop-in upgrade over the stock launcher when you can get one.

## How to fit

- Goes in a **utility mount** — the same small slots that take [[outfitting/shield-booster]]s,
  chaff, and point defence — so it competes with those for utility slots.
- **Pair with Shield Cell Banks.** SCBs spike heat sharply on each cell; a heat sink fired alongside
  the cell keeps the ship out of the danger zone. See [[outfitting/shield-cell-bank]].
- **Explorers and stealth builds** carry one for silent running and to cool down after long fuel
  scooping near hot stars.
- **AX/Thargoid pilots** use sinks to break heat damage from caustic clouds and Thargoid attacks —
  AX content remains `availability: live`.

## Where to get them

Heat Sink Launchers are common utility-mount stock at most outfitting stations, including
**Garay Terminal** in [[locations/deciat]]. No unlock for the standard launcher; the Sirius variant
requires Powerplay acquisition.

[[trunk]]
