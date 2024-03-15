#!/bin/bash

#SBATCH -p general
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --mem=20g
#SBATCH -t 12:00:00
#SBATCH --constraint=rhel8
#SBATCH --output=myjob.out
#SBATCH --mail-type=end
#SBATCH --mail-user=smyersn@ad.unc.edu

### Params to modify
dir='/users/s/m/smyersn/cell_images'
channel='Vinculin'

### Run script
source ~/.bashrc
conda activate segmentation

# Split
python /work/users/s/m/smyersn/elston/projects/segmentation/scripts/utils/gather_data.py "data" "$dir" "$channel"