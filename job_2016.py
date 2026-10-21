"""Paired row for the 2048 test (Fable 21.10, after zenith 97461): N = 2016 at cap 10, four phases.
Families at 2048 and absent at 2016 >= 8 -> step at the power of two; see PREREG-near1024-2048.md addendum 2."""
import os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run([sys.executable, 'job_near1024.py', '2016'], check=True)
