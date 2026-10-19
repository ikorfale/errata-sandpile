"""lchart.py: L (zero run of the midline step g) next to where it shows in the identity picture. Output out/L_vs_identity.png"""
import json, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from gzeros_core import stab_odo
rows = [json.loads(l) for l in open('out/gzeros.jsonl')]
M = 66; six = np.full((M, M), 6, np.int64); s, _ = stab_odo(six); e, _ = stab_odo(six - s); m = M // 2
fig, (a, b) = plt.subplots(1, 2, figsize=(12, 5.2), gridspec_kw={'width_ratios': [1.35, 1]})
on = [r for r in rows if r['L'] > 0]; off = [r for r in rows if r['L'] == 0]
a.scatter([r['M'] for r in off], [0] * len(off), s=8, c='#bbbbbb', label=f'L = 0 ({len(off)} sizes)')
a.scatter([r['M'] for r in on], [r['L'] for r in on], s=22, c='#c0392b', label=f'L > 0 ({len(on)} sizes)')
x = np.arange(0, 402); a.plot(x, 0.125 * x, ls=':', c='#555', lw=1, label='L = M/8')
a.set_xlabel('grid side M (even)'); a.set_ylabel('L, zeros at each end of g'); a.legend(frameon=False, loc='upper left')
a.set_title('Zero run of the midline step g, every even M to 400', fontsize=11); a.spines[['top', 'right']].set_visible(False)
cmap = matplotlib.colors.ListedColormap(['#1b1b1b', '#f1c40f', '#2e86c1', '#ecf0f1'])
b.imshow(e[m - 9:m + 9, :20], cmap=cmap, vmin=0, vmax=3, extent=(-0.5, 19.5, m + 8.5, m - 9.5))
b.add_patch(plt.Rectangle((-0.5, m - 1.5), 20, 1, fill=False, ec='#c0392b', lw=2))
L = next(r['L'] for r in rows if r['M'] == M)
b.annotate(f'first 1 at column {L - 1}\nL = {L}', xy=(L - 1, m - 1), xytext=(9, m - 6), color='#c0392b',
           arrowprops=dict(arrowstyle='->', color='#c0392b'), fontsize=10)
b.set_title(f'Identity, M = {M}: left edge around the midline row', fontsize=11)
b.set_xticks(range(0, 20, 2)); b.set_xlabel('column'); b.set_ylabel('row')
fig.text(0.99, 0.01, 'errata · computed, not illustrated · colours: 0 black, 1 yellow, 2 blue, 3 white', ha='right', fontsize=8, c='#777')
fig.tight_layout(); fig.savefig('out/L_vs_identity.png', dpi=130)
