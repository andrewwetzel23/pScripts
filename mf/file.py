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

from .defs import IMAGE_EXTENSIONS

# BrowseForDir: Open a dialog to browse for a directory.
def browseForDirectory():
	tkinter.Tk().withdraw()
	return askdirectory()

# BrowseForFile: Open a dialog to browse for a file.
def browseForFile():
	tkinter.Tk().withdraw()
	return askopenfilename()

# Returns list of directories from a given directory
def getSubdirectoriesFromDirectory(path):
    return [f.name for f in os.scandir(path) if f.is_dir()]

# Returns list of videos from a given directory
def getVideosFromDirectory(path):
    list_of_files = os.listdir(path)
    list_of_videos = []
    for f in list_of_files:
        if f.endswith('.mp4'):
            list_of_videos.append(f)
    return list_of_videos

def getFilesFromDirectory(dir, exts=None, recursive=False):
    if exts is None:
        exts = [""]

    if not os.path.isdir(dir):
        raise ValueError(f"Directory does not exist: {dir}")

    files = []
    for ext in exts:
        if not ext.startswith("."):
            ext = "." + ext

        if recursive:
            paths = glob.glob(os.path.join(dir, "**", "*"+ext), recursive=True)
        else:
            paths = glob.glob(os.path.join(dir, "*"+ext))

        files.extend(paths)

    return files


def getImagesFromDirectory(dir, recursive=False):
    if not isinstance(IMAGE_EXTENSIONS, list) or not all(isinstance(item, str) for item in IMAGE_EXTENSIONS):
        raise ValueError("IMAGE_EXTENSIONS must be a list of strings")
    return getFilesFromDirectory(dir, exts=IMAGE_EXTENSIONS, recursive=recursive)

def moveImages(sourceDirectory, destinationDirectory, sideDirectories=[], skipDuplicates=True, recursive=True, ignore_hashes=[]):
    try:
        images = getImagesFromDirectory(sourceDirectory, recursive=recursive)
        if not images:
            print("Selected directory did not contain any images.")
            return
        
        # Dictionary to hold unique images from directories if skip_duplicates is set
        unique_files = dict() if skipDuplicates else None

        # List of directories to check for existing files
        directories = [destinationDirectory]
        if skipDuplicates:
            for directory in sideDirectories:
                directories.append(directory)

        if skipDuplicates:
            # Listing out all the files inside our directories
            for directory in directories:
                list_of_files = os.walk(directory)
                for root, _, files in list_of_files:
                    # Running a for loop on all the files
                    for file in files:
                        # Finding complete file path
                        file_path = Path(os.path.join(root, file))

                        # Converting all the content of our file into md5 hash.
                        Hash_file = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
                        
                        # Add file hash to the dictionary
                        unique_files[Hash_file] = file_path
        
        # Copy only those images that do not exist in the specified directories and not in ignore list
        for image in tqdm(images, desc='Loading Images'):
            image_path = Path(os.path.join(sourceDirectory, image))
            if skipDuplicates:
                # Compute md5 hash of the image
                image_hash = hashlib.md5(open(image_path, 'rb').read()).hexdigest()
                # Copy the image only if it's not present in the specified directories and not in ignore list
                if image_hash not in unique_files and image_hash not in ignore_hashes:
                    shutil.copy2(image_path, destinationDirectory)
            else:
                # Copy the image only if it's not in ignore list
                if image_hash not in ignore_hashes:
                    shutil.copy2(image_path, destinationDirectory)

    except Exception as e:
        print(f"Error occurred while loading media: {str(e)}")

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
    imageName = videoFileName + '_' + str(frameCount / frameRate * fps) + ".jpg"
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
                removeFile(file)
            else:
                print("File already exists and overwrite set to False.")
                return False
        with open(file, 'w') as f:
            pass
        return True
    except Exception as e:
        print(f"Unable to create file: {e}")
        return False

# RemoveFile: Safely remove a file.
def removeFile(file):
    try:
        os.remove(file)
    except OSError as e:
        if e.errno != errno.ENOENT:  # Raise the exception if it's not because the file doesn't exist
            print(f"Error: {e}")
            return False
    return True

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

def delete(path):
    if os.path.isfile(path):
        try:
            os.remove(path)
            return True
        except Exception as e:
            return False
    elif os.path.isdir(path):
        try:
            shutil.rmtree(path)
            return True
        except Exception as e:
            return False
    else:
        print(f"The path {path} does not exist.")


