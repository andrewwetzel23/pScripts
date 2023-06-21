from yolov5 import detect

img = R"C:\Users\andrew\OneDrive - Lion Power, LLC\Pictures\HR UKG People Strategy.jpg.jpg"
model = R"C:\Users\andrew\Desktop\ynto\data\PDP\weights\weights10\weights\best.pt"

detect.run(weights=model,
           source=img,
           imgsz=[1600, 900],
           conf_thres=.4,
           view_img=True,
           nosave=True,
           device='cpu'
           )