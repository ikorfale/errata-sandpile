"""Run manifest (theone, board 98245): bind every out/parents400_* summary to its N, cap and phases through the files
that do encode N: the identity out/odo_N.npz (arrays N x N) and the four scan arrays out/hess_s_N_5_CAP_oXY.npy
(rows = lattice windows, columns 0-1 = window corner, max = N - 10). Summaries list a fixed catalog, so equal
reached-sets give equal bytes at different N; the scan-array hashes are what tell the rows apart.
Writes out/MANIFEST.tsv. Usage: python3 manifest.py"""
import glob, hashlib, os, re
import numpy as np
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
rows = ['summary\tN\tcap\tsummary_sha256\treached\tidentity_sha256\tphase\twindows\tcorner_max\tscan_sha256']
for p in sorted(glob.glob('out/parents400_*_W5*_4phase.txt'), key=lambda s: (int(re.search(r'_(\d+)_W5', s)[1]), s)):
    n = int(re.search(r'_(\d+)_W5', p)[1]); cap = 20 if '_P20_' in p else 10
    reached = sum(' reached 0 ' not in l for l in open(p))
    odo = f'out/odo_{n}.npz'; idh = sha(odo) if os.path.exists(odo) else '-'
    for ph in ('o00', 'o01', 'o10', 'o11'):
        s = f'out/hess_s_{n}_5_{cap}_{ph}.npy'
        if os.path.exists(s):
            a = np.load(s, mmap_mode='r')
            rows.append(f'{os.path.basename(p)}\t{n}\t{cap}\t{sha(p)}\t{reached}\t{idh}\t{ph}\t{a.shape[0]}\t{int(a[:, :2].max())}\t{sha(s)}')
        else:
            rows.append(f'{os.path.basename(p)}\t{n}\t{cap}\t{sha(p)}\t{reached}\t{idh}\t{ph}\t-\t-\tnot kept')
open('out/MANIFEST.tsv', 'w').write('\n'.join(rows) + '\n')
print(len(rows) - 1, 'rows; summaries', len({r.split('\t')[0] for r in rows[1:]}))
