"""#406: which band-packing circles can the side-5 scanner detect at period cap PMAX?
Rule (checked on 87,410 windows at N=1024: every scanned p, q has A p in Z^2): the period lattice is L(A) = {p : A p in Z^2}.
A from (a, b, r): A11 + A22 = r + 2, A11 - A22 = a, 2 A12 = b (integer shifts do not change L).
Detectable = the scanner's own rule: p = first lattice vector in its scan order, q = first non-parallel one, p+q or p-q in the scan set.
usage: python ceiling406.py PMAX [reached_file ...]"""
import sys, collections, numpy as np
from fractions import Fraction as F
PMAX = int(sys.argv[1])
src = open('apollo.py').read().split('print(f"band')[0].split('KMAX = 400')[1]
ns = {'np': np}; exec('KMAX = 400' + src, ns); C = ns['C']
pa = open('parents81.py').read()
circ = {(round(c[0], 6), round(c[1] % 2, 6), round(c[2], 6)) for c in C if c[2] > 0 and 1 / c[2] <= 400.5}
exec(pa.split('def parents')[1].split('fam = collections')[0].join(['def parents', '']), globals())
vecs = sorted({(i, j) for i in range(0, PMAX + 1) for j in range(-PMAX, PMAX + 1) if (i, j) > (0, 0)}, key=lambda p: p[0]**2 + p[1]**2)
vset = set(vecs)
def fr(x, k): return F(round(x * 2 * k), 2 * k)  # a, b, r are multiples of 1/(2k)? checked below
def lattice_ok(A11, A12, A22, p): return all(x.denominator == 1 for x in (A11*p[0] + A12*p[1], A12*p[0] + A22*p[1]))
out = collections.defaultdict(list)
for (a, b, r) in sorted(circ):
    k = round(1 / r)
    fa, fb, frr = F(round(a * k), k), F(round(b * k), k), F(1, k)  # curvature-centre coordinates are integers in an Apollonian packing
    assert abs(float(fa) - a) < 2e-6 and abs(float(fb) - b) < 2e-6, (a, b, k)
    A11 = (frr + 2 + fa) / 2; A22 = (frr + 2 - fa) / 2; A12 = fb / 2
    L = [v for v in vecs if lattice_ok(A11, A12, A22, v)]
    det_ok = None; det = None
    if len(L) >= 2:
        p = L[0]; q = next((w for w in L[1:] if p[0]*w[1] - p[1]*w[0]), None)
        if q is not None:
            det = abs(p[0]*q[1] - p[1]*q[0])
            for sg in (1, -1):
                s = (p[0] + sg*q[0], p[1] + sg*q[1])
                if s[0] < 0 or (s[0] == 0 and s[1] < 0): s = (-s[0], -s[1])
                if s in vset: det_ok = True; break
    out[(k, parents(a, b, r))].append((bool(det_ok), det))
reached = set()
for f in sys.argv[2:]:
    for line in open(f):
        if ' reached 0 ' in line: continue
        k = int(line.split()[1]); par = eval(line.split('parents ')[1].split(':')[0]); reached.add((k, par))
det_f = {f for f, v in out.items() if any(d for d, _ in v)}
print(f"PMAX={PMAX}: families {len(out)}, detectable {len(det_f)}, max detectable curvature {max(f[0] for f in det_f)}")
if reached:
    print(f"reached (union of files) {len(reached)}; reached but not detectable: {sorted(reached - det_f)}")
    print(f"detectable but never reached ({len(det_f - reached)}): {sorted(det_f - reached)}")
    bad = [(f, v) for f, v in out.items() if f in reached and any(d != f[0] for _, d in v if d)]
    print("reached families whose scan basis det != curvature:", bad[:5])