def copy(src, dest_dir, replace=False):
    # Check if src file exists
    if not os.path.isfile(src):
        return False

    # Check if destination directory exists, if not create it
    if not os.path.isdir(dest_dir):
        print(f"Destination directory does not exist, creating it: {dest_dir}")
        os.makedirs(dest_dir)

    filename = os.path.basename(src)
    dest_path = os.path.join(dest_dir, filename)

    # If a file with the same name exists in the destination directory
    if os.path.exists(dest_path):
        if replace:
            # If the replace option is true, remove the old file and copy the new one
            os.remove(dest_path)
            shutil.copy(src, dest_path)
    else:
        # If the file does not exist in the destination directory, copy it
        shutil.copy(src, dest_path)


# CreateDirectory: Safely create a new directory, with optional overwrite.
def createDirectory(dir, overwrite=True):
    try:
        if os.path.exists(dir):
            if overwrite:
                removeDirectory(dir)
            else:
                err = "Directory already exists and overwrite set to False."
                return dir, err
        os.mkdir(dir)
        return dir, ""
    except Exception as e:
        err = f"Unable to create directory: {e}"
        return None, err

# RemoveDirectory: Safely remove a directory.
def removeDirectory(dir):
    try:
        shutil.rmtree(dir)
    except OSError as e:
        if e.errno != errno.ENOENT:  # Raise the exception if it's not because the directory doesn't exist
            print(f"Error: {e}")
            return False
    return True

def removeDuplicates(directory):
    filePath = directory
    listOfFiles = os.walk(directory)

    uniqueFiles = dict()
    count = 0

    for root, _,  files in listOfFiles:
        # Iterate over all the files
        for file in tqdm(files, 'Removing duplicates...'):
            filePath = Path(os.path.join(root, file))

            # Convert all the content of our file into an md5 hash.
            hashFile = hashlib.md5(open(filePath, 'rb').read()).hexdigest()

            # If file hash has already been added, we'll simply delete that file
            if hashFile not in uniqueFiles:
                uniqueFiles[hashFile] = filePath
            else:
                os.remove(filePath)
                count += 1
                
    return count

def getMatchingTextFile(image_path):
    ext_pattern = '|'.join(IMAGE_EXTENSIONS).replace('.', r'\.')
    return re.sub(f'({ext_pattern})$', '.txt', image_path, flags=re.IGNORECASE)

def removeMatchingImage(txt_file):
    deletedFiles = []

    # Get the base name of the text file without the extension
    base_name = os.path.splitext(txt_file)[0]

    # Define the directory in which the text file resides
    dir_name = os.path.dirname(txt_file)

    # Loop through all files in the directory
    for file_name in os.listdir(dir_name):
        # Check if the file is an image file with matching base name
        if any(file_name.lower() == base_name + ext for ext in IMAGE_EXTENSIONS):
            # If it is, delete the file
            os.remove(os.path.join(dir_name, file_name))
            deletedFiles += file_name

    return deletedFiles

# Removes last word from each line
def removeLastWords(txt):
    with open(txt, 'r') as f:
        lines = [line[:line.rstrip().rfind(' ')] for line in f]

    with open(txt, 'w') as f:
        for line in lines:
            f.write(f'{line}\n')

def sortByDate(src_dir):
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
                createDirectory(new_dir)

            # move the file to new directory
            move(file, new_dir)

def get_creation_time(filename):
    # Regular expression pattern to match Unix timestamp in filename
    pattern = r'(\d{10})'
    
    # Search for Unix timestamp in filename
    match = re.search(pattern, filename)

    if match:
        # Convert Unix timestamp to date
        timestamp = int(match.group(1))
        date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        return date
    else:
        return None
    
def convertNameToText(name):
    return os.path.splitext(name)[0] + '.txt'

import os

def deleteFileByLabel(label_path, directory, extensions=IMAGE_EXTENSIONS):
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
            try:
                delete(full_path)  # using mf.delete for deleting files
            except Exception as e:
                pass


def deleteFilesWithoutLabel(file_directory, label_directory, extensions=IMAGE_EXTENSIONS):
    # Iterate over each file in the directory
    for ext in extensions:
        for filename in glob.glob(os.path.join(file_directory, '*'+ext)):
            # Construct the corresponding label path
            label_path = os.path.join(label_directory, os.path.splitext(os.path.basename(filename))[0] + '.txt')

            # If the label file does not exist, delete the file
            if not os.path.isfile(label_path):
                try:
                    delete(filename)  # using mf.delete for deleting files
                    print(f"Deleted {filename}")
                except Exception as e:
                    print(f"Error deleting {filename}: {e}")