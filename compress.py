import os
import tarfile
import subprocess


from funcs import browseForDir


def compress_directory_to_tar_7z(path):
    print(f"Compressing {path}/ ...")

    # create a tar file first
    tar_file_path = os.path.join(dir, "..", "compressed") + ".tar"
    with tarfile.open(tar_file_path, "w") as tar:
        tar.add(path, arcname=os.path.basename(path))
    
    # # compress the tar file using 7z
    # command = ["7z", "a", "-t7z", os.path.join(dir, "..", "compressed") + ".tar.7z", tar_file_path]
    # subprocess.run(command)

    # # remove the intermediate tar file
    # os.remove(tar_file_path)


# use the function
dir = browseForDir()
compress_directory_to_tar_7z(dir, )
