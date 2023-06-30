import os
from tqdm import tqdm

import mf

""" 
Resizes all images in a chosen directory

"""


dir = mf.browseForDirectory()
size = [576, 352]
mf.resizeImages(dir, size, False, True)

