#!/bin/sh

data_dir= # path to data directory

spm_encode --model=$data_dir/spm.joint.model --output_format=sample_piece --alpha 0.1 < $data_dir/train.src.raw > $data_dir/train.src &

spm_encode --model=$data_dir/spm.joint.model --output_format=sample_piece --alpha 0.1 < $data_dir/train.trg.raw > $data_dir/train.trg &

wait

