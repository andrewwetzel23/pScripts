import os
from PIL import Image
import logging

from .file import (createDirectory, splitFileFromExtension, splitDirectoryFromFile, delete, 
                   convertNameToText, join, getImagesFromDirectory )

from ultralytics import YOLO

logger = logging.getLogger('mf')


def detectImages(dir, threshold, weights):
    detectionDirectory, _ = createDirectory(os.path.join(dir, "detections"), overwrite=True)
    model = YOLO(weights)
    model.predict(source=dir, conf=threshold, project=detectionDirectory, save_txt=True, device=0)

def labelContainsObject(label, objectID):
    with open(label, 'r') as f:
        for line in f:
            if int(line.split(' ')[0]) == objectID:
                return True

def cropAroundObjects(save_directory, image_path, label_path, object_id, width_ratio, height_ratio):
    createDirectory(save_directory, overwrite=False)
    count = 0
    fname = splitDirectoryFromFile(splitFileFromExtension(image_path)[0])[1]
    coordinates = parseYoloCoordinates(label_path, object_id)

    for coordinate in coordinates:
        cropped_image = cropYoloObject(image_path, coordinate, height_ratio, width_ratio)

        # Generate output filename
        output_filename = f"crop_{count}_{fname}.png"

        # Save the cropped image
        cropped_image.save(os.path.join(save_directory, output_filename))
        count += 1

def cropYoloObject(image_path, object_data, height_ratio, width_ratio):
    img = Image.open(image_path)
    center_x, center_y, object_width, object_height = [coordinate for coordinate in object_data[:2]] + [coordinate for coordinate in object_data[2:]]

    x1 = center_x * img.width - (object_width * img.width * width_ratio) / 2
    y1 = center_y * img.height - (object_height * img.height * height_ratio) / 2
    x2 = center_x * img.width + (object_width * img.width * width_ratio) / 2
    y2 = center_y * img.height + (object_height * img.height * height_ratio) / 2
    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(img.width, x2)
    y2 = min(img.height, y2)

    return img.crop((x1, y1, x2, y2))

def parseYoloCoordinates(labelPath, objectNum):
    coordinates = []
    with open(labelPath, 'r') as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split()
            if int(parts[0]) == objectNum:
                coordinates.append(list(map(float, parts[1:])))
    return coordinates

def classifyConfidence(labelPath, confidenceThreshold):
    with open(labelPath, 'r') as f:
        content = f.read().strip()
        logger.debug(content)
        
        lines = content.split("\n")
        for line in lines:
            values = [float(x) for x in line.split()]
            if len(values) < 6:
                logger.error("Invalid label file", labelPath)
                return "invalid"
            confidence = values[5]
            if confidence < confidenceThreshold:
                return "low"
    return "high"


def cropCradlesFromPinPlates(image_dir, save_dir):
    delete(join(image_dir, "detections"), force=True)
    detectImages(image_dir, .8, "best.pt")

    image_paths = getImagesFromDirectory(image_dir)
    for image_path in image_paths:
        label = convertNameToText(splitDirectoryFromFile(image_path)[1])

        label_path = join(image_dir, "detections", "predict", "labels", label)
        if os.path.exists(label_path):
            cropAroundObjects(save_dir, image_path, label_path, 0, 2, 6)

def MaxClassification(label_path):
    with open(label_path, 'r') as file:
        return max(float(line.split()[0]) for line in file if line.strip())