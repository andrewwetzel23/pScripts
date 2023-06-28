import os
import shutil
from tqdm import tqdm
from dec import browseForDir, createDirectory

"""
Move all images that have a corresponding text file with a line starting with "1" to a new folder

"""

def search_and_copy_images(directory, save_folder):
    # Iterate through each file in the directory
    for file_name in tqdm(os.listdir(directory)):
        # Check if the file is a text file
        if file_name.endswith(".txt"):
            text_file_path = os.path.join(directory, file_name)
            image_file_name = os.path.splitext(file_name)[0]
            
            # Check for image files with various extensions
            image_extensions = (".jpg", ".jpeg", ".png")
            for ext in image_extensions:
                image_file_path = os.path.join(directory, image_file_name + ext)
                
                # Check if the corresponding image file exists
                if os.path.isfile(image_file_path):
                    # Open the text file and search for lines starting with "1"
                    with open(text_file_path, "r") as text_file:
                        for line in text_file:
                            if line.strip().startswith("1"):
                                # Copy the image file to the save folder
                                save_path = os.path.join(save_folder, os.path.basename(image_file_path))
                                shutil.copy2(image_file_path, save_path)
                                break

# Provide the directory path using the "browseForDir()" function or manually
directory_path = browseForDir()

save_directory_path = os.path.join(directory_path, "save")
createDirectory(save_directory_path, True)

# Call the function to search and copy the images
search_and_copy_images(directory_path, save_directory_path)
