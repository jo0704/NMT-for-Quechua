#!/bin/sh

gpu_id=$1

script_dir= # path to scripts directory
data_dir= # path to data directory
working_dir= #path to working directory from train.sh
nematus_home= # path to nematus directory

batchsize=100
beamsize=4
strategy=beam_search
model=model-30000

CUDA_VISIBLE_DEVICES=$gpu_id python3 $nematus_home/nematus/translate.py -m $working_dir/$model -i $data_dir/dev.src -o $data_dir/dev.out --translation_strategy $strategy  --translation_maxlen 200 -k $beamsize -n 0.6 -b $batchsize 
bash $script_dir/postprocess.sh < $data_dir/dev.out > $data_dir/dev.post