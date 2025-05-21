from models.TrackedObject import TrackedObject
from utils.dynamics import  get_overlap_info
from ultralytics import YOLO, checks, hub
def config():
    from ultralytics import YOLO

    model = YOLO("yolo11m.pt")

    checks()  # Verify system setup for Ultralytics training# -*- coding: utf-8 -*-
    return model

def predict(chosen_model, img, classes=[], conf=0.5):
    if classes:
        results = chosen_model.predict(img, classes=classes, conf=conf)
    else:
        results = chosen_model.predict(img, conf=conf)

    return results

def process_frame(chosen_model, img, device, transform, coco_labels, tracker, conf=0.75):
    classes=[]
    results = predict(chosen_model, img, classes, conf=conf)
    objects=[]
    for result in results:
        for box in result.boxes:
            label = result.names[int(box.cls[0])]
            score = round(float(box.conf),2)
            x1, y1, x2, y2 =int(box.xyxy[0][0]), int(box.xyxy[0][1]),int(box.xyxy[0][2]), int(box.xyxy[0][3])
            id=-1
            obj=TrackedObject(label,x1, y1, x2, y2,id,label,score)
            if obj.cat in ['truck', 'motorcycle', 'car', 'bicycle']:
                objects.append(obj)
    return objects
