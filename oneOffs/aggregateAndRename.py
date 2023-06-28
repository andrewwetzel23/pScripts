from os.path import join
from tqdm import tqdm
import cv2
import os

from system import browse_for_dir, getSubdirectoriesFromDirectory, getImagesFromDirectory, remove_extension

"""

Collects all images in subdirectories of selected directory, collects them in a chosen save directory and renames them.

"""


dir = browse_for_dir()
save_dir = browse_for_dir()
subdirs = getSubdirectoriesFromDirectory(dir)

all_images = []
for subdir in subdirs:
	images = getImagesFromDirectory(join(dir, subdir))
	for image in tqdm(images, desc=f'Getting files from {subdir}'):
		all_images.append(join(dir, subdir, image))

i = len(getImagesFromDirectory(save_dir))
print(i)
for image in tqdm(all_images, desc=f'Moving all images to {save_dir}'):
	img = cv2.imread(image)
	cv2.imwrite(join(save_dir, f'image_{i}.jpg'), img)
	i += 1

# for image in tqdm(all_images, desc='Removing old images'):
# 	os.remove(image)
