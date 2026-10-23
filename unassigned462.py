"""zenith 99972: the off-family neighbour lists in 99951/99967 were not a partition (57 at 1248: 80 + 32 + 16 = 128 of 144).
For each target family and row, every hit of the src-2016 S=11 templates that is farther than D from its own family is
labelled with the SET of other families whose scanner windows lie within D (empty set = near no scanner window).
Then the unassigned hits (empty set) are compared between rows in two frames: D4-canonical distance from the nearest corner
(i, j), and the same as a fraction of N. usage: python3 unassigned462.py S D SRC N1 N2 ..."""
import sys, json, collections, numpy as np
src = open('tpl462.py').read().split('SRC = int(sys.argv[3])')[0]
ns = {'__name__': 'x'}; sv = sys.argv; sys.argv = sv[:3]; exec(src, ns); sys.argv = sv
S, D, H, codes, dilate, load, TARGET = ns['S'], ns['D'], ns['H'], ns['codes'], ns['dilate'], ns['load'], ns['TARGET']
SRC = int(sys.argv[3]); TESTS = [int(x) for x in sys.argv[4:]]
T = {int(k): np.array(v, np.int64) for k, v in json.load(open(f'out/tpl462_S{S}_src{SRC}.json')).items()}
def canon(i, j, n):  # D4 image nearest corner (0,0), i <= j
    a, b = min(i, n - 1 - i), min(j, n - 1 - j); return (min(a, b), max(a, b))
res = {}
for n in TESTS:
    e, r = load(n); c = codes(e); fams = sorted(set(r[:, 3].tolist())); near = {}
    for F in fams:
        mf = np.zeros(e.shape, bool); rf = r[r[:, 3] == F]; mf[rf[:, 0], rf[:, 1]] = True; near[F] = dilate(mf, D)
    print(f"N={n}")
    for K in TARGET:
        if K not in T: continue
        hit = np.argwhere(np.isin(c, T[K])) + H
        own = near[K][hit[:, 0], hit[:, 1]] if K in near and len(hit) else np.zeros(len(hit), bool)
        far = hit[~own]; sets = collections.Counter(); un = []
        for i, j in far:
            s = tuple(F for F in fams if F != K and near[F][i, j]); sets[s] += 1
            if not s: un.append(canon(int(i), int(j), n))
        res[(n, K)] = un
        print(f"  K={K}: hits {len(hit)}, off-family {len(far)}; by set of nearby families {dict(sorted(sets.items()))}; unassigned {len(un)}")
for K in TARGET:
    a = [res[(n, K)] for n in TESTS if (n, K) in res]
    if len(TESTS) == 2 and len(a) == 2 and (a[0] or a[1]):
        A, B = set(a[0]), set(a[1]); n1, n2 = TESTS
        fa = {(round(x / n1, 3), round(y / n1, 3)) for x, y in A}; fb = {(round(x / n2, 3), round(y / n2, 3)) for x, y in B}
        tol = 2 / n1  # matched if a position in the other row lies within 2 cells after scaling by N
        mt = sum(1 for x, y in A if any(abs(x / n1 - u / n2) <= tol and abs(y / n1 - v / n2) <= tol for u, v in B))
        print(f"K={K}: unassigned canonical positions {n1}: {len(A)}, {n2}: {len(B)}; same corner offset {len(A & B)}; same fraction of N (3 dp) {len(fa & fb)}; {n1} positions with a {n2} position within 2 cells after scaling: {mt}")
        print(f"   {n1} sample {sorted(A)[:12]}"); print(f"   {n2} sample {sorted(B)[:12]}")
