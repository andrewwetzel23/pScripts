import os
import shutil
import tkinter
import errno
import glob
from tkinter.filedialog import askdirectory, askopenfilename
from pathlib import Path
from tqdm import tqdm
import hashlib
import re
import datetime
import zipfile
import tarfile
import gzip
import logging
import fnmatch

from .defs import IMAGE_EXTENSIONS, VIDEO_EXTENSIONS

logger = logging.getLogger(__name__)

# BrowseForDir: Open a dialog to browse for a directory.
def browseForDirectory():
    logger.debug('Opening dialog to browse for a directory.')
    try:
        tkinter.Tk().withdraw()
        return askdirectory()
    except Exception as e:
        logger.error(f"Error while browsing for a directory: {str(e)}")

# BrowseForFile: Open a dialog to browse for a file.
def browseForFile():
    logger.debug('Opening dialog to browse for a file.')
    try:
        tkinter.Tk().withdraw()
        return askopenfilename()
    except Exception as e:
        logger.error(f"Error while browsing for a file: {str(e)}")

import logging
import os
import glob

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

VIDEO_EXTENSIONS = ['mp4', 'avi', 'mov'] # insert your video extensions here
IMAGE_EXTENSIONS = ['jpg', 'png', 'bmp'] # insert your image extensions here

def getSubdirectoriesFromDirectory(path, recursive=False):
    logger.debug(f"Getting list of directories from: {path}")
    try:
        if recursive:
            subdirs = [os.path.join(dp, f) for dp, dn, _ in os.walk(os.path.expanduser(path)) for f in dn]
        else:
            subdirs = [f.path for f in os.scandir(path) if f.is_dir()]

        return subdirs
    except Exception as e:
        logger.error(f"Error while getting directories from: {path}. Error: {str(e)}")



def getFilesFromDirectory(dir, exts=None, recursive=False):
    logger.debug(f"Getting files from directory: {dir} with extensions: {exts}")
    if exts is None:
        exts = [""]

    if not os.path.isdir(dir):
        logger.error(f"Directory does not exist: {dir}")
        raise ValueError(f"Directory does not exist: {dir}")

    files = []
    for ext in exts:
        ext = "." + ext
        try:
            if recursive:
                paths = glob.glob(os.path.join(dir, "**", "*"+ext), recursive=True)
            else:
                paths = glob.glob(os.path.join(dir, "*"+ext))
            files.extend(paths)
        except Exception as e:
            logger.error(f"Error while getting files from: {dir} with extension: {ext}. Error: {str(e)}")
            
    return files

def getVideosFromDirectory(directory, recursive=False):
    if not isinstance(VIDEO_EXTENSIONS, list) or not all(isinstance(item, str) for item in VIDEO_EXTENSIONS):
        raise ValueError("VIDEO_EXTENSIONS must be a list of strings")
    
    logger.debug(f"Getting list of videos from: {directory}")
    try:
        return getFilesFromDirectory(directory, exts=VIDEO_EXTENSIONS, recursive=recursive)
    except Exception as e:
        logger.error(f"Error while getting videos from: {directory}. Error: {str(e)}")

def getImagesFromDirectory(dir, recursive=False):
    if not isinstance(IMAGE_EXTENSIONS, list) or not all(isinstance(item, str) for item in IMAGE_EXTENSIONS):
        raise ValueError("IMAGE_EXTENSIONS must be a list of strings")

    logger.debug(f"Getting list of images from: {dir}")
    try:
        return getFilesFromDirectory(dir, exts=IMAGE_EXTENSIONS, recursive=recursive)
    except Exception as e:
        logger.error(f"Error while getting images from: {dir}. Error: {str(e)}")


def collectExistingFiles(directories):
    """Collect existing files in the directories."""
    unique_files = dict()
    for directory in directories:
        list_of_files = os.walk(directory)
        for root, _, files in list_of_files:
            for file in files:
                file_path = Path(os.path.join(root, file))
                hash_file = calculateHash(file_path)
                unique_files[hash_file] = file_path
    return unique_files

def copyImages(images, source_directory, destination_directory, unique_files, ignore_hashes, skip_duplicates):
    """Copy images to the destination directory."""
    for image in tqdm(images, desc='Loading Images'):
        image_path = Path(os.path.join(source_directory, image))
        image_hash = calculateHash(image_path)
        if skip_duplicates and image_hash in unique_files or image_hash in ignore_hashes:
            continue
        shutil.copy2(image_path, destination_directory)

