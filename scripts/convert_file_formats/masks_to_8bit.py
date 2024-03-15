from PIL import Image
import sys, os
import numpy as np

def masks_to_8bit(input_folder):
    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith("masks.png"):
            input_path = os.path.join(input_folder, filename)

            # Open the int16 file using numpy
            int16_data = np.array(Image.open(input_path), dtype=np.int16)
            
            # Rescale the int16 values to 8-bit range (0-255)
            rescaled_data = ((int16_data - np.min(int16_data)) / (np.max(int16_data) - np.min(int16_data)) * 255).astype(np.uint8)

            # Create an 8-bit image from the rescaled data
            eight_bit_image = Image.fromarray(rescaled_data, mode='L')

            # Save the 8-bit image as PNG
            eight_bit_image.save(input_path, format="PNG")

if __name__ == "__main__":
    masks_to_8bit(sys.argv[1])