"""lfeat.py A B: test whether L (gzeros.jsonl) is read off the identity e = stab(6 - stab(6)) at the midline row m-1.
Rule under test (found 19.10 on M = 14..70): if e[m-1] starts with 2...2 1, L = 1 + index of that first 1; if it starts with 3, L = 0.
Appends {"M", "L", "pred", "row_head"} to out/lfeat.jsonl."""
import sys, json
import numpy as np
from gzeros_core import stab_odo
Ls = {json.loads(l)['M']: json.loads(l)['L'] for l in open('out/gzeros.jsonl')}

def pred(row):
    i = 0
    while i < len(row) and row[i] == 2: i += 1
    return i + 1 if i < len(row) and row[i] == 1 else (0 if row[0] == 3 else None)

for M in range(int(sys.argv[1]), int(sys.argv[2]) + 1, 2):
    six = np.full((M, M), 6, np.int64)
    s, _ = stab_odo(six); e, _ = stab_odo(six - s); row = e[M // 2 - 1]
    r = {"M": M, "L": Ls[M], "pred": pred(row), "row_head": ''.join(map(str, row[:60]))}
    with open('out/lfeat.jsonl', 'a') as f: f.write(json.dumps(r) + '\n')
    print(M, r['L'], r['pred'], flush=True)
