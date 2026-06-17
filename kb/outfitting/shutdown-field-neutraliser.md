---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/shutdown_field_neutraliser.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T01:41:39+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Shutdown Field Neutraliser (Outfitting)

The **Shutdown Field Neutraliser** is a **utility-mount** module that counters the Thargoid
**EMP shutdown-field pulse** — the electromagnetic wave a Thargoid Interceptor emits that **disables
ship systems** (drives, weapons, life support flicker) for several seconds, leaving you helpless
mid-fight. Activating the neutraliser as the pulse hits keeps your ship online. In the Coriolis data
it is group `sfn`, file `hardpoints/shutdown_field_neutraliser.json`. Current, accessible AX content
— **availability: live**.

## What it does

- **Negates the shutdown pulse.** When a Thargoid winds up its EMP, firing the neutraliser shields
  your systems so drives and weapons keep working instead of going dark. Mistime it and you eat the
  full shutdown.
- **Passive utility.** A `passive: 1` module: it draws a small fixed `power` while fitted and a
  separate `activepower` only while the neutraliser pulse is active. Class-0 (tiny) on both variants.

## Variants

Two variants, both **class 0** utility mounts, both sharing **cooldown 10 s** and **duration 1**:

| id | Name | Symbol | Rating | Range | Power | Active power | Mass | Integrity | Cost |
|----|------|--------|--------|-------|-------|--------------|------|-----------|------|
| `Sn` | Shutdown Field Neutraliser | `Hpt_AntiUnknownShutdown_Tiny` | F | **3000 m** | 0.2 MW | 0.25 MW | 1.3 t | 35 | 63,000 CR |
| `4E` | Thargoid Pulse Neutraliser | `Hpt_AntiUnknownShutdown_Tiny_V2` | E | **0 m** | 0.4 MW | 0.33 MW | 3 t | 70 | 150,000 CR |

## Notes & which to fit

- The **base Shutdown Field Neutraliser** (`Sn`, rating F) carries `range: 3000` in the data — the
  area over which it neutralises the field.
- The **Thargoid Pulse Neutraliser** (`4E`, rating E) is the heavier, tougher V2 build: triple mass
  (3 t), double integrity (70), more power. Its `range` field is **0** in the Coriolis data —
  recorded verbatim; no numeric reach is invented for it here.
- `activepower` (0.25 / 0.33 MW) is the draw *while the neutraliser pulse is firing*, distinct from
  the passive `power` (0.2 / 0.4 MW) drawn just by being fitted.
- **Where to get them:** Human Tech Broker / AX war-effort supply.

## Related AX utilities

One leg of the AX-utility trio every Thargoid-capable ship carries:
[[outfitting/xeno-scanner]] (find the weak points), this Shutdown Field Neutraliser (survive the EMP
pulse), and [[outfitting/caustic-sink-launcher]] (purge caustic DoT). Pair with the AX weapon line —
[[outfitting/ax-multi-cannon]] and the [[outfitting/guardian-gauss-cannon|Guardian trio]].

[[trunk]]
