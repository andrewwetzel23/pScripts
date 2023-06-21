from os.path import join
from os import listdir
from tqdm import tqdm
from funcs import browse_for_dir

""" 
Removes all annotations who don't have a matching test at the beginning of each line

Needs to be cleaned up

"""

def get_texts_from_dir(path):
    list_of_files = listdir(path)
    list_of_texts = []
    for f in list_of_files:
        if f.endswith('.txt'):
            list_of_texts.append(f)
    return list_of_texts


dir = browse_for_dir()
texts = get_texts_from_dir(dir)

for text in tqdm(texts, 'Removing some annotations...'):
    # print(text)remove
    with open(join(dir, text), 'r') as f:
        lines = f.readlines()
    with open(join(dir, text), 'w') as f:
        for line in lines:
            # print(line[0])
            
            if line.strip("\n")[0] == '0':
                f.write(line)