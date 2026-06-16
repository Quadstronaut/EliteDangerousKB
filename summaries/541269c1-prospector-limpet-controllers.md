---
source_url: https://raw.githubusercontent.com/EDCD/coriolis-data/master/modules/internal/prospector_limpet_controllers.json
source_type: coriolis
source_tier: 0
captured_at: 2026-06-16T00:44:44+00:00
source_count: 1
verified: false
availability: live
changed_note:
---


# Prospector Limpet Controller (summary)

Controls **Prospector Limpets** — fired at an asteroid, they report its full mineral composition and apply a yield bonus to that rock. Group `pc`. Classes 1/3/5/7; ratings A–E.

Key claims:
- Max **simultaneous** limpets scales with class: C1 = 1, C3 = 2, C5 = 4, C7 = 8.
- A-rated control range by class: C1 7 km, C3 7.7 km, C5 9.1 km, C7 11.9 km (highest reach).
- Rating sets range/mass/power/cost; class sets simultaneous-limpet count.
- availability: live (current mining mechanic).

| Class | Rating | Max limpets | Range (km) | Mass (t) | Power (MW) | Cost (CR) |
|---|---|---|---|---|---|---|
| 1 | E | 1 | 3 | 1.3 | 0.18 | 600 |
| 1 | D | 1 | 4 | 0.5 | 0.14 | 1,200 |
| 1 | C | 1 | 5 | 1.3 | 0.23 | 2,400 |
| 1 | B | 1 | 6 | 2 | 0.32 | 4,800 |
| 1 | A | 1 | 7 | 1.3 | 0.28 | 9,600 |
| 3 | E | 2 | 3.3 | 5 | 0.27 | 5,400 |
| 3 | D | 2 | 4.4 | 2 | 0.2 | 10,800 |
| 3 | C | 2 | 5.5 | 5 | 0.34 | 21,600 |
| 3 | B | 2 | 6.6 | 8 | 0.48 | 43,200 |
| 3 | A | 2 | 7.7 | 5 | 0.41 | 86,400 |
| 5 | E | 4 | 3.9 | 20 | 0.4 | 48,600 |
| 5 | D | 4 | 5.2 | 8 | 0.3 | 97,200 |
| 5 | C | 4 | 6.5 | 20 | 0.5 | 194,400 |
| 5 | B | 4 | 7.8 | 32 | 0.97 | 388,800 |
| 5 | A | 4 | 9.1 | 20 | 0.6 | 777,600 |
| 7 | E | 8 | 5.1 | 80 | 0.55 | 437,400 |
| 7 | D | 8 | 6.8 | 32 | 0.41 | 874,800 |
| 7 | C | 8 | 8.5 | 80 | 0.69 | 1,749,600 |
| 7 | B | 8 | 10.2 | 128 | 0.97 | 3,499,200 |
| 7 | A | 8 | 11.9 | 80 | 0.83 | 6,998,400 |
