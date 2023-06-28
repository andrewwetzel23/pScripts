import cv2
import torch.nn as nn
from system import getImagesFromDirectory, browse_for_dir

class DMB(nn.Module):
    # YOLOv5 MultiBackend class for python inference on various backends
    def __init__(self, weights):

        super().__init__()
        net = cv2.dnn.readNetFromONNX(weights)
        self.__dict__.update(locals())  # assign all variables to self



image_dir = browse_for_dir()
images = getImagesFromDirectory(image_dir)
model_add = "best.onnx"

# model = DMB(weights=model_add)
model = cv2.dnn.readNetFromONNX(model_add)
print(model)