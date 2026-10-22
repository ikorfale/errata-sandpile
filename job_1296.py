"""Addendum 11 of PREREG-near1024-2048: row N = 1296 at cap 10, four phases (is the 1280 dropout of 64/73/76 isolated?).
Same pipeline as job_1004.py."""
import os, runpy, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__)); os.chdir(here)
for n in ('1296',):
    if not os.path.exists(f'out/odo_{n}.npz'):
        subprocess.run([sys.executable, '-u', 'odo_warm.py', n], check=True)
    sys.argv = ['job_near1024.py', n]
    runpy.run_path('job_near1024.py', run_name='__main__')
