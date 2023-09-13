import mf

from PIL import Image
from tqdm import tqdm
import os

def is_black_and_white(image_path):
    """Check if the image is black and white."""
    with Image.open(image_path) as img:
        # If the image is already in 'L' mode, then it's grayscale
        if img.mode == 'L':
            return True
        pixels = list(img.getdata())
        for pixel in pixels:
            # Ensure it's a RGB tuple and not a single grayscale value
            if len(pixel) == 3:
                r, g, b = pixel
                if r != g or r != b:
                    return False
    return True


def remove_black_and_white_images(image_files):
    """Remove black and white images from the provided list of image files."""
    
    deleted_count = 0

    # Creating the progress bar instance
    pbar = tqdm(image_files, desc='Deleted: 0')
    for image_file in pbar:
        if is_black_and_white(image_file):
            try:
                text_file = mf.convertNameToText(image_file)
                os.remove(image_file)
                os.remove(text_file)
                deleted_count += 1
                # Updating the description to show the number of deleted files
                pbar.set_description(f"Deleted: {deleted_count}")
            except Exception as e:
                print(f"Error removing {image_file}. Reason: {e}")


mf.ConfigureLogger("INFO")
dir = mf.browseForDirectory()
image_files = mf.getImagesFromDirectory(dir)
remove_black_and_white_images(image_files)
