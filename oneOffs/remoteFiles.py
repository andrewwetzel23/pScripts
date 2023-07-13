import paramiko
from scp import SCPClient
import datetime
import os

import mf

# Define server credentials and directories
hostname = "10.10.10.10"
username = "andrew"
password = "password"  # replace with your password
remote_dir = "/mnt/md5/HX500/lpunit0002/images/"
local_dir = mf.browseForDirectory()  # replace with your local directory

# Establish SSH connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password)

# Define date after which files should be copied
date_after = datetime.datetime(2023, 7, 6)

# Get list of all files in remote directory
stdin, stdout, stderr = ssh.exec_command(f"ls -l --time-style=long-iso {remote_dir}")
lines = stdout.readlines()

# Iterate over the lines, checking the date of each file
for line in lines[1:]:  # Skip the first line because it's a total count
    parts = line.strip().split()
    date_str, time_str, filename = parts[5], parts[6], parts[8]
    date_time_obj = datetime.datetime.strptime(date_str + " " + time_str, '%Y-%m-%d %H:%M')
    
    # If file was modified after the specified date, copy it to the local directory
    if date_time_obj > date_after:
        remote_file = os.path.join(remote_dir, filename)
        print(f"Copying {remote_file}")
        try:
            with SCPClient(ssh.get_transport()) as scp:
                scp.get(remote_file, local_path=os.path.join(local_dir, filename))
        except Exception as e:
            print(f"Failed to copy {remote_file}: {str(e)}")

# Close SSH connection
ssh.close()
