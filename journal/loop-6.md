# Loop 6 journal

Mode: search. Targets (tier 0): EDSM `stations/outfitting` for Garay Terminal (marketId
3229756160); Coriolis Cobra Mk V hull.

## Findings

- **Garay Terminal outfitting** (EDSM `api-system-v1/stations/outfitting`, marketId 3229756160):
  653 module SKUs across 107 families. Core internals to Class 8 (Power Plant, Thrusters, Power
  Distributor, Life Support, Sensors, Fuel Scoop, Shield Generator, Bi-Weave). Frame Shift Drive
  to Class 7, **standard and SCO variant**. Limpet controllers to 7, Refinery to 4, AFMU to 8,
  SRV hangars to size 6. Weapons capped ~Class 4. **No Guardian modules** (expected — Tech-Broker
  unlock, never sold on a market).
- **Cobra Mk V hull** (Coriolis `ships/cobra_mk_v.json`, export key `cobramkv`): Faulcon DeLacy
  size-1 multirole; hull 1,477,085 cr / retail 1,989,461 cr; hull mass 150 t; 291/412 m/s;
  shield 160 MJ; armour 180; crew 3. Core internals PP4/T4/FSD4/LS3/PD4/S3/FT4; hardpoints
  3M+2S; 4 utilities; optional internals 5/4/4/4/3/3/3/2/1 + Planetary Approach Suite.

## Source-path correction

- Queue's `dist/ships.json` is a dead path (404). Coriolis `dist/index.json` is build-generated
  at install time and **not committed** to the repo. Correct Tier-0 ship path is
  `ships/<slug>.json` (Cobra Mk V = `ships/cobra_mk_v.json`). Recorded in the queue DONE note.

## Pages updated

- `kb/ships/cobra-mk-v.md` — NEW page (source_count 1, verified false).
- `kb/locations/deciat.md` — added H3 "Garay Terminal — outfitting stock"; `source_count` 3→4.
  See escalation below — `verified` set false pending cloud council.
- `kb/trunk.md` — linked [[ships/cobra-mk-v]] under Ships.

## VERIFY ESCALATION — deciat

Local council on the new outfitting claim returned **verdict=conflict, confidence=0.75,
escalate=true**. Full result:

```json
{"verdict": "conflict", "confidence": 0.75, "votes": [
  {"model": "qwen3-coder:30b", "vote": "refute", "reason": "Source 1 indicates Frame Shift Drives are available up to Class 7, not Class 8 as claimed. Source 2 confirms the terminal's services but doesn't support the specific claim about Class 8 availability."},
  {"model": "qwen3:8b", "vote": "support", "reason": "Source 1 confirms that Garay Terminal sells Frame Shift Drives including the SCO variant up to Class 7 and full core internals up to Class 8. Source 2 confirms the station provides Outfitting service."}],
  "rationale": "Split vote with conflicting evidence. One source supports the claim up to Class 8, while another contradicts it by stating Frame Shift Drives are only available up to Class 7. The sources provide conflicting information about the maximum class availability, resulting in insufficient consensus for a definitive verdict.",
  "dissent": [], "escalate": true}
```

**Operator note (not an auto-resolution):** the split is a claim-wording artifact — the verified
claim said "Frame Shift Drives including the SCO variant **and** full core internals up to Class 8,"
which qwen3-coder read as asserting *FSD* to Class 8 (it is Class 7). The KB page itself states
FSD to C7 and core internals to C8 separately and correctly. Per PHASE 4.5 this is NOT
auto-resolved here: `verified: false` and an `<!-- ESCALATION -->` marker were written into
`kb/locations/deciat.md`. The cloud council (`council` skill) must adjudicate on the next attended
run; expected outcome is to re-affirm `verified: true` after re-phrasing the claim.

## Discards

None.
