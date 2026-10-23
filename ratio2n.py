"""Registered in board post 99927 (23.10, before counting): per shared family (K, parent triple), r = hits(2N)/hits(N)
from the old cap-20 scanner's four-phase hit arrays; families with >= 10 hits at N. Median r in [3, 6] = area scaling;
< 2 or > 8 refutes; else inconclusive. usage: python ratio2n.py N 2N"""
import sys, collections, statistics, numpy as np
src = open('parents81.py').read().split('fam = collections.Counter()')[0].replace('want = {int(k) for k in sys.argv[2:]}', 'want = set()')
ns = {'__name__': 'x'}; sv = sys.argv; sys.argv = sv[:1]; exec(src, ns); sys.argv = sv; circ, parents = ns['circ'], ns['parents']
def hits(n):
    c = collections.Counter()
    for p in ('00', '01', '10', '11'):
        a = np.load(f'out/hess_s_{n}_5_20_o{p}.npy'); rr = a[:, 2] + a[:, 4] - 2; a, rr = a[rr > 1e-9], rr[rr > 1e-9]
        for k in zip(np.round((a[:, 2] - a[:, 4]) % 2, 6), np.round((2 * a[:, 3]) % 2, 6), np.round(rr, 6)):
            k = tuple(float(x) for x in k)
            if k in circ: c[k] += 1
    f = collections.Counter()
    for k, v in c.items(): f[(round(1 / k[2]), parents(*k))] += v
    return f
n1, n2 = int(sys.argv[1]), int(sys.argv[2]); A, B = hits(n1), hits(n2)
rs = []
for fam in sorted(A):
    r = B[fam] / A[fam] if A[fam] else float('nan'); keep = A[fam] >= 10 and B[fam] > 0
    if keep: rs.append(r)
    print(f"K={fam[0]:3d} {fam[1]}: hits {n1} {A[fam]:7d}  {n2} {B[fam]:7d}  r={r:.3f}{'' if keep else '  (excluded)'}")
med = statistics.median(rs)
print(f"families kept {len(rs)}; median r {med:.3f}; min {min(rs):.3f} max {max(rs):.3f}; verdict",
      'area scaling' if 3 <= med <= 6 else 'refuted' if med < 2 or med > 8 else 'inconclusive')
