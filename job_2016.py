"""Paired row for the 2048 test (Fable 21.10, after zenith 97461): N = 2016 at cap 20 (switched from cap 10 by
addendum 3, before any 2016 or 2048 row existed), so the pair rule compares cap-20 totals. See PREREG-near1024-2048.md."""
import os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run([sys.executable, "job406.py", "2016"], check=True)
