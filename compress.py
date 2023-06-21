import os
import tarfile

from funcs import browseForDir

"""
Compresses all data in a given dir to a tar file

"""


def compress_directory_to_tar(path):
    print(f"Compressing {path}/ ...")

    # create a tar file first
    tar_file_path = os.path.join(dir, "..", "compressed") + ".tar"
    with tarfile.open(tar_file_path, "w") as tar:
        tar.add(path, arcname=os.path.basename(path))
    


# use the function
dir = browseForDir()
compress_directory_to_tar(dir, )
