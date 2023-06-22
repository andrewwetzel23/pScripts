from os.path import join
from tqdm import tqdm
import shutil

from systemFuncs import browse_for_dir, getSubdirectoriesFromDirectory, getImagesFromDirectory, get_extension


dir = browse_for_dir()

images = getImagesFromDirectory(dir)
i = 0
for image in tqdm(images, desc=f'Renaming images...'):
		ext = get_extension(image)
		shutil.move(join(dir, image), join(dir, f'image_{i}{ext}'))
		i += 1