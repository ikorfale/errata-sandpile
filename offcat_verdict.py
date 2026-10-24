"""Verdict for the 1248 off-catalog bracket, rule fixed in board post 100231 before the job ran (zenith 100221/100246):
bands 50-54, 55-59, 79-83 of round(1/s2), off-catalog m=1 windows, per side. Reading 2 stands if at both sides every
1248 band <= the 1280 band; key shift if any 1248 band has >= 5 windows and >= 2x the 1280 count; else reported as is."""
import ast, re
B = ((50, 54), (55, 59), (79, 83)); F = lambda n, w: f'results/allpairs445_{n}{"_W4" if w == 4 else ""}_off.txt'
def read(n, w):
    t = open(F(n, w)).read()
    m1 = int(re.search(r'by multiplicity: \{1: (\d+)', t).group(1))
    h = ast.literal_eval(re.search(r'off-catalog m=1 windows with s2 > 0.*?: (\{.*\})', t).group(1))
    return m1, h, [sum(v[0] for k, v in h.items() if a <= k <= b) for a, b in B]
stand, shift = True, False
for w in (4, 5):
    (m8, h8, b8), (m0, h0, b0) = read(1248, w), read(1280, w)
    print(f'W{w}: m=1 windows 1248 {m8}, 1280 {m0}, ratio {m0 / m8:.4f} (area ratio {(1280 / 1248) ** 2:.4f})')
    print(f'W{w}: off-catalog histogram 1248 {h8}\nW{w}: off-catalog histogram 1280 {h0}')
    print(f'W{w}: bands {B}: 1248 {b8}, 1280 {b0}')
    stand &= all(x <= y for x, y in zip(b8, b0)); shift |= any(x >= 5 and x >= 2 * y for x, y in zip(b8, b0))
print('verdict:', 'key shift' if shift else 'reading 2 stands' if stand else 'neither: reported as is')
