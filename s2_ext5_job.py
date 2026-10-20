"""Lab job: gzeros from M = 610 up, then check_s2 on every new on-size (L > 0).
Pre-registered in notes/prediction-typeB.md (fifth registration) before any M > 608 was computed: type B iff L/M < 0.04."""
import os, sys, json, subprocess
here = os.path.dirname(os.path.abspath(__file__)); os.chdir(here)
seen = {json.loads(l)["M"] for l in open("out/gzeros_ext.jsonl")}
for M in range(610, 701, 2):
    if M in seen: continue
    subprocess.run([sys.executable, "gzeros_ext.py", str(M), str(M)], check=True)
    row = [json.loads(l) for l in open("out/gzeros_ext.jsonl") if json.loads(l)["M"] == M][-1]
    if row["L"] > 0:
        subprocess.run([sys.executable, "check_s2.py", str(M), str(M)], stdout=open("out/check_s2_550up.jsonl", "a"), check=True)
