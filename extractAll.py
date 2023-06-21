from zipfile import ZipFile
import os
from tqdm import tqdm

from funcs import browse_for_dir, get_files_of_type, remove_extension

dir = browse_for_dir()
save_dir = browse_for_dir()
files = get_files_of_type(dir, '.zip')

for file in tqdm(files, 'Extracting zip files...'):
	subdir = remove_extension(file)
	with ZipFile(os.path.join(dir, file)) as zip:
		os.mkdir(os.path.join(save_dir, subdir))
		zip.extractall(path=os.path.join(save_dir, subdir))
