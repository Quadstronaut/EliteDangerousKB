---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/hardpoints/xeno_scanner.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-17T01:41:39+00:00
source_count: 1
verified: false
availability: live
changed_note:
---

# Xeno Scanner (Outfitting)

The **Xeno Scanner** is a **utility-mount** scanner that analyses a Thargoid target: it identifies
the Thargoid **type/variant** and reveals its **subsystems and weak points** (the hearts on an
Interceptor). Without a completed xeno scan you cannot meaningfully target a Thargoid's vulnerable
components, so it is mandatory kit for any AX combat build. In the Coriolis data it is group `xs`,
file `hardpoints/xeno_scanner.json`. Current, accessible AX content — **availability: live**.

## What it does

- **IDs the threat.** Completes a scan that names the Thargoid type and unlocks its subsystem list,
  letting your AX weapons ([[outfitting/ax-multi-cannon]], the
  [[outfitting/guardian-gauss-cannon|Guardian trio]]) target the exposed hearts.
- **Hold-to-scan within range.** You must keep the target inside the scanner's range and scan cone
  for the full scan time — the range tier is the practical difference between the variants.
- **Passive utility.** Sits in a utility slot; class-0 (tiny) on every variant.

## Variants

Three variants, all **class 0** utility mounts, all sharing **scan time 10 s**, **scan angle 23°**,
and **boot 2 s**:

| id | Name | Symbol | Rating | Range | Power | Mass | Integrity | Cost |
|----|------|--------|--------|-------|-------|------|-----------|------|
| `xs` | Xeno Scanner | `Hpt_XenoScanner_Basic_Tiny` | E | **500 m** | 0.2 MW | 1.3 t | 56 | 365,698 CR |
| `3y` | Enhanced Xeno Scanner | `Hpt_XenoScannerMk2_Basic_Tiny` | C | **2000 m** | 0.8 MW | 1.3 t | 56 | 745,948 CR |
| `4B` | Pulse Wave Xeno Scanner | `Hpt_XenoScanner_Advanced_Tiny` | C | **1000 m** | 1.0 MW | 3 t | 100 | 850,000 CR |

## Which to fit

- **Range is the whole point.** The base Xeno Scanner's **500 m** forces you dangerously close to a
  hostile Interceptor to complete a scan. The **Enhanced Xeno Scanner (Mk2)** quadruples range to
  **2000 m** for modest extra power — the practical default for AX combat.
- **Pulse Wave Xeno Scanner** sits at **1000 m** but is the toughest build: triple mass (3 t), double
  integrity (100), highest power (1.0 MW). The "Pulse Wave" name reflects its broader detection
  emphasis rather than longest reach.
- **Where to get them:** Human Tech Broker (the Enhanced and Pulse Wave tiers in particular).

## Related AX utilities

One leg of the AX-utility trio every Thargoid-capable ship carries:
this Xeno Scanner (find the weak points), [[outfitting/shutdown-field-neutraliser]] (survive the EMP
shutdown pulse), and [[outfitting/caustic-sink-launcher]] (purge caustic DoT). Pair with the AX
weapon line — [[outfitting/ax-multi-cannon]] and the [[outfitting/guardian-gauss-cannon|Guardian trio]].

[[trunk]]
