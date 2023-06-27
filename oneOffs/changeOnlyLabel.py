from fileFuncs import browse_for_dir, getTextFilesFromDirectory
from tqdm import tqdm

dir = browse_for_dir()
texts = getTextFilesFromDirectory(dir)

"""
Replaces the first charcter in each line of every text file in a chosen directory.

"""

newFirstCharacter = '2'

for file in tqdm(texts):
    with open(file, 'r') as f:
        lines = f.readlines()

    with open(file, 'w') as f:
        for line in lines:
            f.write(newFirstCharacter)
            f.write(line[1:])
