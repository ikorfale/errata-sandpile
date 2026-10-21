"""PREREG-near1024-2048 result section: localise the 992 -> 1016 jump with one row at N = 1008 (cap 10, four phases)."""
import os, runpy, sys
sys.argv = ['job_near1024.py', '1008']
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'job_near1024.py'), run_name='__main__')
