"""zenith 98560: are the half-orbit W=3 hits chance? At each hit and at its transpose, list every OK period vector of the
3x3 window and solve the Hessian from EVERY non-parallel pair (p, q) with p+q or p-q also OK, instead of hess_stream's
first-p, first-q choice (whose equal-norm tie order is not transpose-equivariant). Prints the classes found."""
import sys, numpy as np
from fractions import Fraction as F
N = int(sys.argv[1]); Ks = set(map(int, sys.argv[2:]))
src = open('parents81.py').read().split('fam = collections.Counter()')[0].replace('want = {int(k) for k in sys.argv[2:]}', 'want = set()')
ns = {'__name__': 'x'}; sv = sys.argv; sys.argv = sv[:1]; exec(src, ns); sys.argv = sv; circ = ns['circ']
z = np.load(f'out/odo_{N}.npz'); v = z['v'].astype(np.int64); e = z['e']; W = int(__import__("os").environ.get("WW", 3)); PMAX = 20
vecs = sorted({(i, j) for i in range(0, PMAX + 1) for j in range(-PMAX, PMAX + 1) if (i, j) > (0, 0)}, key=lambda p: p[0]**2 + p[1]**2)
def okd(a, b, p):
    ds = set()
    for x in range(a, a + W):
        for y in range(b, b + W):
            xp, yp, xm, ym = x + p[0], y + p[1], x - p[0], y - p[1]
            if not (0 <= min(xp, yp, xm, ym) and max(xp, yp, xm, ym) < N): return None
            if e[xp, yp] != e[x, y] or e[xm, ym] != e[x, y]: return None
            ds.add(int(v[xp, yp] - 2 * v[x, y] + v[xm, ym]))
    return ds.pop() if len(ds) == 1 else None
def key(A): return (round((A[0] - A[2]) % 2, 6) % 2, round((2 * A[1]) % 2, 6) % 2, round(A[0] + A[2] - 2, 6))
# regression (theone 98945): two representatives differing by the integer-harmonic shift diag(1,-1) are one class
assert key((1.5, 0, 1.5)) == key((2.5, 0, 0.5)) == (0.0, 0.0, 1.0)
def norm(s): return s if (s[0] > 0 or (s[0] == 0 and s[1] > 0)) else (-s[0], -s[1])
def classes(c):
    # theone 98945: dedupe by class (curvature, canonical key k), keep raw Hessian representatives separately
    a, b = c[0] - W // 2, c[1] - W // 2; D = {p: d for p in vecs if (d := okd(a, b, p)) is not None}; out = {}
    for p in D:
        for q in D:
            if p >= q or p[0] * q[1] - p[1] * q[0] == 0: continue
            for sg in (1, -1):
                s = norm((p[0] + sg * q[0], p[1] + sg * q[1]))
                if s not in D: continue
                pq = sg * F(D[s] - D[p] - D[q], 2)
                M = np.array([[p[0]**2, 2*p[0]*p[1], p[1]**2], [q[0]**2, 2*q[0]*q[1], q[1]**2], [p[0]*q[0], p[0]*q[1]+p[1]*q[0], p[1]*q[1]]], float)
                A = np.linalg.solve(M, [D[p], D[q], float(pq)]); s2 = A[0] + A[2] - 2
                k = key(A)
                # class identity at 4 decimals: the 6-decimal key splits one class when float noise straddles a rounding edge
                # (0.5078125 -> 0.507812 / 0.507813 at 1248 K=73, found in the recount); circle membership keeps the 6-decimal key
                out.setdefault((round(1 / s2) if s2 > 1e-9 else 0, k in circ, tuple(round(x + 1e-9, 4) for x in k)), set()).add(tuple(float(x) for x in np.round(A, 4)))
    return len(D), out
R = np.concatenate([np.load(f'out/hess_s_{N}_{W}_20_o{ph}.npy') for ph in ((('00','01','10','11')) if W == 5 else ('00',))])
for r in R:
    s = r[2] + r[4] - 2
    if s <= 1e-9: continue
    k = (round((r[2] - r[4]) % 2, 6), round((2 * r[3]) % 2, 6), round(s, 6))
    if not (k in circ and round(1 / s) in Ks): continue
    c = (int(r[0]), int(r[1])); t = (c[1], c[0])
    h, tr = classes(c)[1], classes(t)[1]
    fmt = lambda o: sorted((K_, on, len(r)) for (K_, on, _), r in o.items())
    print(f"N={N} K={round(1/s)} hit {c} classes {len(h)} reps {sum(map(len, h.values()))} (K, on circle, reps) {fmt(h)} | transpose {t} classes {len(tr)} {fmt(tr)}", flush=True)
