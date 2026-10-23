"""PREREG-rows465.md: rows 1232 and 1252 (same pipeline as job_p20_rows.py)."""
import os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run([sys.executable, '-u', 'job_p20_rows.py', '1232', '1252'], check=True)
