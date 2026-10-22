"""#406 lab job: side-5 scan at period cap 20 (ceiling 155 families of 189, ceiling406.py) in four phases, then
families against the curvature<=400 catalog. Cap 10 could only ever show 32 families, so the 1024 excess could not be
compared with a repeat at 2048. usage: job406.py N [N ...]"""
import os, subprocess, sys, time
import numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.makedirs('scratch', exist_ok=True)
for n in sys.argv[1:]:
    t0 = time.time()
    for oi, oj in ((0, 0), (0, 1), (1, 0), (1, 1)):
        f = f'out/hess_s_{n}_5_20_o{oi}{oj}.npy'
        if not os.path.exists(f): subprocess.run([sys.executable, 'hess_stream.py', n, '5', '20', str(oi), str(oj)], check=True)
    u = f'scratch/job406_{n}.npy'
    np.save(u, np.concatenate([np.load(f'out/hess_s_{n}_5_20_o{p}.npy') for p in ('00', '01', '10', '11')]))
    with open(f'out/parents400_{n}_W5_P20_4phase.txt', 'w') as f:
        subprocess.run([sys.executable, 'parents81.py', u] + [str(k) for k in range(1, 401)], check=True, stdout=f)
    os.remove(u)  # scratch was in /tmp = RAM on this host; 570 MB of leftovers OOM-killed other work 22.10
    fams = sum(1 for l in open(f'out/parents400_{n}_W5_P20_4phase.txt') if ' reached 0 ' not in l)
    print(f"N={n} P20 families {fams} wall {time.time() - t0:.0f}s", flush=True)
