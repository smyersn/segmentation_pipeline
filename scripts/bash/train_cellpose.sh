#!/bin/bash

#SBATCH -p volta-gpu
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=16g
#SBATCH -t 12:00:00
#SBATCH --constraint=rhel8
#SBATCH --output=myjob.out
#SBATCH --qos gpu_access
#SBATCH --gres=gpu:1
#SBATCH --mail-type=end
#SBATCH --mail-user=smyersn@ad.unc.edu

### Params to modify
model=cyto2
training_dir='/users/s/m/smyersn/Vinculin/Vinculin_training_data'

### Run script
source ~/.bashrc
conda activate segmentation

# Create model name for saving weights
IFS='/' read -ra dirs <<< "$training_dir"
model_name="${dirs[-1]}_${model}_weights"

# Train Cellpose
python -m cellpose --train --verbose --min_train_masks 1 --dir "$training_dir" --pretrained_model $model --mask_filter _seg.npy --chan 0 --use_gpu --learning_rate 0.1 --weight_decay 0.0001 --n_epochs 100 --model_name_out "$model_name"
