import cv2
import os
from tqdm import tqdm
from PIL import Image
import random
import concurrent.futures
import logging
import numpy as np

from .file import getImagesFromDirectory, generateImageName, delete
from .defs import IMAGE_EXTENSIONS

logger = logging.getLogger('mf')

def deleteLandscape(image_path):
    with Image.open(image_path) as img:
        width, height = img.size

    if width > height:
        delete(image_path)
        logger.debug("Delete Landscape: Landscape - Deleted")
        return True
    else:
        logger.debug("Delete Landscape: Portrait - Not Deleted")
        return False

def deleteLandscapeFromDirectory(directory):
    count = 0
    images = getImagesFromDirectory(directory)
    for image in tqdm(images, desc="Deleting landscape images..."):
        if deleteLandscape(image):
            count += 1
    logger.info(f"Deleted {count} landscape images.")

# ImagesToGrayscale: Converts all images in a directory to grayscale
def imagesToGrayscale(path):
    logger.debug(f"Converting images to grayscale at path: {path}")
    if os.listdir(path):
        list_of_images = getImagesFromDirectory(path)
        for img in tqdm(list_of_images, desc=f'Converting images to grayscale...'):
            image = cv2.imread(os.path.join(path, img))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(os.path.join(path, img), gray)
    else:
        logger.info('Directory is empty')

def convertVideoToJpgs(videoPath, outputPath, fps):
    logger.debug(f"Converting video at {videoPath} to jpgs at {outputPath} with fps {fps}")
    video = cv2.VideoCapture(videoPath)
    frameRate = video.get(cv2.CAP_PROP_FPS)  # frame rate of the video

    frameCount = 0
    success, image = video.read()
    while success:
        # Save frame as JPEG file
        imageName = generateImageName(videoPath, frameCount, frameRate, fps)
        cv2.imwrite(os.path.join(outputPath, imageName), image)

        # Adjust the count to the fps provided
        for i in range(0, int(frameRate / fps)):
            success, image = video.read()

        frameCount += 1

def imageIsGrayscale(image):
    logger.debug(f"Checking if image is grayscale")
    if image.mode != "RGB":
        image = image.convert("RGB")
    pixels = image.getdata()

    if all(r == g == b for r, g, b in pixels):
        return True
    else:
        return False


def deleteGrayscaleImages(directory):
    count = 0
    for file_name in tqdm(os.listdir(directory)):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            try:
                image = Image.open(file_path)
                if imageIsGrayscale(image):
                    os.remove(file_path)
                    count += 1
            except (IOError, OSError):
                print(f"Error opening or processing file: {file_name}")
    return count


def resizeImages(dir, size,recursiveSearch=False, keepAspectRatio=True):
    images = getImagesFromDirectory(dir, recursiveSearch)
    for image in tqdm(images, desc="Resizing images..."):
        resizeImage(image, size, keepAspectRatio)



# ResizeImage: Resize an image, optionally keeping its aspect ratio.
def resizeImage(imagePath: str, targetSize: tuple, keepAspectRatio=True):
    # Read the image using OpenCV
    image = cv2.imread(imagePath)

    if keepAspectRatio:
        # If we want to keep the aspect ratio, we calculate the scale factor
        # and resize the image to that scale.
        maxWidth, maxHeight = targetSize
        targetAspectRatio = maxWidth / maxHeight

        # Get the current image dimensions
        imageHeight, imageWidth, _ = image.shape
        imageAspectRatio = imageWidth / imageHeight

        # Determine the scale based on width or height
        if imageAspectRatio > targetAspectRatio:
            scale = imageWidth / maxWidth
        else:
            scale = imageHeight / maxHeight

        # Calculate new dimensions and resize
        newImageWidth = int(imageWidth / scale)
        newImageHeight = int(imageHeight / scale)
        newImageSize = (newImageWidth, newImageHeight)
        imageResized = cv2.resize(image, newImageSize)
    else:
        # If we do not want to keep the aspect ratio, we resize to the target size directly.
        imageResized = cv2.resize(image, targetSize)

    # Write the resized image back to the file
    cv2.imwrite(imagePath, imageResized)

def deleteBadImages(dir, console):
    images = getImagesFromDirectory(dir)

    count = 0
    for image in tqdm(images, file=console, desc="Removing bad images"):
        count += 1
        imagePath = os.path.join(dir, image)
        if os.path.getsize(imagePath) == 0:
            os.remove(imagePath)
    if count > 0:
        console.print(f"Remove {count} bad images.")
    else:
        console.print("No bad images found.")

def containsMuchRed(filename, number_of_pixels):
    with Image.open(filename) as image:
        data = np.array(image)

        # Ensure image has at least 3 channels
        if data.shape[2] < 3:
            return False

        h, w, _ = data.shape
        total_pixels = h * w

        if number_of_pixels > total_pixels:
            raise ValueError(f'n = {number_of_pixels} is larger than the total number of pixels in the image = {total_pixels}')

        # Randomly sample pixel indices
        idx = np.random.choice(h * w, number_of_pixels, replace=False)
        sampled_pixels = data[idx // w, idx % w, :3]  # Assuming image is RGB

        # Calculate average RGB
        avg_color = sampled_pixels.mean(axis=0)

        # If the red value is significantly higher than the others, delete the image
        if avg_color[0] > avg_color[1] * 2 and avg_color[0] > avg_color[2] * 2:
            os.remove(filename)
            return True
        
    return False


def deleteRedFromDirectory(directory):
    # Get a list of all image files in the directory
    image_paths = getImagesFromDirectory(directory)

    deleted_images = 0
    
    # Create a tqdm progress bar
    with tqdm(total=len(image_paths), desc="Deleting Red Images...", dynamic_ncols=True) as pbar:
        for image_file in image_paths:
            if containsMuchRed(image_file, 100):
                deleted_images += 1

            # Update progress bar and display the number of images deleted so far
            pbar.set_postfix(deleted=f"{deleted_images}/{len(image_paths)}")
            pbar.update(1)
