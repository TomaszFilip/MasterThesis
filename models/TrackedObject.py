import math
class TrackedObject:
    def __init__(self, obj_type, x1, y1, x2, y2, obj_id=None, cat=None, cat_prob=None, overlaps=False):
        self.type = obj_type
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.H=0
        self.vector=None
        self.centroid = ((x1 + x2) // 2, (y1 + y2) // 2)  # Use integer division for consistency
        self.width=x2-x1
        self.height=y2-y1
        self.past_centroids=[]
        self.speeds=[]
        self.accelerations=[]
        self.norm_vectors = []
        self.magnitudes=[]
        self.id = obj_id  # Optional ID, can be assigned later
        self.cat=cat
        self.cat_prob=cat_prob
        self.overlaps=overlaps
        self.overlaps_with=None
        self.is_accident=False
        self.speed=None
        self.magnitude=None
        self.norm_vector=None
        self.acceleration=None
        self.avr_acceleration=None
        self.is_present=True

    def compute_speed(self):
      if len(self.past_centroids) >= 5:
        x1, y1 = self.past_centroids[-5]
        x2, y2 = self.past_centroids[-1] #-1=last element
        s=(((float(x2) - x1) ** float(2) + (float(y2) - y1) ** 2) ** 0.5)/4
        self.speed = s*(((self.H-self.height)/self.H)+1)
        self.speeds.append(self.speed)
      #else:
        #x1, y1 = self.past_centroids[-(len(self.past_centroids))]
        #x2, y2 = self.past_centroids[-1] #-1=last element
        #self.speed = (((float(x2) - float(x1)) ** 2 + (float(y2) - float(y1)) ** 2) ** 0.5)/(len(self.past_centroids))
        #self.speeds.append(self.speed)

    def compute_acceleration(self):
      if(len(self.speeds)>=5):
        self.acceleration=float(self.speeds[-1])-float(self.speeds[-5])
        self.accelerations.append(self.acceleration)

        self.avr_acceleration=sum(self.accelerations[-15:]) / min(len(self.accelerations),15)

    def compute_magnitude(self):
        x1sq=self.vector[0]*self.vector[0]
        x2sq=self.vector[1]*self.vector[1]
        self.magnitude=math.sqrt(x1sq+x2sq)
        if self.magnitude!=0:
            self.magnitudes.append(self.magnitude)

    def trajectory_anomaly(self):
        if self.vector is not None and self.overlaps_with.vector is not None:
            dot_product=self.vector[0]*self.overlaps_with.vector[0]+self.vector[1]*self.overlaps_with.vector[1]
            try:
                magnitude_product=self.magnitude*self.overlaps_with.magnitude
                res= math.acos(dot_product/magnitude_product)
            except:
                return 0
            return res
        return 0

    def angle_anomaly(self):
        if (len(self.norm_vectors) >= 5):
            dot_product = self.norm_vectors[-1][0] * self.norm_vectors[-5][0] + self.norm_vectors[-1][1] * self.norm_vectors[-5][1]

            x1sq = self.norm_vectors[-1][0]*self.norm_vectors[-1][0]
            x2sq = self.norm_vectors[-1][1]*self.norm_vectors[-1][1]
            magnitude1=math.sqrt(x1sq+x2sq)

            x3sq = self.norm_vectors[-5][0] *self.norm_vectors[-5][0]
            x4sq = self.norm_vectors[-5][1] *self.norm_vectors[-5][1]
            magnitude2 = math.sqrt(x3sq + x4sq)

            magnitude_product = magnitude1 * magnitude2
            if (magnitude_product!=0):
                try:
                    res = math.acos(dot_product / magnitude_product)
                    return res
                except:
                    return 0
        return 0

    def acceleration_anomaly(self):
        if self.acceleration is not None and self.avr_acceleration is not None:
            if self.acceleration !=0:
                alpha=(self.acceleration-self.avr_acceleration)
                return alpha
        return 0

    def compute_vector(self):
        if len(self.past_centroids) >= 5:
            x1, y1 = self.past_centroids[-5]
            x2, y2 = self.past_centroids[-1]
            self.vector = x2-x1, y2-y1
            self.compute_magnitude()
            if self.magnitude>0:
                self.norm_vector=self.vector[0]/self.magnitude, self.vector[1]/self.magnitude
                self.norm_vectors.append(self.norm_vector)
        else:
            return 0,0

    def check_accident(self,a=0,b=0,g=0):
      self.is_accident=False
      if self.overlaps and self.overlaps_with is not None:
            alpha=self.acceleration_anomaly()
            beta=self.trajectory_anomaly()
            gamma=self.angle_anomaly()
            if (a*alpha)+(b*beta)+(g*gamma)>10:
              self.is_accident=True
            else:
              self.is_accident=False