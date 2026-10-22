"""#442 (zenith 98484): direct search of an identity for chosen band families, independent of hess_stream's scan order.
From a reference row N_REF take every window that hess_stream mapped to curvature K: its period vectors p, q and its
exact D values at p, q, p+q. In the target identity, test exactly those vectors in every 5x5 window (step 1) and count
windows where all three are periods with the same D (= the same Hessian, i.e. the same family). Found > 0 at a row the
scan called absent = the scan under-reports; 0 = absent on this instrument too. usage: direct442.py N_REF[,N_REF2...] N K [K ...]"""
import sys, numpy as np
NREFS, N = [int(x) for x in sys.argv[1].split(',')], int(sys.argv[2]); KS = [int(k) for k in sys.argv[3:]]; W = 5
src = open('parents81.py').read().split('fam = collections.Counter()')[0].replace('want = {int(k) for k in sys.argv[2:]}', 'want = set()')
ns = {'__name__': 'x'}; exec(src, ns); circ = ns['circ']
def key(r):
    rr = r[2] + r[4] - 2
    return None if rr <= 1e-9 else (round((r[2] - r[4]) % 2, 6), round((2 * r[3]) % 2, 6), round(rr, 6))
ref = {}
for NREF, ph in ((a, b) for a in NREFS for b in ('00', '01', '10', '11')):
    for r in np.load(f'out/hess_s_{NREF}_5_20_o{ph}.npy'):
        k = key(r)
        if k in circ and round(1 / k[2]) in KS:
            p = (int(r[5]), int(r[6])); q = (int(r[7]), int(r[8])); A = (r[2], r[3], r[4])
            D = lambda v: round(A[0] * v[0]**2 + 2 * A[1] * v[0] * v[1] + A[2] * v[1]**2)
            s = (p[0] + q[0], p[1] + q[1]); m = (p[0] - q[0], p[1] - q[1])
            ref.setdefault((round(1 / k[2]), k), {}).setdefault((p, q), set()).add((D(p), D(q), s, D(s), m, D(m)))
z = np.load(f'out/odo_{N}.npz'); v = z['v']; e = z['e']; del z
I0 = np.arange(0, N - W + 1); J0 = np.arange(0, N - W + 1)
def sh(a, di, dj):
    out = np.zeros_like(a); ok = np.zeros(a.shape, bool)
    si = slice(max(0, -di), N - max(0, di)); sj = slice(max(0, -dj), N - max(0, dj))
    ti = slice(max(0, di), N - max(0, -di)); tj = slice(max(0, dj), N - max(0, -dj))
    out[si, sj] = a[ti, tj]; ok[si, sj] = True; return out, ok
def wsum(bad, h, w):
    S = np.zeros((N + 1, N + 1), np.int64); S[1:, 1:] = bad.astype(np.int64).cumsum(0).cumsum(1)
    a, b = I0[:, None], J0[None, :]
    return S[a + h, b + w] - S[a, b + w] - S[a + h, b] + S[a, b]
cache = {}
def okd(p):
    if p not in cache:
        e1, o1 = sh(e, *p); v1, _ = sh(v, *p); em, om = sh(e, -p[0], -p[1]); vm, _ = sh(v, -p[0], -p[1])
        d = v1 - 2 * v + vm
        bad = ~(o1 & om) | (e1 != e) | (em != e)
        dh, _ = sh(d, 0, 1); dv, _ = sh(d, 1, 0)
        ok = (wsum(bad, W, W) == 0) & (wsum(dh != d, W, W - 1) == 0) & (wsum(dv != d, W - 1, W) == 0)
        if len(cache) >= 4: cache.clear()   # each entry is ~15 MB at N=1280; an unbounded cache was OOM-killed at 900 MB
        cache[p] = (ok, d[I0[:, None], J0[None, :]].astype(np.int32))
    return cache[p]
# Same family = same Hessian up to the harmonic integer quadratics the circle key quotients out (Fable 22.10): adding
# m*(x1^2-x2^2)/2-ish or n*x1*x2 terms shifts D(v) by m*(v1^2-v2^2) + n*2*v1*v2 with integer m, n and keeps e and the lattice.
def same_class(Dv, dv, vecs3):
    (a1, a2, a3), (b1, b2, b3) = [[v[0]**2 - v[1]**2 for v in vecs3], [2 * v[0] * v[1] for v in vecs3]]
    d1, d2, d3 = (x - y for x, y in zip(Dv, dv)); det = a1 * b2 - a2 * b1
    if det == 0: return np.zeros(d1.shape, bool)
    mn, nn = d1 * b2 - d2 * b1, a1 * d2 - a2 * d1
    ok = (mn % det == 0) & (nn % det == 0)
    return ok & ((mn // det) * a3 + (nn // det) * b3 == d3)
for K in sorted({K for K, _ in ref}):
    hit = 0; npair = 0
    for (K2, k), combos in ref.items():
        if K2 != K: continue
        for (p, q), vals in combos.items():
            npair += 1
            (op, Dp), (oq, Dq) = okd(p), okd(q)
            for (dp, dq, s, ds, m, dm) in vals:
                found = np.zeros(op.shape, bool)
                for w, dw in ((s, ds), (m, dm)):
                    ow, Dw = okd(w); found |= op & oq & ow & same_class((Dp, Dq, Dw), (dp, dq, dw), (p, q, w))
                hit += int(found.sum())
    print(f"N={N} ref {sys.argv[1]} curvature {K}: {npair} (p,q) pairs over its circles; windows in the Hessian class {hit}", flush=True)
