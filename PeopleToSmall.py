from funcs import browse_for_dir, get_images_from_dir
from tqdm import tqdm
import os
import shutil
import cv2
from math import ceil, floor

SIZE = [576,352]
AR = SIZE[0]/SIZE[1]

people_dir = browse_for_dir()
small_dir = browse_for_dir()

images = get_images_from_dir(people_dir)
count = 0
print(len(images))
dir_count = ceil(len(images) / 10000)

print(dir_count)

for i in range(0, dir_count):
	try:
		os.mkdir(os.path.join(small_dir, f'{i}'))
	except:
		pass

for image in tqdm(images, 'Creating directories with resized grayscale images...'):
	img = cv2.imread(os.path.join(people_dir, image))

	h, w, c = img.shape
	if w/h > AR:
		scale = w/576
	else:
		scale = h/352
	width = w /scale
	height = h /scale
	new_size = [int(width), int(height)]
	img_resized = cv2.resize(img, new_size)

	gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
	cv2.imwrite(os.path.join(small_dir, f'{floor(count / 10000)}', image), gray)
	count += 1
