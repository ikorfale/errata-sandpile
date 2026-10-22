"""zenith 98537: is 1248 thin because its patches are smaller? Per row, the share of 5x5 windows whose exact period lattice
maps to a catalog circle, by curvature band (all four phases; windows counted with multiplicity across phases)."""
import sys, numpy as np
src = open('parents81.py').read().split('fam = collections.Counter()')[0].replace('want = {int(k) for k in sys.argv[2:]}', 'want = set()')
ns = {'__name__': 'x'}; exec(src, ns); circ = ns['circ']
BANDS = [(1, 9), (10, 39), (40, 99), (100, 400)]
for n in map(int, sys.argv[1:]):
    tot = 0; c = {b: 0 for b in BANDS}; nonc = 0
    for ph in ('00', '01', '10', '11'):
        oi, oj = int(ph[0]), int(ph[1]); tot += len(range(oi, n - 4, 2)) * len(range(oj, n - 4, 2))
        R = np.load(f'out/hess_s_{n}_5_20_o{ph}.npy')
        rr = R[:, 2] + R[:, 4] - 2
        for r, s in zip(R, rr):
            if s <= 1e-9: nonc += 1; continue
            k = (round((r[2] - r[4]) % 2, 6), round((2 * r[3]) % 2, 6), round(s, 6))
            if k not in circ: nonc += 1; continue
            K = round(1 / s)
            for b in BANDS:
                if b[0] <= K <= b[1]: c[b] += 1
    print(n, ' '.join(f"K{b[0]}-{b[1]}: {c[b] / tot:.5f}" for b in BANDS), f"other: {nonc / tot:.4f}", flush=True)
