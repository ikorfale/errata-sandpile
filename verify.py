"""#439 (theone 98245, Fable checks 1-2), check 1: re-derive a random sample of scan rows from the identity itself.
For each MANIFEST row whose scan array is kept: draw K rows of out/hess_s_N_5_CAP_oXY.npy, and for each, straight from
out/odo_N.npz with plain per-window code (no shifted whole-grid arrays, no cumulative sums): (a) p is the first vector
in scan order that is OK on the 5x5 window (c +- p inside the grid for every cell, e equal at c, c+p, c-p, second
difference D constant over the window); (b) q is the first later OK vector not parallel to p; (c) D(p) = p^T A p,
D(q) = q^T A q exactly, with A solved exactly as in (d). Any mismatch is printed with the row.
(d) (theone 99970: D(p) and D(q) leave one direction of A free) the third vector s = norm(p+q) if it is in the scan's
vector list and OK on the window, else norm(p-q), as hess_stream picks it; D(s) = s^T A s; and A solved exactly from the
three re-derived D equals the stored floats bit for bit (no fraction recovery needed for this part). (e) mutation test:
each sampled row's A shifted along the null direction of the p and q equations (D(p), D(q) unchanged) must fail (d).
Exit status 1 if any mismatch or any mutant passes. Check 2 is verify2.py. Usage: python3 verify.py [K] [N ...]"""
import csv, sys, random
import numpy as np
from fractions import Fraction as F
K = int(sys.argv[1]) if len(sys.argv) > 1 else 20; ONLY = {int(a) for a in sys.argv[2:]}
rows = [r for r in csv.DictReader(open('out/MANIFEST.tsv'), delimiter='\t') if r['windows'] != '-' and (not ONLY or int(r['N']) in ONLY)]
W = 5; rng = random.Random(439); bad = 0; done = 0; cache = {}; mut_pass = 0; mut_done = 0
def norm(s): return s if (s[0] > 0 or (s[0] == 0 and s[1] > 0)) else (-s[0], -s[1])
def qf(A, s): return A[0] * s[0]**2 + 2 * A[1] * s[0] * s[1] + A[2] * s[1]**2
def det3(m): return m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1]) - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0]) + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0])
def solve3(M, y):
    d = det3(M); out = []
    for c in range(3):
        Mc = [r[:] for r in M]
        for i in range(3): Mc[i][c] = y[i]
        out.append(F(det3(Mc)) / d)
    return out
def row(s): return [s[0]**2, 2 * s[0] * s[1], s[1]**2]
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
        kp, dp = first_ok(v, e, N, x, y, vecs); p = vecs[kp] if kp is not None else None
        kq, dq = first_ok(v, e, N, x, y, vecs, kp + 1, p) if p else (None, None)
        want_p, want_q = (int(p0), int(p1)), (int(q0), int(q1))
        q = vecs[kq] if kq is not None else None
        s = ds = None
        if p and q:
            for sg in (1, -1):
                c = norm((p[0] + sg * q[0], p[1] + sg * q[1]))
                if c in vidx:
                    k3, d3 = first_ok(v, e, N, x, y, [c])
                    if k3 is not None: s, ds = c, d3; break
        ok = p == want_p and q == want_q and s is not None and (x - int(ph[1])) % (W // 2) == 0 and (y - int(ph[2])) % (W // 2) == 0
        if ok:  # A solved exactly from the three re-derived D (det = -cross^3, nonzero), against the stored floats bit for bit;
            # no fraction snapping (Fable 23.10: denominators divide 2 cross^3, up to 2*800^3, so a cap of 1000 can misread a correct row)
            Ax = solve3([row(p), row(q), row(s)], [F(dp), F(dq), F(ds)])
            ok = all(float(a) == float(b) for a, b in zip(Ax, (a11, a12, a22))) and dp == qf(Ax, p) and dq == qf(Ax, q) and ds == qf(Ax, s)
            # mutation (e): shift A along the null direction of the p and q equations; the s equation must reject it
            nd = [row(p)[1] * row(q)[2] - row(p)[2] * row(q)[1], row(p)[2] * row(q)[0] - row(p)[0] * row(q)[2], row(p)[0] * row(q)[1] - row(p)[1] * row(q)[0]]
            Am = [a + F(1, 7) * n_ for a, n_ in zip(Ax, nd)]; mut_done += 1
            assert qf(Am, p) == dp and qf(Am, q) == dq
            if ds == qf(Am, s): mut_pass += 1; print(f'MUTANT PASSED N={N} cap={cap} {ph} row {t}: p={p} q={q} s={s}')
        done += 1
        if not ok: bad += 1; print(f'MISMATCH N={N} cap={cap} {ph} row {t}: scan p={want_p} q={want_q} A={a11},{a12},{a22}; re-derived p={p} q={q} s={s} D(p)={dp} D(q)={dq} D(s)={ds}')
    print(f'N={N} cap={cap} {ph}: {min(K, n)} of {n} rows re-derived, mismatches so far {bad}', flush=True)
print(f'total: {done} rows re-derived from the identity, {bad} mismatches; mutants {mut_done}, passed {mut_pass}')
sys.exit(1 if bad or mut_pass else 0)
