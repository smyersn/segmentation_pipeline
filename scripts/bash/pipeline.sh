#!/bin/bash

#SBATCH -p volta-gpu
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=16g
#SBATCH -t 1:00:00
#SBATCH --constraint=rhel8
#SBATCH --output=myjob.out
#SBATCH --qos gpu_access
#SBATCH --gres=gpu:1
#SBATCH --mail-type=end
#SBATCH --mail-user=smyersn@ad.unc.edu

### Params to modify
dir='/users/s/m/smyersn/cell_images'
channel='Vinculin'
model=nuclei

### Run script
source ~/.bashrc
conda activate segmentation


### Process data
python /work/users/s/m/smyersn/elston/projects/segmentation/scripts/utils/gather_data.py "data" "$dir" "$channel"
###

### Train model
# Get Parent directory
parent_dir=''
IFS='/' read -ra terms <<< "$dir"

array_length=${#terms[@]}
for ((i = 0; i < (array_length - 1); i++)); do
    parent_dir+="${terms[i]}/"
done

# Create model name for saving weights
training_dir="${parent_dir}/${channel}/${channel}_training_data"
IFS='/' read -ra dirs <<< "$training_dir"
model_name="${dirs[-1]}_${model}_weights"

# Train Cellpose
python -m cellpose --train --verbose --min_train_masks 1 --dir "$training_dir" --pretrained_model $model --mask_filter _seg.npy --chan 0 --use_gpu --learning_rate 0.1 --weight_decay 0.0001 --n_epochs 100 --model_name_out "$model_name"
###

### Run model
test_dir="${parent_dir}/${channel}/${channel}_test_data"

# Create directory to save results
results_dir="${test_dir}/${model_name}_results"
mkdir "$results_dir"

find "$test_dir" -type f -exec cp {} "$results_dir" \;


# Run Cellpose for Binder
#python -m cellpose --use_gpu --verbose --dir "$results_dir"  --save_outlines --save_tif --no_npy --pretrained_model "$custom_model" --chan 0 --diameter 150
# Run Cellpose for Vinculin
python -m cellpose --use_gpu --verbose --dir "$results_dir"  --save_outlines --save_tif --no_npy --pretrained_model "$custom_model" --chan 0 --diameter 10
