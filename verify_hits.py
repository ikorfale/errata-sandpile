"""#401 independent check of reached windows: for each sampled row, recompute centred second differences
v(x+p) - 2v(x) + v(x-p) over the 5x5 window for every p with |p_i| <= 10, keep those constant with e periodic,
and check that the row's A gives p'Ap for all of them (not just the three used to solve)."""
import sys, numpy as np, random
from fractions import Fraction as F
N = int(sys.argv[1]); R = np.load(f'out/hess_small_{N}_5_10_full.npy'); z = np.load(f'out/odo_{N}.npz'); v = z['v'].astype(np.int64); e = z['e']
want = {int(k) for k in sys.argv[2:]}
rows = [r for r in R if r[2] + r[4] - 2 > 1e-9 and round(1 / (r[2] + r[4] - 2)) in want]
random.seed(1); ok = bad = 0
for r in random.sample(rows, min(40, len(rows))):
    ci, cj = int(r[0]), int(r[1]); A = np.array([[r[2], r[3]], [r[3], r[4]]]); n = 0
    for i in range(0, 11):
        for j in range(-10, 11):
            if (i, j) <= (0, 0): continue
            ds = set(); per = True
            for x in range(ci - 2, ci + 3):
                for y in range(cj - 2, cj + 3):
                    xs = [(x + i, y + j), (x - i, y - j)]
                    if not all(0 <= a < N and 0 <= b < N for a, b in xs): per = False; break
                    if any(e[a, b] != e[x, y] for a, b in xs): per = False; break
                    ds.add(int(v[x + i, y + j] - 2 * v[x, y] + v[x - i, y - j]))
                if not per: break
            if per and len(ds) == 1:
                n += 1; pAp = A[0, 0] * i * i + 2 * A[0, 1] * i * j + A[1, 1] * j * j
                if abs(pAp - ds.pop()) > 1e-9: bad += 1; break
    else: ok += 1
print(f"N={N} curvatures {sorted(want)}: {len(rows)} windows, sampled {min(40, len(rows))}: consistent {ok}, contradicted {bad}")
