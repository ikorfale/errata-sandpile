"""#394: band circles (one period 0 <= b < 2, curvature <= K) reached by exact period lattices in hess_small output,
per curvature, plus windows off the packing. usage: python reach81.py npy [K]"""
import sys, collections, numpy as np
from fractions import Fraction as F
src = open('apollo.py').read().split('print(f"band')[0].split('KMAX = 400')[1]
ns = {'np': np}; exec('KMAX = 400' + src, ns); C = ns['C']
K = int(sys.argv[2]) if len(sys.argv) > 2 else 81
band = collections.Counter(); reached = collections.Counter(); seen = set(); off = 0; offc = collections.Counter()
circ = {(round(c[0], 6), round(c[1] % 2, 6), round(c[2], 6)) for c in C if c[2] > 0 and 1 / c[2] <= K + 0.5}
for c in circ: band[round(1 / c[2])] += 1
for r in np.load(sys.argv[1]):
    rr = r[2] + r[4] - 2
    if rr <= 1e-9: continue
    a = (r[2] - r[4]) % 2; b = (2 * r[3]) % 2
    key = (round(a, 6), round(b, 6), round(rr, 6))
    if key in circ:
        if key not in seen: seen.add(key); reached[round(1 / rr)] += 1
    else:
        off += 1; offc[key] += 1
print(f"{sys.argv[1]}: band circles with curvature <= {K} per period: {sum(band.values())}, reached {len(seen)}")
for k in sorted(band): print(f"  curvature {k:3d}: {reached[k]} of {band[k]}")
print(f"windows off the packing (positive r): {off}; most common: {offc.most_common(3)}")
