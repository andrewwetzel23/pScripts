import cv2, os, shutil
from tqdm import tqdm
import numpy as np
from  system import browse_for_dir, getImagesFromDirectory


"""
Sort's through images and finds ones that are appropraite for a test set for a yolov8 model

Needs to be checked and cleaned up

"""

def create_window():
	test_img = np.zeros(shape=(352,576,3)).astype('uint8')
	cv2.imshow('testImage',test_img)
	cv2.moveWindow('testImage',100, 100)
	cv2.waitKey(1)

dir = browse_for_dir()
images = getImagesFromDirectory(dir)

create_window()
for image in tqdm(images):
	img = cv2.imread(os.path.join(dir, image))
	cv2.imshow("testImage", cv2.resize(img, [1152, 704]))
	key = cv2.waitKey(0)
	if key == 97:  # store
		shutil.move(os.path.join(dir, image), os.path.join(dir, "testSet", image))
	elif key == 100:  # delete
		os.remove(os.path.join(dir, image))
	elif key == 113:   # quit
		print("Exiting...")
		exit(0)
	else:  # skip
		print("Not valid. Leaving image in main folder.")

