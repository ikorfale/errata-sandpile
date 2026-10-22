"""Fable 22.10: are W=3 hits of 73/76 genuine? Compare their period bases (|p^q|, |p|^2, |q|^2, |p.q|) with W=5 hits at 1216."""
import sys, collections, numpy as np
src = open('parents81.py').read().split('fam = collections.Counter()')[0].replace('want = {int(k) for k in sys.argv[2:]}', 'want = set()')
ns = {'__name__': 'x'}; exec(src, ns); circ = ns['circ']
def sig(files, Ks):
    out = collections.defaultdict(collections.Counter)
    for f in files:
        for r in np.load(f):
            s = r[2] + r[4] - 2
            if s <= 1e-9: continue
            k = (round((r[2] - r[4]) % 2, 6), round((2 * r[3]) % 2, 6), round(s, 6))
            if k in circ and round(1 / s) in Ks:
                p, q = r[5:7].astype(int), r[7:9].astype(int)
                out[round(1 / s)][(abs(int(p[0]*q[1]-p[1]*q[0])), int(p@p), int(q@q), abs(int(p@q)))] += 1
    return out
Ks = {52, 57, 73, 76, 81}
w5 = sig([f'out/hess_s_1216_5_20_o{ph}.npy' for ph in ('00', '01', '10', '11')], Ks)
for n in (1248, 1280):
    w3 = sig([f'out/hess_s_{n}_3_20_o00.npy'], Ks)
    for K in sorted(Ks):
        a, b = set(w3[K]), set(w5[K])
        print(f"N={n} W3 K={K}: {sum(w3[K].values())} rows, bases {sorted(a)[:4]}; shared with 1216 W5: {len(a & b)} of {len(a)}; W5 bases {sorted(b)[:3]}")
