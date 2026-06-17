# Loop 20 — AX-utility trio completed (search mode)

3 new Tier-0 Coriolis outfitting pages, all `availability: live`, source_count 1, verified false.
All are class-0 utility mounts — the survival/targeting kit that makes any hull Thargoid-capable.

## Pages

1. **kb/outfitting/caustic-sink-launcher.md** (csl, id 4A rating I, `Hpt_CausticSinkLauncher_Turret_Tiny`)
   — caustic analogue of the Heat Sink Launcher; fires a caustic sink that instantly purges
   accumulated caustic DoT (Thargoid clouds / enzyme missiles / Titan-Maelstrom). No class/rating
   ladder. clip 1 + ammo 5 = **6 sinks** (vs heat sink's 4). ammocost 10, fireint 5.0, reload 10,
   power 0.6, eps 0.4, distdraw 2, mass 1.7, integ 45, cost 50,000, passive.
2. **kb/outfitting/xeno-scanner.md** (xs) — IDs Thargoid type + reveals subsystems/weak points
   (required to target Interceptor hearts). 3 variants, all class 0, shared scantime 10s / angle 23 /
   boot 2s. Range is the differentiator: base E **500 m** (cost 365,698) / Enhanced (Mk2) C **2000 m**
   (cost 745,948, the practical default) / Pulse Wave C **1000 m** but heavier (mass 3, integ 100,
   power 1.0, cost 850,000).
3. **kb/outfitting/shutdown-field-neutraliser.md** (sfn) — counters the Thargoid EMP shutdown-field
   pulse that disables ship systems. 2 variants, both class 0, shared cooldown 10 / duration 1 /
   passive. Base (Sn) rating F range **3000 m** (cost 63,000) / "Thargoid Pulse Neutraliser" V2 (4E)
   rating E (mass 3, integ 70, cost 150,000) — `range` field is **0** in Coriolis data (recorded
   verbatim, not invented). `activepower` (draw while firing) distinct from passive `power`.

## Edits / links

- trunk.md: +3 Outfitting bullets + new **AX utilities** line in the AX/Thargoid section
  (scanner / shutdown neutraliser / caustic sink trio).
- Bidirectional AX-utility cross-links across all 3 new pages + `[[outfitting/heat-sink-launcher]]`.

## Path notes

All 3 `hardpoints/*.json` (caustic_sink_launcher, xeno_scanner, shutdown_field_neutraliser) resolved
first try, no 404 — index.js keys csl/xs/sfn confirmed last loop. Follow-on queued:
**decontamination_limpet_controller** (dtl, internal/) = the AX limpet line (sustained caustic
removal, self/ally). After that the core AX-utility set is complete.

## Verify

Verify enabled, but all 3 pages are source_count 1 with no CONFLICT markers — none met the council
threshold (source_count >= 2 OR conflict). No escalation. Left verified=false (single Tier-0 source).
