import os, sys
import numpy as np
import matplotlib.pyplot as plt
from cellpose import plot, utils, io

def draw_masks_unorganized(input_directory):
    files = os.listdir(input_directory)
    
    headers = []

    for file in files:
        if '_Binder' in file:
            header = file.split('_Binder')[0]
            headers.append(header) if header not in headers else None
        
    for header in headers:
        dat = np.load(os.path.join(input_directory, header + '_Binder_seg.npy'), allow_pickle=True).item()
        img = io.imread(os.path.join(input_directory, header + '_Binder.tif'))
        
        # plot image with masks overlaid
        mask_RGB = plot.mask_overlay(img, dat['masks'])

        # plot image with outlines overlaid in red
        outlines = utils.outlines_list(dat['masks'])
        plt.imshow(img, cmap='gray')
        for o in outlines:
            plt.plot(o[:,0], o[:,1], color='r')

        plt.savefig(os.path.join(input_directory, header + '_cp_masks.png'))
        plt.close()

def draw_masks_organized(input_directory):
        
    for root, dirs, files in os.walk(input_directory):
        if 'Binder_seg.npy' in files and 'Binder.tif' in files:
            dat = np.load('Binder_seg.npy', allow_pickle=True).item()
            img = io.imread('Binder.tif')
            
            # plot image with masks overlaid
            mask_RGB = plot.mask_overlay(img, dat['masks'])

            # plot image with outlines overlaid in red
            outlines = utils.outlines_list(dat['masks'])
            plt.imshow(img, cmap='gray')
            for o in outlines:
                plt.plot(o[:,0], o[:,1], color='r')

            plt.savefig(os.path.join('Binder_cp_masks.png'))
            plt.close()

def generate_masks_tif(input_directory):
    for root, dirs, files in os.walk(input_directory):
        if 'Binder_seg.npy' in files:
            dat = np.load(os.path.join(root, 'Binder_seg.npy'), allow_pickle=True).item()
            masks = dat['masks']
            io.imsave(os.path.join(root,'Cell_Mask.tif'), masks)

if __name__ == "__main__":
    # take system arguments as inputs to function
    generate_masks_tif(sys.argv[1])