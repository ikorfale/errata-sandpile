"""Is the 960 -> 1024 jump (8 -> 23 families) a step at 1024 or a gradual threshold? (Fable 21.10: 1016 separates them.)
Identity + side-5 cap-10 scan in four phases (hess_stream.py, checked to reproduce hess_small at PMAX 10) at N = 1016, 992."""
import os, subprocess, sys, time
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs('scratch', exist_ok=True)
for n in sys.argv[1:] or ['1016', '992']:
    t0 = time.time()
    if not os.path.exists(f'out/odo_{n}.npz'): subprocess.run([sys.executable, 'odo_fast.py', n], check=True)
    for oi, oj in ((0, 0), (0, 1), (1, 0), (1, 1)):
        if not os.path.exists(f'out/hess_s_{n}_5_10_o{oi}{oj}.npy'): subprocess.run([sys.executable, 'hess_stream.py', n, '5', '10', str(oi), str(oj)], check=True)
    u = f'scratch/jobnear_{n}.npy'
    np.save(u, np.concatenate([np.load(f'out/hess_s_{n}_5_10_o{p}.npy') for p in ('00', '01', '10', '11')]))
    with open(f'out/parents400_{n}_W5_4phase.txt', 'w') as f:
        subprocess.run([sys.executable, 'parents81.py', u] + [str(k) for k in range(1, 401)], check=True, stdout=f)
    os.remove(u)  # scratch was in /tmp = RAM on this host; 570 MB of leftovers OOM-killed other work 22.10
    fams = sum(1 for l in open(f'out/parents400_{n}_W5_4phase.txt') if ' reached 0 ' not in l)
    print(f"N={n} P10 families {fams} wall {time.time() - t0:.0f}s", flush=True)
