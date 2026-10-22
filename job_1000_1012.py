"""Addendum 7 of PREREG-near1024-2048: rows N = 1000 (residue control) and 1012 at cap 10, four phases.
Identity by odo_warm.py (certified by the burning test), then the same pipeline as job_near1024.py."""
import os, runpy, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__)); os.chdir(here)
for n in ('1000', '1012'):
    if not os.path.exists(f'out/odo_{n}.npz'):
        subprocess.run([sys.executable, '-u', 'odo_warm.py', n], check=True)
    sys.argv = ['job_near1024.py', n]
    runpy.run_path('job_near1024.py', run_name='__main__')
