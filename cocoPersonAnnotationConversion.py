import cv2
from tqdm import tqdm

from funcs import browse_for_file

""" 
Converts large csv file of annotations data from a _____ repository to yolov5/yolov8 copliant annotaitons

Need to find the relevant repository to add to this description.

"""

with open(r"C:\Users\andrew\Desktop\coco_person_dataset\annotations_download_person.csv", 'r') as f:
	lines = f.readlines()

	for line in tqdm(lines):
		nameAnnotation = line.split('/')[-1]
		image = nameAnnotation.split(',')[0]

		pic = cv2.imread(r"C:/Users/andrew/Desktop/coco_person_dataset/coco_downloaded_images/" + image)

		ih, iw, ic = pic.shape 
		x1 = int(nameAnnotation.split(',')[1])
		y1 = int(nameAnnotation.split(',')[2])
		x2 = int(nameAnnotation.split(',')[3])
		y2 = int(nameAnnotation.split(',')[4])

		xc = ((x1+x2)/2) / iw
		yc = ((y1+y2)/2) / ih
		w = (x2 - x1) / iw
		h = (y2 - y1) / ih

		text = r"C:/Users/andrew/Desktop/coco_person_dataset/coco_downloaded_images/" + image.split('.')[0] + '.txt'

		# print(text)

		# print(image)
		# print(text)
		with open(text, 'a') as t:
			t.write(f'0 {xc} {yc} {w} {h}\n')
		# print(0, xc, yc, w, h)




		# print(x1, y1, x2, y2)
