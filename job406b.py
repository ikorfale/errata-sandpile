import os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run([sys.executable, "job406.py"] + "1088 1152 1216 1280 1536".split(), check=True)
