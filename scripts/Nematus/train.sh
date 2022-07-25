#!/bin/sh


# To train a model call like:
# 	  bash train.sh GPU_NR
# where GPU_NR is the id of the GPU you want to train on

# For BPE-dropout, add this option to the list of hyperparameter:
#     --preprocess_script $script_dir/apply_bpedropout_during_training.sh \


gpu_id=$1

nematus_home="/home/user/gasser/anaconda3/nematus" # path to nematus directory
script_dir="/home/user/gasser/scripts" # path to scripts directory
data_dir="/home/user/gasser/quechua/normalized/xfst_tags" # path to data directory
# data_dir="/home/user/gasser/quechua/data" # path to data directory
working_dir=$data_dir/xfst_normalized_tags_model

mkdir -p $working_dir

CUDA_VISIBLE_DEVICES=$gpu_id python3 $nematus_home/nematus/train.py \
    --source_dataset $data_dir/train.src \
    --target_dataset $data_dir/train.trg \
    --dictionaries $data_dir/concat_normalized_roots.vocab.json \
                    $data_dir/concat_normalized_roots.vocab.json \
    --save_freq 30000 \
    --model $working_dir/model \
    --reload latest_checkpoint \
    --model_type transformer \
    --transformer_num_heads 4 \
    --transformer_enc_depth 2 \
    --transformer_dec_depth 2 \
    --embedding_size 512 \
    --state_size 512 \
    --tie_decoder_embeddings \
    --tie_encoder_decoder_embeddings \
    --loss_function per-token-cross-entropy \
    --label_smoothing 0.3 \
    --exponential_smoothing 0.0001 \
    --optimizer adam \
    --adam_beta1 0.9 \
    --adam_beta2 0.98 \
    --adam_epsilon 1e-09 \
    --learning_schedule transformer \
    --warmup_steps 4000 \
    --maxlen 200 \
    --batch_size 256 \
    --token_batch_size 16384 \
    --max_tokens_per_device 4500 \
    --valid_source_dataset $data_dir/dev.src \
    --valid_target_dataset $data_dir/dev.trg \
    --valid_batch_size 120 \
    --valid_token_batch_size 4096 \
    --valid_freq 250 \
    --valid_script $script_dir/validate_tags.sh \
    --disp_freq 250 \
    --sample_freq 0 \
    --beam_freq 0 \
    --beam_size 4 \
    --translation_maxlen 200 \
    --normalization_alpha 0.6 \
    --patience 5 \
    --transformer_dropout_embeddings 0.2 \
    --transformer_dropout_attn 0.3 \
    --transformer_dropout_relu 0.3 \
    --transformer_dropout_residual 0.3 \
    --finish_after 250000
