from .dec import *
from .file import *
from .media import *
from .system import *
from .yolo import *

# In your __init__.py file
import logging

# Create a logger with the name of the package
logger = logging.getLogger(__package__)

# Setup your logger (handlers, formatters, level, etc.)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


