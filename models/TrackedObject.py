class TrackedObject:
    def __init__(self, obj_type, x1, y1, x2, y2, obj_id=None, cat=None, cat_prob=None, overlaps=False):
        self.type = obj_type
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.centroid = ((x1 + x2) // 2, (y1 + y2) // 2)  # Use integer division for consistency
        self.width=x2-x1
        self.height=y2-y1
        self.past_centroids=[]
        self.speeds=[]
        self.accelerations=[]
        self.id = obj_id  # Optional ID, can be assigned later
        self.cat=cat
        self.cat_prob=cat_prob
        self.overlaps=overlaps
        self.is_accident=False
        self.speed=None
        self.acceleration=None
        self.avr_acceleration=None
        self.is_present=True

    def compute_speed(self):
      if len(self.past_centroids) >= 5:
        x1, y1 = self.past_centroids[-5]
        x2, y2 = self.past_centroids[-1] #-1=last element
        self.speed = (((float(x2) - x1) ** float(2) + (float(y2) - y1) ** 2) ** 0.5)/4
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
        self.avr_acceleration=sum(self.accelerations) / len(self.accelerations)

    def check_accident(self):
      self.is_accident=False
      if self.overlaps:
        if self.acceleration is not None and self.avr_acceleration is not None:
            alpha=(self.acceleration-self.avr_acceleration)
            if alpha<-12:
              print(alpha)
              self.is_accident=True
              print(alpha)
              print("ACCIDENT!!!")
            else:
              self.is_accident=False