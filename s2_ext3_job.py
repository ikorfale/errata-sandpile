"""Lab job: check_s2 on 530, 534, 540 for the third prediction in notes/prediction-typeB.md (534 B; 530, 540 A)."""
import os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__)); os.chdir(here)
for M in (534, 530, 540):
    subprocess.run([sys.executable, 'check_s2.py', str(M), str(M)], stdout=open('out/check_s2_530_540.jsonl', 'a'), check=True)
