"""zenith 99899: is the 1248 dip narrow in N? Rows 1240 and 1256 at cap 20, four phases, same pipeline as job_p20_1248.py
(identity by odo_warm.py if missing, then job406.py). Rows from argv; registered on the board before this job ran."""
import os, runpy, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
for n in sys.argv[1:] or ['1240', '1256']:
    if not os.path.exists(f'out/odo_{n}.npz'):
        subprocess.run([sys.executable, '-u', 'odo_warm.py', n], check=True)
    subprocess.run([sys.executable, '-u', 'job406.py', n], check=True)
