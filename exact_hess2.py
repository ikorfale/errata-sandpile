"""exact_hess2.py (#391): exact_hess.py vectorised per period vector (integral images), same windows, same rule,
so PMAX can reach 40 on N = 1024. Prints the same table; checked to reproduce exact_hess_512.txt at W=12, PMAX=10.
usage: python exact_hess2.py N [W] [PMAX] [full]
'full': windows over the whole grid (out-of-grid shifts are rejected per cell), instead of exact_hess.py's
margins M = 2 PMAX below and 2M above, which at PMAX = 40 drop most of the grid."""
import sys, time, collections, numpy as np
from fractions import Fraction as F
import sympy
N = int(sys.argv[1]); W = int(sys.argv[2]) if len(sys.argv) > 2 else 24; PMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 10
z = np.load(f'out/odo_{N}.npz'); v = z['v']; e = z['e']
vecs = sorted({(i, j) for i in range(0, PMAX + 1) for j in range(-PMAX, PMAX + 1) if (i, j) > (0, 0)}, key=lambda p: p[0]**2 + p[1]**2)
FULL = len(sys.argv) > 4 and sys.argv[4] == 'full'
M = 2 * PMAX
I0 = np.arange(0, N - W + 1, W // 2) if FULL else np.arange(M, N - W - 2 * M, W // 2); J0 = I0.copy()
def sh(a, di, dj):  # a(x + (di, dj)) on the full grid, out of bounds -> None mask
    out = np.zeros_like(a); ok = np.zeros(a.shape, bool)
    si = slice(max(0, -di), N - max(0, di)); sj = slice(max(0, -dj), N - max(0, dj))
    ti = slice(max(0, di), N - max(0, -di)); tj = slice(max(0, dj), N - max(0, -dj))
    out[si, sj] = a[ti, tj]; ok[si, sj] = True; return out, ok
def wsum(bad, h, w):  # number of bad cells in [i0, i0+h) x [j0, j0+w) for all windows
    S = np.zeros((N + 1, N + 1), np.int64); S[1:, 1:] = bad.astype(np.int64).cumsum(0).cumsum(1)
    a, b = I0[:, None], J0[None, :]
    return S[a + h, b + w] - S[a, b + w] - S[a + h, b] + S[a, b]
t0 = time.time()
OK = np.zeros((len(vecs), len(I0), len(J0)), bool); D = np.zeros((len(vecs), len(I0), len(J0)), np.int16)  # p'Ap where OK; int16 keeps N = 1024 under the lab's 700 MB
for k, p in enumerate(vecs):
    e1, o1 = sh(e, *p); v1, _ = sh(v, *p); v2, o2 = sh(v, 2 * p[0], 2 * p[1])
    d = v2 - 2 * v1 + v
    bad = ~(o1 & o2) | (e1 != e)
    dh, _ = sh(d, 0, 1); dv, _ = sh(d, 1, 0)
    OK[k] = (wsum(bad, W, W) == 0) & (wsum(dh != d, W, W - 1) == 0) & (wsum(dv != d, W - 1, W) == 0)
    dk = np.where(OK[k], d[I0[:, None], J0[None, :]], 0)
    assert np.abs(dk).max() < 32767, (p, int(np.abs(dk).max()))
    D[k] = dk
print(f"N={N} W={W} PMAX={PMAX} full={FULL}: {len(vecs)} vectors scanned in {time.time() - t0:.0f}s", flush=True)
rows = []
for a in range(len(I0)):
    for b in range(len(J0)):
        ks = np.flatnonzero(OK[:, a, b])
        if len(ks) < 2: continue
        per = [(vecs[k], int(D[k, a, b])) for k in ks]
        p, dp = per[0]; q = None
        for qq, dd in per[1:]:
            if p[0] * qq[1] - p[1] * qq[0] != 0: q, dq = qq, dd; break
        if q is None: continue
        s = (p[0] + q[0], p[1] + q[1])
        if s[0] < 0 or (s[0] == 0 and s[1] < 0): s = (-s[0], -s[1])
        ds = [dd for pp, dd in per if pp == s]
        if not ds: continue
        pq = F(ds[0] - dp - dq, 2)
        P = [[p[0]**2, 2 * p[0] * p[1], p[1]**2], [q[0]**2, 2 * q[0] * q[1], q[1]**2], [p[0] * q[0], p[0] * q[1] + p[1] * q[0], p[1] * q[1]]]
        sol = sympy.Matrix(P).LUsolve(sympy.Matrix([F(dp), F(dq), pq]))
        A11, A12, A22 = [F(int(x.p), int(x.q)) for x in sol]
        rows.append((I0[a] + W // 2, J0[b] + W // 2, A11, A12, A22, p, q))
print(f"N={N} W={W}: windows with an exact period lattice: {len(rows)}")
cnt = collections.Counter((r[2], r[3], r[4]) for r in rows)
out = []
for (A11, A12, A22), n in cnt.most_common():
    a = (A11 - A22) % 2; b = (2 * A12) % 2; r = A11 + A22 - 2
    out.append((n, A11, A12, A22, a, b, r))
    print(f"  {n:4d} windows  A = [[{A11}, {A12}], [{A12}, {A22}]]   (a, b, r) = ({a}, {b}, {r})")
np.save(f'out/exact_hess2_{N}_{W}_{PMAX}{"_full" if FULL else ""}.npy', np.array([(r[0], r[1], float(r[2]), float(r[3]), float(r[4]), *r[5], *r[6]) for r in rows]))
src = open('apollo.py').read().split('print(f"band')[0].split('KMAX = 400')[1]
ns = {'np': np}; exec('KMAX = 400' + src, ns); Cb = ns['C']
print("membership in the band packing (circles r >= 1/400, lines x = 0, 2):")
for n, A11, A12, A22, a, b, r in out:
    if r == 0: on = a == 0 or a == 2; what = 'line point (degenerate, trace 2)'
    else:
        dist = np.min(np.abs(Cb[:, 0] - float(a)) + np.abs(Cb[:, 1] - float(b)) + np.abs(Cb[:, 2] - float(r))); on = dist < 1e-6; what = f'circle, |diff| {dist:.1e}'
    print(f"  ({a}, {b}, {r}) x{n}: {'ON' if on else 'NOT on'} the packing  [{what}]")
