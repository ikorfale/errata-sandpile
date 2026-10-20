"""#391: which circles of the Apollonian band packing (curvature <= 36, one period 0 <= b < 2) the N=1024 identity
reaches with an exact period lattice (side-6 periods <= 20, side-12 periods <= 40). usage: python band_reach.py"""
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from fractions import Fraction as F
src = open('apollo.py').read().split('print(f"band')[0].split('KMAX = 400')[1]
ns = {'np': np}; exec('KMAX = 400' + src, ns); C = ns['C']
hits = set()
for W, P in ((6, 20), (12, 40)):
    for r in np.load(f'out/exact_hess2_1024_{W}_{P}_full.npy'):
        rr = F(r[2] + r[4] - 2).limit_denominator(1000)
        if rr > 0: hits.add((F(r[2] - r[4]).limit_denominator(1000) % 2, F(2 * r[3]).limit_denominator(1000) % 2, rr))
fig, ax = plt.subplots(figsize=(7, 7)); rows = []
for x, y, r in C:
    if r <= 0 or not (0 <= x <= 2 and -0.05 <= y <= 2.05): continue
    k = int(round(1 / r)); a, b = F(x).limit_denominator(2000), F(y).limit_denominator(2000)
    if k > 36:
        ax.add_patch(plt.Circle((x, y), r, fill=False, lw=0.3, color='#c8c8c8')); continue
    hit = (a, b % 2, F(1, k)) in hits
    if 0 <= b < 2: rows.append((k, a, b, hit))
    ax.add_patch(plt.Circle((x, y), r, fc='#2a6db0' if hit else 'none', ec='#2a6db0' if hit else '#d9480f', lw=1.6 if not hit else 0.8, alpha=0.85 if hit else 1))
    if k > 1 and 0 <= y < 2: ax.text(x, y, str(k), ha='center', va='center', fontsize=7 if k < 20 else 5, color='white' if hit else '#d9480f')
ax.axvline(0, color='k', lw=1); ax.axvline(2, color='k', lw=1)
ax.set_xlim(-0.05, 2.05); ax.set_ylim(-0.05, 2.05); ax.set_aspect('equal'); ax.set_xlabel('a'); ax.set_ylabel('b')
n = sum(1 for t in set(rows) if t[3]); m = len(set(rows))
ax.set_title(f'Sandpile identity N = 1024: {n} of {m} band circles with curvature <= 36 reached\n'
             'filled blue = found as an exact periodic patch, orange ring = not found; number = curvature', fontsize=9)
fig.tight_layout(); fig.savefig('out/band_reach_1024.png', dpi=150)
for t in sorted(set(rows)): print(t[0], t[1], t[2], 'hit' if t[3] else 'MISS')
print(f'{n} of {m} reached')
