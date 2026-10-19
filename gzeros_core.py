import numpy as np

def stab_odo(z):
    z = z.astype(np.int64).copy(); u = np.zeros_like(z)
    while True:
        t = z >> 2
        if not t.any(): return z, u
        u += t; z -= 4 * t
        z[1:, :] += t[:-1, :]; z[:-1, :] += t[1:, :]
        z[:, 1:] += t[:, :-1]; z[:, :-1] += t[:, 1:]

