"""Where are the curvature-25 band-circle windows at N (default 1024), in grid fractions; and what do windows of
another size M show near the same fractions? usage: python where25.py N M [curv]"""
import sys, collections, numpy as np
N, M = int(sys.argv[1]), int(sys.argv[2]); CV = int(sys.argv[3]) if len(sys.argv) > 3 else 25
def load(n):
    fs = [f'out/hess_small_{n}_5_10_full.npy'] + [f'out/hess_small_{n}_5_10_full_o{p}.npy' for p in ('01', '10', '11')]
    return np.concatenate([np.load(f) for f in fs])
a = load(N); rr = a[:, 2] + a[:, 4] - 2
sel = a[(rr > 1e-9) & (np.abs(1 / np.where(rr > 1e-9, rr, 1) - CV) < 0.5)]
print(f"N={N}: {len(sel)} windows at curvature {CV}")
fr = np.round(sel[:, :2] / N, 3)
cl = collections.Counter(map(tuple, np.round(fr, 2)))
print(" clusters (i/N, j/N) -> windows:", cl.most_common(8))
b = load(M); fb = b[:, :2] / M; rb = b[:, 2] + b[:, 4] - 2
for (ci, cj), _ in cl.most_common(2):
    near = (np.abs(fb[:, 0] - ci) < 0.01) & (np.abs(fb[:, 1] - cj) < 0.01)
    kinds = collections.Counter(round(1 / x) if x > 1e-9 else ('flat' if abs(x) < 1e-9 else f'neg{round(-1/x)}') for x in rb[near])
    print(f" N={M} windows within 0.01 of ({ci},{cj}): {near.sum()}, by curvature: {kinds.most_common(6)}")
