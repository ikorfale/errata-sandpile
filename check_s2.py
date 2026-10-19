"""check_s2.py A B: independent check of glitchfox 94706. With w = u1 - u2 (e = -Lap w), m = M/2, L from gzeros.jsonl:
identity e[m-2] - e[m-1] = s2 - 2 step + H(step) (H = standard 2nd diff, zero outside) on j < L-1, where step = w[m-1]-w[m-2], s2 = w[m-2]-w[m-3], H = horizontal 2nd diff;
classify sizes with L > 0 as type A (s2 = 1 on [0,L], 2 at L+1) or B (s2 = 0 on [0,L]) or other."""
import sys, json
import numpy as np
from gzeros_core import stab_odo
Ls = {json.loads(l)['M']: json.loads(l)['L'] for l in open('out/gzeros.jsonl')}
for M in range(int(sys.argv[1]), int(sys.argv[2]) + 1, 2):
    L = Ls[M]
    if L == 0: continue
    six = np.full((M, M), 6, np.int64)
    s, u1 = stab_odo(six); e, u2 = stab_odo(six - s); w = u1 - u2; m = M // 2
    lap = -4 * w; lap[1:] += w[:-1]; lap[:-1] += w[1:]; lap[:, 1:] += w[:, :-1]; lap[:, :-1] += w[:, 1:]
    assert (e == -lap).all()
    step = w[m-1] - w[m-2]; s2 = w[m-2] - w[m-3]
    H = np.zeros_like(step); H[1:-1] = step[:-2] - 2 * step[1:-1] + step[2:]
    H[0] = step[1] - 2 * step[0]; H[-1] = step[-2] - 2 * step[-1]  # zero outside the grid
    lhs = e[m-2] - e[m-1]; rhs = s2 - 2 * step + H  # H = standard 2nd difference; glitchfox writes -H for the same term
    ok = bool((lhs[:L-1] == rhs[:L-1]).all()); full = bool((lhs == rhs).all())
    head = s2[:L+2]
    typ = 'A' if (head[:L+1] == 1).all() and head[L+1] == 2 else ('B' if (head[:L+1] == 0).all() else 'other')
    print(json.dumps({"M": M, "L": L, "identity_j<L-1": ok, "identity_all_j": full, "type": typ,
                      "step_ok": bool((step[:L] == 0).all() and (step[L:M-L] == 1).all()),
                      "s2": ''.join(map(str, head)), "e_m1": ''.join(map(str, e[m-1][:L+1])), "e_m2": ''.join(map(str, e[m-2][:L+2]))}), flush=True)
