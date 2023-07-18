import os
import shutil

import sys
sys.path.append('..')
from pyFuncs import browseForDir

def duplicate_html_files(directory):
    # Walk the directory structure
    for dirpath, dirnames, filenames in os.walk(directory):
        # Loop over every file in the directory
        for filename in filenames:
            # If the file is an HTML file
            if filename.endswith('.html'):
                # Construct the full file path
                full_file_path = os.path.join(dirpath, filename)
                # Construct the new file path
                new_file_path = os.path.join(dirpath, 'spanish_' + filename)
                # Duplicate the file
                shutil.copyfile(full_file_path, new_file_path)

# Call the function with the path to your directory
duplicate_html_files(browseForDir())

