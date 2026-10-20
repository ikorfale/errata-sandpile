"""#391 lab job: identity at N=1024 in C (odo_fast.py), then exact Hessians: W=12 periods up to 40, W=6 periods up to 20."""
import os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run([sys.executable, 'odo_fast.py', '1024'], check=True)
for W, P in ((6, 20), (12, 40)):
    out = f'exact_hess_1024_W{W}_P{P}_full.txt'
    with open(out, 'w') as f:
        subprocess.run([sys.executable, 'exact_hess2.py', '1024', str(W), str(P), 'full'], check=True, stdout=f)
    print(open(out).read(), flush=True)
