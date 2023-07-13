import subprocess
from datetime import datetime
import os
from tqdm import tqdm

import mf

import subprocess

def copy_new_files(remote_user, remote_password, remote_host, remote_path, local_path, record_file):
    # Copy all files from the remote directory to the local directory
    try:
        command = ["rsync", "-azP", f"{remote_user}@{remote_host}:{remote_path}", local_path]
        subprocess.call(['sshpass', '-p', remote_password] + command)

    except Exception as e:
        print(f"Failed to copy files. Reason: {str(e)}")
        return

    # Load copied files record
    copied_files = {}
    if os.path.exists(record_file):
        with open(record_file, 'r') as f:
            copied_files = {line.strip(): datetime.strptime(time.strip(), "%Y-%m-%d %H:%M") for line, time in (x.split('|') for x in f.readlines())}

    # Delete local files that have been copied before
    for file in os.listdir(local_path):
        if file in tqdm(copied_files, 'deleting old files...'):
            os.remove(os.path.join(local_path, file))
        else:
            # Update copied files record with new files
            mod_time = datetime.fromtimestamp(os.path.getmtime(os.path.join(local_path, file)))
            copied_files[file] = mod_time
            with open(record_file, 'a') as f:
                f.write(f"{file}|{mod_time.strftime('%Y-%m-%d %H:%M')}\n")




# Set your parameters here
remote_user = 'andrew'
remote_password = 'password'
remote_host = '10.10.10.10'
remote_path = '/mnt/md5/HX500/lpunit0002/images/'
local_path = '/home/andrew/Desktop/images/'
record_file = 'copied_files.txt'

copy_new_files(remote_user, remote_password, remote_host, remote_path, local_path, record_file)

mf.deleteRedFromDirectory(local_path)
mf.resizeImages(local_path, 576, 352)
mf.sortByDate(local_path)

