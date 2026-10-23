"""Circle-to-orbit mapping for the allpairs445 rows (zenith 99737: "every orbit that shows up shows up complete";
multiples of 4 fit complete orbits but do not prove them). D4 acts on the class key (u, v, s) = ((a-c) mod 2,
(2b) mod 2, a+c-2) through a Klein four-group: a<->c sends u -> 2-u, b -> -b sends v -> 2-v, the rotation does both,
s is fixed (Fable 23.10). Distances on u, v are circular mod 2 (a rounded 1e-12 next to 0 must meet its image next to 2).
For each N and K: the catalogue's orbits, which of them are seen, and whether every seen circle's orbit is seen whole.
NOTE (23.10, board 99859): 'partial orbits 0' is FORCED by symmetry (e and its odometer are D4-invariant, the window set
is D4-closed, the instrument equivariant), so it only checks the code's equivariance, not a property of e. Non-forced:
first-appearance N per orbit, persistence across N, count scaling.
Usage: orbits445.py [--verified] N [N ...]  (reads results/allpairs445_N_circles.json, or _circles_verified.json:
the seen set from full-set verified m = 1 windows only, zenith 99841)"""
import collections, json, sys
src = open('parents81.py').read().split('fam = collections.Counter()')[0].replace('want = {int(k) for k in sys.argv[2:]}', 'want = set()')
ns = {'__name__': 'x'}; sv = sys.argv; sys.argv = sv[:1]; exec(src, ns); sys.argv = sv; circ = ns['circ']
EPS = 1e-5
def cd(x, y): d = abs(x - y) % 2; return min(d, 2 - d)
def same(k, m): return cd(k[0], m[0]) < EPS and cd(k[1], m[1]) < EPS and abs(k[2] - m[2]) < EPS
def images(k): u, v, s = k; return [(u, v, s), ((2 - u) % 2, v, s), (u, (2 - v) % 2, s), ((2 - u) % 2, (2 - v) % 2, s)]
def orbit_id(k, cat):  # the catalogue circles in k's orbit, as a frozenset of catalogue keys
    return frozenset(c for c in cat if any(same(c, im) for im in images(k)))
cat_by_K = collections.defaultdict(list)
for c in circ:
    if c[2] > 0: cat_by_K[round(1 / c[2])].append(tuple(c))
args = sys.argv[1:]; VF = '--verified' in args; args = [a for a in args if a != '--verified']
for N in args:
    seen = json.load(open(f'results/allpairs445_{N}_circles' + ('_verified' if VF else '') + '.json'))
    print(f"N={N}" + (" (verified windows only)" if VF else " (all m = 1 windows)"))
    for K in sorted(map(int, seen)):
        cat = cat_by_K[K]; S = [tuple(x) for x in seen[str(K)]]
        orbs = {orbit_id(c, cat) for c in cat}
        not_in_cat = [k for k in S if not any(same(k, c) for c in cat)]
        seen_orbs = {orbit_id(k, cat) for k in S}
        partial = [o for o in seen_orbs if not all(any(same(c, k) for k in S) for c in o)]
        print(f"  K={K}: catalogue {len(cat)} circles in {len(orbs)} orbits (sizes {sorted(len(o) for o in orbs)}); "
              f"seen {len(S)} circles in {len(seen_orbs)} orbits; partial orbits {len(partial)}"
              + (f" {[sorted(tuple(round(float(x), 4) for x in c) for c in o) for o in partial]}" if partial else "") + (f"; NOT IN CATALOGUE {not_in_cat}" if not_in_cat else ""))
