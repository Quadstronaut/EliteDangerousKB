---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/caustic_sink_launcher.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T01:41:39+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Caustic Sink Launcher (Outfitting)

The **Caustic Sink Launcher** is a **utility-mount** module that ejects a *caustic sink* — the
direct anti-Thargoid analogue of the [[outfitting/heat-sink-launcher|Heat Sink Launcher]]. Where a
heat sink dumps accumulated **heat**, a caustic sink purges accumulated **caustic** damage: firing
one immediately clears the corrosive enzyme effect that Thargoid caustic clouds, caustic missiles
(see [[outfitting/enzyme-missile-rack]]), and Maelstrom/Titan environments stack onto your hull. In
the Coriolis data it is group `csl`, file `hardpoints/caustic_sink_launcher.json`. This is current,
accessible AX kit — **availability: live**.

## What it does

- **Vents caustic on demand.** Caustic damage is a hull-eating damage-over-time that keeps ticking
  after you leave the source. Launching a caustic sink strips that DoT off the ship at once — the
  only instant counter short of flying out of range and waiting it out.
- **Survival kit for caustic environments.** Essential for diving Titan wrecks, lingering near
  Maelstroms, and weathering Thargoid Interceptor caustic clouds without watching your hull melt.
- **Passive utility.** It is a `passive: 1` module that sits in a utility slot drawing power only on
  activation; it is not deployed/retracted like a weapon.

## Stats (single size — class 0, rating I)

Like the Heat Sink Launcher, there is **no class/rating ladder** — one size only, a **class-0 (tiny)
utility mount**, rating **I** (id `4A`, symbol `Hpt_CausticSinkLauncher_Turret_Tiny`).

| Field | Value | Meaning |
|---|---|---|
| Clip | 1 | sinks ready to fire before reload |
| Ammo (reserve) | 5 | spare sinks held |
| **Sinks carried** | **6** | clip 1 + reserve 5 (vs the Heat Sink Launcher's 4) |
| Ammo cost | 10 CR | per sink restocked |
| Fire interval | 5.0 s | minimum time between launches |
| Reload | 10 s | time to reload the clip |
| Power | 0.6 MW | draw on activation (passive otherwise) |
| EPS | 0.4 | energy-per-second draw while active |
| Distributor draw | 2 | weapons-capacitor cost per launch |
| Mass | 1.7 t | |
| Integrity | 45 | module hit points |
| Cost | 50,000 CR | base purchase |

A stock launcher carries **six caustic sinks** before needing a restock — two more than a Heat Sink
Launcher's clip-1 + reserve-3.

## How to fit

- Goes in a **utility mount**, competing with [[outfitting/shield-booster]]s, the
  [[outfitting/xeno-scanner]], the [[outfitting/shutdown-field-neutraliser]], chaff, and point
  defence for those small slots.
- **Pair with a Heat Sink Launcher on dedicated AX builds.** Caustic and heat are separate problems
  with separate sinks — a caustic-heavy fight (caustic clouds + your own thermal weapons) can demand
  both. See [[outfitting/heat-sink-launcher]].
- **Where to get them:** Human Tech Broker / AX war-effort supply (no Guardian unlock).

## Related AX utilities

The AX-utility family that turns a hull into a Thargoid-capable ship:
[[outfitting/xeno-scanner]] (find the weak points), [[outfitting/shutdown-field-neutraliser]]
(survive the EMP pulse), and this Caustic Sink Launcher (purge the caustic DoT). Pair with the AX
weapon line — see [[outfitting/ax-multi-cannon]] and the [[outfitting/guardian-gauss-cannon|Guardian trio]].

[[trunk]]
