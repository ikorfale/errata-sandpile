"""#406: does the scanner's period lattice equal L(A) = {p in Z^2 : A p in Z^2}? Check on per-window records."""
import sys, collections, numpy as np
from fractions import Fraction as F
rows = np.concatenate([np.load(f) for f in sys.argv[1:]])
def frac(x): return F(x).limit_denominator(100000)
stat = collections.Counter(); ex = []
for r in rows:
    A11, A12, A22 = map(frac, r[2:5]); p = (int(r[5]), int(r[6])); q = (int(r[7]), int(r[8]))
    rr = A11 + A22 - 2
    if rr <= 0: continue
    k = round(1 / rr)
    inZ = lambda v: all(x.denominator == 1 for x in (A11*v[0] + A12*v[1], A12*v[0] + A22*v[1]))
    det = abs(p[0]*q[1] - p[1]*q[0])
    # index of L(A): count p in [0,k)^2 box? use lattice of denominators: brute force over a k x k fundamental box of Z^2/kZ^2
    stat[(inZ(p) and inZ(q), det == k)] += 1
    if not (inZ(p) and inZ(q)) and len(ex) < 5: ex.append((k, p, q, A11, A12, A22))
print(stat); print(*ex, sep='\n')
