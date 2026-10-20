"""odo_fast.py (#391): same potential as odometer.py (v = u2 - u1, L v = e), stabilised in C (c/stab.c).
usage: python odo_fast.py N  -> out/odo_N.npz (refuses to overwrite one that differs)"""
import sys, os, time, ctypes, numpy as np
lib = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'c', 'libstab.so'))
lib.stab_odo.restype = ctypes.c_long
P = ctypes.POINTER(ctypes.c_int64)
def stab_odo(z):
    z = np.ascontiguousarray(z, np.int64).copy(); u = np.zeros_like(z)
    s = lib.stab_odo(z.ctypes.data_as(P), u.ctypes.data_as(P), z.shape[0]); return z, u, s
def lap(v):
    p = np.pad(v, 1); return p[:-2, 1:-1] + p[2:, 1:-1] + p[1:-1, :-2] + p[1:-1, 2:] - 4 * v
N = int(sys.argv[1]); t0 = time.time()
s6, u1, a = stab_odo(np.full((N, N), 6, np.int64)); e, u2, b = stab_odo(6 - s6); v = u2 - u1
ee, _, _ = stab_odo(2 * e)
print(f"N={N} {time.time() - t0:.1f}s sweeps {a}+{b}  L v == e: {bool((lap(v) == e).all())}  e+e=e: {bool((ee == e).all())}  max e {e.max()}", flush=True)
f = f'out/odo_{N}.npz'
if os.path.exists(f):
    z = np.load(f); print("matches existing", f, bool((z['v'] == v).all() and (z['e'] == e).all()))
else: np.savez_compressed(f, v=v, e=e); print("wrote", f)
