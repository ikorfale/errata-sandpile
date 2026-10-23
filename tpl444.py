"""#444 (Fable 22.10): is the 1248 absence of K = 52, 57, 64, 73, 76, 81 in the identity or in the scanner's footprint?
Exact 5x5 e-blocks from 1216 family windows (allpairs, m == 1) as templates, no period margin. A template must never occur
at 1216 farther than D cells from every window of its family (in-sample specificity), and belong to one family only.
Then count template hits and their clusters at other N. Control: 1280, where the scanner sees 52, 57, 81.
usage: python tpl444.py [S] [D]   (block side S = 5, specificity distance D = 10)"""
import sys, collections, numpy as np
S = int(sys.argv[1]) if len(sys.argv) > 1 else 5; D = int(sys.argv[2]) if len(sys.argv) > 2 else 10; H = S // 2
TARGET = [52, 57, 64, 73, 76, 81]
RM = np.random.default_rng(445).integers(1, 2**62, size=(S, S), dtype=np.int64) | 1
def codes(e):  # hash of the SxS block centred at (i, j) (wrapping int64 sum of e * random odd multipliers; S = 5 run: exact)
    n = e.shape[0]; c = np.zeros((n - S + 1, n - S + 1), np.int64)
    with np.errstate(over='ignore'):
        for a in range(S):
            for b in range(S): c = c + e[a:a + n - S + 1, b:b + n - S + 1] * RM[a, b]
    return c  # c[i - H, j - H] is the block centred at (i, j)
def dilate(mask, d):  # Chebyshev dilation by d with a summed-area table
    n = mask.shape[0]; s = np.zeros((n + 1, n + 1), np.int64); s[1:, 1:] = mask.cumsum(0).cumsum(1)
    lo = np.clip(np.arange(n) - d, 0, n); hi = np.clip(np.arange(n) + d + 1, 0, n)
    return (s[hi][:, hi] - s[lo][:, hi] - s[hi][:, lo] + s[lo][:, lo]) > 0
def load(n):
    e = np.load(f'out/odo_{n}.npz')['e'].astype(np.int64); r = np.load(f'out/ap445_{n}.npz')['rows']
    return e, r[(r[:, 2] == 1)]
e0, r0 = load(1216); c0 = codes(e0); n0 = e0.shape[0]
fams = sorted(set(r0[:, 3].tolist()))
T = {}
for K in fams:
    m = np.zeros((n0, n0), bool); rk = r0[r0[:, 3] == K]; m[rk[:, 0], rk[:, 1]] = True
    near = dilate(m, D)[H:n0 - H, H:n0 - H]
    inside = set(c0[m[H:n0 - H, H:n0 - H]].tolist()); outside = set(c0[~near].tolist())
    T[K] = inside - outside
owner = collections.Counter(x for K in T for x in T[K])
for K in T: T[K] = {x for x in T[K] if owner[x] == 1}
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
print(f"S={S} D={D}; templates from 1216 family windows")
for n in (1216, 1248, 1280):
    e, r = load(n); c = codes(e); fam_at = {(int(a), int(b)): int(k) for a, b, _, k, _ in r}
    print(f"N={n}: scanner families {len(set(r[:, 3].tolist()))}")
    for K in TARGET:
        if K not in T: print(f"  K={K}: no family windows at 1216"); continue
        TK = np.fromiter(T[K], np.int64); hit = np.argwhere(np.isin(c, TK)) + H
        d4 = sum(int(np.isin(codes(np.rot90(e, k).T if f else np.rot90(e, k)), TK).sum()) for k in range(4) for f in (0, 1)) - len(hit)
        scan = int((r[:, 3] == K).sum())
        mk = np.zeros(e.shape, bool); rk = r[r[:, 3] == K]; mk[rk[:, 0], rk[:, 1]] = True; nearK = dilate(mk, D)
        prec = int(nearK[hit[:, 0], hit[:, 1]].sum()) if len(hit) else 0
        other = collections.Counter(fam_at.get((int(a), int(b)), 0) for a, b in hit)  # 0 = no family window at that centre
        k = clusters(hit) if len(hit) <= 4000 else -1
        far = hit[~nearK[hit[:, 0], hit[:, 1]]] if len(hit) else hit; nb = collections.Counter()
        for F in sorted(set(r[:, 3].tolist()) - {K}):  # off-family hits: which other family's windows lie within D
            mf = np.zeros(e.shape, bool); rf = r[r[:, 3] == F]; mf[rf[:, 0], rf[:, 1]] = True
            nf = int(dilate(mf, D)[far[:, 0], far[:, 1]].sum()) if len(far) else 0
            if nf: nb[F] = nf
        print(f"  K={K}: templates {len(T[K])}; hits {len(hit)} in {k} clusters, {prec} within D of a scanner {K}-window; other 7 D4 images {d4}; scanner windows {scan}; hit centres by scanner class {dict(sorted(other.items()))}; off-family hits {len(far)} near other families {dict(nb)}")
