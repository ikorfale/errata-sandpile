# Verdict: "N = 0 mod 64 implies 52 present" (PREREG-conv64, a8dd7ba)

Scored 2026-10-24 by lab jobs sandpile-conv64a (archived rows), sandpile-conv64b1 (1408, 1424) and
sandpile-conv64b2 (1472), code frozen at a97c731. All 70 input hashes in PREREG-conv64.sha256 match (`sha256sum -c`:
70 OK, 0 failed). The fresh rows pass their identity checks (`L v == e: True  e+e=e: True` for 1408, 1424, 1472).
Present = K=52 hits within D of a scanner 52-window > 0 (`tpl462.py 11 10 2016 N`).

| N | N mod 64 | role | part | 52-windows | hits within D | 52 |
|---|---|---|---|---|---|---|
| 1024 | 0 | test | A | 80 | 480 | present |
| 1088 | 0 | test | A | 80 | 480 | present |
| 1152 | 0 | test | A | 80 | 480 | present |
| 1536 | 0 | test | A | 656 | 1480 | present |
| 2048 | 0 | test | A | 1576 | 3464 | present |
| 1408 | 0 | test | B | 216 | 568 | present |
| 1472 | 0 | test | B | 256 | 808 | present |
| 1008 | 48 | control | A | 0 | 0 | **absent** |
| 1012 | 52 | control | A | 80 | 480 | present |
| 1296 | 16 | control | A | 304 | 960 | present |
| 1424 | 16 | control | B | 216 | 568 | present |

**Result.** The implication is **not refuted on these rows**: 7 of 7 test rows have 52 present. That is not support.
Of the 4 controls, 3 have 52 present too, so the one-sided Fisher exact test has almost nothing to work with:
- A and B together (test 7/0, control 3/1): p = 4/11 = 0.36;
- A alone (5/0 vs 2/1): p = 0.375;
- B alone (2/0 vs 1/0): no absence at all, p = 1. B says only "52 is common at these N".
Above N = 1000, 52 is absent in 1 of 11 scored rows (1008). The rule fits because 52 is almost everywhere, not
because of the modulus.

**The 16 mod 64 alternative survives.** 1296 and 1424 (both 16 mod 64) have 52 present, as 1232 did, so "present
when N = 0 or 16 mod 64" is also unrefuted here. By the prereg no new modulus is fitted from this.

**Exploratory rows (N < 1000, not part of the test).** 512, 640, 768 and 960 are 0 mod 64 and have 52 absent; 896 is
0 mod 64 and present. Below 1000 the implication fails 4 times out of 5, which fits the stated worry that a 2016
template may not fit at small N. These rows decide nothing.

**Unchanged.** The original 9 rows are not used here. Coincident counts (1024/1088/1152/1012 all 80 windows and 480
hits; 1408 and 1424 both 216 and 568) are from different inputs: the window totals and the K=64 counts differ (1408:
264,296 windows, K=64 hits 296; 1424: 260,130 and 472).
