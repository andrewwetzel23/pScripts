import subprocess
import os
from tqdm import tqdm
import mf

def copy_new_files(remote_user, remote_password, remote_host, remote_path, local_path):
    # Copy all files from the remote directory to the local directory
    try:
        command = ["rsync", "-azP", "--remove-source-files", "--ignore-existing", f"{remote_user}@{remote_host}:{remote_path}", local_path]
        subprocess.call(['sshpass', '-p', remote_password] + command)
    except Exception as e:
        print(f"Failed to copy files. Reason: {str(e)}")
        return

# Set your parameters here
remote_user = 'andrew'
remote_password = 'password'
remote_host = '10.10.10.10'
remote_path = '/mnt/md5/HX500/lpunit0002/images/'
remote_path1 = '/mnt/md5/HX500/lpunit0001/images/'
remote_path2 = '/mnt/md5/HX500/lpunit0004/images/'
local_path = '/home/andrew/Desktop/images/'

# copy_new_files(remote_user, remote_password, remote_host, remote_path, local_path)
# copy_new_files(remote_user, remote_password, remote_host, remote_path1, local_path)
copy_new_files(remote_user, remote_password, remote_host, remote_path2, local_path)


mf.deleteRedFromDirectory(local_path)
mf.resizeImages(local_path, [576, 352])
mf.sortByDate(local_path)
