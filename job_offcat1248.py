"""Fable 23.10 on the zenith 99936 bracket: 0 hits for K=52/57/81 at 1248 is only 'absent' if no m=1 window carries
s2 near 1/52, 1/57, 1/81 with a key OFF the circle catalog. Count off-catalog m=1 windows by round(1/s2) at 1248 (W4, W5)
and the 1280 control (W4, W5; zenith 100221: background at the same sides, neighbouring bins read from the full histogram). Writes results/allpairs445_N[_W4]_off.txt; the bracket files are not overwritten."""
import os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
env = dict(os.environ, OFFCAT='1')
for n, w in (('1248', '4'), ('1248', '5'), ('1280', '4'), ('1280', '5')):
    subprocess.run([sys.executable, '-u', 'allpairs445.py', n, w, '20'], check=True, env=env)
