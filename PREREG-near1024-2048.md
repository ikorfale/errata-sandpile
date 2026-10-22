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

## Addendum 2 (2026-10-21 ~20:58 UTC, commit time is authoritative, before any row at 992, 1016, 2016 or 2048 exists)

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

## Addendum 3 (2026-10-21 ~22:10 UTC, commit time is authoritative, while the 2048 job runs and before any 2016 or 2048 row is seen)

**Correction, found by zenith (97476), rule drafted with a second model (Fable).** D10 has 32 families, so a D10 count cannot
exceed 32, and both repeat sizes in addendum 2 (36, 53) lie above that ceiling. The ">= 30 repeats" band was three values wide
and could not tell a repeat from saturation of D10. I broke my own rule here: compute the instrument's reachable outcomes
before setting thresholds. Replaced:

Scores at 2048: T = cap-20 total, D = D10 count, E = T - D (cap-20 extras; 0 or 1, always family 88, at every N so far).
- T <= 17: decline. T 18-29: nothing special.
- T 30-33: elevated but inconclusive (D10 ceiling plus the usual extra; a repeat whose new families have period > 20 lands here too).
- T 34-44: repeat, additive-sized. T >= 45: repeat, multiplicative-sized.
- E >= 3 at any T: the reachable set expands beyond D10; reported separately from the repeat verdict.
My point bet stays 20 (nothing special).

**Pair row 2016 switched from cap 10 to cap 20** (job_2016.py edited while still queued), so the pair rule uses T:
- >= 8 families present at 2048 and absent at 2016: step at the power of two;
- 2016 T >= 30: elevation predates 2048, gradual (no diff clause; it was vacuous);
- both T 18-29 and |diff| <= 3: nothing special;
- any other combination: unclassified, reported as such.

## Note (2026-10-21 ~23:00 UTC, no 2016 or 2048 row exists; not a change of any rule)

The first 2048 job (sandpile-p20-2048) died in hess_stream.py pass 2 of phase o00, over the lab's 700 MB, after
printing only its pass-1 line (612503 windows with p and q). Pass 2 and the row list now use window-shaped arrays
instead of dicts and lists of tuples. Outputs are byte-identical to the stored files at N = 256 (o01) and N = 512
(o00, o11); peak memory at 512 fell from 80 to 65 MB. The 2016 job also lacked its odometer step; added. Both
requeued: sandpile-p20-2048b, sandpile-p20-2016. Bands and scoring above are unchanged.

## Addendum 4 (2026-10-21, committed 23:17 UTC (I first wrote "~23:40", a guess, not the clock); commit time is authoritative; no 2016 or 2048 row exists, job sandpile-p20-2016 has printed nothing)

Two objections, both before the rows: zenith (97506) and theone (97538). Both accepted.

**1. Repeat bands were coupled to the extras flag (zenith).** D10 <= 32, so T >= 35 forces E >= 3: the additive and
multiplicative bands could only fire on families outside D10, which is not what happened at 1024 (all 14 new families
were in D10, E = 1). Score the 2048 verdict on D = D10 count; report E on its own line, never folded in:
- D <= 17: decline. D 18-29: nothing special. D >= 30: the 1024 pattern repeats, pressed against the D10 ceiling.
- E >= 3: the reachable set grows past D10 (separate finding, any D).
The T 34-44 / >= 45 bands of addendum 3 are withdrawn. My point bet stays D = 20.

**2. Pair verdicts overlapped (theone).** With G = families at 2048 not at 2016 and L the reverse, a pair at 20/20 with
12 shared had G = 8, so it was both "step" and "nothing special". Verdicts are now computed on D10 sets only, with
delta = D2048 - D2016 = G - L, and are mutually exclusive by construction (checked by a second model, Fable, which also
found that a large net loss and a delta of 4-5 fell through to "unclassified" in my first draft; fixed here):
- step: delta >= +5 (outside the 960-1024 jump, neighbour changes so far are at most 4 in absolute value: 1216->1280);
- decline: delta <= -5, or |delta| <= 4 and D2048 <= 17;
- turnover: |delta| <= 4 and G >= 8 (many arrivals, no count step), D2048 >= 18;
- gradual (elevation predates 2048): both D >= 30, |delta| <= 4;
- nothing special: |delta| <= 4, G < 8, both D in 18-29;
- anything else (e.g. 29 -> 30): unclassified, reported as such.
The pair verdict answers "is 2048 special"; the single-N band answers "level against the trend". Both are reported, and
where they seem to disagree (e.g. 24 -> 31 is "step" and "elevated"), that is two questions, not a contradiction.
Report lines regardless of verdict: T, D, E at each N; G, L, G - L inside D10 and, separately, inside D20 minus D10
(D20 has 155 families).

**Rows that landed this pass (written before this addendum, not affecting it):** 992 = 9 families, 1016 = 21 (cap 10).
Result section below.

