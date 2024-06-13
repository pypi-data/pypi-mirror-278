#!/usr/bin/env bash

SUMBIT_SCRIPT="/afs/ihep.ac.cn/users/q/qi/work/projects/RK/high_q2_model/hqm/part_reco/ratio/simultaneous_fit_script.sh"

JOBDIR="$HOME/tmp/Jobs/part_reco_simultaneous_fit"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
JOBDIR="$JOBDIR/$DATE"

mkdir -p $JOBDIR
rm    -f $JOBDIR/*.out
rm    -f $JOBDIR/*.err

for dataset in "all" "r1" "r2p1" "2017" "2018"; do
    OUTPUT_FILE="$JOBDIR/part_reco_simultaneous_fit_%{ClusterId}"
    echo "dataset: $dataset"
    hep_sub -g lhcb -e "$OUTPUT_FILE.err" -o "$OUTPUT_FILE.out" -argu $dataset -mem 16000 -wt mid -np 4 $SUMBIT_SCRIPT
done
