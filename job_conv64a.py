"""PREREG-conv64.md part A: score archived rows with the frozen 2016 templates (no new scans)."""
import os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
for grp in (['1024', '1088', '1152', '1536'], ['2048'], ['1008', '1012', '1296'], ['512', '640', '768', '896', '960']):
    subprocess.run([sys.executable, '-u', 'tpl462.py', '11', '10', '2016'] + grp, check=False)
