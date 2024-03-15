#!/bin/bash

#SBATCH -p volta-gpu
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=16g
#SBATCH -t 2:00:00
#SBATCH --constraint=rhel8
#SBATCH --output=./slurm/slurm-%j.out
#SBATCH --qos gpu_access
#SBATCH --gres=gpu:1
#SBATCH --mail-type=end
#SBATCH --mail-user=smyersn@ad.unc.edu

### Params to modify
test_dir='/users/s/m/smyersn/Vinculin/Vinculin_test_data'
custom_model='/users/s/m/smyersn/Vinculin/Vinculin_training_data/models/Vinculin_training_data_cyto2_weights'

### Run script
source ~/.bashrc
conda activate segmentation

# Get name of model
IFS='/' read -ra dirs <<< "$custom_model"
model_name="${dirs[-1]}"

# Create directory to save results
results_dir_name=''
IFS='_' read -ra terms <<< "$model_name"

array_length=${#terms[@]}
for ((i = 0; i < (array_length - 1); i++)); do
    results_dir_name+="${terms[i]}_"
done

results_dir="${test_dir}/${results_dir_name}results"
mkdir "$results_dir"

find "$test_dir" -type f -exec cp {} "$results_dir" \;


# Run Cellpose for Binder
#python -m cellpose --use_gpu --verbose --dir "$results_dir"  --save_outlines --save_tif --no_npy --pretrained_model "$custom_model" --chan 0 --diameter 150
# Run Cellpose for Vinculin
python -m cellpose --use_gpu --verbose --dir "$results_dir"  --save_outlines --save_tif --no_npy --pretrained_model "$custom_model" --chan 0 --diameter 10