def moveImages(sourceDirectory, destinationDirectory, sideDirectories=[], skipDuplicates=True, recursive=True, ignore_hashes=[]):
    try:
        logger.info(f"Moving images from {sourceDirectory} to {destinationDirectory}")
        images = getImagesFromDirectory(sourceDirectory, recursive=recursive)
        if not images:
            logger.warning("Selected directory did not contain any images.")
            return

        directories = [destinationDirectory] + sideDirectories if skipDuplicates else None
        unique_files = collectExistingFiles(directories) if skipDuplicates else None
        copyImages(images, sourceDirectory, destinationDirectory, unique_files, ignore_hashes, skipDuplicates)

    except Exception as e:
        logger.error(f"Error occurred while loading media: {str(e)}")

    return list(unique_files.keys()) if unique_files is not None else []



# Returns list of text files from a given directory
def getTextFilesFromDirectory(path):
    list_of_files = os.listdir(path)
    list_of_texts = []
    for f in list_of_files:
        if f.endswith('.txt'):
            list_of_texts.append(os.path.join(path, f))
    return list_of_texts

# GenerateImageName: Generates a name for the frame image based on video path, frame count, frame rate, and fps.    
def generateImageName(videoPath, frameCount, frameRate, fps):
    videoFileName = os.path.splitext(os.path.basename(videoPath))[0]
    imageName = videoFileName + '_' + str(frameCount / frameRate * fps) + ".png"
    return imageName

# RemoveLastWords: Removes last word from each line in a text file.
def removeLastWords(txtFile):
    with open(txtFile, 'r') as file:
        lines = [line[:line.rstrip().rfind(' ')] for line in file]

    with open(txtFile, 'w') as file:
        for line in lines:
            file.write(f'{line}\n')

# Returns the filename and extension of a file
def splitFileFromExtension(file):
    fileName, extension = os.path.splitext(file)
    return fileName, extension

def splitDirectoryFromFile(file_path):
    directory, file_name = os.path.split(file_path)
    return directory, file_name


