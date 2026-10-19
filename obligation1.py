"""obligation1.py: check the one open piece of the odd-grid cross theorem on every even grid M.

w = u1 - u2 (odometers of stab(6) and of stab(6 - stab(6))), so identity(M) = L w. Twin row r = w[m-1] (= w[m]).
Inserted row r' = r[:m] + [r[m-1]] + r[m:] on the odd grid M+1. Obligation (1): d(j) = 2r'(j) - r'(j-1) - r'(j+1)
(0 outside) lies in {1, 2, 3} for every j != m. If it does, identity(M+1) is identity(M) cut open with the cross
inserted (recurrence proof: notes/recurrence-proof.md). For M <= 64 the conclusion is also checked directly.
usage: python obligation1.py A B   (even M from A to B) -> appends JSON lines to out/obligation1.jsonl"""
import sys, json
import numpy as np
from identity import identity

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
    s, u1 = stab_odo(six); e, u2 = stab_odo(six - s)
    w = u1 - u2; m = M // 2
    twin = bool((w[m - 1] == w[m]).all())
    r = w[m - 1]; rp = np.concatenate([r[:m], [r[m - 1]], r[m:]])
    pad = np.concatenate([[0], rp, [0]])
    d = 2 * rp - pad[:-2] - pad[2:]
    arm = np.delete(d, m)
    row = {"M": M, "twin": twin, "centre": int(d[m]), "arm_min": int(arm.min()), "arm_max": int(arm.max()),
           "ones": int((arm == 1).sum()), "ok": twin and int(arm.min()) >= 1 and int(arm.max()) <= 3}
    if M <= 64:
        wp = np.insert(np.insert(w, m, w[m - 1], axis=0), m, np.insert(w, m, w[m - 1], axis=0)[:, m - 1], axis=1)
        P = np.pad(wp, 1)
        ep = 4 * wp - P[:-2, 1:-1] - P[2:, 1:-1] - P[1:-1, :-2] - P[1:-1, 2:]
        row["direct"] = bool((ep == identity(M + 1)[0]).all())
    with open("out/obligation1.jsonl", "a") as f: f.write(json.dumps(row) + "\n")
    print(row, flush=True)
