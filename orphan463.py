"""Fable 23.10 review of #463: are the K=57/81 template hits that lie near no family window at 1256 a missed family (tiling with its period) or scattered background? Same templates as tpl462.py."""

import os, sys, collections, numpy as np
S = int(sys.argv[1]) if len(sys.argv) > 1 else 5; D = int(sys.argv[2]) if len(sys.argv) > 2 else 10; H = S // 2
TARGET = [52, 57, 64, 73, 76, 81]
RM = np.random.default_rng(445).integers(1, 2**62, size=(S, S), dtype=np.int64) | 1
def codes(e):  # hash of the SxS block centred at (i, j) (wrapping int64 sum of e * random odd multipliers; S = 5 run: exact)
    n = e.shape[0]; c = np.zeros((n - S + 1, n - S + 1), np.int64)
    with np.errstate(over='ignore'):
        for a in range(S):
            for b in range(S): c = c + e[a:a + n - S + 1, b:b + n - S + 1] * RM[a, b]
    return c  # c[i - H, j - H] is the block centred at (i, j)
def dilate(mask, d):  # Chebyshev dilation by d, separable boolean shifts (the summed-area version OOM-killed at 2016)
    m = mask.copy()
    for ax in (0, 1):
        src = m.copy()
        for s in range(1, d + 1):
            if ax == 0: m[s:] |= src[:-s]; m[:-s] |= src[s:]
            else: m[:, s:] |= src[:, :-s]; m[:, :-s] |= src[:, s:]
    return m
src = open('parents81.py').read().split('fam = collections.Counter()')[0].replace('want = {int(k) for k in sys.argv[2:]}', 'want = set()')
ns = {'__name__': 'x'}; sv = sys.argv; sys.argv = sv[:1]; exec(src, ns); sys.argv = sv; circ = ns['circ']
def load(n):  # family windows from allpairs rows if present, else from the old cap-20 scanner's four phases (one class each)
    e = np.load(f'out/odo_{n}.npz')['e'].astype(np.int64)
    if os.path.exists(f'out/ap445_{n}.npz'): r = np.load(f'out/ap445_{n}.npz')['rows']; return e, r[(r[:, 2] == 1)]
    out = []; cs = {k: round(1 / k[2]) for k in circ}
    for p in ('00', '01', '10', '11'):
        a = np.load(f'out/hess_s_{n}_5_20_o{p}.npy'); rr = a[:, 2] + a[:, 4] - 2; a, rr = a[rr > 1e-9], rr[rr > 1e-9]
        ks = np.stack([np.round((a[:, 2] - a[:, 4]) % 2, 6), np.round((2 * a[:, 3]) % 2, 6), np.round(rr, 6)], 1)
        u, inv = np.unique(ks, axis=0, return_inverse=True); lab = np.array([cs.get(tuple(float(x) for x in r), 0) for r in u])[inv.ravel()]
        keep = lab > 0; out.append(np.stack([a[keep, 0], a[keep, 1], np.ones(keep.sum()), lab[keep], np.ones(keep.sum())], 1).astype(np.int64))
        del a, rr, ks
    return e, np.concatenate(out)
SRC = int(sys.argv[3]); TESTS = [int(x) for x in sys.argv[4:]]
e0, r0 = load(SRC); c0 = codes(e0); n0 = e0.shape[0]
fams = sorted(set(r0[:, 3].tolist()))
T = {}
for K in fams:
    m = np.zeros((n0, n0), bool); rk = r0[r0[:, 3] == K]; m[rk[:, 0], rk[:, 1]] = True
    near = dilate(m, D)[H:n0 - H, H:n0 - H]
    inside = np.unique(c0[m[H:n0 - H, H:n0 - H]]); T[K] = set(inside[~np.isin(inside, c0[~near])].tolist())
owner = collections.Counter(x for K in T for x in T[K])
for K in T: T[K] = {x for x in T[K] if owner[x] == 1}
pass  # json.dump({str(K): sorted(T[K]) for K in TARGET if K in T}, open(f'out/tpl462_S{S}_src{SRC}.json', 'w'))
def clusters(pos, gap=S):  # positions within `gap` (Chebyshev) of each other form one cluster
    pos = sorted(map(tuple, pos)); seen = set(); k = 0; idx = {p: True for p in pos}
    for p in pos:
        if p in seen: continue
        k += 1; st = [p]; seen.add(p)
        while st:
            a, b = st.pop()
            for q in pos:
                if q not in seen and abs(q[0] - a) <= gap and abs(q[1] - b) <= gap: seen.add(q); st.append(q)
    return k

print("orphan K=57/81 template hits (near no family window within D), by cluster", flush=True)
for n in TESTS:
    e, r = load(n); c = codes(e); allm = np.zeros(e.shape, bool); allm[r[:, 0], r[:, 1]] = True; nearAny = dilate(allm, D)
    for K in (57, 81):
        TK = np.fromiter(T[K], np.int64); hit = np.argwhere(np.isin(c, TK)) + H
        orph = hit[~nearAny[hit[:, 0], hit[:, 1]]] if len(hit) else hit
        pos = sorted(map(tuple, orph.tolist())); seen = set(); cl = []
        for p in pos:
            if p in seen: continue
            st = [p]; seen.add(p); mem = [p]
            while st:
                a, b = st.pop()
                for q in pos:
                    if q not in seen and abs(q[0] - a) <= S and abs(q[1] - b) <= S: seen.add(q); st.append(q); mem.append(q)
            cl.append((len(mem), tuple(int(x) for x in np.mean(mem, 0).round()), len({x for x in TK if x in set(c[np.array(mem)[:, 0] - H, np.array(mem)[:, 1] - H].tolist())})))
        print(f"N={n} K={K}: hits {len(hit)}, orphans {len(orph)} in {len(cl)} clusters; (size, centre, distinct templates):", sorted(cl, key=lambda t: t[1]), flush=True)
