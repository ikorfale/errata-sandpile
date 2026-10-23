"""#439 check 2 (Fable): rebuild each parents400 summary from its four kept scan arrays and compare with the summary's
sha256 in out/MANIFEST.tsv. Same path as job406.py / job_near1024.py: concatenate o00, o01, o10, o11, run parents81.py
against curvatures 1..400. The scratch file lives in scratch/ (never /tmp: RAM on this host) and is removed.
Usage: python3 verify2.py [N ...]   -> one line per summary: MATCH / DIFFER / SKIP (a phase not kept)"""
import csv, hashlib, os, subprocess, sys, collections
import numpy as np
os.makedirs('scratch', exist_ok=True); ONLY = {int(a) for a in sys.argv[1:]}
by = collections.OrderedDict()
for r in csv.DictReader(open('out/MANIFEST.tsv'), delimiter='\t'):
    if ONLY and int(r['N']) not in ONLY: continue
    by.setdefault(r['summary'], []).append(r)
ok = bad = skip = 0
for summ, rs in by.items():
    N, cap = rs[0]['N'], rs[0]['cap']
    if any(r['windows'] == '-' for r in rs) or len(rs) != 4: print(f'SKIP   {summ} (a phase not kept)'); skip += 1; continue
    u = f'scratch/verify2_{N}_{cap}.npy'
    np.save(u, np.concatenate([np.load(f'out/hess_s_{N}_5_{cap}_{r["phase"]}.npy') for r in rs]))
    out = subprocess.run([sys.executable, 'parents81.py', u] + [str(k) for k in range(1, 401)], check=True, capture_output=True).stdout
    os.remove(u)
    h = hashlib.sha256(out).hexdigest(); same = h == rs[0]['summary_sha256']
    ok += same; bad += not same
    print(f'{"MATCH " if same else "DIFFER"} {summ}: rebuilt {h[:12]} vs manifest {rs[0]["summary_sha256"][:12]}', flush=True)
print(f'total: {ok} match, {bad} differ, {skip} skipped')
sys.exit(1 if bad else 0)  # theone 99970: a DIFFER must fail the command; SKIP stays a separate count, not a pass
