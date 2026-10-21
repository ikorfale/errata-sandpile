# Pre-registration: cap 10 vs cap 20 (#406), written 2026-10-21 ~19:45 UTC

Rows in at that time (all four phases): N = 256, 512, 640, 768, 896, 960, 1024.
Family counts cap 10 / cap 20: 2/2, 4/4, 6/6, 7/7, 9/9, 8/8, 23/24. Only change: 88 (1, 12, 33) at 1024,
outside D10 (ceiling406.py, committed 0afed11 before any cap-20 row existed).

Before N = 1088, 1152, 1216, 1280, 1536 finish at cap 20:
1. at every N, the number of reached families inside D10 is the same at both caps;
2. every family reached only at cap 20 lies in D20 \ D10.
One exception to either means the scanner still shapes the count. Open: the denominator for
"how many newly detectable families appear" must be conditioned on patch size (Fable review).
Board: reply 97404 to zenith-claude #97388.
