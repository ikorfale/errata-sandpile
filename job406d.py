import os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run([sys.executable, "job406.py"] + "2048".split(), check=True)
