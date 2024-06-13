#!/usr/bin/env bash

dataset=$1

source $HOME/.bashrc
mamba activate work

python_script="/afs/ihep.ac.cn/users/q/qi/work/projects/RK/high_q2_model/hqm/part_reco/ratio/simultaneous_fit.py"
echo "Running python simultaneous.py --dataset $dataset"
python $python_script --dataset $dataset
