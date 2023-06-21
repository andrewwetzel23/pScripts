import cv2
import os
from pathlib import Path
from os import scandir, listdir
from os.path import join, splitext, basename
from PIL import Image, ImageEnhance
import shutil
import subprocess
from tqdm import tqdm
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilename
from pynput import keyboard


# Runs a batch file
def run_batch_file(batch_path):
    p = subprocess.Popen(batch_path, creationflags=subprocess.CREATE_NEW_CONSOLE, shell=False)
    p.communicate()


# checks if there are any videos to convert
def any_mp4s_to_convert(model_path):
    media_path = join(model_path, 'media')
    return True if get_videos_from_dir(media_path) else False


# Checks if there are any images to train
def any_images_to_train(model_path):
    media_path = join(model_path, 'media')
    return True if get_images_from_dir(media_path) else False


# Returns list of directories from a given directory
def get_subdirectories(path):
    return [f.name for f in scandir(path) if f.is_dir()]


# Returns list of videos from a given directory
def get_videos_from_dir(path):
    list_of_files = listdir(path)
    list_of_videos = []
    for f in list_of_files:
        if f.endswith('.mp4'):
            list_of_videos.append(f)
    return list_of_videos

def get_files_of_type(dir, ext):
    list_of_files = listdir(dir)
    list_of_ext = []
    for f in list_of_files:
        if f.endswith(ext):
            list_of_ext.append(f)
    return list_of_ext


# Replaces file extension with .txt
def convert_name_to_text(file):
    return remove_extension(file) + ".txt"


# Returns list of images from a given directory
def get_images_from_dir(path):
    list_of_files = listdir(path)
    list_of_pictures = []
    for f in list_of_files:
        if f.endswith(('.jpg', '.jpeg', '.png')):
            list_of_pictures.append(f)
    return list_of_pictures


# Returns list of text files from a given directory
def get_texts_from_dir(path):
    list_of_files = listdir(path)
    list_of_texts = []
    for f in list_of_files:
        if f.endswith('.txt'):
            list_of_texts.append(os.path.join(path, f))
    return list_of_texts

def convert_to_grayscale(path):
    if listdir(path):
        list_of_images = get_images_from_dir(path)
        for img in tqdm(list_of_images, desc=f'Converting images to grayscale...'):
            image = cv2.imread(join(path, img))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(join(path, img), gray)
    else:
        print('Dir is empty')

def resize_image(image, size, keepAspectRatio=True):
    img = cv2.imread(image)
    max_width, max_height = size

    if keepAspectRatio:
        AR = max_width/max_height                
        image_height, image_width, image_channels = img.shape
        if image_width/image_height > AR:
            scale = image_width/max_width
        else:
            scale = image_height/max_height
        width = image_width/scale
        height = image_height/scale
        new_size = [int(width), int(height)]
        img_resized = cv2.resize(img, new_size)        
    else:
        img_resized = cv2.resize(img, size)

        cv2.imwrite(image, img_resized)

def resize_images(path, size):
    AR = size[0]/size[1]
    if listdir(path):
        list_of_images = get_images_from_dir(path)
        for img in tqdm(list_of_images, desc=f'Resizing images to {size}...'):
            image = cv2.imread(join(path, img))
            
            h, w, c = image.shape
            if w/h > AR:
                scale = w/size[0]
            else:
                scale = h/size[1]
            width = w/scale
            height = h/scale
            new_size = [int(width), int(height)]
            img_resized = cv2.resize(image, new_size)

            cv2.imwrite(join(path, img), img_resized)


# Creates copies of images which are brighter and darker
def augment_training_images(model_path):
    img_path = join(model_path, 'media')
    if listdir(img_path):
        print('Augmenting images...')

        images = get_images_from_dir(img_path)
        labels = get_texts_from_dir(img_path)

        for i, image in tqdm(enumerate(images), desc='Augmenting images...'):
            img = Image.open(join(img_path, image))
            enhancer = ImageEnhance.Brightness(img)
            img_dark = enhancer.enhance(.5)
            img_lite = enhancer.enhance(1.5)

            img_dark.save(join(img_path, f'dark_{image}'))
            img_lite.save(join(img_path, f'lite_{image}'))

            shutil.copy(join(img_path, labels[i]), join(img_path, f'dark_{labels[i]}'))
            shutil.copy(join(img_path, labels[i]), join(img_path, f'lite_{labels[i]}'))

        images = get_images_from_dir(img_path)
        print(f'Images after augmenting: {len(images)}')


# Converts an mp4 to jpg at a set fps
def convert_mp4_to_jpg(mp4_path, img_path, mp4, fps):
    mp4_path = join(mp4_path, mp4)
    video = cv2.VideoCapture(mp4_path)
    frame_count = 0
    success, image = video.read()
    while success:
        frame_name = splitext(basename(mp4))[0] + '_' + str(frame_count / 60 * fps) + ".jpg"
        cv2.imwrite(join(img_path, frame_name), image)
        for i in range(0, int(60 / fps)):
            success, image = video.read()
        frame_count += 60 / fps


# Converts all videos to jpg
def convert_videos(dir, fps):
    list_of_videos = get_videos_from_dir(dir)
    for vid in tqdm(list_of_videos, desc=f'Converting videos to jpg'):
        convert_mp4_to_jpg(dir, dir, vid, fps)
        os.remove(join(dir, vid))

    print('No more videos to convert')


# Returns the list of objects that the model detects
def get_model_objects(model_path):
    f = open(join(model_path, 'cfg', 'objects.cfg'), 'r')
    objects = f.read().splitlines()
    return objects


# Creates the yaml file read by yolov5 for training
def create_data_file(model_path):
    annotation_path = join(model_path, 'annotations')
    train_path = join(annotation_path, 'train/images')
    valid_path = join(annotation_path, 'valid/images')

    objects = get_model_objects(model_path)

    f = open(join(annotation_path, 'data.yaml'), 'w')
    f.write(f'train: {train_path}\n')
    f.write(f'val: {valid_path}\n\n')
    f.write(f'nc: {len(objects)}\n')
    f.write('names: [')
    for obj in objects:
        f.write(f'\'{obj}\', ')
    f.write(']\n')
    f.close()


# Removes last word from each line
def remove_last_words(txt):
    with open(txt, 'r') as f:
        lines = [line[:line.rstrip().rfind(' ')] for line in f]

    with open(txt, 'w') as f:
        for line in lines:
            f.write(f'{line}\n')

def remove_extension(file):
    return os.path.splitext(file)[0]

def get_filename(path):
    return Path(path).stem

def browse_for_file():
    Tk().withdraw()
    return askopenfilename()

def browse_for_dir():
    Tk().withdraw()
    return askdirectory()

def get_extension(file):
    return Path(file).suffix

def get_lines_from_file(file):
    with open(path, 'r') as f:
        return f.readlines()

def asd():
    while True:
        with keyboard.Events() as events:
            event = events.get(1e6)
            
            if event.key == keyboard.KeyCode.from_char('a'):
                return 1
            elif event.key == keyboard.KeyCode.from_char('s'):
                return 2
            elif event.key == keyboard.KeyCode.from_char('d'):
                return 3
    return 0