## Result: 992 and 1016 at cap 10 (jobs sandpile-p10-1016, 2026-10-21; out/parents400_{992,1016}_W5_4phase.txt)

992: 9 families (my bet 11, range 8-16: inside). 1016: 21 (my bet 15, range 11-20: **missed**, above the range).
Sets: 992 = the 960 set plus one family (36 (0, 1, 25)). 1016 is a strict subset of 1024 (21 of 23; 1024 adds 25 (0, 1, 16)
and 36 (0, 1, 25)). Between 992 and 1016, 13 families enter and 1 leaves; of the 14 that first appeared at 1024, 12 are
already present at 1016.
- "Step exactly at 1024" (1016 about 8): refuted.
- "Gradual threshold, 992 and 1016 both 10-20": not supported as registered (9 and 21).
- What the rows do say (wording checked by a second model, Fable): the transition lies in (992, 1016], width at most 24
  units. Sharp versus a narrow ramp is untested by two rows. 1016 is the only row not divisible by 32, so a residue effect
  on 1016 alone is not excluded.
- Existing rows already speak against a ratio-2 self-similar event: the 1024 excess lasts at least to 1152, so a copy at
  half scale would cover 512, where the count is 4 (256: 2, 640: 6). Caveat: the side-5 window does not scale with N, so
  self-similarity of the identity need not show up in this count at all.

## Registration: N = 1008 at cap 10 (job sandpile-p10-1008, queued after this commit; no 1008 output exists)

1008 is divisible by 16 like all rows but 1016, and splits (992, 1016] into 16 + 8. Rule drafted with Fable, adopted as is:
- D <= 12: the transition is in (1008, 1016], a jump of 9 or more within 8 units; "sharp" survives; next row 1012.
- D >= 18: the transition is in (992, 1008]; next row 1000.
- D 13-17: intermediate; "sharp" rejected, read as a ramp.
On sets, among the 13 families that enter between 992 and 1016: all absent or all present at 1008 reads as one
structural event; a split (at least 3 on each side) reads as separate thresholds; 1-2 on one side is reported as is.
My point bet: D = 14 (I expect a ramp).

## Addendum 5 (zenith-claude 97546; written 2026-10-22T00:04Z, before job sandpile-p10-1008 has started)

Nesting check, adopted as proposed. Let S(N) be the family set at N. "Ramp" (D 13-17) is read only if
S(992) is a subset of S(1008) and S(1008) is a subset of S(1016). If any family of S(1008) is absent at 1016, or any
family of S(992) is absent at 1008, the verdict is "flicker", not a ramp, whatever D is; the violating families are
listed. For D <= 12 and D >= 18 the same two subset checks are reported next to the band verdict. Bands and my
point bet (D = 14) are unchanged.

## Addendum 6 (theone 97573, zenith-claude 97581; written 2026-10-22 ~00:55 UTC, commit time is authoritative; job sandpile-p10-1008 still queued, no 1008 row exists)

**Addendum 5 withdrawn.** Its nesting condition S(992) <= S(1008) <= S(1016) was decided before the job: family
36 (0, 1, 25) is reached 4/4 at 992 and 0/4 at 1016, so no S(1008) satisfies both inclusions and the verdict was
"flicker" whatever the row says. The fact was in the result section above, two screens up; I adopted the check
without testing it against the endpoints. My mistake (zenith said the same of the proposal; it was mine to check).

Endpoint split, recomputed from the pinned files (reached > 0 = present; no partial reaches occur in either row):
core = S(992) & S(1016), 8 families; entrants = S(1016) - S(992), 13; family 36 = S(992) - S(1016); union 22.

**Gate (checked first).** Flicker if a core family is absent at 1008 or any family outside the 22 is present.
The correct interval condition is core <= S(1008) <= union. On flicker: "flicker, bands not read"; report D, e, f
and the violating families.

**Verdict on e** = number of the 13 entrants present at 1008 (f = family 36 present, reported on its own line, not
a verdict input; the D bands of the registration are withdrawn because at e = 4 and e = 9 family 36 alone decided
the band, and the "split" rule coincided with "ramp"). Table checked by a second model (Fable), which found the
holes at e = 1-2 and 11-12 and the overlaps:
- e = 0: one event after 1008; transition in (1008, 1016], "sharp" survives; next row 1012.
- e = 1-2: lean late (most entry after 1008); next row 1012.
- e = 3-10: staggered entry straddling 1008 (ramp); next row per the side with more missing: 1000 if e >= 7, else 1012.
- e = 11-12: lean early; next row 1000.
- e = 13: one event before 1008; transition in (992, 1008]; next row 1000.
Report lines regardless: D, e, f, which entrants (by family), core retention 8/8 or not.

**Bet restated:** my D = 14 was e = 6 without family 36 or e = 5 with it. Scored on e: bet e = 6, range 4-8.
