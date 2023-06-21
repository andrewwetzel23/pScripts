from zipfile import ZipFile
import os
from tqdm import tqdm

from funcs import browse_for_file, get_files_of_type, remove_extension, browse_for_dir

file = browse_for_file()
save_dir = browse_for_dir()
subdir = remove_extension(file)
with ZipFile(file) as zip:
	os.mkdir(os.path.join(save_dir, subdir))
	zip.extractall(path=os.path.join(save_dir, subdir))
