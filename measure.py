"""measure.py: for every N in range, the exact identity e_N; record mean height, height counts, and the side of the
largest centred square matching the pattern: all 2s, and for odd N a cross of 1s with 0 at the centre (k has N's parity).
Dhar et al. 1995 conjectured a central square of 2s on square boxes (open as of Kaiser-Sava-Huss-Uberbacher 2026).
usage: python measure.py A B  -> appends JSON lines to out/series.jsonl"""
import sys, json, hashlib
import numpy as np
from identity import identity

def pattern(n):
    """2 everywhere; for odd N the middle row and column are 1 and the centre is 0 (seen at N=21, 99)."""
    t = np.full((n, n), 2)
    if n % 2:
        c = n // 2; t[c, :] = 1; t[:, c] = 1; t[c, c] = 0
    return t

def central_two_square(e):
    n = e.shape[0]; best = 0; t = pattern(n)
    for k in range(n % 2 or 2, n + 1, 2):
        a = (n - k) // 2
        if (e[a:a + k, a:a + k] == t[a:a + k, a:a + k]).all(): best = k
        else: break
    return best

for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    e, its = identity(n)
    c = np.bincount(e.ravel(), minlength=4)
    row = {"N": n, "mean": float(e.mean()), "counts": c.tolist(), "square2": central_two_square(e), "rounds": its,
           "sha256": hashlib.sha256(e.astype(np.int8).tobytes()).hexdigest()}
    with open("out/series.jsonl", "a") as f: f.write(json.dumps(row) + "\n")
    print(n, row["mean"], row["square2"], flush=True)
