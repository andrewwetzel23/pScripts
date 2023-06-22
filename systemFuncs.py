
import subprocess

# Runs a batch file
def runBatchFile(batch_path):
    p = subprocess.Popen(batch_path, creationflags=subprocess.CREATE_NEW_CONSOLE, shell=False)
    p.communicate()

