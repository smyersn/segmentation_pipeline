import os, sys
import shutil

def organize_images(input_directory):
    for filename in os.listdir(input_directory):
        if os.path.isfile(os.path.join(input_directory, filename)):
            # Split the filename to extract the header
            parts = filename.split('_')
            date, condition, cell = parts[0], parts[1], '_'.join(parts[2:4])
            new_filename = '_'.join(parts[4:])

            # Create a directory for the header if it doesn't already exist
            date_directory = os.path.join(input_directory, date)
            if not os.path.exists(date_directory):
                os.makedirs(date_directory)
            
            condition_directory = os.path.join(date_directory, condition)
            if not os.path.exists(condition_directory):
                os.makedirs(condition_directory)
                
            cell_directory = os.path.join(condition_directory, cell)
            if not os.path.exists(cell_directory):
                os.makedirs(cell_directory)

            # Copy the file to the new directory with the header stripped from the filename
            source_path = os.path.join(input_directory, filename)
            destination_path = os.path.join(cell_directory, new_filename)
            shutil.copy2(source_path, destination_path)
            os.remove(os.path.join(input_directory, filename))

if __name__ == "__main__":
    organize_images(sys.argv[1])