# Pre-registration: does "N = 0 mod 64 implies 52 present" survive new rows? (zenith 100650; reviewed by a second model)

Written 2026-10-24 ~02:15 UTC, before any row below was scored. Code frozen at commit a97c731.

**Where the reading comes from.** PREREG-rows465 killed R52 ("52 present iff N = 0 mod 64") at 1232. zenith noticed
afterwards that the other half holds on all 9 scored rows: wherever 52 is absent, N is not 0 mod 64. That was found
after scoring, so those 9 rows are evidence for nothing here and are excluded.

**Present** is unchanged from PREREG-rows465: `tpl462.py 11 10 2016 N`, family K=52 present at N iff the
"within D of a scanner 52-window" count is > 0. Family labels are K = round(1/curvature) of the period lattice,
the same integer at every N. Per row I also report the number of scanner 52-windows and the hit count, not only
present/absent.

**Part A, archived rows (pre-specified analysis of old data, not a blind test).** The W=5, cap-20, four-phase scanner
arrays `out/hess_s_<N>_5_20_o??.npy` were computed on 21-23.10 for other questions (job406.py; its only later
change, 229dc36, moves scratch arrays to disk). They have never been scored with 2016 templates, but their text
summaries list families, so I cannot certify I never saw a class-52 line. Inclusion fixed by which N exist, not by
outcomes: every archived row with N >= 1000, N != 2016 (the template source).
- test (0 mod 64): 1024, 1088, 1152, 1536, 2048
- control (not 0 mod 64): 1008, 1012, 1296 (1296 is 16 mod 64, like 1232)
- rows below 1000 (512, 640, 768, 896, 960) scored and reported as exploratory only: a 2016 template may simply not
  fit at small N.

**Part B, fresh rows (the real pre-registration).** Not computed before this file: 1408 and 1472 (0 mod 64, test),
1424 (16 mod 64, control). Same pipeline: `odo_warm.py`, `job406.py`, then `tpl462.py 11 10 2016 N`.

**Rules.**
- The implication is **killed** by any test row (A or B, N >= 1000) where 52 is absent. Not killed = "not refuted on
  these rows", never "confirmed".
- It only means something if controls show absences. Statistic: one-sided Fisher exact test on the 2x2 table
  (0 mod 64 or not) x (present or not), on A and B together, A alone and B alone; the original 9 rows reported
  separately, never pooled into the test. If all controls are present, the result is "52 is common at these N" and
  says nothing about mod 64.
- If 1296 or 1424 is present, the alternative "present when N = 0 or 16 mod 64" also survives and I say so.
- No new modulus or interval is fitted afterwards. A row whose identity check fails is reported as failed and unused.

Input hashes (sha256 of the archived scanner arrays and identities) are in PREREG-conv64.sha256, committed with this file.
