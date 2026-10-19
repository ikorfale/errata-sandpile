"""Lab job: extend the gzeros table past 400 (out/gzeros_ext.jsonl), one row per even M, as far as 4 hours allow.
Pre-registered 19.10 before any M > 400 was computed: on-sizes (L > 0) keep clustering at M mod 32 in {18..30, 0..4}
(39 of 47 up to 400, vs 62.5% of sizes); no adjacent on-pair; gaps only 4, 6, 10, 14, 18; L/M <= 0.125."""
import os, sys, runpy
here = os.path.dirname(os.path.abspath(__file__)); os.chdir(here)
sys.argv = ["gzeros_ext.py", "402", "600"]
runpy.run_path("gzeros_ext.py", run_name="__main__")
