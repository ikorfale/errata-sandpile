"""Split band-circle reach by distance from the grid edge: which circles are reached only by windows within D cells
of the boundary? usage: python edge_split.py N [D=40]"""
import sys, collections, numpy as np
src = open('apollo.py').read().split('print(f"band')[0].split('KMAX = 400')[1]
ns = {'np': np}; exec('KMAX = 400' + src, ns); C = ns['C']
N = int(sys.argv[1]); D = int(sys.argv[2]) if len(sys.argv) > 2 else 40
circ = {(round(c[0], 6), round(c[1] % 2, 6), round(c[2], 6)) for c in C if c[2] > 0 and 1 / c[2] <= 81.5}
fs = [f'out/hess_small_{N}_5_10_full.npy'] + [f'out/hess_small_{N}_5_10_full_o{p}.npy' for p in ('01', '10', '11')]
near, far = collections.Counter(), collections.Counter()
for f in fs:
    for r in np.load(f):
        rr = r[2] + r[4] - 2
        if rr <= 1e-9: continue
        key = (round((r[2] - r[4]) % 2, 6), round((2 * r[3]) % 2, 6), round(rr, 6))
        if key not in circ: continue
        d = min(r[0], r[1], N - 1 - r[0], N - 1 - r[1])
        (near if d < D else far)[key] += 1
only_near = [k for k in near if k not in far]
byk = collections.Counter(round(1 / k[2]) for k in only_near)
print(f"N={N} D={D}: reached {len(set(near) | set(far))}, by interior windows {len(far)}, only within {D} cells of the edge {len(only_near)}: {dict(sorted(byk.items()))}")
