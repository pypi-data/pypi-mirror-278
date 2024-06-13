#!/usr/bin/env bash

for dataset in "all" "r1" "r2p1" "2017" "2018"; do
# for dataset in "2018"; do
    for q2 in "jpsi" "psi2"; do
        for kind in "jpsi" "psi2"; do
            echo "Running python fit_MC.py --dataset $dataset --q2 $q2 --kind $kind"
            python fit_MC.py --dataset $dataset --q2 $q2 --kind $kind
        done
    done
done
