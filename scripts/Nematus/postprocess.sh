#!/bin/sh
#removing bpe splits

data_dir= # path to data directory

spm_decode --model=$data_dir/spm.joint.model
# spm_decode --model=$data_dir/spm_normalized.joint.model | sed 's/▁/ /g' | sed 's/^ //g'