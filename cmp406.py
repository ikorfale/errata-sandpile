"""#406 prereg check: per N, families reached at cap 10 vs cap 20, split by D10 / D20\\D10 (ceiling406.py sets)."""
import runpy, sys, io, contextlib
def det(p):
    sys.argv = ['ceiling406.py', str(p)]
    with contextlib.redirect_stdout(io.StringIO()): g = runpy.run_path('ceiling406.py', run_name='x')
    return g['det_f']
def reached(f):
    return {(int(l.split()[1]), eval(l.split('parents ')[1].split(':')[0])) for l in open(f) if ' reached 0 ' not in l}
NS = sys.argv[1:]
D10, D20 = det(10), det(20)
print(f"|D10|={len(D10)} |D20|={len(D20)} D10<=D20 {D10 <= D20}")
for n in NS:
    a, b = reached(f'out/parents400_{n}_W5_4phase.txt'), reached(f'out/parents400_{n}_W5_P20_4phase.txt')
    ia, ib = a & D10, b & D10
    extra = b - a
    print(f"N={n} cap10 {len(a)} cap20 {len(b)} | in D10: {len(ia)} vs {len(ib)} same={ia == ib} | cap10-only {sorted(a-b)} | cap20-only {sorted(extra)} all in D20\\D10: {all(f in D20 and f not in D10 for f in extra)}")
