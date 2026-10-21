#!/bin/bash
# where the 1024-1088 layout switches before 1280 (97023)
cd "$(dirname "$0")"
for n in 1152 1216; do
  [ -f out/odo_$n.npz ] || python3 odo_fast.py $n || exit 1
  f=""
  for ph in "0 0" "0 1" "1 0" "1 1"; do
    set -- $ph
    python3 hess_small.py $n 5 10 full $1 $2 > out/hess_small_${n}_W5_P10_o$1$2.txt || exit 1
    if [ "$1$2" = 00 ]; then g=out/hess_small_${n}_5_10_full.npy; else g=out/hess_small_${n}_5_10_full_o$1$2.npy; fi
    f="$f${f:+,}$g"
  done
  python3 reach81.py "$f" > out/reach81_${n}_W5_4phase.txt
  echo "N=$n $(head -1 out/reach81_${n}_W5_4phase.txt) $(date -u +%H:%M)"
done
