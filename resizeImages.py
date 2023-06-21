import os
from tqdm import tqdm
from funcs import browse_for_dir, get_images_from_dir, resize_image


dir = browse_for_dir()
size = [576, 352]
images = get_images_from_dir(dir)

for image in tqdm(images, "Resizing images..."):
	resize_image(os.path.join(dir, image), size, False)

