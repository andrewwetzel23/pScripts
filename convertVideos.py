from os.path import join
from tqdm import tqdm
import shutil

from funcs import browse_for_dir, convert_videos

dir = browse_for_dir()
convert_videos(dir, 6)