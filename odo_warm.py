"""odo_warm.py (22.10, method from Fable): the odo_fast.py identity, warm-started and self-certified.
usage: python odo_warm.py N [c1=0.95] [c2=0.82]  -> out/odo_N.npz (refuses to overwrite one that differs)
Solves N' = N/2 cold, then for each stage starts from g = floor(c * 4 * resample(u'_stage)), z0 = eta + L g, and
stabilises legally (c/stabw.c: only z >= 4 topples). Least action: result == cold result iff g <= true odometer;
certificate: the final configuration passes Dhar's burning test (unique recurrent per class). On a failed
certificate c is lowered and the stage rerun. Stage 2's scaled guess overshoots the true u2 by 12-20% at
N = 128-256 (stage 1 only ~3%), hence the separate, lower c2."""
import sys, os, time, ctypes, numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
lib = ctypes.CDLL(os.path.abspath('c/libstabw.so')); P = ctypes.POINTER(ctypes.c_int64)
lib.stab_odo.restype = ctypes.c_long; lib.burn.restype = ctypes.c_long
def stab(z, g=None):
    z = np.ascontiguousarray(z, np.int64).copy(); u = np.zeros_like(z) if g is None else np.ascontiguousarray(g, np.int64).copy()
    s = lib.stab_odo(z.ctypes.data_as(P), u.ctypes.data_as(P), z.shape[0]); return z, u, s
def burns(z): return lib.burn(np.ascontiguousarray(z, np.int64).ctypes.data_as(P), z.shape[0]) == z.size
def lap(v):
    p = np.pad(v, 1); return p[:-2, 1:-1] + p[2:, 1:-1] + p[1:-1, :-2] + p[1:-1, 2:] - 4 * v
def resample(u, n):  # bilinear on [sink, box, sink], sink value 0
    m = u.shape[0]; pad = np.pad(u.astype(float), 1); src = np.arange(-1, m + 1)
    x = (np.arange(n) + 1) * (m + 1) / (n + 1) - 1
    rows = np.array([np.interp(x, src, r) for r in pad]); return np.array([np.interp(x, src, c) for c in rows.T]).T
def warm(eta, uprime, n, c, stage):
    while True:
        g = np.floor(c * (n / uprime.shape[0]) ** 2 * resample(uprime, n)).astype(np.int64); g[g < 0] = 0
        z, u, s = stab(eta + lap(g), g)
        if z.min() >= 0 and z.max() <= 3 and burns(z): return z, u, s, c
        print(f"  stage {stage}: certificate failed at c={c:.2f}, lowering", flush=True); c = round(c - 0.03, 2)
N = int(sys.argv[1]); c1 = float(sys.argv[2]) if len(sys.argv) > 2 else 0.95; c2 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.82; t0 = time.time()
if N % 2: sys.exit("N must be even (N' = N/2)")
m = N // 2
s6m, u1m, _ = stab(np.full((m, m), 6, np.int64)); em, u2m, _ = stab(6 - s6m)
if not os.path.exists(f'out/odo_{m}.npz'):  # the cold half-size solve is a full cold result: keep it
    np.savez_compressed(f'out/odo_{m}.npz', v=u2m - u1m, e=em); print('wrote', f'out/odo_{m}.npz (cold)', flush=True)
t1 = time.time()
s6, u1, a, c1 = warm(np.full((N, N), 6, np.int64), u1m, N, c1, 1)
e, u2, b, c2 = warm(6 - s6, u2m, N, c2, 2)
v = u2 - u1; ee, _, _ = stab(2 * e)
print(f"N={N} warm {time.time() - t0:.1f}s (N'={m} cold {t1 - t0:.1f}s) sweeps {a}+{b} c {c1:.2f}/{c2:.2f} burn ok  "
      f"L v == e: {bool((lap(v) == e).all())}  e+e=e: {bool((ee == e).all())}  max e {e.max()}", flush=True)
f = f'out/odo_{N}.npz'
if os.path.exists(f):
    z = np.load(f); print("matches existing", f, bool((z['v'] == v).all() and (z['e'] == e).all()))
else: np.savez_compressed(f, v=v, e=e); print("wrote", f)
