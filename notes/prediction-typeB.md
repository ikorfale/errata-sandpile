# Prediction, written 2026-10-19 ~18:50 UTC while check_s2.py had reached M = 276 (not yet 318 or 386)

Type B (s2 = 0 on [0, L]) so far: M = 32 (L 1), 132 (L 4), 184 (L 5): L/M = 0.031, 0.030, 0.027.
Every type A size up to 276 has L/M >= 0.05 (smallest: 60:3, 156:8).
Prediction: the two low outliers above 276, M = 318 (L 8, 0.025) and M = 386 (L 14, 0.036), are type B;
every other L > 0 size in 278..400 (all have L/M >= 0.05) is type A.
If 318 or 386 is A, or any other size is B, the "type B = small L/M" reading is wrong.

## Result so far (18:55 UTC): M = 318 is type B (s2 = 0000000001), M = 282..352 others A. 386 pending.

## Second prediction, written 2026-10-19 ~18:56 UTC before check_s2 is run on any M > 400
Rule: type B iff L/M < 0.04. On the sizes the lab job found in 402..528 this predicts
B = {420 (10), 448 (6), 452 (12), 476 (13), 486 (8), 506 (13), 510 (19, 0.037)}, A = the other 9
(410, 416, 434, 444, 458, 472, 482, 492, 516; all L/M >= 0.08). Checked by lab job sandpile-s2-ext.
