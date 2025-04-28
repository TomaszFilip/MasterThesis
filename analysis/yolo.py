from models.TrackedObject import TrackedObject
from utils.dynamics import EuclideanDistTracker, get_overlap_info
from ultralytics import YOLO, checks, hub
import cv2
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

def process_frame(chosen_model, img, device, transform, coco_labels, tracker, conf=0.75, rectangle_thickness=2, text_thickness=1):
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

            if obj.cat in ['truck', 'motorcycle', 'car']:
              objects.append(obj)
    boxes = tracker.update(objects)
    get_overlap_info(boxes)
    for box in boxes:
        cv2.putText(img, str(box.id),(box.x1,box.y1-15),  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
        cv2.rectangle(img, (box.x1,box.y1),(box.x2, box.y2), (255,255,255), 2)
        # Draw bounding box
        box.past_centroids.append(box.centroid)
        if not box.overlaps:
          cv2.rectangle(img, (box.x1, box.y1), (box.x2, box.y2), (255, 0, 0), rectangle_thickness)
        else:
          cv2.rectangle(img, (box.x1, box.y1), (box.x2, box.y2), (0, 0, 255), rectangle_thickness)
        # Add class label
        cv2.putText(img, f"{box.cat} ({box.cat_prob})",
                    (box.x1, box.y1 - 10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), text_thickness)
        box.past_centroids.append(box.centroid) #store the current centroid.
        for past_centroid in box.past_centroids:
          cv2.circle(img, past_centroid, 3, (0, 255, 0), -1)

    return img,boxes