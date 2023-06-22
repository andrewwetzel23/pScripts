import os
from tqdm import tqdm


from fileFuncs import getTextFilesFromDirectory, splitFileFromExtension

def removeClusteredDetections(dir):
    txts = getTextFilesFromDirectory(dir)
    removed = 0
    for txt in tqdm(txts):
        with open(os.path.join(dir, txt), 'r') as f:
            count = len(f.readlines())
        if count > 8:
            os.remove(os.path.join(dir, txt))
            fileName, _ = splitFileFromExtension(txt)
            os.remove(os.path.join(dir, fileName + '.jpg'))
            removed += 1

    print(f'Removed {removed} annotations')