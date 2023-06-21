from yolov5 import export
from funcs import browse_for_file

export.run(imgsz=[576, 352], weights=browse_for_file())