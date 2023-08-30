import subprocess
import logging

logger = logging.getLogger('mf')

def ConfigureLogger(level=logging.DEBUG):
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(level)

# Runs a batch file
def runBatchFile(batch_path):
    p = subprocess.Popen(batch_path, creationflags=subprocess.CREATE_NEW_CONSOLE, shell=False)
    p.communicate()

