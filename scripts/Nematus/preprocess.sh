#!/bin/sh

vocab_size="3000" # your desired vocab_size (for some guidelines on what size to choose depending on the amount of training data see here: https://aclanthology.org/2020.coling-main.304.pdf)

script_dir= # path to scripts directory
data_dir= # path to data directory

# train BPE models
/home/user/amrhein/sentencepiece/build/src/
spm_train --input=$data_dir/train.src.trg.raw \
		  --model_prefix=$data_dir/spm_normalized.joint \
		  --vocab_size=$vocab_size \
		  --character_coverage 1.0 \
		  --model_type=bpe \
		  --shuffle_input_sentence=True 
		  
		  
# create nematus vocabulary files

python3 $script_dir/convert_spm_vocab.py $data_dir/spm_normalized.joint.vocab
mv $data_dir/spm_normalized.joint.vocab.json $data_dir/vocab_normalized.joint.json

# encode all data

spm_encode --model=$data_dir/spm_normalized.joint.model < $data_dir/train.src.raw > $data_dir/train.src
spm_encode --model=$data_dir/spm_normalized.joint.model < $data_dir/dev.src.raw > $data_dir/dev.src
spm_encode --model=$data_dir/spm_normalized.joint.model < $data_dir/test.src.raw > $data_dir/test.src

spm_encode --model=$data_dir/spm_normalized.joint.model < $data_dir/train_normalized.trg.raw > $data_dir/train.trg
spm_encode --model=$data_dir/spm_normalized.joint.model < $data_dir/dev_normalized.ref > $data_dir/dev.trg
spm_encode --model=$data_dir/spm_normalized.joint.model < $data_dir/test_normalized.ref > $data_dir/test.trg