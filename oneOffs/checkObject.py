import os
from tqdm import tqdm
import shutil

import mf

"""
Consolidates all annotation data from a yolov5/yolov8 annotations directory
excluding those with the name 'dark' or 'lite' in their names

No longer used.
"""

dir = mf.browseForDirectory()
sdir = mf.browseForDirectory()

vdir = os.path.join(dir, "valid")
tdir = os.path.join(dir, "train")

def sort_images(dir):
	idir = os.path.join(dir, "images")
	ldir = os.path.join(dir, "labels")

	images = mf.getImagesFromDirectory(idir)

	for image in tqdm(images, f"Sorting dir"):
		if "dark" not in image and "lite" not in image:
			present = False
			label = mf.convertNameToText(image)
			with open(os.path.join(ldir, label), 'r') as f:
				lines = f.readlines()
				for line in lines:
					if line[0] == '1':
						present = True

				if present:
					shutil.copy(os.path.join(ldir, label), os.path.join(sdir, label))
					shutil.copy(os.path.join(idir, image), os.path.join(sdir, image))


sort_images(vdir)
sort_images(tdir)
