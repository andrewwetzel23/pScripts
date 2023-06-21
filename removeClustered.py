from funcs import get_texts_from_dir, browse_for_dir, remove_extension
import os
from tqdm import tqdm


"""
Removes annotations who have a large number of objects

"""

dir = browse_for_dir()

txts = get_texts_from_dir(dir)
removed = 0
for txt in tqdm(txts):
	with open(os.path.join(dir, txt), 'r') as f:
		count = len(f.readlines())
	if count > 8:
		os.remove(os.path.join(dir, txt))
		os.remove(os.path.join(dir, remove_extension(txt) + '.jpg'))
		removed += 1

print(f'Removed {removed} annotations')
