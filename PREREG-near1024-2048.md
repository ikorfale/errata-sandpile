# Pre-registration: the 960 -> 1024 jump, and N = 2048 at cap 20 (written 2026-10-21 ~20:45 UTC, before any row)

Known counts (cap 10, four phases): 896:9 960:8 1024:23 1088:22 1152:20 1216:18 1280:14 1536:17.
Jobs queued, no output yet: sandpile-p10-1016 (job_near1024.py: N = 1016, 992 at cap 10) and sandpile-p20-2048
(job406d.py: N = 2048 at cap 20). 1536 at cap 20 is registered separately (PREREG-cap20-406.md addendum).

Competing readings (decision table drafted with a second model, Fable, and adopted as is):
- step exactly at 1024 (a power-of-two effect or a code constant): 1016 about 8, like 960;
- gradual threshold near 1000 (patches outgrow what the side-5 window can reach): 992 and 1016 in between, 10-20;
- at 2048, inside D10: >= 23 supports power-of-two; <= 16 with >= 8 cap-20 extras supports scaling; 17-22 with <= 3
  extras reads as noise in which families happen to have a clean patch. Differences under 6 are treated as noise
  (1280:14 vs 1536:17 shows jitter of about 3).

My own point bets (one of them will probably miss):
1. 992: 11 families (range 8-16). 1016: 15 (range 11-20). So: gradual, not a step.
2. 2048 at cap 20: 20 families inside D10 (range 15-26), cap-20-only extras <= 3.
Checks done before registering: no literal 512/1024/2048 in hess_stream.py, parents81.py or job406.py; 960 and 1088
identities were computed the same day by the same odo_fast.py, so the jump is not a batch boundary.

## Addendum 2 (2026-10-21 ~21:10 UTC, before any row at 992, 1016, 2016 or 2048 exists)

**Correction of my 2048 band.** The flank trend (zenith 97245: count ~ N^1.2, 10.05 at 1024) predicts 10.05 x 2^1.2 = 23.1
at 2048. My rule ">= 23 supports power-of-two" therefore read the null as support. Found by a second model (Fable) on review.
Replaced, for 2048 families inside D10 (equal to the cap-10 count at every N checked so far):
- <= 17: decline (reach or scaling); 18-29: nothing special at 2048; >= 30: the 1024 bump repeats
  (a repeat of 1024's excess predicts ~36 additive, ~53 multiplicative).
My point bet of 20 stays, so under the corrected bands I am betting "nothing special".

**Paired row added: N = 2016 at cap 10** (job sandpile-p10-2016, after 2048). Adjacent rows share families, so the
neighbour difference is tight (observed changes 896->1536: -1, +15, -1, -2, -2, -4). Decision on the pair:
- >= 8 families present at 2048 and absent at 2016: step at the power of two;
- 2016 already >= 30 and |2048 - 2016| <= 3: gradual threshold just below 2048;
- both 18-29 and |diff| <= 3: nothing special.
2304 (trend ~27, tests whether the decay length is absolute or scales with N) is deferred for cost.

**Observation from the existing presence table (896-1536), made before these rows:** all 14 families that are new at
1024 have their first appearance at exactly 1024 (none at 960 or earlier). Exit is not one-way: 7 of them, after vanishing,
reappear at 1280 or 1536. So "each family has one visibility interval in N" is false here; the 1088-1280 decay is
flicker, not one-by-one exit, and synchronized entry is not explained by reach.
