"""Where do the small band circles (curvature 40..81) sit at N, in absolute cells and as offsets from the centre?
Their window counts are identical at 1088 and 1152, i.e. they do not scale with N^2. usage: python motif_where.py N"""
import sys, numpy as np
N = int(sys.argv[1])
fs = [f'out/hess_small_{N}_5_10_full.npy'] + [f'out/hess_small_{N}_5_10_full_o{p}.npy' for p in ('01', '10', '11')]
a = np.concatenate([np.load(f) for f in fs]); rr = a[:, 2] + a[:, 4] - 2
ok = rr > 1e-9; cv = np.where(ok, 1 / np.where(ok, rr, 1), 0)
sel = a[ok & (cv > 39.5) & (cv < 81.5)]
c = (N - 1) / 2
i, j = sel[:, 0], sel[:, 1]
print(f"N={N}: {len(sel)} windows at curvature 40..81")
print(" bounding box rows", int(i.min()), int(i.max()), "cols", int(j.min()), int(j.max()))
d = np.minimum.reduce([i, j, N - 1 - i, N - 1 - j])
print(" distance to nearest edge: min", int(d.min()), "max", int(d.max()))
q = (i < c) & (j < c)
print(" one quadrant (i,j < centre), first 6 windows by i:", sorted(map(tuple, sel[q][:, :2].astype(int).tolist()))[:6])
print(" offsets from centre in that quadrant: i-c in", float((i[q] - c).min()), float((i[q] - c).max()), "; j-c in", float((j[q] - c).min()), float((j[q] - c).max()))
