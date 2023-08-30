import logging

logger = logging.getLogger('mf')

def configure_logging(level=logging.DEBUG):
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(level)


IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.JPG', '.PNG', '.JPEG']
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov']