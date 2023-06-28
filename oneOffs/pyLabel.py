import cv2
import numpy as np
from system import browse_for_dir
import os

"""
Orginal attempt at replacing yololabel with a python based gui labeler

Good idea but needs to be cleaned up.
"""

def redraw_boxes(event, x, y, flags, params):
    global boxes, redraw, current_box, current_class_id
    if event == cv2.EVENT_LBUTTONDOWN:
        current_box = [x, y, x, y]
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        current_box[2] = x
        current_box[3] = y
    elif event == cv2.EVENT_LBUTTONUP:
        current_box[2] = x
        current_box[3] = y
        boxes.append(current_box + [current_class_id])
        redraw = True

def label_objects(image_path, detection_path):
    global boxes, redraw, current_box, current_class_id
    # Load the input image
    image = cv2.imread(image_path)

    # Load the YOLOv5 detections
    detections = np.loadtxt(detection_path, dtype='float32', delimiter=',')

    # Parse the detections and draw bounding boxes on the image
    conf_threshold = 0.5
    class_names = ['class1', 'class2', 'class3']  # replace with your own class names
    boxes = []
    for detection in detections:
        class_id = int(detection[0])
        confidence = detection[1]
        if confidence > conf_threshold:
            x_center = int(detection[2] * image.shape[1])
            y_center = int(detection[3] * image.shape[0])
            width = int(detection[4] * image.shape[1])
            height = int(detection[5] * image.shape[0])
            left = int(x_center - width / 2)
            top = int(y_center - height / 2)
            right = left + width
            bottom = top + height
            boxes.append([left, top, right, bottom, class_id])
    current_box = []
    current_class_id = 0
    redraw = True
    while redraw:
        redraw = False
        cv2.namedWindow('Object detection')
        cv2.setMouseCallback('Object detection', redraw_boxes)
        for box in boxes:
            left, top, right, bottom, class_id = box
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(image, class_names[class_id], (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        if len(current_box) == 4:
            cv2.rectangle(image, (current_box[0], current_box[1]), (current_box[2], current_box[3]), (0, 0, 255), 2)
            cv2.putText(image, class_names[current_class_id], (current_box[0], current_box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.imshow('Object detection', image)
        key = cv2.waitKey(1)
        if key == ord('q'):
            return
        elif key == ord('c'):
            current_box = []
            redraw = True
        elif key == ord('1'):
            current_class_id = 0
        elif key == ord('2'):
            current_class_id = 1
        elif key == ord('3'):
            current_class_id = 2
        elif key == ord('4'):
            current_class_id = 3
        elif key == ord('5'):
            current_class_id = 4
        elif key == ord('6'):
            current_class_id = 5
        elif key == ord('7'):
            current_class_id = 6
        elif key == ord('8'):
            current_class_id = 7
        elif key == ord('9'):
            current_class_id = 8
    cv2.destroyAllWindows()

dir = browse_for_dir()
detectionDir = browse_for_dir()

label_objects(dir, detectionDir)
