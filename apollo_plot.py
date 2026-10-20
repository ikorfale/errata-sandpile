"""apollo_plot.py: windows of the identity's potential, (a, b) = (A11-A22, 2 A12) mod 2, over the Apollonian band packing.
Left: the identity e (N). Right: band circles (grey) and window Hessians, colour = trace(A) - 2 = the radius they should have."""
import sys, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Circle
N = int(sys.argv[1]); RMS = 0.6
exec(open('apollo.py').read().split('print(f"band')[0].replace('N = int(sys.argv[1]); RMS = float(sys.argv[2]) if len(sys.argv) > 2 else 0.6', ''))
e = np.load(f'out/odo_{N}.npz')['e']; H = np.load(f'out/hess_{N}.npy'); H = H[H[:, 5] <= RMS]
a = np.mod(H[:, 2] - H[:, 4], 2); b = np.mod(2 * H[:, 3], 2); r = H[:, 2] + H[:, 4] - 2
fig, ax = plt.subplots(1, 2, figsize=(13, 6.3), facecolor='white')
ax[0].imshow(e, cmap=matplotlib.colors.ListedColormap(['#1b1b2f', '#3d5a80', '#98c1d9', '#f4d35e']), interpolation='nearest')
ax[0].set_title(f'Identity of the sandpile group, {N}x{N}', fontsize=12); ax[0].axis('off')
for x, y, rr in C:
    if rr > 0.01: ax[1].add_patch(Circle((x, y), rr, fill=False, lw=0.6, color='#888'))
ax[1].axvline(0, color='#888', lw=0.6); ax[1].axvline(2, color='#888', lw=0.6)
sc = ax[1].scatter(a, b, c=np.clip(r, 0, 1), s=14, cmap='viridis', vmin=0, vmax=1, zorder=3, edgecolor='none')
ax[1].set_xlim(-0.05, 2.05); ax[1].set_ylim(-0.05, 2.05); ax[1].set_aspect('equal')
ax[1].set_xlabel('A11 - A22  (mod 2)'); ax[1].set_ylabel('2 A12  (mod 2)')
ax[1].set_title('Local Hessian of a potential v with Lv = e\nover the Apollonian band packing (Levine-Pegden-Smart)', fontsize=11)
plt.colorbar(sc, ax=ax[1], fraction=0.046, label='trace(A) - 2  (predicted circle radius)')
fig.text(0.5, 0.01, 'errata (AI agent) · computed exactly, fitted on 16x16 windows · github.com/ikorfale/errata-sandpile', ha='center', fontsize=8, color='#666')
plt.tight_layout(); plt.savefig(f'out/apollo_{N}.png', dpi=110); print('ok')
