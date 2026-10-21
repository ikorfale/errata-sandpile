#!/bin/bash
# theone #96847: union of the four start phases of the side-5 scan, per N; mirror-closed reach
cd "$(dirname "$0")"
for n in 256 512 640 768 896 1024 1280 1536; do
  f=""
  for ph in "0 0" "0 1" "1 0" "1 1"; do
    set -- $ph
    python3 hess_small.py $n 5 10 full $1 $2 > out/hess_small_${n}_W5_P10_o$1$2.txt || exit 1
    if [ "$1$2" = 00 ]; then g=out/hess_small_${n}_5_10_full.npy; else g=out/hess_small_${n}_5_10_full_o$1$2.npy; fi
    f="$f${f:+,}$g"
  done
  python3 reach81.py "$f" > out/reach81_${n}_W5_4phase.txt
  echo "N=$n $(head -1 out/reach81_${n}_W5_4phase.txt | sed 's/.*reached/reached/')"
done
