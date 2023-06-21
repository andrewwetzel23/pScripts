from zipfile import ZipFile
import os
from tqdm import tqdm

from funcs import browse_for_file, remove_extension, browse_for_dir

"""
Extracts a zipr file to a chosen output dir

"""

file = browse_for_file()
save_dir = browse_for_dir()
subdir = remove_extension(file)
with ZipFile(file) as zip:
	os.mkdir(os.path.join(save_dir, subdir))
	zip.extractall(path=os.path.join(save_dir, subdir))
