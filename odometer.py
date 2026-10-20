"""odometer.py (#367): a potential whose Laplacian IS the identity, and its local Hessians.

stab(z) with odometer u (u[x] = times x toppled) gives  stab(z) = z + L u,  L = grid Laplacian, sink outside.
u1 = odometer of stab(6), u2 = odometer of stab(6 - stab(6)) = e. Then
    e = (6 - stab6) + L u2 = 6 - (6 + L u1) + L u2   =>   L (u2 - u1) = e   exactly.
So v = u2 - u1 is an integer potential with L v = e. On a periodic patch of e, v ~ 1/2 x'Ax + b.x + periodic,
trace(A) = mean height of the patch. Levine-Pegden-Smart: the A of periodic sandpile patterns lie in an
Apollonian structure. Here: compute v, check L v == e exactly, fit A on sliding windows (least squares, the
periodic part averages out over a window much larger than the period), and dump (x, y, a, b, c, rms) rows.
usage: python odometer.py N [W] -> out/odo_N.npz, out/hess_N.npy"""
import sys, time
import numpy as np

def stab_odo(z):
    z = z.astype(np.int64).copy(); u = np.zeros_like(z)
    while True:
        t = z >> 2
        if not t.any(): return z, u
        u += t; z -= 4 * t
        z[1:, :] += t[:-1, :]; z[:-1, :] += t[1:, :]
        z[:, 1:] += t[:, :-1]; z[:, :-1] += t[:, 1:]

def lap(v):
    p = np.pad(v, 1)
    return p[:-2, 1:-1] + p[2:, 1:-1] + p[1:-1, :-2] + p[1:-1, 2:] - 4 * v

N = int(sys.argv[1]); W = int(sys.argv[2]) if len(sys.argv) > 2 else max(8, N // 16)
t0 = time.time()
six = np.full((N, N), 6, np.int64)
s6, u1 = stab_odo(six); e, u2 = stab_odo(6 - s6); v = u2 - u1
ref = np.load(f'out/identity_{N}.npy') if __import__('os').path.exists(f'out/identity_{N}.npy') else None
print(f"N={N} stabilised in {time.time() - t0:.1f}s  e matches identity_{N}.npy: {None if ref is None else bool((ref == e).all())}")
print(f"L v == e exactly: {bool((lap(v) == e).all())}   v range {v.min()}..{v.max()}  mean e {e.mean():.4f}")
# local quadratic fit: v ~ c0 + bx x + by y + a x^2/2 + b x y + c y^2/2 on WxW windows, stride W/2
yy, xx = np.mgrid[0:W, 0:W].astype(float); xx -= xx.mean(); yy -= yy.mean()
X = np.stack([np.ones(W * W), xx.ravel(), yy.ravel(), xx.ravel()**2 / 2, (xx * yy).ravel(), yy.ravel()**2 / 2], 1)
pinv = np.linalg.pinv(X)
rows = []
for i in range(0, N - W + 1, W // 2):
    for j in range(0, N - W + 1, W // 2):
        win = v[i:i + W, j:j + W].astype(float).ravel(); co = pinv @ win
        res = win - X @ co; m = e[i:i + W, j:j + W].mean()
        rows.append((i + W / 2, j + W / 2, co[3], co[4], co[5], np.sqrt((res**2).mean()), m))
H = np.array(rows)
np.savez_compressed(f'out/odo_{N}.npz', v=v, e=e); np.save(f'out/hess_{N}.npy', H)
print(f"windows {len(H)} (W={W})  trace(A) - mean(e) on window: max |diff| {np.abs(H[:, 2] + H[:, 4] - H[:, 6]).max():.3f}")
print(f"time {time.time() - t0:.1f}s")
