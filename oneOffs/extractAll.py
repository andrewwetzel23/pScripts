from zipfile import ZipFile
import os
from tqdm import tqdm

from system import browse_for_dir, getFilesFromDirectory, remove_extension

"""
Extracts all zip files in a chosen directory into a chosen output directory

"""

dir = browse_for_dir()
save_dir = browse_for_dir()
files = getFilesFromDirectory(dir, '.zip')

for file in tqdm(files, 'Extracting zip files...'):
	subdir = remove_extension(file)
	with ZipFile(os.path.join(dir, file)) as zip:
		os.mkdir(os.path.join(save_dir, subdir))
		zip.extractall(path=os.path.join(save_dir, subdir))
