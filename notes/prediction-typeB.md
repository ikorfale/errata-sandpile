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

## Result of the first prediction (19:03 UTC): both hit. 386 is B (s2 = 0000000000000001), 392 is A.
Up to 400: 47 sizes with L > 0, 42 A, 5 B (32, 132, 184, 318, 386), none other. B: L/M 0.025..0.036; A: L/M >= 0.048 (228:11).
Identity e[m-2] - e[m-1] = s2 - 2 step + H(step) holds on every column at all 47 sizes; step is the indicator of [L, M-L) at all 47.

## Third prediction, written 2026-10-19 ~20:10 UTC, before check_s2 is run on any M > 528
The gzeros-ext job reached M = 548 (4-hour limit). New L > 0 sizes past 528: 530 (L 52, 0.098), 534 (L 21, 0.0393), 540 (L 32, 0.059).
Rule B iff L/M < 0.04 predicts: 534 = B (a close call, 0.0393), 530 = A, 540 = A.

## Mod-32 pre-registration (gzeros_job.py), final on 402..548
19 on-sizes; 16 in the window {18..30, 0..4} (84%, vs 10/16 = 62.5%; one-sided binomial tail 0.037). Outside: 458 (10), 486 (6), 492 (12).
No adjacent on-pair. Gaps (from 392): 18, 6, 4, 14, 10, 4, 4, 6, 14, 4, 6, 4, 6, 14, 4, 6, 14, 4, 6 — all in {4, 6, 10, 14, 18}. Max L/M 0.115 <= 0.125.
All four pre-registered claims survive. The window was chosen after seeing <=400, so 0.037 is the only honest p here.
