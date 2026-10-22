#!/bin/bash
# 22.10: lab runner is at 8 jobs/day; run the 2016 row and then 1296 as a user service once 2048c has finished.
cd "$(dirname "$0")"
while [ "$(cat ../jobs/sandpile-p20-2048c/status 2>/dev/null)" = running ] || [ ! -f ../jobs/sandpile-p20-2048c/status ]; do sleep 60; done
python3 -u job_2016.py > out/chain_2016.log 2>&1; echo "rc $?" >> out/chain_2016.log
python3 -u job_1296.py > out/chain_1296.log 2>&1; echo "rc $?" >> out/chain_1296.log
