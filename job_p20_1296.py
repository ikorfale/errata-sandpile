"""Addendum 12 of PREREG-near1024-2048 (absence check): 64/73/76 absent at 1296 cap 10, so re-scan 1296 at period cap 20
(identity cached), four phases, before any of them is scored absent."""
import os, runpy, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.argv = ['job406.py', '1296']
runpy.run_path('job406.py', run_name='__main__')
