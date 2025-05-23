import torch
import torchvision.transforms as T
from torchvision.models.detection import MaskRCNN_ResNet50_FPN_Weights, maskrcnn_resnet50_fpn
from utils.dynamics import EuclideanDistTracker, get_overlap_info
import cv2
from models.TrackedObject import TrackedObject

def config():
    # Define image transformation for the model input


    COCO_INSTANCE_CATEGORY_NAMES = [
        '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
        'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
        'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
        'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
        'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
        'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
        'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
        'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
        'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
        'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
        'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A',
        'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
    ]
    # Check if GPU is available (T4 recommended)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    transform = T.Compose([T.ToTensor()])

    # Enable performance optimization
    torch.backends.cudnn.benchmark = True

    # Load the Mask R-CNN model with pre-trained COCO weights
    model = maskrcnn_resnet50_fpn(weights=MaskRCNN_ResNet50_FPN_Weights.COCO_V1).to(device)
    model.eval()
    return transform, COCO_INSTANCE_CATEGORY_NAMES, model, device

def predict(chosen_model, img, device, transform, conf=0.5):
     # Convert image to tensor and normalize
    img_tensor = transform(img).unsqueeze(0).to(device)  # Add batch dimension

    with torch.no_grad():
        results = chosen_model(img_tensor)  # Get predictions

    return results[0]  # Mask R-CNN returns a list, we take the first result

def process_frame(chosen_model, img, device, transform, coco_labels, tracker, conf=0.75, rectangle_thickness=2, text_thickness=1):
    results = predict(chosen_model, img, device, transform, conf)
    objects=[]
    for i in range(len(results["boxes"])):
        score = results["scores"][i].item()
        if score < conf:
            continue  # Skip low-confidence detections

        label_index = results["labels"][i].item()  # Class label
        label = coco_labels[label_index] # get label name
        # Extract bounding box coordinates
        x1, y1, x2, y2 = map(int, results["boxes"][i])
        id=-1
        obj=TrackedObject(label,x1, y1, x2, y2,id,label,score)
        if obj.cat in ['truck', 'motorcycle', 'car', 'bicycle']:
          objects.append(obj)
    return objects


