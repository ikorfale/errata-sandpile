"""#445 (zenith 98600/98612): an equivariant W=5 instrument. hess_stream takes the first OK p and the first OK q not
parallel to p (equal-norm ties in a fixed order, not transpose-equivariant) and drops the window if p+q and p-q both fail.
Here every window keeps ALL its OK period vectors (same okd test as hess_stream), the Hessian is solved exactly from EVERY
non-parallel pair (p, q) with p+q or p-q also OK, and the window's classes are the set of distinct exact class keys
(as in transpose444.add). Multiplicity m = number of classes; a family hit is a window with m == 1.
Windows with identical (vector, D) signatures share one solve. All 4 phases at step W//2 = every window position.
usage: python allpairs445.py N [W] [PMAX]   -> results/allpairs445_N.txt (per-family counts, old vs new) + out/ap445_N.npz"""
import sys, time, collections, numpy as np
from fractions import Fraction as F
N = int(sys.argv[1]); W = int(sys.argv[2]) if len(sys.argv) > 2 else 5; PMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 20
src = open('parents81.py').read().split('fam = collections.Counter()')[0].replace('want = {int(k) for k in sys.argv[2:]}', 'want = set()')
ns = {'__name__': 'x'}; sv = sys.argv; sys.argv = sv[:1]; exec(src, ns); sys.argv = sv; circ = ns['circ']
z = np.load(f'out/odo_{N}.npz'); v = z['v'].astype(np.int64); e = z['e']; del z
vecs = sorted({(i, j) for i in range(0, PMAX + 1) for j in range(-PMAX, PMAX + 1) if (i, j) > (0, 0)}, key=lambda p: p[0]**2 + p[1]**2)
vidx = {p: k for k, p in enumerate(vecs)}
def norm(s): return s if (s[0] > 0 or (s[0] == 0 and s[1] > 0)) else (-s[0], -s[1])
def key(A): return (round((A[0] - A[2]) % 2, 6) % 2, round((2 * A[1]) % 2, 6) % 2, round(A[0] + A[2] - 2, 6))
def solve3(M, b):
    det = lambda m: (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1]) - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
                     + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
    d = F(det(M)); return [F(det([[b[r] if c == j else M[r][c] for c in range(3)] for r in range(3)])) / d for j in range(3)]
def cls(A):  # exact class key (transpose444.add) + family label: K if on a band circle, else None
    s2 = A[0] + A[2] - 2; kx = ((A[0] - A[2]) % 2, (2 * A[1]) % 2, s2)
    fk = key([float(x) for x in A]); K = round(1 / s2) if s2 > 0 and fk in circ else None
    return kx, K, fk
# regression: the diag(1,-1) shift (theone 98945) gives one class
assert cls((F(3, 2), F(0), F(3, 2)))[0] == cls((F(5, 2), F(0), F(1, 2)))[0]
def sig_classes(sig):
    D = dict(sig); out = {}
    for p in D:
        for q in D:
            if p >= q or p[0] * q[1] - p[1] * q[0] == 0: continue
            for sg in (1, -1):
                s = norm((p[0] + sg * q[0], p[1] + sg * q[1]))
                if s not in D: continue
                M = [[p[0]**2, 2*p[0]*p[1], p[1]**2], [q[0]**2, 2*q[0]*q[1], q[1]**2], [p[0]*q[0], p[0]*q[1]+p[1]*q[0], p[1]*q[1]]]
                kx, K, fk = cls(solve3(M, [F(D[p]), F(D[q]), sg * F(D[s] - D[p] - D[q], 2)]))
                out[kx] = (K, fk)
    return out
def sh(a, di, dj):
    out = np.zeros_like(a); ok = np.zeros(a.shape, bool)
    si = slice(max(0, -di), N - max(0, di)); sj = slice(max(0, -dj), N - max(0, dj))
    ti = slice(max(0, di), N - max(0, -di)); tj = slice(max(0, dj), N - max(0, -dj))
    out[si, sj] = a[ti, tj]; ok[si, sj] = True; return out, ok
