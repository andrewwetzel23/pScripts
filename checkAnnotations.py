from funcs import browse_for_dir, browse_for_file, get_images_from_dir, asd, convert_name_to_text
from pyFuncs import safeRemove
import os
import cv2
import shutil
from ultralytics import YOLO
from tqdm import tqdm
import numpy as np

"""
Intended to parse through yolov5/yolov8 annotations and compare used annotations to 
one created by a given model.

Needs to be cleaned up and tested

"""

color = [[144, 238, 144], [52,71,21], [232,219,164], [126,37,3]]

def consolidate(idir, sdir):
	tDir = os.path.join(idir, "train")
	vDir = os.path.join(idir, "valid")

	tImages = get_images_from_dir(os.path.join(tDir, "images"))
	vImages = get_images_from_dir(os.path.join(vDir, "images"))

	for image in tqdm(tImages, "Consolidating from Train..."):
		label = convert_name_to_text(image)
		if "dark" not in image and "lite" not in image:
				shutil.copy(os.path.join(tDir, "images", image), os.path.join(sdir, "images", image))
				shutil.copy(os.path.join(tDir, "labels", label), os.path.join(sdir, "labels", label))

	for image in tqdm(vImages, "Consolidating from Valid..."):
		label = convert_name_to_text(image)
		if "dark" not in image and "lite" not in image:
				shutil.copy(os.path.join(vDir, "images", image), os.path.join(sdir, "images", image))
				shutil.copy(os.path.join(vDir, "labels", label), os.path.join(sdir, "labels", label))

def generate_yolo_labels(iDir, sDir, weight):
	model = YOLO(weight)
	model.predict(source=iDir,
			   conf=.4,
			   project=sDir,
			   save_txt=True,
			   nosave=True,
			   device=0)

def create_windows():
	test_img = np.zeros(shape=(352,576,3)).astype('uint8')
	cv2.imshow('Annotated',test_img)
	cv2.imshow('Detected', test_img) 
	cv2.moveWindow('Annotated',100, 100)
	cv2.moveWindow('Detected', 800, 100)
	cv2.waitKey(1)

def draw_boxes(img, label):
	with open(label) as f:
		lines = f.readlines()
		for line in lines:
			a, x, y, w, h = [float(x) for x in line.split()]
			r, c, b = img.shape
			x1, y1, x2,y2 = yolo_to_bb(w, h, x, y, c, r)
			draw_rectangle(img, x1, y1, x2, y2, color[int(a)])
	return img

def draw_rectangle(img, x1, y1, x2, y2, color):
	return cv2.resize(cv2.rectangle(img, [x1, y1], [x2, y2], color, 2), [576, 352])

def yolo_to_bb(w, h, x, y, c, r):
	x1 = int(x*c - w*c/2)
	x2 = int(x*c + w*c/2)
	y1 = int(y*r - h*r/2)
	y2 = int(y*r + h*r/2)
	return x1, y1, x2, y2

def store_current(image, img, idir,ldir, sdir):
	cv2.imwrite(os.path.join(sdir, image), img)
	label = convert_name_to_text(image)
	shutil.copy(os.path.join(ldir, label), os.path.join(sdir, label))

def redo():
	# print('new')
	pass

def contains(label, num):
	try:
		with open(label, 'r') as f:
			lines = f.readlines()
			for line in lines:
				if line[0] == str(num):
					return True
		return False
	except:
		return False

def check_dir(dir, weight):
	idir = os.path.join(dir, "images")
	ldir = os.path.join(dir, "labels")
	sdir = os.path.join(dir, "good")
	ydir = os.path.join(dir, "ydir")
	rdir = os.path.join(dir, "relabel")

	images = get_images_from_dir(idir)

	# generate_yolo_labels(idir, ydir, weight)
	create_windows()
	# TODO - add key to delete images
	for image in tqdm(images):
		label = convert_name_to_text(image)
		current_annotation = os.path.join(ldir, label)
		yolo_label = os.path.join(ydir, "exp", "labels", label)
		img = cv2.imread(os.path.join(idir, image))
		aframe = img.copy()
		dframe = img.copy()
		if contains(current_annotation, 2) or contains(label, 2):
			cv2.imshow('Annotated', draw_boxes(aframe, current_annotation))
			try:
				cv2.imshow('Detected', draw_boxes(dframe, yolo_label))
			except:
				pass
			key = cv2.waitKey(0)
			if key == 97:  # current annotation - a
				cv2.imwrite(os.path.join(sdir, image), img)
				shutil.copy(os.path.join(ldir, label), os.path.join(sdir, label))
			elif key == 100:  # model annotated image - d
				cv2.imwrite(os.path.join(sdir, image), img)
				try:
					shutil.copy(yolo_label, os.path.join(sdir, label))
				except:
					pass
			elif key == 115:  # delete - s
				pass
			elif key == 113:   # quit - q
				print("Exiting...")
				break
			else:  # reannotated manually later
				cv2.imwrite(os.path.join(rdir, image), img)
			# safeRemove(os.path.join(idir, image))

def setup_dir_for_checks(dir):
	if os.path.isdir(dir):
		shutil.rmtree(dir)
	else:
		print(f'{dir} does not exist.')

	os.mkdir(dir)

def setup_dirs(dir):
	safeRemove(os.path.join(dir, "good"))
	safeRemove(os.path.join(dir, "images"))
	safeRemove(os.path.join(dir, "labels"))
	safeRemove(os.path.join(dir, "relabel"))
	safeRemove(os.path.join(dir, "ydir"))



	setup_dir_for_checks(os.path.join(dir, "good"))
	setup_dir_for_checks(os.path.join(dir, "images"))
	setup_dir_for_checks(os.path.join(dir, "labels"))
	setup_dir_for_checks(os.path.join(dir, "relabel"))
	setup_dir_for_checks(os.path.join(dir, "ydir"))


Dir = browse_for_dir()
sDir = browse_for_dir()
weight = browse_for_file()
# weight = R"C:\Users\andrew\Desktop\ynto\data\PDP\weights\weights13\weights\best.pt"


setup_dirs(sDir)
consolidate(Dir, sDir)
check_dir(sDir, weight)
