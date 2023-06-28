import os
from tqdm import tqdm
from system import browse_for_dir, getImagesFromDirectory, resize_image

""" 
Resizes all images in a chosen directory

"""


dir = browse_for_dir()
size = [576, 352]
images = getImagesFromDirectory(dir)

for image in tqdm(images, "Resizing images..."):
	resize_image(os.path.join(dir, image), size, False)

