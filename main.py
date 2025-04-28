# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 22:09:31 2024

@author: tomfi
"""

from analysis import yolo
import cv2
import os

def predict_and_detect(chosen_model, img, classes=[], conf=0.5, rectangle_thickness=2, text_thickness=1):
    results = yolo.predict(chosen_model, img, classes, conf=conf)
    for result in results:
        for box in result.boxes:
            cv2.rectangle(img, (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                          (int(box.xyxy[0][2]), int(box.xyxy[0][3])), (255, 0, 0), rectangle_thickness)
            cv2.putText(img, f"{result.names[int(box.cls[0])]}",
                        (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                        cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), text_thickness)
    return img, results

image = cv2.imread("./sample_img/sample2.jpg")
model = yolo.config()
result_img, _ = predict_and_detect(model, image, classes=[], conf=0.5)
cv2.imshow("Image", result_img)
# cv2.imwrite("YourSavePath", result_img)
cv2.waitKey(0)

# Specify the folder containing the frames
frames_folder = './0'


# Helper function to extract numeric part from filename
def extract_number(filename):
    try:
        return int(os.path.splitext(filename)[0])  # Extract the number before '.jpg'
    except ValueError:
        return float('inf')  # If filename isn't a number, sort it last


# Get sorted list of image filenames
frame_filenames = sorted(
    [f for f in os.listdir(frames_folder) if f.endswith('.jpg')],
    key=extract_number
)

# Convert to full paths
frame_filenames = [os.path.join(frames_folder, f) for f in frame_filenames]

# Process each frame
# for frame_filename in frame_filenames:
# Read the image
# frame = cv2.imread(frame_filename)
# if frame is None:
# print(f"Error loading {frame_filename}")
#     continue

# result_img, _ = predict_and_detect(model, frame, classes=[], conf=0.5)
# Process the frame (e.g., display it, perform operations, etc.)
# cv2.imshow('Frame', frame)

# Simulate video playback by waiting (30ms here for ~30 FPS)
# if cv2.waitKey(30) & 0xFF == ord('q'):
#  break

# Cleanup
cv2.destroyAllWindows()

# Initialize VideoWriter
shape = cv2.imread(frame_filenames[0]).shape[:2]  # Replace with actual dimensions
frame_size = (480, 360)
fps = 10  # Desired frames per second

# Initialize VideoWriter with AVI codec
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for AVI
out = cv2.VideoWriter("output_file.avi", fourcc, fps, frame_size)

for frame_filename in frame_filenames:
    frame = cv2.imread(frame_filename)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

    if frame is None:
        continue

    result_frame, _ = predict_and_detect(model, frame, classes=[], conf=0.5)
    cv2.imshow('Frame', result_frame)
    print(frame_filename)
    out.write(frame)

out.release()