PRE = int(__import__('os').environ.get('PRE', 12))  # prefix size before shell completion
NRM = np.array([p[0]**2 + p[1]**2 for p in vecs]); va = np.array(vecs)
CR = va[:, None, 0] * va[None, :, 1] - va[:, None, 1] * va[None, :, 0]
SUM = {sg: np.array([[vidx.get(norm((p[0] + sg * q[0], p[1] + sg * q[1])), -1) for q in vecs] for p in vecs], np.int32) for sg in (1, -1)}
def sig_classes2(sig):
    out = {}
    for i, j, sg, dp, dq, ds in sig:
        p, q = vecs[i], vecs[j]
        M = [[p[0]**2, 2*p[0]*p[1], p[1]**2], [q[0]**2, 2*q[0]*q[1], q[1]**2], [p[0]*q[0], p[0]*q[1]+p[1]*q[0], p[1]*q[1]]]
        A = solve3(M, [F(dp), F(dq), sg * F(ds - dp - dq, 2)]); kx, K, fk = cls(A)
        out[kx] = (K, fk, A)
    return out
def full_ok(A, okk, x, y):
    # Fable 23.10: m == 1 on the prefix is made rigorous for ALL OK vectors if D(p) == p^T A p exactly for every one of
    # them (then every triple solves to this A). False only says 'not verified', not m > 1.
    L = 1
    for a in A: L = L * a.denominator // __import__('math').gcd(L, a.denominator)
    a, b, c = (int(t * L) for t in A); px, py = va[okk, 0], va[okk, 1]
    D = v[x + px, y + py] - 2 * v[x, y] + v[x - px, y - py]
    return bool(np.all(L * D == a * px * px + 2 * b * px * py + c * py * py))
t0 = time.time(); memo = {}
rows = []  # (ci, cj, m, K or -1 when m != 1, full-set verified) for family windows (m == 1) and all m > 1 windows
fams_new = collections.defaultdict(lambda: [0, set()]); fams_res = collections.Counter(); mult = collections.Counter(); fullv = collections.Counter(); fams_full = collections.Counter(); fams_vset = collections.defaultdict(set)
for OI, OJ in ((0, 0), (0, 1), (1, 0), (1, 1)):
    I0 = np.arange(OI, N - W + 1, W // 2); J0 = np.arange(OJ, N - W + 1, W // 2); shp = (len(I0), len(J0))
    def wsum(bad, h, w):
        S = np.zeros((N + 1, N + 1), np.int64); S[1:, 1:] = bad.astype(np.int64).cumsum(0).cumsum(1)
        a, b = I0[:, None], J0[None, :]
        return S[a + h, b + w] - S[a, b + w] - S[a + h, b] + S[a, b]
    # 840 OK vectors per window is common (probe 23.10: 105M (window, vector) entries per phase at 1216, median 379 per
    # window), so keep only a packed OK bitmask per window and read D from v on demand
    BM = np.zeros(shp + ((len(vecs) + 7) // 8,), np.uint8)
    for k, p in enumerate(vecs):
        e1, o1 = sh(e, *p); v1, _ = sh(v, *p); em, om = sh(e, -p[0], -p[1]); vm, _ = sh(v, -p[0], -p[1])
        d = v1 - 2 * v + vm; bad = ~(o1 & om) | (e1 != e) | (em != e); del e1, em, v1, vm, o1, om
        dh, _ = sh(d, 0, 1); dv, _ = sh(d, 1, 0)
        ok = (wsum(bad, W, W) == 0) & (wsum(dh != d, W, W - 1) == 0) & (wsum(dv != d, W - 1, W) == 0)
        BM[..., k // 8] |= (ok.astype(np.uint8) << (7 - k % 8))
    print(f"phase {OI}{OJ}: bitmask done {time.time() - t0:.0f}s", flush=True)
    for a, b in zip(*np.nonzero(BM.any(-1))):
        okk = np.flatnonzero(np.unpackbits(BM[a, b])[:len(vecs)])
        if len(okk) < 3: continue
        # equivariant prefix: the smallest OK vectors, cut only at a whole norm shell (D4 maps shells to shells)
        n2 = NRM[okk]; cut = len(okk) if len(okk) <= PRE else int(np.searchsorted(n2, n2[PRE - 1], 'right'))
        pre = okk[:cut]; oks = set(okk.tolist()); x, y = int(I0[a]), int(J0[b])
        Dv = lambda k: int(v[x + vecs[k][0], y + vecs[k][1]] - 2 * v[x, y] + v[x - vecs[k][0], y - vecs[k][1]])
        sig = []
        for i in pre:
            for j in pre:
                if i >= j or CR[i, j] == 0: continue
                for sg in (1, -1):
                    sk = SUM[sg][i, j]
                    if sk >= 0 and sk in oks: sig.append((int(i), int(j), sg, Dv(i), Dv(j), Dv(sk)))
        if not sig: continue
        hs = hash(tuple(sig)); c = memo.get(hs)  # key by hash: 1216 died at 700 MB holding full signatures (23.10)
        if c is None: c = memo[hs] = sig_classes2(sig)
        ci, cj = x + W // 2, y + W // 2; m = len(c); mult[m] += 1
        if m == 1:
            K, fk, A = next(iter(c.values())); fv = full_ok(A, okk, x, y); fullv[fv] += 1
            if K is not None: fams_new[K][0] += 1; fams_new[K][1].add(fk); fams_full[K] += fv
            if K is not None and fv: fams_vset[K].add(fk)  # zenith 99841: seen set from verified windows only
            if K is not None: rows.append((ci, cj, 1, K, fv))  # only family windows are kept (memory)
        else:
            for K in {t[0] for t in c.values()} - {None}: fams_res[K] += 1
            rows.append((ci, cj, m, -1, 0))
    print(f"phase {OI}{OJ}: {len(memo)} distinct signatures so far, {time.time() - t0:.0f}s", flush=True)
# old instrument (hess_stream rows), same family keying as w3check
fams_old = collections.defaultdict(lambda: [0, set()]); old_hits = []
for ph in ('00', '01', '10', '11'):
    for r in np.load(f'out/hess_s_{N}_{W}_{PMAX}_o{ph}.npy'):
        s = r[2] + r[4] - 2
        if s <= 1e-9: continue
        k = key(r[2:5])  # same keying as the new path (Fable: the w3check key lacks the trailing % 2)
        if k in circ: fams_old[round(1 / s)][0] += 1; fams_old[round(1 / s)][1].add(k); old_hits.append((int(r[0]), int(r[1]), round(1 / s)))
np.savez_compressed(f'out/ap445_{N}.npz', rows=np.array(rows, np.int32), old=np.array(old_hits, np.int32))
# per-window join (Fable: aggregate counts can cancel gains and losses)
new_at = {(r[0], r[1]): r for r in rows}; join = collections.defaultdict(collections.Counter)
for ci, cj, K in old_hits:
    r = new_at.get((ci, cj))
    join[K]['absent' if r is None else 'm>1' if r[2] > 1 else 'same K' if r[3] == K else 'other K'] += 1
old_at = {(a, b) for a, b, _ in old_hits}; gained = collections.Counter(r[3] for r in rows if r[2] == 1 and r[3] > 0 and (r[0], r[1]) not in old_at)
with open(f'results/allpairs445_{N}.txt', 'w') as fo:
    out = lambda t: (print(t), fo.write(t + '\n'))
    out(f"N={N} W={W} PMAX={PMAX}: all-pairs, keep-if-agree (allpairs445.py). windows with >=1 solvable pair by multiplicity: {dict(sorted(mult.items()))}")
    out("K: old hess_stream windows / circles | new m=1 windows / circles | windows with m>1 that include K (residue)")
    for K in sorted(set(fams_old) | set(fams_new) | set(fams_res)):
        a, b = fams_old.get(K, [0, set()]), fams_new.get(K, [0, set()])
        out(f"K={K}: old {a[0]} / {len(a[1])} | new {b[0]} / {len(b[1])} (full-set verified {fams_full.get(K, 0)}) | residue {fams_res.get(K, 0)} | old hits now: {dict(join.get(K, {}))} | new hits not in old: {gained.get(K, 0)}")
    out(f"m == 1 windows verified on the full OK set: {fullv[True]}, not verified: {fullv[False]}")
    out(f"total {time.time() - t0:.0f}s, {len(memo)} distinct signatures")
# circles seen per family, for the circle-to-orbit mapping (zenith 99737: multiples of 4 fit orbits but do not prove them)
import json
json.dump({str(K): sorted(map(list, b[1])) for K, b in fams_new.items()}, open(f'results/allpairs445_{N}_circles.json', 'w'))
json.dump({str(K): sorted(map(list, S)) for K, S in fams_vset.items()}, open(f'results/allpairs445_{N}_circles_verified.json', 'w'))
