import subprocess
import logging

logger = logging.getLogger('mf')


def ConfigureLogger(level=logging.DEBUG, to_std=True, to_file=False, log_file='app.log'):
    # Creating a basic formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # If logger has handlers, clear them
    if logger.hasHandlers():
        logger.handlers.clear()

    # Configure handler for standard output
    if to_std:
        std_handler = logging.StreamHandler()
        std_handler.setFormatter(formatter)
        logger.addHandler(std_handler)

    # Configure handler for file output
    if to_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Set the logger level
    logger.setLevel(level)


# Runs a batch file
def runBatchFile(batch_path):
    p = subprocess.Popen(batch_path, creationflags=subprocess.CREATE_NEW_CONSOLE, shell=False)
    p.communicate()

