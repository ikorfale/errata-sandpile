"""identity.py: the identity element of the abelian sandpile group on an NxN grid (sink = the boundary).

e = stab(6 - stab(6)), where 6 is the all-sixes configuration (6 = 2 * max stable height).
Stabilisation topples every site with >= 4 grains, in parallel and in bulk (z // 4 topplings at once);
the abelian property makes the final configuration independent of order, so bulk toppling is exact.

Checks (the picture is only shown if they pass):
  1. e is stable (all heights 0..3);
  2. e + e stabilises to e;
  3. e + c stabilises to c for random recurrent c (c = stab(random stable + 3 everywhere) is recurrent);
  4. e + 0 is NOT required (0 is not recurrent) -- instead check e is recurrent by the burning test.

usage: python identity.py N [N ...]    writes out/identity_N.npy and prints checks + timing.
"""
import sys, time, os
import numpy as np

def stab(z):
    z = z.astype(np.int64).copy()
    it = 0
    while True:
        t = z >> 2                      # topplings this round (z // 4)
        if not t.any():
            return z, it
        z -= 4 * t
        z[1:, :] += t[:-1, :]; z[:-1, :] += t[1:, :]
        z[:, 1:] += t[:, :-1]; z[:, :-1] += t[:, 1:]
        it += 1

def burning_ok(z):
    """Dhar's burning test: add 1 grain per boundary edge; z is recurrent iff every site topples exactly once."""
    n = z.shape[0]
    b = np.zeros_like(z)
    b[0, :] += 1; b[-1, :] += 1; b[:, 0] += 1; b[:, -1] += 1
    w = z + b
    count = np.zeros_like(z)
    while True:
        t = w >> 2
        if not t.any():
            break
        count += t
        w -= 4 * t
        w[1:, :] += t[:-1, :]; w[:-1, :] += t[1:, :]
        w[:, 1:] += t[:, :-1]; w[:, :-1] += t[:, 1:]
    return bool((count == 1).all() and (w == z).all())

def identity(n):
    six = np.full((n, n), 6, np.int64)
    s, i1 = stab(six)
    e, i2 = stab(six - s)
    return e, i1 + i2

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    rng = np.random.default_rng(343)
    for n in map(int, sys.argv[1:]):
        t0 = time.time()
        e, its = identity(n)
        dt = time.time() - t0
        ok_stable = bool(((e >= 0) & (e <= 3)).all())
        ok_ee = bool((stab(e + e)[0] == e).all())
        ok_ec = True
        for _ in range(3):
            c = stab(rng.integers(0, 4, (n, n)) + 3)[0]
            ok_ec &= bool((stab(e + c)[0] == c).all())
        ok_burn = burning_ok(e)
        np.save(f"out/identity_{n}.npy", e.astype(np.int8))
        counts = np.bincount(e.ravel(), minlength=4)
        print(f"N={n} rounds={its} time={dt:.1f}s stable={ok_stable} e+e=e:{ok_ee} e+c=c(3 random):{ok_ec} "
              f"recurrent(burning):{ok_burn} heights0-3={counts.tolist()} sha256={__import__('hashlib').sha256(e.astype(np.int8).tobytes()).hexdigest()[:16]}",
              flush=True)
