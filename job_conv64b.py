"""PREREG-conv64.md part B: fresh rows, same pipeline as job_p20_rows.py, then 2016-template scoring. Rows from argv."""
import os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
for n in sys.argv[1:]:
    if not os.path.exists(f'out/odo_{n}.npz'):
        subprocess.run([sys.executable, '-u', 'odo_warm.py', n], check=True)
    subprocess.run([sys.executable, '-u', 'job406.py', n], check=True)
    subprocess.run([sys.executable, '-u', 'tpl462.py', '11', '10', '2016', n], check=False)