# Unzips Files
def decompressFile(filePath, outputPath):
    if filePath.endswith('.zip'):
        with zipfile.ZipFile(filePath, 'r') as zip_ref:
            zip_ref.extractall(outputPath)
    elif filePath.endswith('.tar.gz'):
        with tarfile.open(filePath, 'r:gz') as tar_ref:
            tar_ref.extractall(outputPath)
    elif filePath.endswith('.tar.bz2'):
        with tarfile.open(filePath, 'r:bz2') as tar_ref:
            tar_ref.extractall(outputPath)
    elif filePath.endswith('.tar'):
        with tarfile.open(filePath, 'r:') as tar_ref:
            tar_ref.extractall(outputPath)
    elif filePath.endswith('.gz'):
        with gzip.open(filePath, 'rb') as f_in:
            with open(os.path.join(outputPath, os.path.splitext(os.path.basename(filePath))[0]), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    elif filePath.endswith('.bz2'):
        import bz2
        with bz2.open(filePath, 'rb') as f_in:
            with open(os.path.join(outputPath, os.path.splitext(os.path.basename(filePath))[0]), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    else:
        raise ValueError('Unsupported file type')
    
# CreateFile: Safely create a new file, with optional overwrite.
def createFile(file, overwrite=True):
    try:
        if os.path.exists(file):
            if overwrite:
                delete(file)
            else:
                print("File already exists and overwrite set to False.")
                return False
        with open(file, 'w') as f:
            pass
        return True
    except Exception as e:
        print(f"Unable to create file: {e}")
        return False

def move(src, dest_dir, replace=False):
    # Check if src file exists
    if not os.path.isfile(src):
        print(f"Source file does not exist: {src}")
        return

    # Check if destination directory exists, if not create it
    if not os.path.isdir(dest_dir):
        print(f"Destination directory does not exist, creating it: {dest_dir}")
        os.makedirs(dest_dir)

    filename = os.path.basename(src)
    dest_path = os.path.join(dest_dir, filename)

    # If a file with the same name exists in the destination directory
    if os.path.exists(dest_path):
        if replace:
            # If replace is True, move the file, replacing the existing file
            shutil.move(src, dest_path)
    else:
        # If the file does not exist in the destination directory, move it
        shutil.move(src, dest_path)

def delete(path, force=False):
    try:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            if len(os.listdir(path)) != 0:  # if directory is not empty
                if force:
                    logger.warning(f"The directory {path} is not empty. Force deleting.")
                    shutil.rmtree(path)
                else:
                    logger.warning(f"The directory {path} is not empty. Not deleting.")
                    return False
            else:
                shutil.rmtree(path)
        else:
            logger.warning(f"The path {path} does not exist.")
            return False

        logger.info(f"Successfully deleted {path}")
        return True

    except Exception as e:
        logger.error(f"Failed to delete {path}. Error: {str(e)}")
        return False




def copy(src, dest_dir, replace=False):
    try:
        if not os.path.isfile(src):
            logger.error(f"Source file does not exist: {src}")
            return False

        if not os.path.isdir(dest_dir):
            logger.info(f"Destination directory does not exist, creating it: {dest_dir}")
            os.makedirs(dest_dir)

        filename = os.path.basename(src)
        dest_path = os.path.join(dest_dir, filename)

        if os.path.exists(dest_path) and replace:
            os.remove(dest_path)

        shutil.copy(src, dest_path)
        logger.info(f"Copied {src} to {dest_path}")

        return True

    except Exception as e:
        logger.error(f"Failed to copy file. Error: {str(e)}")
        return False


def createDirectory(dir, overwrite=True):
    try:
        if os.path.exists(dir) and overwrite:
            shutil.rmtree(dir)

        os.mkdir(dir)
        logger.info(f"Directory created: {dir}")
        return dir, ""

    except Exception as e:
        logger.error(f"Failed to create directory. Error: {str(e)}")
        return None, str(e)


def removeDuplicates(directory):
    try:
        listOfFiles = os.walk(directory)
        uniqueFiles = dict()
        count = 0

        for root, _,  files in listOfFiles:
            for file in files:
                filePath = Path(os.path.join(root, file))
                hashFile = hashlib.md5(open(filePath, 'rb').read()).hexdigest()

                if hashFile not in uniqueFiles:
                    uniqueFiles[hashFile] = filePath
                else:
                    os.remove(filePath)
                    count += 1

        logger.info(f"Removed {count} duplicate files from {directory}")
        return count

    except Exception as e:
        logger.error(f"Failed to remove duplicates. Error: {str(e)}")
        return 0

def getMatchingTextFile(file_path):
    try:
        fileName, extension = os.path.splitext(file_path)
        if not extension:
            raise ValueError(f"File has no extension: {file_path}")
        matching_file = f"{fileName}.txt"
        logger.info(f"Matching text file for {file_path} is {matching_file}")
        return matching_file
    except ValueError as ve:
        logger.error(str(ve))
        raise ve
    except Exception as e:
        logger.error(f"Failed to find matching text file. Error: {str(e)}")
        return None

def removeMatchingImage(txt_file):
    try:
        # Ensure the text file exists
        if not os.path.isfile(txt_file):
            raise FileNotFoundError(f"No such file: '{txt_file}'")

        deleted_files = []

        # Get the base name of the text file without the extension
        base_name = os.path.splitext(os.path.basename(txt_file))[0]

        # Define the directory in which the text file resides
        dir_name = os.path.dirname(txt_file)

        # Loop through all files in the directory
        for file_name in os.listdir(dir_name):
            file_base_name, ext = os.path.splitext(file_name)

            # Check if the file is an image file with matching base name
            if file_base_name.lower() == base_name.lower() and ext != '.txt':
                # If it is, delete the file
                file_path = os.path.join(dir_name, file_name)
                os.remove(file_path)
                deleted_files.append(file_name)

        logger.info(f"Removed {len(deleted_files)} matching images.")
        return deleted_files

    except FileNotFoundError:
        logger.error(f"Failed to remove matching images. Error: No such file: '{txt_file}'")
        raise  # re-raise the FileNotFoundError

    except Exception as e:
        logger.error(f"Failed to remove matching images. Error: {str(e)}")
        return None
    

def removeLastWords(txt):
    try:
        with open(txt, 'r') as f:
            lines = [line[:line.rstrip().rfind(' ')] for line in f]

        with open(txt, 'w') as f:
            for line in lines:
                f.write(f'{line}\n')

        logger.info(f"Successfully removed last word from each line in {txt}")
        return True

    except Exception as e:
        logger.error(f"Failed to remove last words. Error: {str(e)}")
        return False
    

def sortByDate(src_dir):
    try:
        # iterate over all the files in the directory
        for filename in tqdm(os.listdir(src_dir)):
            file = os.path.join(src_dir, filename)

            # ignore directories
            if os.path.isfile(file):
                # get the modification time and convert it into a date string
                date = get_creation_time(file)

                # create a new directory path
                new_dir = os.path.join(src_dir, date)

                # create new directory if it doesn't exist
                if not os.path.exists(new_dir):
                    os.mkdir(new_dir)

                # move the file to new directory
                shutil.move(file, new_dir)

        logger.info(f"Successfully sorted files in {src_dir} by date.")
        return True

    except Exception as e:
        logger.error(f"Failed to sort files by date. Error: {str(e)}")
        return False


def get_creation_time(filename):
    try:
        # Regular expression pattern to match Unix timestamp in filename
        pattern = r'(\d{10})'
        
        # Search for Unix timestamp in filename
        match = re.search(pattern, filename)

        if match:
            # Convert Unix timestamp to date
            timestamp = int(match.group(1))
            date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            logger.info(f"Creation date for {filename} is {date}")
            return date
        else:
            logger.error(f"No match found in {filename}")
            return None

    except Exception as e:
        logger.error(f"Failed to get creation time. Error: {str(e)}")
        return None


def convertNameToText(name):
    try:
        txt_name = os.path.splitext(name)[0] + '.txt'
        logger.info(f"Converted {name} to {txt_name}")
        return txt_name
    except Exception as e:
        logger.error(f"Failed to convert name to text. Error: {str(e)}")
        return None


def deleteFileByLabel(label_path, directory, extensions=IMAGE_EXTENSIONS):
    try:
        # Get the filename from the label_path
        base_name = os.path.basename(label_path)

        # For each extension, try to delete the file
        for ext in extensions:
            # Construct the full filename by appending the extension
            filename = os.path.splitext(base_name)[0] + ext

            # Construct the full file path
            full_path = os.path.join(directory, filename)

            # If the file exists, delete it
            if os.path.isfile(full_path):
                os.remove(full_path)
                logger.info(f"File {full_path} deleted.")
        return True

    except Exception as e:
        logger.error(f"Failed to delete file by label. Error: {str(e)}")
        return False


def deleteFilesWithoutLabel(file_directory, label_directory, extensions=IMAGE_EXTENSIONS):
    try:
        # Iterate over each file in the directory
        for ext in extensions:
            for filename in glob.glob(os.path.join(file_directory, '*'+ext)):
                # Construct the corresponding label path
                label_path = os.path.join(label_directory, os.path.splitext(os.path.basename(filename))[0] + '.txt')

                # If the label file does not exist, delete the file
                if not os.path.isfile(label_path):
                    os.remove(filename)
                    logger.info(f"Deleted {filename} without label.")
        return True

    except Exception as e:
        logger.error(f"Failed to delete files without label. Error: {str(e)}")
        return False


def remove_duplicates(directory):
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        unique_files = dict()
        count = 0

        for file in tqdm(files, 'Removing duplicates...'):
            file_path = Path(os.path.join(directory, file))
            file_hash = calculateHash(file_path)

            if file_hash is not None:
                if file_hash not in unique_files:
                    unique_files[file_hash] = file_path
                else:
                    os.remove(file_path)
                    count += 1
                    logger.info(f"File {file_path} deleted, it was a duplicate.")

        logger.info(f'Removed {count} duplicates')
        return count

    except Exception as e:
        logger.error(f"Failed to remove duplicates. Error: {str(e)}")
        return None

def calculateHash(file_path, hash_type='md5'):
    '''Calculate the hash of a given file.'''
    try:
        # map the hash_type to the corresponding hashlib function
        hash_func = getattr(hashlib, hash_type)
    except AttributeError:
        logger.error(f"Invalid hash type: {hash_type}. Available types are md5, sha1, sha256, sha512.")
        return None
    try:
        with open(file_path, 'rb') as f:
            file_hash = hash_func(f.read()).hexdigest()
        logger.info(f"Hash ({hash_type}) calculated for file: {file_path}")
        return file_hash
    except Exception as e: 
        logger.error(f"An error occurred while hashing the file: {e}")
        return None
    
def emptyDirectory(directory, remove_subdirs=False):
    try:
        logger.info(f"Starting to empty directory: {directory}")
        for file in os.listdir(directory):
            filepath = os.path.join(directory, file)
            if os.path.isfile(filepath):
                os.remove(filepath)
                logger.debug(f"Removed file: {filepath}")
            elif os.path.isdir(filepath) and remove_subdirs:
                shutil.rmtree(filepath)
                logger.debug(f"Removed subdirectory: {filepath}")
        logger.info(f"Successfully emptied directory: {directory}")
        return True
    except Exception as e:
        logger.error(f"Failed to empty directory: {directory}. Error: {str(e)}")
        return False

def getNewestFile(directory, extensions, recursive=True, startlevel=0, endlevel=None):
    newest_file = ''
    newest_time = 0
    logger = logging.getLogger(__name__)

    if not os.path.exists(directory):
        logger.error(f"The directory {directory} does not exist.")
        return ''

    try:
        for root, dirs, files in os.walk(directory):
            if recursive or root == directory:
                level = root[len(directory):].count(os.sep)
                if level >= startlevel and (endlevel is None or level <= endlevel):
                    for ext in extensions:
                        for file in fnmatch.filter(files, '*.' + ext):
                            file_path = os.path.join(root, file)
                            file_time = os.path.getctime(file_path)
                            if file_time > newest_time:
                                newest_file = file_path
                                newest_time = file_time
    except Exception as e:
        logger.error(f"An error occurred while searching for the newest file: {str(e)}")

    if newest_time == 0:
        logger.warning(f"No files with the given extensions {extensions} were found in the directory {directory}.")

    return newest_file if newest_time > 0 else ''