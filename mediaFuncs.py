import cv2
import os
from tqdm import tqdm

from fileFuncs import getImagesFromDirectory, generateImageName

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