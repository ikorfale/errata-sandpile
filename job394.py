"""#394 lab job: time the C stabiliser at N=1536 (identity + checks), to estimate whether N=2048 fits a 4-hour job;
then side-5 windows (periods <= 10) on the 1536 identity to see whether the curvature-36 wall circles appear."""
import os, subprocess, sys, time
os.chdir(os.path.dirname(os.path.abspath(__file__)))
t0 = time.time()
subprocess.run([sys.executable, 'odo_fast.py', '1536'], check=True)
print(f"identity 1536 wall time {time.time() - t0:.0f}s", flush=True)
out = 'out/hess_small_1536_W5_P10.txt'
with open(out, 'w') as f:
    subprocess.run([sys.executable, 'hess_small.py', '1536', '5', '10', 'full'], check=True, stdout=f)
print(open(out).read()[:4000], flush=True)
print(f"total wall time {time.time() - t0:.0f}s", flush=True)
