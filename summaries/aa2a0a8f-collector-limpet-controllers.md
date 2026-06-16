---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/collector_limpet_controllers.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T00:44:44+00:00
source_count: 1
verified: false
availability: live
changed_note:
---


# Collector Limpet Controller (summary)

Controls **Collector Limpets** — autonomous drones that scoop mined fragments and floating cargo canisters and ferry them to your hold. Group `cc`. Classes 1/3/5/7; ratings A–E.

Key claims:
- Max **simultaneous** limpets by class: C1 = 1, C3 = 2, C5 = 3, C7 = 4.
- `time` = limpet **lifetime** in seconds: A 720 (longest, 12 min), D 600, C 510, B 420, E 300.
- A-rated gives the longest-lived limpets — standard pick for sustained mining.
- availability: live (current mining mechanic).

| Class | Rating | Max limpets | Lifetime (s) | Range (km) | Mass (t) | Power (MW) | Cost (CR) |
|---|---|---|---|---|---|---|---|
| 1 | E | 1 | 300 | 0.8 | 0.5 | 0.14 | 600 |
| 1 | D | 1 | 600 | 0.6 | 0.5 | 0.18 | 1,200 |
| 1 | C | 1 | 510 | 1 | 1.3 | 0.23 | 2,400 |
| 1 | B | 1 | 420 | 1.4 | 2 | 0.28 | 4,800 |
| 1 | A | 1 | 720 | 1.2 | 2 | 0.32 | 9,600 |
| 3 | E | 2 | 300 | 0.88 | 2 | 0.2 | 5,400 |
| 3 | D | 2 | 600 | 0.66 | 2 | 0.27 | 10,800 |
| 3 | C | 2 | 510 | 1.1 | 5 | 0.34 | 21,600 |
| 3 | B | 2 | 420 | 1.54 | 8 | 0.41 | 43,200 |
| 3 | A | 2 | 720 | 1.32 | 8 | 0.48 | 86,400 |
| 5 | E | 3 | 300 | 1.04 | 8 | 0.3 | 48,600 |
| 5 | D | 3 | 600 | 0.78 | 8 | 0.4 | 97,200 |
| 5 | C | 3 | 510 | 1.3 | 20 | 0.5 | 194,400 |
| 5 | B | 3 | 420 | 1.82 | 32 | 0.6 | 388,800 |
| 5 | A | 3 | 720 | 1.56 | 32 | 0.7 | 777,600 |
| 7 | E | 4 | 300 | 1.36 | 32 | 0.41 | 437,400 |
| 7 | D | 4 | 600 | 1.02 | 32 | 0.55 | 874,800 |
| 7 | C | 4 | 510 | 1.7 | 80 | 0.69 | 1,749,600 |
| 7 | B | 4 | 420 | 2.38 | 128 | 0.83 | 3,499,200 |
| 7 | A | 4 | 720 | 2.04 | 128 | 0.97 | 6,998,400 |
