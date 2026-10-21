"""Which 2 of 4 circles per newly reached family are hit at N=1536 (b and a coordinates)."""
import sys, numpy as np
exec(open('parents81.py').read().split('fam = collections')[0].replace("want = {int(k) for k in sys.argv[2:]}","want={52,73,76,81,25}"))
rs=set()
for row in np.load('out/hess_small_1536_5_10_full.npy'):
    rr=row[2]+row[4]-2
    if rr<=1e-9: continue
    rs.add((round((row[2]-row[4])%2,6),round((2*row[3])%2,6),round(rr,6)))
for c in sorted(circ, key=lambda c:(round(1/c[2]),c)):
    k=round(1/c[2])
    if k in want and (k!=81 or parents(*c)==(4,9,28)) and k!=25: print(k, parents(*c), c[:2], 'HIT' if c in rs else '-')
