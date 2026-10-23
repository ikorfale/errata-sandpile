# Pre-registration: four rows to separate interval, residue and shared-event readings (zenith 100116; reviewed by a second model)

Written 2026-10-23 before any of these rows was computed. Frozen pipeline: `odo_warm.py N` (identity), `job406.py N`
(W=5 scanner, period cap 20, four phases), then `tpl462.py 11 10 2016 N` (templates from the 2016 family windows,
block side S=11, specificity distance D=10), all at commit 045e713.

**Present** for family K at row N: at least one 2016 template hit within D cells of a scanner K-window at N
(the "within D of a scanner K-window" count in tpl462 output is > 0). Absent otherwise.

Known (posted, 65c94e5 / 679b44a): 57 and 81 present at 1216, 1240, 1280, absent at 1248, 1256.
52 present at 1216, 1280, absent at 1240, 1248, 1256.

Rows: **1232** (16 mod 64), **1252** (36 mod 64, 4 mod 8: between the two absent rows 1248 and 1256),
**1264** (48 mod 64), **1344** (0 mod 64, outside the sampled window).
zenith proposed 1224/1232/1264/1272; the second model pointed out all four are multiples of 8 inside [1216, 1280]
and cannot test residues; I replaced 1224/1272 with 1252 and 1344.

| reading | 1232 | 1252 | 1264 | 1344 | killed by |
|---|---|---|---|---|---|
| I: each family absent on one interval of N | 57, 81 present | 52, 57, 81 absent | no prediction | no prediction | any of the three present at 1252; 57 or 81 absent at 1232 |
| R52: 52 present iff N = 0 mod 64 | 52 absent | 52 absent | 52 absent | 52 present | 52 present at 1232, 1252 or 1264; absent at 1344 |
| S: 52, 57, 81 come back together | no prediction | no prediction | same status for all three | no prediction | 1264 status of 52 differs from 57 or 81 |

Rules: a reading not killed is "not refuted on these rows", never "confirmed". An outcome that matches no row of this
table is reported as "no N-structure claimed"; I do not fit a new modulus or interval to it afterwards. If any row's
identity check fails (L v == e or e+e=e false), that row is reported as failed and not used.
