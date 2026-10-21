# Pre-registration: the 960 -> 1024 jump, and N = 2048 at cap 20 (written 2026-10-21 ~20:55 UTC, before any row)

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
