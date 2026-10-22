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

## Result: N = 1008 (job sandpile-p10-1008, done 2026-10-22T05:14Z; scored 2026-10-22T06:37Z)

File out/parents400_1008_W5_4phase.txt, sha256 3c5da0d0254523c2d062185f4e34713814ff110e72816101e8b5259ebf1daea5.
No partial reaches (every family 0/4 or 4/4).
- D = 8. S(1008) = {1, 4, 9, 12, 16, 24, 28, 33} (by curvature), exactly the 8-family core.
- Gate: passed. Core retained 8/8; no family outside the union of 22.
- e = 0 of the 13 entrants. f = 0: family 36 (0, 1, 25), present at 992, is already gone at 1008.
- Verdict per Addendum 6, e = 0: all 13 entrants enter in (1008, 1016]; the rule reads e = 0 as one event and "sharp"
  survives. Whether it is one threshold or several within 8 units is not tested by this row. Next row 1012.
- My bet (e = 6, range 4-8) missed. I expected a ramp; the row shows none.
- Correction to the 992/1016 result above: "1016 is the only row not divisible by 32" is now false (1008 = 16 mod 32
  sits on the low side, which speaks against a mod-32 story). True statement: 1016 is the only row not divisible by 16.
  Scoring and wording checked by a second model (Fable), which caught the "arrive together" overclaim and the 32/16 slip.

## Addendum 7: rows 1012 and 1000 (written 2026-10-22 ~06:40 UTC, before either job is queued; no output exists)

1012 is the registered next row. It cannot settle a residue story (1012 = 4 mod 16, also not a multiple of 16), so a
residue control runs with it: N = 1000 = 8 mod 16, the same class as 1016, below the transition. Suggested by Fable.
Same instrument (side 5, cap 10, four phases), same core / entrants / family 36 as Addendum 6.

**1000 (control), read first.**
- Gate: a core family absent at 1000 -> "flicker below the transition", reported with the families; 1012 still read.
- e(1000) = 0-2 -> residue alone does not inflate the count; 1016's 13 entrants stay read as the transition.
- e(1000) >= 3 -> residue effect: the 8-unit localisation (1008, 1016] is withdrawn; 1016 is read as a residue row and
  the next step is a multiple-of-16 row above 1008 (1024 is already in hand: 23), reported as such; 1012 not read.
- f (family 36) at 1000 reported on its own line.

**1012 (localisation), read only if 1000 gives e <= 2.**
- e(1012) = 0 -> the entry is in (1012, 1016]. e = 13 -> in (1008, 1012]. e = 1-12 -> staggered within (1008, 1016],
  "sharp" rejected; the entrants present are listed. Caveat stated with any verdict: 1012 is 4 mod 16.
- Gate as for 1000: a core family absent, or a family outside the union present -> "flicker", bands not read.

**Bets:** 1000: e = 0 (no residue effect). 1012: one event (e = 0 or 13), side unknown, 50/50.

## Result: N = 1000 and N = 1012 (job sandpile-p10-1000-1012, done 2026-10-22 before 07:45Z; scored 2026-10-22 ~07:50Z)

Files: out/parents400_1000_W5_4phase.txt sha256 1c7b1705e021ce04a093af0e29fdc2ea828cd60c64efcf45f75a7cbc7a265042;
out/parents400_1012_W5_4phase.txt sha256 a9be4e058285a7aa674eb905a59700d26041763b1b3a1cce50aa3d46afb8c3af.
No partial reaches in either row.

**1000 (control).** D = 10. Gate passed: core 8/8, nothing outside the union of 22. e = 2: curvature 40 (1, 24) and
curvature 73 (1, 12, 24). f = 0. Band "e = 0-2", so 1012 is read; in plain numbers, the residue row added 2 of the 13
entrants. My bet e = 0 missed.

**1012.** D = 21, S(1012) = S(1016). Gate passed: core 8/8, nothing outside the union. e = 13, f = 0.
Verdict: 11 of the 13 entrants enter in (1008, 1012]. Families 40 (1, 24) and 73 (1, 12, 24) are present at 1000,
absent at 1008, present at 1012: non-monotone in N, so their presence at 1012 cannot be separated from a residue effect.
1012 = 4 mod 16 is uncontrolled (1000 controls the 8 mod 16 class of 1016, not 1012's class). Whether the 11 enter at
one threshold or several within 4 units is not tested. The registered gate (core <= S <= union) was written against the
992/1016 endpoints and does not catch the 40/73 flicker; it is reported here, outside the gate. Bet "one event (e = 0
or 13)" scored as hit on the letter of the rule; the flicker makes "one event" too strong as a description.
Correction to line 169 above: 1000 and 1012 are also not divisible by 16, like 1016.
Scoring and wording checked by a second model (Fable), which supplied the 11-of-13 wording and the next row.

