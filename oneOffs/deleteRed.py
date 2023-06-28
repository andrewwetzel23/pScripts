import os
import concurrent.futures
from PIL import Image

from system import browse_for_dir

"""
Deletes all images in a directory with a strong red tint.

Uses multithreading. Could use gpu one day

"""

# Function to process each image
def process_image(filename):
    # Load the image
    image = Image.open(filename)

    # Calculate the average red, green, and blue values
    red_sum, green_sum, blue_sum, count = 0, 0, 0, 0
    for pixel in image.getdata():
        red_sum += pixel[0]
        green_sum += pixel[1]
        blue_sum += pixel[2]
        count += 1
    red_avg = red_sum / count
    green_avg = green_sum / count
    blue_avg = blue_sum / count

    # If the red value is significantly higher than the others, delete the image
    if red_avg > green_avg * 1.5 and red_avg > blue_avg * 1.5:
        os.remove(filename)
        return True
    return False

# Change this to the directory you want to use
directory = browse_for_dir()

# Get a list of all image files in the directory
image_files = [os.path.join(directory, filename) for filename in os.listdir(directory)
               if filename.endswith(".jpg") or filename.endswith(".png")]

# Use a ThreadPoolExecutor to process multiple images in parallel
deleted_images = 0
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Submit tasks to thread pool
    futures = {executor.submit(process_image, image_file): image_file for image_file in image_files}

    for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
        # Check if the image was deleted
        if future.result():
            deleted_images += 1
        # Print progress
        print(f"Progress: {i}/{len(image_files)} ({100.0 * i / len(image_files):.2f}%), Deleted images: {deleted_images}", end='\r')
