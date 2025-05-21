import cv2
def visualize(img,boxes):
    rectangle_thickness = 2
    text_thickness = 1
    for box in boxes:
        cv2.putText(img, str(box.id), (box.x1, box.y1 - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.rectangle(img, (box.x1, box.y1), (box.x2, box.y2), (255, 255, 255), 2)
        # Draw bounding box
        box.past_centroids.append(box.centroid)
        if not box.overlaps:
            cv2.rectangle(img, (box.x1, box.y1), (box.x2, box.y2), (255, 0, 0), rectangle_thickness)
        else:
            cv2.rectangle(img, (box.x1, box.y1), (box.x2, box.y2), (0, 0, 255), rectangle_thickness)
        # Add class label
        cv2.putText(img, f"{box.cat} ({box.cat_prob})",
                    (box.x1, box.y1 - 10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), text_thickness)
        box.past_centroids.append(box.centroid)  # store the current centroid.
        for past_centroid in box.past_centroids:
            cv2.circle(img, past_centroid, 3, (0, 255, 0), -1)
    return img