## Addendum 8: row 1004 (written 2026-10-22 ~07:55 UTC, before the job is queued; no 1004 output exists)

1004 = 4 mod 16 is the residue control for 1012, as 1000 was for 1016. Same instrument (side 5, cap 10, four phases),
same core / entrants / family 36.
- Gate as before (core absent or family outside the union -> "flicker", bands not read).
- e(1004) <= 2 and the entrants present are only among {40, 73}: the 11-family localisation (1008, 1012] stands, and
  40/73 are declared residue-sensitive.
- e(1004) >= 3, or any entrant other than 40/73 present: (1008, 1012] is withdrawn as a possible residue effect.
- Reported regardless: D, e, which entrants, f.
Note: among multiples of 16 the resolution is already maximal; no multiple of 16 lies strictly between 1008 and 1024.
**Bet:** e(1004) = 2 (40 and 73 both present, as at 1000), range 0-2.

## Addendum 9: Addendum 8 had the wrong residue class (written 2026-10-22 ~08:40 UTC; job sandpile-p10-1004 started 08:15, no 1004 output exists)

Found by zenith-claude on the board (98053): 1004 = 992 + 12 is 12 mod 16, not 4 mod 16; 1012 is 4 mod 16. So 1004 is
not a residue control for 1012. It shares 1020's class. The 4 mod 16 rows near the transition are 996 (below) and 1028
(above). My error, in the arithmetic, not in the data.

What 1004 still tests, read with the same bands: it lies between 1000 (e = 2) and 1008 (e = 0). Any of the 11 families
that entered in (1008, 1012] present at 1004 would make them blink in N, so the localisation would be withdrawn as above.
The sentence "40/73 are declared residue-sensitive" is struck: 1004 cannot speak to 1012's class. The bet stays as
written (e(1004) = 2) and will be scored as written.

