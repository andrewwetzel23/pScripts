import os

from .file import getImagesFromDirectory, createDirectory

from ultralytics import YOLO

def detectImages(dir, threshold, weights):
    detectionDirectory, _ = createDirectory(os.path.join(dir, "detections"), overwrite=True)
    model = YOLO(weights)
    model.predict(source=dir, conf=threshold, project=detectionDirectory, save_txt=True, device=0)

def getImagesWithObject(dir, objectID):
    images = getImagesFromDirectory(dir)
    for image in images:
        pass

def labelContainsObject(label, objectID):
    with open(label, 'r') as f:
        for line in f:
            if line.split(' ')[0] == objectID:
                return True