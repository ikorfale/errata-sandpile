"""hess_stream.py (#406): hess_small.py in two streaming passes over the period vectors, so PMAX = 20 fits in the lab's
700 MB at N = 1024 and 2048 (hess_small keeps OK and D for every vector: 840 x 1022^2 x 3 B is 2.6 GB at 2048).
Pass 1: per window, the first OK vector p and the first OK vector q not parallel to p, in hess_small's scan order,
with their D. Pass 2: D at p+q (else p-q), exactly as hess_small picks it. Same rows, same .npy columns; the output
name carries _s so it never overwrites a hess_small file. Checked to reproduce hess_small at PMAX = 10 (see README).
usage: python hess_stream.py N W PMAX OI OJ"""
import sys, time, numpy as np
from fractions import Fraction as F
N, W, PMAX, OI, OJ = map(int, sys.argv[1:6])
z = np.load(f'out/odo_{N}.npz'); v = z['v']; e = z['e']; del z
vecs = sorted({(i, j) for i in range(0, PMAX + 1) for j in range(-PMAX, PMAX + 1) if (i, j) > (0, 0)}, key=lambda p: p[0]**2 + p[1]**2)
vidx = {p: k for k, p in enumerate(vecs)}
I0 = np.arange(OI, N - W + 1, W // 2); J0 = np.arange(OJ, N - W + 1, W // 2)
def sh(a, di, dj):
    out = np.zeros_like(a); ok = np.zeros(a.shape, bool)
    si = slice(max(0, -di), N - max(0, di)); sj = slice(max(0, -dj), N - max(0, dj))
    ti = slice(max(0, di), N - max(0, -di)); tj = slice(max(0, dj), N - max(0, -dj))
    out[si, sj] = a[ti, tj]; ok[si, sj] = True; return out, ok
def wsum(bad, h, w):
    S = np.zeros((N + 1, N + 1), np.int64); S[1:, 1:] = bad.astype(np.int64).cumsum(0).cumsum(1)
    a, b = I0[:, None], J0[None, :]
    return S[a + h, b + w] - S[a, b + w] - S[a + h, b] + S[a, b]
def okd(p):
    e1, o1 = sh(e, *p); v1, _ = sh(v, *p); em, om = sh(e, -p[0], -p[1]); vm, _ = sh(v, -p[0], -p[1])
    d = v1 - 2 * v + vm
    bad = ~(o1 & om) | (e1 != e) | (em != e)
    dh, _ = sh(d, 0, 1); dv, _ = sh(d, 1, 0)
    ok = (wsum(bad, W, W) == 0) & (wsum(dh != d, W, W - 1) == 0) & (wsum(dv != d, W - 1, W) == 0)
    return ok, d[I0[:, None], J0[None, :]].astype(np.int64)
t0 = time.time(); shp = (len(I0), len(J0))
P = np.full(shp, -1, np.int32); Q = np.full(shp, -1, np.int32); DP = np.zeros(shp, np.int64); DQ = np.zeros(shp, np.int64)
va = np.array(vecs)
for k, p in enumerate(vecs):
    ok, d = okd(p)
    newp = ok & (P < 0); P[newp] = k; DP[newp] = d[newp]
    pv = va[np.maximum(P, 0)]; cross = pv[..., 0] * p[1] - pv[..., 1] * p[0]
    newq = ok & (P >= 0) & ~newp & (Q < 0) & (cross != 0); Q[newq] = k; DQ[newq] = d[newq]
print(f"pass 1: {len(vecs)} vectors in {time.time() - t0:.0f}s; windows with p and q: {int((Q >= 0).sum())}", flush=True)
def norm(s): return s if (s[0] > 0 or (s[0] == 0 and s[1] > 0)) else (-s[0], -s[1])
# Pass 2 kept as window-shaped arrays, not dicts of tuples: at N = 2048 the dicts held ~1.2M Python tuples and the job
# died over 700 MB (sandpile-p20-2048, 21.10). SI[sg] = index of norm(p + sg q) in vecs, or -1; G/GOK = D there and ok.
SI = {}; G = {}; GOK = {}
for sg in (1, -1):
    SI[sg] = np.full(shp, -1, np.int32); G[sg] = np.zeros(shp, np.int64); GOK[sg] = np.zeros(shp, bool)
for a, b in zip(*np.nonzero(Q >= 0)):
    p, q = vecs[P[a, b]], vecs[Q[a, b]]
    for sg in (1, -1):
        s = norm((p[0] + sg * q[0], p[1] + sg * q[1]))
        if s in vidx: SI[sg][a, b] = vidx[s]
need = sorted((set(np.unique(SI[1]).tolist()) | set(np.unique(SI[-1]).tolist())) - {-1})
for k in need:
    ok, d = okd(vecs[k])
    for sg in (1, -1):
        m = (SI[sg] == k) & ok; G[sg][m] = d[m]; GOK[sg][m] = True
print(f"pass 2: {len(need)} vectors, total {time.time() - t0:.0f}s", flush=True)
def solve3(Pm, y):
    M = [[F(x) for x in r] for r in Pm]
    def det(m): return m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1]) - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0]) + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0])
    dd = det(M); out = []
    for c in range(3):
        Mc = [r[:] for r in M]
        for i in range(3): Mc[i][c] = y[i]
        out.append(det(Mc) / dd)
    return out
R = np.zeros((int((Q >= 0).sum()), 9)); n = 0  # preallocated: a list of 600k tuples was the other big heap at 2048
for a, b in zip(*np.nonzero(Q >= 0)):
    p, q = vecs[P[a, b]], vecs[Q[a, b]]; dp, dq = int(DP[a, b]), int(DQ[a, b]); pq = None
    for sg in (1, -1):
        if GOK[sg][a, b]: pq = sg * F(int(G[sg][a, b]) - dp - dq, 2); break
    if pq is None: continue
    Pm = [[p[0]**2, 2 * p[0] * p[1], p[1]**2], [q[0]**2, 2 * q[0] * q[1], q[1]**2], [p[0] * q[0], p[0] * q[1] + p[1] * q[0], p[1] * q[1]]]
    A11, A12, A22 = solve3(Pm, [F(dp), F(dq), pq])
    R[n] = (I0[a] + W // 2, J0[b] + W // 2, float(A11), float(A12), float(A22), *p, *q); n += 1
print(f"N={N} W={W} PMAX={PMAX} phase {OI}{OJ}: windows with an exact period lattice: {n}")
np.save(f'out/hess_s_{N}_{W}_{PMAX}_o{OI}{OJ}.npy', R[:n] if n else np.array([]))
