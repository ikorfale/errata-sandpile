"""exact_plot.py: where the exactly periodic patches of the 512x512 identity sit, coloured by their band circle."""
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
N = 512; W = 12
e = np.load(f'out/odo_{N}.npz')['e']; X = np.load(f'out/exact_hess_{N}.npy')     # ci, cj, A11, A12, A22
a = np.mod(X[:, 2] - X[:, 4], 2); r = X[:, 2] + X[:, 3] * 0 + X[:, 4] - 2
cls = np.where(r == 0, 0, np.where(r == 1, 1, 2))
col = ['#e07a5f', '#3d405b', '#81b29a']; lab = ['line point (0,0), r=0: A = I, trace 2', 'circle (1,0), r=1: trace 3', 'circles (1/4,1) and (7/4,1), r=1/4: trace 9/4']
fig, ax = plt.subplots(1, 2, figsize=(14, 7), facecolor='white', gridspec_kw={'width_ratios': [1, 1]})
ax[0].imshow(e, cmap=matplotlib.colors.ListedColormap(['#111', '#555', '#aaa', '#eee']), interpolation='nearest')
for k in range(3):
    m = cls == k
    for ci, cj in X[m, :2]:
        ax[0].add_patch(Rectangle((cj - W / 2 - .5, ci - W / 2 - .5), W, W, fill=False, ec=col[k], lw=0.7))
ax[0].set_title('Identity, 512x512: windows with an exact period lattice (periods <= 12)', fontsize=10); ax[0].axis('off')
src = open('apollo.py').read().split('print(f"band')[0].split('KMAX = 400')[1]; ns = {'np': np}; exec('KMAX = 400' + src, ns); C = ns['C']
for x, y, rr in C:
    if rr > 0.008: ax[1].add_patch(Circle((x, y), rr, fill=False, lw=0.5, color='#999'))
ax[1].axvline(0, color='#999', lw=0.5); ax[1].axvline(2, color='#999', lw=0.5)
hit = [((1, 0), 1, 1), ((1, 2), 1, 1), ((0.25, 1), 0.25, 2), ((1.75, 1), 0.25, 2)]
for (x, y), rr, k in hit: ax[1].add_patch(Circle((x, y), rr, fill=True, alpha=0.35, color=col[k]))
for x, y in ((0, 0), (0, 2), (2, 0), (2, 2)): ax[1].plot(x, y, 'o', color=col[0], ms=8)
for k in range(3): ax[1].plot([], [], 's', color=col[k], label=f'{lab[k]}  ({(cls == k).sum()} windows)')
ax[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.06), fontsize=8, frameon=False)
ax[1].set_xlim(-0.05, 2.05); ax[1].set_ylim(-0.05, 2.05); ax[1].set_aspect('equal')
ax[1].set_title('Exact Hessian A per patch as an LPS circle\ncentre (A11-A22, 2A12) mod 2, radius tr A - 2: all 13 A on the band packing', fontsize=10)
fig.text(0.5, 0.01, 'errata (AI agent) · exact integer arithmetic, no fitting · github.com/ikorfale/errata-sandpile', ha='center', fontsize=8, color='#666')
plt.tight_layout(rect=(0, 0.03, 1, 0.96)); plt.savefig('out/exact_apollo_512.png', dpi=100); print('ok')
