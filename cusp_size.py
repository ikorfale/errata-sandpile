"""#393: patch size (windows found) per band circle at N = 1024, windows of side 4, 5, 6.
Cusp chains = circles in the cusp between a unit circle and a wall (0, 1, n^2) or between two unit circles (1, 1, 2n(n+1)).
usage: python cusp_size.py  (needs out/hess_small_1024_{4,5}_10_full.npy and out/exact_hess2_1024_6_20_full.npy)"""
import numpy as np, collections, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fns = {6: 'out/exact_hess2_1024_6_20_full.npy', 5: 'out/hess_small_1024_5_10_full.npy', 4: 'out/hess_small_1024_4_10_full.npy'}
src = open('apollo.py').read().split('print(f"band')[0].split('KMAX = 400')[1]
ns = {'np': np}; exec('KMAX = 400' + src, ns)
band = {}
for x, y, r in ns['C']:
    if r <= 0 or not (0 <= x <= 2 and 0 <= y < 2): continue
    k = int(round(1 / r))
    if k <= 36: band[(k, round(x % 2, 3), round(y % 2, 3))] = (x, y)
def chain(k, x, y):  # wall cusp: touches a line and a unit circle at (1, 2m) with y = 2m +- 2/n; circle cusp: y = 1, k = 2n(n+1)
    n = round(k ** 0.5)
    if n * n == k and min(x, 2 - x) < 0.5 and any(abs(abs(y - c) - 2 / n) < 1e-6 for c in (0, 2)): return 'wall cusp'
    if abs(y - 1) < 1e-6 and k in (4, 12, 24, 40): return 'circle cusp'
    return 'elsewhere'
cnt = {}
for W, fn in fns.items():
    c = collections.Counter()
    for r in np.load(fn):
        rr = r[2] + r[4] - 2
        if rr > 1e-9: c[(int(round(1 / rr)), round((r[2] - r[4]) % 2, 3), round((2 * r[3]) % 2, 3))] += 1
    cnt[W] = c
fig, axs = plt.subplots(1, 3, figsize=(12, 4), sharey=True)
col = {'wall cusp': '#d9480f', 'circle cusp': '#7048e8', 'elsewhere': '#2a6db0'}
print('k a b chain W6 W5 W4')
for key in sorted(band):
    ch = chain(key[0], *band[key]); print(*key, ch, *[cnt[W][key] for W in (6, 5, 4)])
for ax, W in zip(axs, (6, 5, 4)):
    for key in band:
        ch = chain(key[0], *band[key]); n = cnt[W][key]
        ax.scatter(key[0], max(n, 0.6), color=col[ch], marker='o' if n else 'x', s=28)
    ax.set_yscale('log'); ax.set_xlabel('curvature'); ax.set_title(f'window side {W}'); ax.axhline(1, color='#999', lw=0.5)
axs[0].set_ylabel('windows with an exact period lattice (x = none)')
for ch, c in col.items(): axs[2].scatter([], [], color=c, label=ch)
axs[2].legend(fontsize=8, loc='upper right')
fig.suptitle('Sandpile identity N = 1024: circles deep in a cusp have much smaller patches than others of the same curvature', fontsize=10)
fig.tight_layout(); fig.savefig('out/cusp_size_1024.png', dpi=140)
