import cv2
import os
from tqdm import tqdm
from PIL import Image
import random
import concurrent.futures
import logging

from .file import getImagesFromDirectory, generateImageName
from .defs import IMAGE_EXTENSIONS

logger = logging.getLogger('mf')

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
    # Load the image
    image = Image.open(filename)
    
    # Get the image data and pick n random pixels
    data = image.getdata()
    total_pixels = len(data)
    if number_of_pixels > total_pixels:
        raise ValueError(f'n = {number_of_pixels} is larger than the total number of pixels in the image = {total_pixels}')
    sample_pixels = random.sample(list(data), number_of_pixels)

    # Calculate the average red, green, and blue values
    red_sum, green_sum, blue_sum, count = 0, 0, 0, 0
    for pixel in sample_pixels:
        red_sum += pixel[0]
        green_sum += pixel[1]
        blue_sum += pixel[2]
        count += 1
    red_avg = red_sum / count
    green_avg = green_sum / count
    blue_avg = blue_sum / count

    # If the red value is significantly higher than the others, delete the image
    if red_avg > green_avg * 2 and red_avg > blue_avg * 2:
        os.remove(filename)
        return True
    return False


def deleteRedFromDirectory(directory):
    # Get a list of all image files in the directory
    image_files = [os.path.join(directory, filename) for filename in os.listdir(directory)
                if (filename.endswith(".jpg") or filename.endswith(".png")) and os.path.isfile(os.path.join(directory, filename))]

    # Use a ThreadPoolExecutor to process multiple images in parallel
    deleted_images = 0
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit tasks to thread pool
        futures = {executor.submit(containsMuchRed, image_file, 100): image_file for image_file in image_files}

        for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
            # Check if the image was deleted
            if future.result():
                deleted_images += 1
            # Print progress
            print(f"Progress: {i}/{len(image_files)} ({100.0 * i / len(image_files):.2f}%), Deleted Red Images: {deleted_images}", end='\r')
