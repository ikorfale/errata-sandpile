"""Addendum 10 of PREREG-near1024-2048: re-scan 1008 and 1012 at period cap 20 (identities cached), four phases.
Tests the only load-bearing absence in the (1008, 1012] localisation (Fable's review, 22.10)."""
import os, runpy, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.argv = ['job406.py', '1008', '1012']
runpy.run_path('job406.py', run_name='__main__')
