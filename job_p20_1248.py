"""Addendum 13 of PREREG-near1024-2048: row N = 1248 at cap 20, four phases (midpoint of 1217-1280: a split of 64/73/76
refutes a joint onset). Identity by odo_warm.py if missing, then the cap-20 scan as in job_p20_1296.py."""
import os, runpy, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
if not os.path.exists('out/odo_1248.npz'):
    subprocess.run([sys.executable, '-u', 'odo_warm.py', '1248'], check=True)
sys.argv = ['job406.py', '1248']
runpy.run_path('job406.py', run_name='__main__')
