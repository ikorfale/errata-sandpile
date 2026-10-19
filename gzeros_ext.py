"""gzeros.py: on even M, the midline step g = w[m-1] - w[m-2] (w = u1 - u2) and its zero blocks (glitchfox #94555).
Records for each M: values of g, L = length of the zero block at each end, whether zeros are only 0..L-1 and M-L..M-1.
usage: python gzeros_ext.py A B -> appends JSON lines to out/gzeros_ext.jsonl"""
import sys, json
import numpy as np

def stab_odo(z):
    z = z.astype(np.int64).copy(); u = np.zeros_like(z)
    while True:
        t = z >> 2
        if not t.any(): return z, u
        u += t; z -= 4 * t
        z[1:, :] += t[:-1, :]; z[:-1, :] += t[1:, :]
        z[:, 1:] += t[:, :-1]; z[:, :-1] += t[:, 1:]

for M in range(int(sys.argv[1]), int(sys.argv[2]) + 1, 2):
    six = np.full((M, M), 6, np.int64)
    s, u1 = stab_odo(six); _, u2 = stab_odo(six - s)
    w = u1 - u2; m = M // 2
    g = w[m - 1] - w[m - 2]
    L = int(np.argmax(g != 0)) if g[0] == 0 else 0
    ind = np.r_[np.zeros(L), np.ones(M - 2 * L), np.zeros(L)]
    row = {"M": M, "values": sorted(set(int(x) for x in g)), "L": L, "indicator": bool((g == ind).all())}
    with open("out/gzeros_ext.jsonl", "a") as f: f.write(json.dumps(row) + "\n")
    print(row, flush=True)
