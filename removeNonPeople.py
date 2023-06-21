from funcs import get_images_from_dir, get_texts_from_dir, browse_for_dir, remove_extension
from os.path import join
import os
from tqdm import tqdm


print('Choose the directory of the images:')
image_dir = browse_for_dir()
label_dir = browse_for_dir()

labels = get_texts_from_dir(label_dir)

for lbl in tqdm(labels, desc='Removing images and labels without people in them...'):
	path = join(label_dir, lbl)

	person = False
	with open(path, 'r') as f:
		lines = f.readlines()
		for line in lines:
			if line[:2] == '0 ':
				person = True

	if not person:
		os.remove(path)
		img_path = join(image_dir, remove_extension(lbl) + '.jpg')
		try:
			os.remove(img_path)
		except:
			img_path = join(image_dir, remove_extension(lbl) + '.png')
			os.remove(img_path)
