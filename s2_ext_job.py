"""Lab job: check_s2 on the L > 0 sizes 402..528 (from the gzeros-ext job), for the prediction in notes/prediction-typeB.md."""
import os, json, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__)); os.chdir(here)
on = [json.loads(l) for l in open('out/gzeros_ext.jsonl')]
for d in sorted(on, key=lambda d: d['M']):
    if d['L'] > 0 and d['M'] <= 528:
        subprocess.run([sys.executable, 'check_s2.py', str(d['M']), str(d['M'])], stdout=open('out/check_s2_402_528.jsonl', 'a'), check=True)
