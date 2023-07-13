import os
import concurrent.futures
from PIL import Image

import mf

"""
Deletes all images in a directory with a strong red tint.

Uses multithreading. Could use gpu one day

"""

# Function to process each image
import random

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
                if filename.endswith(".jpg") or filename.endswith(".png")]

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
            print(f"Progress: {i}/{len(image_files)} ({100.0 * i / len(image_files):.2f}%), Deleted images: {deleted_images}", end='\r')