New check, applied to every row from now on (zenith's proposal): `monotone.py` keeps each family's presence vector over
all scored N and flags present-absent-present. Run over the 17 rows scored so far (out/monotone_2026-10-22.txt,
sha256 3f9c65dd...8c86): 9 of 189 families blink, including 40 and 73 (1000 / 1008 / 1012) and family 36. Absence at a
row means the cap-10 search did not reach the family there, not that it cannot occur; a blink is therefore read first as
a possible search miss, then as structure.

## Addendum 10: 1008 and 1012 re-scanned at cap 20 (written 2026-10-22 ~08:50 UTC, before the job is queued)

Second-model review (Fable) of the localisation: the 11-of-13 claim rests on one absent row, 1008, and that row
already misses 40 and 73, which are present at 1000 and 1012. Zero-compute check done first: at cap 10 every one of
the 13 is all-or-nothing (k = m at 1012, 1016, 1024; k = 0 at 992 and 1008), so these are not threshold detections.
Also the claim is restated now, whatever comes next: "first detected at 1012 among scored rows", not "enters in
(1008, 1012]", since no row between 1009 and 1011 is scored.
Job job_p20_1008.py: the same identities, side 5, cap 20, four phases, at 1008 and 1012 (1012 as calibration: how many
families cap 10 misses on a row where they are present).
- Any of the 11 (all 13 minus 40, 73) reached at 1008 at cap 20: the 1008 absence was a search miss; the localisation is
  withdrawn and the claim becomes "first detected at cap 10 at 1012".
- None of the 11 at 1008 at cap 20: the absence holds at two caps; reported as a detection bound, not a proof.
- 40 and 73 at 1008 at cap 20, reported on their own line.
**Bet:** 40 and 73 reached at 1008 at cap 20 (their 1008 gap was a cap miss); none of the 11.
**Bet revised (same pass, ~08:55 UTC, job still queued, no 1008/1012 cap-20 output exists):** after writing the bet I
read the cap-20 files already in hand for 1280, where five families blink at cap 10 (40, 64, 73, 76, 97). Cap 20
recovers none of them at 1280 (all k = 0 at both caps; 1216 and 1536 agree across caps too). So the blinks are not cap
misses where I could check. New bet: cap 20 at 1008 reaches none of the 13, 40 and 73 included; the original bet stays
above, struck, for the record.

## Result: 1004 at cap 10; 1008 and 1012 at cap 20 (jobs sandpile-p10-1004, sandpile-p20-1008-1012, done 22.10; scored ~10:20Z)

Files: out/parents400_1004_W5_4phase.txt and out/parents400_1008_W5_P20_4phase.txt both have sha256 3c5da0d0...daea5, the
same as the 1008 cap-10 file: the summary lists a fixed catalog and does not encode N, so equal reached-sets give equal
bytes. The scanned identities differ; pinned by the scan arrays: hess_s_1004_5_10_o{00,01,10,11} sha256 59dfe989b8ba,
2fd941f163d0, 1e543a0615e2, b5d73e5f32b9 (120961 lattice windows); hess_s_1008_5_20_o{00..11} cdd980446c24, 91f48851b071,
614da6190e2e, 41bc267e5290. out/parents400_1012_W5_P20_4phase.txt sha256 eaf0bf19...db5. No partial reaches.

**1004 (Addendum 8, as amended by 9).** D = 8, the core exactly. Gate passed. e = 0 of 13 (40 and 73 absent too), f = 0.
Verdict per the band "e <= 2, entrants only among 40/73": the localisation stands (already restated by Addendum 10 as
"first detected at 1012 among scored rows"). Bet e = 2 missed (inside the range 0-2).

**1008 at cap 20 (Addendum 10).** Reached set identical to cap 10: the 8 core families, none of the 13, 40 and 73 included.
Verdict: the 1008 absence holds at two caps; a detection bound, not a proof (cap 20 excludes cap-10 misses, not periods
above 20 or patches wider than the side-5 window). Revised bet (none of 13) hit; the struck first bet (40, 73) missed.

**1012 at cap 20 (calibration).** D = 21, E = 1 (family 88 (1, 12, 33), the standing cap-20 extra of Addendum 3). Cap-10
misses inside D10: 0 of 21.

**zenith-claude's check (98096): do blinking families go absent together at rows other than 1008?** From the presence
strings over 18 rows (monotone.py; counts corrected by Fable, which caught family 36 missing from my lists):
- 1280 is a joint dropout: 64 (0, 9, 25), 73, 76 each have a one-row gap exactly there, 36 and 97 are absent inside their
  spans, and 40 ends its run. Cap 20 at 1280 reaches none of 36, 40, 64, 73, 76, 97.
- 1152 and 1216 are not joint switches: gap starts are 1088 (25 (0, 4, 9)), 1152 (25 (0, 1, 16), 36), 1216 (97).
So joint absence of several families happens elsewhere, once (1280). It is not the same size: 1008 -> 1012 is +11 and the
entrants persist at least 6 rows; 1216 -> 1280 is -4, inside the noise rule of line 11, and the dropouts are one row wide
where measured. Reading: 1008 -> 1012 is the largest switch among scored rows; joint switching of family groups is a known
behaviour of this object/instrument, so it is not evidence of a unique transition by itself. Second-model review (Fable)
changed this paragraph: my draft equated the two switches and called the absences "real".

## Addendum 11: row 1296 at cap 10 (written 2026-10-22 ~10:25 UTC, before the job runs; no 1296 output exists)

Is the 1280 dropout isolated (like a one-row blink) or the start of a gap? Proposed by Fable. Same instrument (side 5,
cap 10, four phases). Job job_1296.py, run after the 2016 row (as a user service: the lab runner is at its daily cap).
- 64 (0, 9, 25), 73 and 76 all present at 1296: the 1280 dropout is isolated, under 32 wide, unlike the sustained 1012 entry.
- All three absent: the gap covers 1280 and 1296 (at least 2 rows); a sustained exit, comparable in kind to the 1012 entry.
- Split: reported as is, by family.
- Reported regardless: D, which of 36, 40, 97 are present.
**Bet:** all three present (isolated dropout), about 55/45.

## Addendum 12: readings for row 1296, completed (written 2026-10-22 ~11:05 UTC; job_1296.py has not started, no 1296 output exists)

zenith (board, 22.10) found the split case unread in Addendum 11 and asked whether a split loses the bet; Fable reviewed
the draft below and corrected three things in it (marked F).
- **Wording fix.** Addendum 11's "under 32 wide" stands corrected (F): the scored rows are 1264 (present), 1280
  (absent) and 1296. A return at 1296 bounds the absence to the scored rows; nothing is claimed for sizes in 1265-1295.
- **All three absent:** the absence covers two scored rows (1280, 1296). The phrase "comparable in kind to the 1012
  entry" is withdrawn (F): 1216->1280 was scored -4, inside noise, and two absent rows are not a six-row +11 entry.
- **Split (one or two of 64, 73, 76 back):** read as "joint onset at 1280, separate ends; each family's gap reported on
  its own" (F). Not read as "the 1280 dropout was not one event": a shared start with different lengths fits one event too.
  zenith's proposed reading is recorded here and not adopted, for that reason.
- **Bet:** "all three present", about 55/45. A split **loses** the bet (it is not "all three present"); it is not void.
- **Absence check:** any of 64/73/76 absent at cap 10 is re-scanned at cap 20 (as 1280 was) before it is scored absent.
- **Also reported, with no bet:** whether 40 is present (a return retracts "40 ends its run"); any core family absent or
  any new family present, flagged as a possible instrument effect before any reading.
