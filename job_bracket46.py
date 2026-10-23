"""zenith 99936: two-sided footprint test at 1248, control 1280. allpairs445 with window side 4 (more sensitive, can only
gain hits) and side 6 (can only lose). For K = 40..88 at 1248: present at side 4 and absent at side 6 = the dip is the
footprint's; absent even at side 4 = points at the identity; present at side 6 = the side-5 scan is wrong. Only side-4
windows whose key is on a known side-5 family circle count (allpairs keys against the same circle catalog)."""
import os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
for n in ('1248', '1280'):
    for w in ('4', '6'):
        subprocess.run([sys.executable, '-u', 'allpairs445.py', n, w, '20'], check=True)
