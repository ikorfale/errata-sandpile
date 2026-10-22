"""Presence-monotonicity flag over all scored rows (side 5, cap 10, four phases), suggested by zenith-claude on the board
(22.10): a family that is absent-present-absent or present-absent-present across N blinks, and the endpoint gate
core <= S <= union cannot see it. Family = (curvature, parents); present = reached > 0. Usage: python3 monotone.py [N ...]"""
import glob, re, sys
def fams(n):
    out = {}
    for l in open(f'out/parents400_{n}_W5_4phase.txt'):
        m = re.match(r'curvature\s+(\d+) parents (\([^)]*\)): reached (\d+) of', l)
        if m: out[(int(m[1]), m[2])] = int(m[3]) > 0
    return out
ns = sorted(int(re.search(r'_(\d+)_W5_4phase', p)[1]) for p in glob.glob('out/parents400_*_W5_4phase.txt'))
if sys.argv[1:]: ns = sorted(int(a) for a in sys.argv[1:])
rows = {n: fams(n) for n in ns}; keys = sorted(set().union(*[set(r) for r in rows.values()]))
flagged = 0
for k in keys:
    v = ''.join('1' if rows[n].get(k) else '0' for n in ns)
    if re.search('10+1', v): flagged += 1; print(f'BLINK     curvature {k[0]:>3} parents {k[1]:<14} {v}')   # present-absent-present
    elif re.fullmatch('0+1+0+', v): print(f'transient curvature {k[0]:>3} parents {k[1]:<14} {v}')    # one interval, enters then leaves
print(f'rows {ns}\n{len(keys)} families, {flagged} blinking (present-absent-present in N order); "absent" = the cap-10 search did not reach it, not a proof')
