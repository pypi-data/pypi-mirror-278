#!/usr/bin/env bash

for dataset in "all" "r1" "r2p1" "2017" "2018"; do
    echo "Running python fully_reco_shape.py --dataset $dataset"
    python fully_reco_shape.py --dataset $dataset
done
