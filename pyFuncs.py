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

# TimeIt: A decorator for timing a single execution of a function.
def timeit(func):
	def wrap_func(*args, **kwargs):
		t1 = time_ns()
		result = func(*args, **kwargs)
		t2 = time_ns()
		print(f"Function {func.__name__!r} took {(t2-t1)/1000000:.6f}ms")
		return result
	return wrap_func

# TimeItRepeated: A decorator for timing multiple executions of a function and reporting mean and standard deviation.
def timeitR(count):
	def decorator(func):
		def wrapper(*args, **kwargs):
			deltas = np.empty([0])
			for _ in range(count):
				t1 = time_ns()
				result = func(*args, **kwargs)
				t2 = time_ns()
				deltas = np.append(deltas, (t2-t1)/1000000)
			print(f"Function {func.__name__!r} took {np.mean(deltas):.6f} ms with std of {np.std(deltas):.6f}")
			return result
		return wrapper
	return decorator

# CreateFile: Safely create a new file, with optional overwrite.
def createFile(file, overwrite=True):
    try:
        if os.path.exists(file):
            if overwrite:
                removeFile(file)
            else:
                print("File already exists and overwrite set to False.")
                return False
        with open(file, 'w') as f:
            pass
        return True
    except Exception as e:
        print(f"Unable to create file: {e}")
        return False

# RemoveFile: Safely remove a file.
def removeFile(file):
    try:
        os.remove(file)
    except OSError as e:
        if e.errno != errno.ENOENT:  # Raise the exception if it's not because the file doesn't exist
            print(f"Error: {e}")
            return False
    return True

# CreateDirectory: Safely create a new directory, with optional overwrite.
def createDirectory(dir, overwrite=True):
    try:
        if os.path.exists(dir):
            if overwrite:
                removeDirectory(dir)
            else:
                print("Directory already exists and overwrite set to False.")
                return False
        os.mkdir(dir)
        return True
    except Exception as e:
        print(f"Unable to create directory: {e}")
        return False

# RemoveDirectory: Safely remove a directory.
def removeDirectory(dir):
    try:
        shutil.rmtree(dir)
    except OSError as e:
        if e.errno != errno.ENOENT:  # Raise the exception if it's not because the directory doesn't exist
            print(f"Error: {e}")
            return False
    return True


		

# GetFilesFromDir: Get files with specified extensions from a directory, optionally recursive.
def getFilesFromDir(dir, exts=[""], recursive=False):
	files = []
	for ext in exts:
		files.extend(glob.glob(os.path.join(dir, "**", "*"+ext), recursive=recursive))
	return files

# GetImagesFromDir: Get image files from a directory, optionally recursive.
def getImagesFromDir(dir, recursive=False):
	return getFilesFromDir(dir, exts=[".jpeg", ".jpg", ".png"], recursive=recursive)

# BrowseForDir: Open a dialog to browse for a directory.
def browseForDir():
	tkinter.Tk().withdraw()
	return askdirectory()

# BrowseForFile: Open a dialog to browse for a file.
def browseForFile():
	tkinter.Tk().withdraw()
	return askopenfilename()

def resizeImages(dir, size, recursiveSearch=False, keepAspectRatio=True):
	images = getImagesFromDir(dir, recursiveSearch)
	for image in tqdm(images, "Resizing images..."):
		resizeImage(image, size, keepAspectRatio)


# ResizeImage: Resize an image, optionally keeping its aspect ratio.
def resizeImage(imagePath: str, targetSize: tuple, keepAspectRatio=True):
    # Read the image using OpenCV
    image = cv2.imread(imagePath)

    if keepAspectRatio:
        # If we want to keep the aspect ratio, we calculate the scale factor
        # and resize the image to that scale.
        maxWidth, maxHeight = targetSize
        targetAspectRatio = maxWidth / maxHeight

        # Get the current image dimensions
        imageHeight, imageWidth, _ = image.shape
        imageAspectRatio = imageWidth / imageHeight

        # Determine the scale based on width or height
        if imageAspectRatio > targetAspectRatio:
            scale = imageWidth / maxWidth
        else:
            scale = imageHeight / maxHeight

        # Calculate new dimensions and resize
        newImageWidth = int(imageWidth / scale)
        newImageHeight = int(imageHeight / scale)
        newImageSize = (newImageWidth, newImageHeight)
        imageResized = cv2.resize(image, newImageSize)
    else:
        # If we do not want to keep the aspect ratio, we resize to the target size directly.
        imageResized = cv2.resize(image, targetSize)

    # Write the resized image back to the file
    cv2.imwrite(imagePath, imageResized)


def removeDuplicates(directory):
    filePath = directory
    listOfFiles = os.walk(directory)

    uniqueFiles = dict()
    count = 0

    for root, folders, files in listOfFiles:
        # Iterate over all the files
        for file in tqdm(files, 'Removing duplicates...'):
            filePath = Path(os.path.join(root, file))

            # Convert all the content of our file into an md5 hash.
            hashFile = hashlib.md5(open(filePath, 'rb').read()).hexdigest()

            # If file hash has already been added, we'll simply delete that file
            if hashFile not in uniqueFiles:
                uniqueFiles[hashFile] = filePath
            else:
                os.remove(filePath)
                count += 1
                
    print(f"Removed {count} duplicates.")
