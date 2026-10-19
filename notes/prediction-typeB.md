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

## Result of the second prediction (20:20 UTC): 16 of 16 as predicted. B = 420, 448, 452, 476, 486, 506, 510; A = the other 9. Identity on all columns and step_ok at all 16.

## Result of the third prediction (lab job sandpile-s2-ext3, done 20:31 UTC, read 21:30 UTC): 3 of 3.
534 = B (s2 = 00000000000000000000001, L 21, L/M 0.0393), 530 = A, 540 = A. Identity on all columns and step_ok at all three.
Total on sizes not yet checked when each prediction was written: 15 (282..400) + 16 (402..528) + 3 = 34 of 34 typed as predicted, 10 of them B (318 386 420 448 452 476 486 506 510 534).
Gap on L/M now: largest B 0.0393 (534), smallest A 0.048 (228).

## Fourth pre-registration, written 2026-10-19 ~21:35 UTC, before L is known for any M > 548
Lab job sandpile-s2-ext4 extends gzeros from 550 and, for every new size with L > 0, runs check_s2.
Fixed before either L or type is known: type B iff L/M < 0.04, for every on-size it reaches.
Also carried forward: on-sizes mostly in the mod-32 window {18..30, 0..4}; no adjacent on-pair; gaps in {4, 6, 10, 14, 18}; L/M <= 0.125.
Any size with L/M in [0.0393, 0.048) is the interesting one: it tells where the cut is, if there is one.
