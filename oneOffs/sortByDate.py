import os
import shutil
import datetime
from tqdm import tqdm
import re

import mf
        
def get_creation_time(filename):
    # Regular expression pattern to match Unix timestamp in filename
    pattern = r'(\d{10})'
    
    # Search for Unix timestamp in filename
    match = re.search(pattern, filename)

    if match:
        # Convert Unix timestamp to date
        timestamp = int(match.group(1))
        date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        return date
    else:
        return None

# specify the directory you want to organize
src_dir = mf.browseForDirectory()

def sortByDate(src_dir):
    # iterate over all the files in the directory
    for filename in tqdm(os.listdir(src_dir)):
        file = os.path.join(src_dir, filename)

        # ignore directories
        if os.path.isfile(file):
            # get the modification time and convert it into a date string
            date = get_creation_time(file)

            # create a new directory path
            new_dir = os.path.join(src_dir, date)

            # create new directory if it doesn't exist
            if not os.path.exists(new_dir):
                mf.createDirectory(new_dir)

            # move the file to new directory
            mf.move(file, new_dir)
