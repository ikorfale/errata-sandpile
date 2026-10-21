"""#401 lab job: is side-5 reach monotone in N? Identity + centred side-5 scan + reach81 at N = 896 and 1280,
to place 1024 (75 of 99) and 1536 (55) among neighbours (512: 9, 640: 15, 768: 21)."""
import os, subprocess, sys, time
os.chdir(os.path.dirname(os.path.abspath(__file__)))
for n in ('896', '1280'):
    t0 = time.time()
    if not os.path.exists(f'out/odo_{n}.npz'): subprocess.run([sys.executable, 'odo_fast.py', n], check=True)
    with open(f'out/hess_small_{n}_W5_P10.txt', 'w') as f:
        subprocess.run([sys.executable, 'hess_small.py', n, '5', '10', 'full'], check=True, stdout=f)
    with open(f'out/reach81_{n}_W5.txt', 'w') as f:
        subprocess.run([sys.executable, 'reach81.py', f'out/hess_small_{n}_5_10_full.npy'], check=True, stdout=f)
    print(open(f'out/reach81_{n}_W5.txt').read(), f"N={n} wall time {time.time() - t0:.0f}s", flush=True)
