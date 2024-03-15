from PIL import Image
import sys, os

def convert_tiff_to_8bit(input_folder):
    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".tiff") or filename.endswith(".tif"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(input_folder, filename.replace(".tiff", "_8bit.png").replace(".tif", "_8bit.png"))

            # Open the TIFF image
            tiff_image = Image.open(input_path)

            # Convert the image to 8-bit
            eight_bit_image = tiff_image.convert("L")

            # Save the 8-bit image as PNG
            eight_bit_image.save(output_path, format="PNG")

if __name__ == "__main__":
    # take system argument as input folder
    input_folder = f'{sys.argv[1]}'
    
    # generate output folder in parent folder
    parent_folder = os.path.abspath(os.path.join(input_folder, os.pardir))
    output_folder = os.path.join(parent_folder, f'{os.path.basename(input_folder)}_png')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Call the function to convert TIFF to 8-bit and save as PNG
    convert_tiff_to_8bit(input_folder, output_folder)
