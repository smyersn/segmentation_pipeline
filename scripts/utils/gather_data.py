import sys, os, pathlib
import shutil

def copy_and_rename_images(images, root, output_directory):
    """Renames files organized into date, condition, and cell directories.

    Args:
        images (list of strings): Files to rename
        root (string): Path to images
        output_directory (string): Path to copy renamed images to
    
    """
    # takes files organized by date, condition, and cell
    for image in images:
        condition = os.path.basename(os.path.dirname(root))
        date = os.path.basename(os.path.dirname(os.path.dirname(root)))
        new_file_name = "_".join([date, condition, os.path.basename(root), image])
        
        # Build source and destination paths
        source_path = os.path.join(root, image)
        destination_path = os.path.join(output_directory, new_file_name)

        # Copy the file to the new directory
        shutil.copy2(source_path, destination_path)

def gather_training_data(input_directory, channel):
    """Consolidates training data for one channel into one directory

    Args:
        input_directory (string): Path to directory to recursively search for
            labeled data. input_directory should have date/condition/cell
            subdirectory format.
        channel (string): Name of image channel w/ labeled data
        
    Examples:
        Gather training data for Binder channel from example path
        >>> gather_training_data('an/example/path, 'Binder')
        
    """
    channel_directory = os.path.join(str(pathlib.Path(input_directory).parent), channel)
    os.makedirs(channel_directory, exist_ok=True)
    
    output_directory = os.path.join(str(channel_directory), channel + '_training_data')
    os.makedirs(output_directory, exist_ok=True)
    
    images = [channel + '.tif', channel + '_seg.npy']

    # recursively check if each directory contains both image and masks
    for root, dirs, files in os.walk(input_directory):
        if images[0] in files and images[1] in files:
            copy_and_rename_images(images, root, output_directory)

def gather_test_data(input_directory, channel):
    """Consolidates test data for one channel into one directory

    Args:
        input_directory (string): Path to directory to recursively search for
            labeled data. input_directory should have date/condition/cell
            subdirectory format
        channel (string): Name of image channel w/o labels
        
    Examples:
        Gather test data for Vinculin channel from example path
        >>> gather_test_data('an/example/path, 'Vinculin')
        
    """
    channel_directory = os.path.join(str(pathlib.Path(input_directory).parent), channel)
    os.makedirs(channel_directory, exist_ok=True)
    
    output_directory = os.path.join(str(channel_directory), channel + '_test_data')
    os.makedirs(output_directory, exist_ok=True)
    
    images = [channel + '.tif', channel + '_seg.npy']

    # recursively check if each directory contains image and no mask
    for root, dirs, files in os.walk(input_directory):
        if images[0] in files and images[1] not in files:
            copy_and_rename_images(images[:1], root, output_directory)
            
def gather_masks(input_directory, channel):
    """Gathers masks from prior methods for channel

    Args:
        input_directory (string): Path to directory to recursively search for
            labeled data. input_directory should have date/condition/cell
            subdirectory format
        channel (string): Name of image channel for gathering masks
        
    """   
    if channel == 'Binder':
        images = ['Cell_Mask.tif', 'Cell_Mask_MSA.tif']
    if channel == 'Vinculin':
        images = ['FA_mask.tif', 'FA_mask_FAAS.tif']

    # recursively check if each directory contains image and no mask
    for root, dirs, files in os.walk(input_directory):
        if 'Binder.tif' in files and 'Binder_seg.npy' not in files:
            copy_and_rename_images(images, root, input_directory)

                                               
if __name__ == "__main__":
    # take system arguments as inputs to function
    if sys.argv[1] == 'data':
        gather_training_data(sys.argv[2], sys.argv[3])
        gather_test_data(sys.argv[2], sys.argv[3])
    if sys.argv[1] == 'masks':
        gather_masks(sys.argv[2])