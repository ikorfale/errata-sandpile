"""PREREG-rows465.md (c831ef7) kill table applied to out/tpl468.txt (tpl462.py 11 10 2016 1232 1252 1264 1344).
Present = 'within D of a scanner K-window' count > 0."""
import re
P = {}; n = None
for l in open('out/tpl468.txt'):
    m = re.match(r'N=(\d+):', l)
    if m: n = int(m.group(1))
    m = re.match(r'\s+K=(\d+):.*?, (\d+) within D of a scanner', l)
    if m: P[(n, int(m.group(1)))] = int(m.group(2)) > 0
R = (1232, 1252, 1264, 1344)
for k in (52, 57, 64, 73, 76, 81): print(f'K={k}: ' + '  '.join(f'{r} {"present" if P[(r, k)] else "absent"}' for r in R))
kill = {
 'I (one interval each)': [f'{k} present at 1252' for k in (52, 57, 81) if P[(1252, k)]] + [f'{k} absent at 1232' for k in (57, 81) if not P[(1232, k)]],
 'R52 (52 iff N = 0 mod 64)': [f'52 present at {r}' for r in (1232, 1252, 1264) if P[(r, 52)]] + (['52 absent at 1344'] if not P[(1344, 52)] else []),
 'S (52, 57, 81 together)': [f'52 at 1264 differs from {k}' for k in (57, 81) if P[(1264, 52)] != P[(1264, k)]]}
for r, why in kill.items(): print(f'{r}: ' + ('KILLED by ' + '; '.join(why) if why else 'not refuted on these rows'))
