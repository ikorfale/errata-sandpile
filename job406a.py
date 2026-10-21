import os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run([sys.executable, "job406.py"] + "1024 512 640 768 896 960".split(), check=True)
