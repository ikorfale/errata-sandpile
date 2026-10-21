"""Fable review 21.10 of the 1024 spike: 'reached' is 99 brittle indicators. Same matching as reach81.py, but counts
windows per band circle (support) and prints reach at support >= 1, 4, 8, 16, plus >= 8*(N/1024)^2 (area-scaled).
usage: python reach_support.py N [K]  (reads the four W5 phase files of N)"""
import sys, collections, numpy as np
src = open('apollo.py').read().split('print(f"band')[0].split('KMAX = 400')[1]
ns = {'np': np}; exec('KMAX = 400' + src, ns); C = ns['C']
N = int(sys.argv[1]); K = int(sys.argv[2]) if len(sys.argv) > 2 else 81
circ = {(round(c[0], 6), round(c[1] % 2, 6), round(c[2], 6)) for c in C if c[2] > 0 and 1 / c[2] <= K + 0.5}
files = [f'out/hess_small_{N}_5_10_full.npy'] + [f'out/hess_small_{N}_5_10_full_o{p}.npy' for p in ('01', '10', '11')]
sup = collections.Counter()
for f in files:
    for r in np.load(f):
        rr = r[2] + r[4] - 2
        if rr <= 1e-9: continue
        key = (round((r[2] - r[4]) % 2, 6), round((2 * r[3]) % 2, 6), round(rr, 6))
        if key in circ: sup[key] += 1
area = 8 * (N / 1024) ** 2
row = {t: sum(1 for k in sup if sup[k] >= t) for t in (1, 4, 8, 16)}
print(f"N={N} circles {len(circ)} reach>=1 {row[1]} >=4 {row[4]} >=8 {row[8]} >=16 {row[16]} >=8(N/1024)^2={area:.1f} {sum(1 for k in sup if sup[k] >= area)}")
if len(sys.argv) > 3:  # per-curvature support (min..max over that curvature's reached circles)
    byk = collections.defaultdict(list)
    for k, s in sup.items(): byk[round(1 / k[2])].append(s)
    print(' '.join(f"{c}:{len(v)}/{min(v)}-{max(v)}" for c, v in sorted(byk.items())))
