import subprocess
from datetime import datetime
import os
from tqdm import tqdm

import mf

def copy_new_files(remote_user, remote_password, remote_host, remote_path, local_path, record_file):
    # Load copied files record
    copied_files = {}
    if os.path.exists(record_file):
        with open(record_file, 'r') as f:
            copied_files = {line.strip(): datetime.strptime(time.strip(), "%Y-%m-%d %H:%M") for line, time in (x.split('|') for x in f.readlines())}
    
    # Create a temporary file with the names of already copied files for rsync to exclude
    with open('exclude_files.txt', 'w') as f:
        for file in copied_files:
            f.write(file + '\n')

    # Copy all files from the remote directory to the local directory excluding already copied ones
    try:
        command = ["rsync", "-azP", "--exclude-from=exclude_files.txt", f"{remote_user}@{remote_host}:{remote_path}", local_path]
        subprocess.call(['sshpass', '-p', remote_password] + command)
    except Exception as e:
        print(f"Failed to copy files. Reason: {str(e)}")
        return

    # Update copied files record with new files
    for file in os.listdir(local_path):
        if file not in tqdm(copied_files, 'updating copied files record...'):
            mod_time = datetime.fromtimestamp(os.path.getmtime(os.path.join(local_path, file)))
            copied_files[file] = mod_time
            with open(record_file, 'a') as f:
                f.write(f"{file}|{mod_time.strftime('%Y-%m-%d %H:%M')}\n")
    

# Remove the temporary file
mf.delete('exclude_files.txt')

# Set your parameters here
remote_user = 'andrew'
remote_password = 'password'
remote_host = '10.10.10.10'
remote_path = '/mnt/md5/HX500/lpunit0002/images/'
remote_path1 = '/mnt/md5/HX500/lpunit0001/images/'
local_path = '/home/andrew/Desktop/images/'
record_file = 'copied_files.txt'

copy_new_files(remote_user, remote_password, remote_host, remote_path, local_path, record_file)
copy_new_files(remote_user, remote_password, remote_host, remote_path1, local_path, record_file)

mf.deleteRedFromDirectory(local_path)
mf.resizeImages(local_path, [576, 352])
mf.sortByDate(local_path)
