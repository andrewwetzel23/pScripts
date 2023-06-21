import os
import errno
import shutil
import numpy as np
import errno
import glob
import tkinter
import cv2
import hashlib

from time import time_ns
from tqdm import tqdm
from pathlib import Path
from tkinter.filedialog import askdirectory, askopenfilename

"""
Another python funcs file.

Needs to be cleaned and checked.

"""

def timeit(func):
	def wrap_func(*args, **kwargs):
		t1 = time_ns()
		result = func(*args, **kwargs)
		t2 = time_ns()
		print(f"Function {func.__name__!r} took {(t2-t1)/1000000:.6f}ms")
		return result
	return wrap_func

def timeitR(count):
	def decorator(func):
		def wrapper(*args, **kwargs):
			deltas = np.empty([0])
			for i in range(0, count):
				t1 = time_ns()
				result = func(*args, **kwargs)
				t2 = time_ns()
				deltas = np.append(deltas, (t2-t1)/1000000)
			print(f"Function {func.__name__!r} took {np.mean(deltas, axis=0)} ms with std of {np.std(deltas, axis=0)}")
			return result
		return wrapper
	return decorator



def safeRemove(object):
	if os.path.isfile(object):
		try:
			os.remove(object)
		except OSError as e:
			if e.errno != errno.ENOENT:
				raise
	elif os.path.isdir(object):
		try:
			shutil.rmtree(object)
		except OSError as e:
			if e.errno != errno.ENOENT:
				raise

def createBlankFile(object):
	with open(object, 'w') as f:
		pass
	return True

def safeCreate(object, overwrite=True):
	if os.path.isfile(object):
		if not os.path.exists(object):
			return createBlankFile()

		elif overwrite:
			safeRemove(object)
			return createBlankFile(file)
		
		else:
			return False
	
	if os.path.isdir(object):
		if not os.path.exists(object):
			os.mkdir(object)
			return True

		elif overwrite:
			safeRemove(object)
			os.mkdir(object)
			return True

		else:
			return False

def getFilesFromDir(dir, exts=[""], recursive=False):
	files = []
	for ext in exts:
		files.extend(glob.glob(os.path.join(dir, "**", "*"+ext), recursive=recursive))
	return files

def getImagesFromDir(dir, recursive=False):
	return getFilesFromDir(dir, exts=[".jpeg", ".jpg", ".png"], recursive=recursive)

def browseForDir():
	tkinter.Tk().withdraw()
	return askdirectory()

def browseForFile():
	tkinter.Tk().withdraw()
	return askopenfilename()

def resizeImages(dir, size, recursiveSearch=False, keepAspectRatio=True):
	images = getImagesFromDir(dir, recursiveSearch)
	for image in tqdm(images, "Resizing images..."):
		resizeImage(image, size, keepAspectRatio)


def resizeImage(image, size, keepAspectRatio=True):
	img = cv2.imread(image)

	if keepAspectRatio:
		max_width, max_height = size
		AR = max_width/max_height                
		image_height, image_width, image_channels = img.shape
		if image_width/image_height > AR:
			scale = image_width/max_width
		else:
			scale = image_height/max_height
		width = image_width/scale
		height = image_height/scale
		new_size = [int(width), int(height)]
		img_resized = cv2.resize(img, new_size)        
	else:
		img_resized = cv2.resize(img, size)

	cv2.imwrite(image, img_resized)

def removeDuplicates(dir):
    file_path = dir
    list_of_files = os.walk(dir)

    unique_files = dict()
    count = 0
    for root, folders, files in list_of_files:
        # Running a for loop on all the files
        for file in tqdm(files, 'Removing duplicates...'):
            file_path = Path(os.path.join(root, file))

            # Converting all the content of
            # our file into md5 hash.
            Hash_file = hashlib.md5(open(file_path, 'rb').read()).hexdigest()

            # If file hash has already #
            # been added we'll simply delete that file
            if Hash_file not in unique_files:
                unique_files[Hash_file] = file_path
            else:
                os.remove(file_path)
                try:
                    os.remove(os.path.join(dir, convert_name_to_text(file)))
                except:
                    pass
                count += 1
    print(f"Removed {count} duplicates.")
