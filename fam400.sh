#!/bin/bash
# theone #97236: the curvature<=81 catalog has only 28 families, so a 2048 "repeat" branch of >=40 was unreachable.
# Recount families against the curvature<=400 catalog (189 families) at every size, four start phases.
cd "$(dirname "$0")"; mkdir -p scratch
for n in 256 512 640 768 896 960 1024 1088 1152 1216 1280 1536; do
  python3 -c "
import numpy as np
fs=['out/hess_small_${n}_5_10_full.npy']+['out/hess_small_${n}_5_10_full_o%s.npy'%p for p in ('01','10','11')]
np.save('scratch/fam400_u.npy',np.concatenate([np.load(f) for f in fs]))" || exit 1
  python3 parents81.py scratch/fam400_u.npy $(seq 1 400) > out/parents400_${n}_W5_4phase.txt
  rm -f scratch/fam400_u.npy
  echo "N=$n families $(grep -vc 'reached 0 ' out/parents400_${n}_W5_4phase.txt) of $(wc -l < out/parents400_${n}_W5_4phase.txt)"
done
