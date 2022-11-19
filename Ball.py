# Ball object class defining python file
# Ver 0.01

FRAME_MIN_X = 1
FRAME_MAX_X = 500
FRAME_MIN_Y = 1
FRAME_MAX_Y = 500

import random

class Ball:
    
    # instance variables:
    # radius = 1
    # x = 0
    # y = 0
    # x_vel = 0.0
    # y_vel = 0.0
    # mass = 100
    
    def __init__(self):
        self.x = random.randint(FRAME_MIN_X, FRAME_MAX_X)
        self.y = random.randint(FRAME_MIN_Y, FRAME_MAX_Y)
        self.radius = random.randint(10,50)
        self.mass = int(self.radius*self.radius*3.14)
        self.x_vel = random.random() * 5
        self.y_vel = random.random() * 5
        return None
    
    
    
    
    
random.seed()
print("Randomization complete.")