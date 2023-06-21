from yolov5 import detect
# print(detect.run(imgsz=[576, 352] , weights=R"C:\Users\andrew\Desktop\ynto\data\person\weights\weights5\weights\best.pt")


print(detect.run(source=R"C:\Users\andrew\OneDrive - Lion Power, LLC\Pictures\PeopleDataSmall\image_213.jpg", weights=R"C:\Users\andrew\Desktop\ynto\data\person\weights\weights5\weights\best.pt", conf_thres=0.25, imgsz=640))

print('end')
