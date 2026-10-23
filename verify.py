"""#439 (theone 98245, Fable checks 1-2), check 1: re-derive a random sample of scan rows from the identity itself.
For each MANIFEST row whose scan array is kept: draw K rows of out/hess_s_N_5_CAP_oXY.npy, and for each, straight from
out/odo_N.npz with plain per-window code (no shifted whole-grid arrays, no cumulative sums): (a) p is the first vector
in scan order that is OK on the 5x5 window (c +- p inside the grid for every cell, e equal at c, c+p, c-p, second
difference D constant over the window); (b) q is the first later OK vector not parallel to p; (c) D(p) = p^T A p,
D(q) = q^T A q exactly (A from the row, recovered as the nearest fraction with denominator <= 1000). Any mismatch is printed with the row.
Check 2 (reached sets from the scan arrays) is not here yet. Usage: python3 verify.py [K] [N ...]"""
import csv, sys, random
import numpy as np
from fractions import Fraction as F
K = int(sys.argv[1]) if len(sys.argv) > 1 else 20; ONLY = {int(a) for a in sys.argv[2:]}
rows = [r for r in csv.DictReader(open('out/MANIFEST.tsv'), delimiter='\t') if r['windows'] != '-' and (not ONLY or int(r['N']) in ONLY)]
W = 5; rng = random.Random(439); bad = 0; done = 0; cache = {}
def first_ok(v, e, N, x, y, vecs, start=0, p=None):
    for k in range(start, len(vecs)):
        s = vecs[k]
        if p is not None and p[0] * s[1] - p[1] * s[0] == 0: continue
        d0 = None; ok = True
        for i in range(x, x + W):
            for j in range(y, y + W):
                a, b, c, dd = i + s[0], j + s[1], i - s[0], j - s[1]
                if not (0 <= a < N and 0 <= b < N and 0 <= c < N and 0 <= dd < N) or e[a, b] != e[i, j] or e[c, dd] != e[i, j]: ok = False; break
                D = int(v[a, b]) - 2 * int(v[i, j]) + int(v[c, dd])
                if d0 is None: d0 = D
                elif D != d0: ok = False; break
            if not ok: break
        if ok: return k, d0
    return None, None
for r in rows:
    N, cap, ph = int(r['N']), int(r['cap']), r['phase']
    if N not in cache: z = np.load(f'out/odo_{N}.npz'); cache.clear(); cache[N] = (z['v'], z['e'])
    v, e = cache[N]
    vecs = sorted({(i, j) for i in range(0, cap + 1) for j in range(-cap, cap + 1) if (i, j) > (0, 0)}, key=lambda p: p[0]**2 + p[1]**2)
    vidx = {p: k for k, p in enumerate(vecs)}
    S = np.load(f'out/hess_s_{N}_5_{cap}_{ph}.npy', mmap_mode='r'); n = S.shape[0]
    for t in rng.sample(range(n), min(K, n)):
        ci, cj, a11, a12, a22, p0, p1, q0, q1 = S[t]; x, y = int(ci) - W // 2, int(cj) - W // 2
        A = [F(float(a)).limit_denominator(1000) for a in (a11, a12, a22)]  # stored as float from an exact Fraction (1/4, 1/9, 5/3 seen); a cap of 2 broke 1/4 (23.10)
        kp, dp = first_ok(v, e, N, x, y, vecs); p = vecs[kp] if kp is not None else None
        kq, dq = first_ok(v, e, N, x, y, vecs, kp + 1, p) if p else (None, None)
        want_p, want_q = (int(p0), int(p1)), (int(q0), int(q1))
        q = vecs[kq] if kq is not None else None
        ok = p == want_p and q == want_q and dp == A[0] * p[0]**2 + 2 * A[1] * p[0] * p[1] + A[2] * p[1]**2 and dq == A[0] * q[0]**2 + 2 * A[1] * q[0] * q[1] + A[2] * q[1]**2
        done += 1
        if not ok: bad += 1; print(f'MISMATCH N={N} cap={cap} {ph} row {t}: scan p={want_p} q={want_q} A={a11},{a12},{a22}; re-derived p={p} q={q} D(p)={dp} D(q)={dq}')
    print(f'N={N} cap={cap} {ph}: {min(K, n)} of {n} rows re-derived, mismatches so far {bad}', flush=True)
print(f'total: {done} rows re-derived from the identity, {bad} mismatches')
