"""#406 check (Fable 21.10): is patch extent E vs reach 2R+W the reason families saturate?
Per distinct Hessian A in phase 00 at N=512 and 1024 (cap 20): R = max |p|,|q|,|p+q|,|p-q|;
E = bbox side (cells) of the largest 8-connected cluster of hit window centres (stride 2).
Predictions: seen at 512 iff E1024 > 2R+5; for both, E512 ~ E1024/2 - R - 2.5."""
import numpy as np
def label(g, structure=None):
    lab = np.zeros(g.shape, int); n = 0
    for s0 in zip(*np.nonzero(g)):
        if lab[s0]: continue
        n += 1; st = [s0]; lab[s0] = n
        while st:
            i, j = st.pop()
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    a, b = i + di, j + dj
                    if 0 <= a < g.shape[0] and 0 <= b < g.shape[1] and g[a, b] and not lab[a, b]:
                        lab[a, b] = n; st.append((a, b))
    return lab, n
def stats(N):
    r = np.load(f'out/hess_s_{N}_5_20_o00.npy')
    out = {}
    keys = np.round(r[:, 2:5], 6)
    for k in {tuple(x) for x in keys}:
        m = np.all(keys == k, axis=1); s = r[m]
        p, q = s[0, 5:7], s[0, 7:9]
        R = max(np.hypot(*v) for v in (p, q, p + q, p - q))
        gi = ((s[:, 0] - s[:, 0].min()) // 2).astype(int); gj = ((s[:, 1] - s[:, 1].min()) // 2).astype(int)
        g = np.zeros((gi.max() + 1, gj.max() + 1), bool); g[gi, gj] = True
        lab, n = label(g, structure=np.ones((3, 3)))
        best = 0
        for c in range(1, n + 1):
            ii, jj = np.nonzero(lab == c); best = max(best, 2 * (max(np.ptp(ii), np.ptp(jj)) + 1))
        out[k] = (R, best, int(m.sum()))
    return out
a, b = stats(512), stats(1024)
print(f"distinct A: 512 {len(a)}, 1024 {len(b)}")
print("A(11,12,22)            R    E1024 n1024 2R+5 pred512 seen512  E512  predE512")
hit = 0; tot = 0
for k in sorted(b, key=lambda k: b[k][0]):
    R, E, n = b[k]; pred = E > 2 * R + 5; seen = k in a
    tot += 1; hit += pred == seen
    e5 = a[k][1] if seen else '-'
    if 0: print(f"{str(k):22s} {R:5.1f} {E:6d} {n:5d} {2*R+5:5.1f} {str(pred):7s} {str(seen):7s} {e5!s:>5} {E/2-R-2.5:7.1f}")
print(f"presence prediction right on {hit} of {tot}")
only512 = [k for k in a if k not in b]; print("seen at 512 only:", len(only512))

# 2x2 and a no-mechanism control (best single cut on E1024 alone, which is fitted, so it is generous)
import itertools
ks = list(b); seen = np.array([k in a for k in ks]); E = np.array([b[k][1] for k in ks]); R = np.array([b[k][0] for k in ks])
pred = E > 2 * R + 5
print("2x2 pred/seen: TT %d TF %d FT %d FF %d" % ((pred & seen).sum(), (pred & ~seen).sum(), (~pred & seen).sum(), (~pred & ~seen).sum()))
best = max(((E > c) == seen).sum() for c in range(0, 120, 2)); print("control: best cut on E alone right on", best, "of", len(ks))
both = [k for k in ks if k in a]; x = np.array([b[k][1] / 2 - b[k][0] - 2.5 for k in both]); y = np.array([a[k][1] for k in both])
print("both seen: n %d, median |E512-pred| %.1f, corr %.2f; control E1024/2 median |err| %.1f" % (len(both), np.median(abs(y - x)), np.corrcoef(x, y)[0, 1], np.median(abs(y - np.array([b[k][1] / 2 for k in both])))))
