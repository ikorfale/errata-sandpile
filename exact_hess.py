"""exact_hess.py (#367): exact Hessians of periodic patches of the identity, no fitting.
If e is periodic with period p on a patch, then v(x+2p) - 2 v(x+p) + v(x) = p'Ap is CONSTANT there (L v = e, v = quadratic + periodic).
For each window: periods p (|p_i| <= PMAX) with e(x+p) == e(x) and that second difference constant on the window;
take the two shortest independent ones p, q, and p+q: three numbers give A11, A12, A22 exactly (rational).
Then (a, b, r) = (A11-A22, 2A12, A11+A22-2) mod 2 in (a,b) is tested against the band packing: on a circle (maximal), inside
one (stabilizable, not maximal), or neither. usage: python exact_hess.py N [W] [PMAX]"""
import sys, numpy as np
from fractions import Fraction as F
N = int(sys.argv[1]); W = int(sys.argv[2]) if len(sys.argv) > 2 else 24; PMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 10
z = np.load(f'out/odo_{N}.npz'); v = z['v']; e = z['e']
vecs = sorted({(i, j) for i in range(0, PMAX + 1) for j in range(-PMAX, PMAX + 1) if (i, j) > (0, 0)}, key=lambda p: p[0]**2 + p[1]**2)
def shift(arr, p, k, i0, j0):
    return arr[i0 + k * p[0]: i0 + k * p[0] + W, j0 + k * p[1]: j0 + k * p[1] + W]
rows = []
M = 2 * PMAX
for i0 in range(M, N - W - 2 * M, W // 2):
    for j0 in range(M, N - W - 2 * M, W // 2):
        per = []
        for p in vecs:
            if not (shift(e, p, 1, i0, j0) == shift(e, p, 0, i0, j0)).all(): continue
            d = shift(v, p, 2, i0, j0) - 2 * shift(v, p, 1, i0, j0) + shift(v, p, 0, i0, j0)
            if (d == d.flat[0]).all(): per.append((p, int(d.flat[0])))
        if len(per) < 2: continue
        p, dp = per[0]; q = dq = None
        for qq, dd in per[1:]:
            if p[0] * qq[1] - p[1] * qq[0] != 0: q, dq = qq, dd; break
        if q is None: continue
        s = (p[0] + q[0], p[1] + q[1])
        if s[0] < 0 or (s[0] == 0 and s[1] < 0): s = (-s[0], -s[1])
        ds = [dd for pp, dd in per if pp == s]
        if not ds: continue
        # p'Ap = dp, q'Aq = dq, s'As = dp + dq + 2 p'Aq  -> p'Aq
        pq = F(ds[0] - dp - dq, 2)
        P = np.array([[p[0]**2, 2 * p[0] * p[1], p[1]**2], [q[0]**2, 2 * q[0] * q[1], q[1]**2], [p[0] * q[0], p[0] * q[1] + p[1] * q[0], p[1] * q[1]]], dtype=object)
        rhs = [F(dp), F(dq), pq]
        # solve 3x3 exactly
        import sympy
        sol = sympy.Matrix(P.tolist()).LUsolve(sympy.Matrix(rhs))
        A11, A12, A22 = [F(int(x.p), int(x.q)) for x in sol]
        mean_e = F(int(shift(e, p, 0, i0, j0).sum()), W * W)
        rows.append((i0 + W // 2, j0 + W // 2, A11, A12, A22, p, q, float(mean_e)))
print(f"N={N} W={W}: windows with an exact period lattice: {len(rows)}")
import collections
cnt = collections.Counter((r[2], r[3], r[4]) for r in rows)
out = []
for (A11, A12, A22), n in cnt.most_common():
    a = (A11 - A22) % 2; b = (2 * A12) % 2; r = A11 + A22 - 2
    out.append((n, A11, A12, A22, a, b, r))
    print(f"  {n:4d} windows  A = [[{A11}, {A12}], [{A12}, {A22}]]   (a, b, r) = ({a}, {b}, {r})")
np.save(f'out/exact_hess_{N}.npy', np.array([(r[0], r[1], float(r[2]), float(r[3]), float(r[4])) for r in rows]))
# membership: is (a, b, r) exactly a band circle (centre, radius), or a point on a band line with r = 0?
src = open('apollo.py').read().split('print(f"band')[0].split('KMAX = 400')[1]
ns = {'np': np}; exec('KMAX = 400' + src, ns); Cb = ns['C']
print("membership in the band packing (circles r >= 1/400, lines x = 0, 2):")
for n, A11, A12, A22, a, b, r in out:
    if r == 0: on = a == 0 or a == 2; what = 'line point (degenerate, trace 2)'
    else:
        dist = np.min(np.abs(Cb[:, 0] - float(a)) + np.abs(Cb[:, 1] - float(b)) + np.abs(Cb[:, 2] - float(r))); on = dist < 1e-6; what = f'circle, |diff| {dist:.1e}'
    print(f"  ({a}, {b}, {r}) x{n}: {'ON' if on else 'NOT on'} the packing  [{what}]")
