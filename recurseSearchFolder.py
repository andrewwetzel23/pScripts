from funcs import browse_for_dir
from glob import iglob
import os

"""
Get's all files of a certain extension from a directory recursively

"""

dir = browse_for_dir()
RUNS = 20

def recursiveSearch(dir, exts):
	files = []
	for ext in exts:
		files.extend(list(iglob(os.path.join(dir, '**', f"*{ext}"), recursive=True)))

	return files

images = recursiveSearch(dir, [".jpg", ".png", ".jpeg"])
count = 0
for image in images:
	count += 1
	print(image)

print(count)