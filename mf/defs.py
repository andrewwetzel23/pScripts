import logging

logger = logging.getLogger('mf')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.JPG', '.PNG', '.JPEG']
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov']