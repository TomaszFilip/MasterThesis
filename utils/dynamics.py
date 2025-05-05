import math
from models.TrackedObject import TrackedObject
# Function to find the minimum distance between objects in a list
def find_min_distance(objects :list[TrackedObject]):
    min_distance = float("inf")
    closest_pair = None

    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            obj1, obj2 = objects[i], objects[j]
            dist = math.hypot(obj1.centroid[0] - obj2.centroid[0], obj1.centroid[1] - obj2.centroid[1])
            if dist < min_distance:
                min_distance = dist
                closest_pair = (obj1, obj2)

    return min_distance#, closest_pair
def euclidean_distance(pt1, pt2):
    return math.hypot(pt1[0] - pt2[0], pt1[1] - pt2[1])

def magnitude(vector):
    return math.sqrt(vector[0]**2 + vector[1]**2)

def compute_theta(vec1, vec2):
    dot_product = vec1[0] * vec2[0] + vec1[1] * vec2[1]
    magnitude_product = magnitude(vec1) * magnitude(vec2)
    res = math.acos(dot_product / magnitude_product)
    return res

class EuclideanDistTracker:
    def __init__(self):
        self.center_points = {}  # Stores object ID -> (centroid_x, centroid_y)
        self.id_count = 0  # Counter for assigning new IDs
        self.threshold_distance = 50  # Maximum allowed distance for tracking the same object
    def update(self, objects_rect):
        updated_objects = []
        min_distance=find_min_distance(objects_rect)

        for obj in objects_rect:
            cx, cy = obj.centroid
            assigned_id = None

            # Find the closest existing object
            for obj_id, (prev_cx, prev_cy) in self.center_points.items():
                dist = euclidean_distance((cx, cy), (prev_cx, prev_cy))

                if dist < min_distance and dist<self.threshold_distance:
                    assigned_id = obj_id
                    break  # Stop checking once we find a close enough match

            # Assign ID
            if assigned_id is not None:
                self.center_points[assigned_id] = (cx, cy)  # Update position
                obj.id = assigned_id
            else:
                # New object detected
                self.center_points[self.id_count] = (cx, cy)
                obj.id = self.id_count
                self.id_count += 1

            updated_objects.append(obj)

        # Remove old IDs that are no longer present
        self.center_points = {obj.id: obj.centroid for obj in updated_objects}

        return updated_objects

def check_overlap(a:TrackedObject,b:TrackedObject):
    x_intersect= 2*(abs(a.centroid[0]-b.centroid[0]))<(a.width+b.width)
    y_intersect= 2*(abs(a.centroid[1]-b.centroid[1]))<(a.height+b.height)
    return x_intersect and y_intersect
    #x_left = max(obj1.x1, obj2.x1)
    #y_top = max(obj1.y1, obj2.y1)
    #x_right = min(obj1.x2, obj2.x2)
    #y_bottom = min(obj1.y2, obj2.y2)
    #if x_right > x_left and y_bottom > y_top:
        #return True
    #else:
        #return False

def get_overlap_info(objects : list[TrackedObject]):
    overlap_info = {}
    for i, obj1 in enumerate(objects):
      obj1.overlaps=False
      obj1.overlaps_with=None
    for i, obj1 in enumerate(objects):
        for j, obj2 in enumerate(objects):
            if i != j and check_overlap(obj1, obj2) and obj1.is_present and obj2.is_present:
                obj1.overlaps=True
                obj1.overlaps_with=obj2