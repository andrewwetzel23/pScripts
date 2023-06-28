import cv2
import os
from tqdm import tqdm
from PIL import Image

from .file import getImagesFromDirectory, generateImageName
from .defs import IMAGE_EXTENSIONS

# ImagesToGrayscale: Converts all images in a directory to grayscale
def imagesToGrayscale(path):
    if os.listdir(path):
        list_of_images = getImagesFromDirectory(path)
        for img in tqdm(list_of_images, desc=f'Converting images to grayscale...'):
            image = cv2.imread(os.path.join(path, img))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(os.path.join(path, img), gray)
    else:
        print('Dir is empty')

# Converts an mp4 to jpg at a set fps
def convertVideoToJpgs(videoPath, outputPath, fps):
    video = cv2.VideoCapture(videoPath)
    frameRate = video.get(cv2.CAP_PROP_FPS)  # Get the actual fps of the video

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
    # Convert image to RGB if it's not
    if image.mode != "RGB":
        image = image.convert("RGB")
    # Get the RGB pixel values of the image
    pixels = image.getdata()

    # Check if all RGB values are the same for each pixel
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


def resizeImages(dir, size, recursiveSearch=False, keepAspectRatio=True):
	images = getImagesFromDirectory(dir, recursiveSearch)
	for image in tqdm(images, "Resizing images..."):
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