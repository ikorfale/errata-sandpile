"""Parent triple (the three tangent circles/lines of smaller curvature) of every band circle reached
by exact period lattices, for chosen curvatures. usage: python parents81.py npy K1 [K2 ...]"""
import sys, collections, numpy as np
src = open('apollo.py').read().split('print(f"band')[0].split('KMAX = 400')[1]
ns = {'np': np}; exec('KMAX = 400' + src, ns); C = ns['C']
want = {int(k) for k in sys.argv[2:]}
circ = {(round(c[0], 6), round(c[1] % 2, 6), round(c[2], 6)) for c in C if c[2] > 0 and 1 / c[2] <= 400.5}
def parents(a, b, r):
    k = round(1 / r); ps = []
    if abs(a - r) < 1e-6: ps.append(0)
    if abs(a + r - 2) < 1e-6: ps.append(0)
    for (a2, b2, r2) in circ:
        if round(1 / r2) >= k: continue
        db = (b - b2 + 1) % 2 - 1
        if abs(np.hypot(a - a2, db) - (r + r2)) < 1e-5: ps.append(round(1 / r2))
    return tuple(sorted(ps))
fam = collections.Counter(); reach = collections.Counter(); seen = set()
for (a, b, r) in circ:
    if round(1 / r) in want: fam[(round(1 / r), parents(a, b, r))] += 1
for row in np.load(sys.argv[1]):
    rr = row[2] + row[4] - 2
    if rr <= 1e-9: continue
    key = (round((row[2] - row[4]) % 2, 6), round((2 * row[3]) % 2, 6), round(rr, 6))
    if key in circ and key not in seen and round(1 / rr) in want:
        seen.add(key); reach[(round(1 / rr), parents(*key))] += 1
for f in sorted(fam): print(f"curvature {f[0]:3d} parents {f[1]}: reached {reach[f]} of {fam[f]}")
