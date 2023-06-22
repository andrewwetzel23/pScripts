import os
import zipfile
import tarfile
import gzip
import shutil

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

def getFilesFromDirectory(dir, ext=""):
    list_of_files = os.listdir(dir)
    list_of_ext = []
    for f in list_of_files:
        if f.endswith(ext):
            list_of_ext.append(f)
    return list_of_ext

# Returns list of images from a given directory
def getImagesFromDirectory(path):
    list_of_files = os.listdir(path)
    list_of_pictures = []
    for f in list_of_files:
        if f.endswith(('.jpg', '.jpeg', '.png')):
            list_of_pictures.append(f)
    return list_of_pictures

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