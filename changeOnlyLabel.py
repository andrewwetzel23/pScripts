from funcs import browse_for_dir, get_texts_from_dir
import os
from tqdm import tqdm

dir = browse_for_dir()
texts = get_texts_from_dir(dir)

for file in tqdm(texts):
	with open(file, 'r') as f:
	    lines = f.readlines()

	with open(file, 'w') as f:
		for line in lines:
			f.write('2')
			f.write(line[1:])


