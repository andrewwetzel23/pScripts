from os.path import join
from tqdm import tqdm
import shutil

from funcs import browse_for_dir, get_subdirectories, get_images_from_dir, get_extension


dir = browse_for_dir()

images = get_images_from_dir(dir)
i = 0
for image in tqdm(images, desc=f'Renaming images...'):
		ext = get_extension(image)
		shutil.move(join(dir, image), join(dir, f'image_{i}{ext}'))
		i += 1