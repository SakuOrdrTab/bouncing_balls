# Ball object class defining python file
# Ver 0.01
# Ver 0.02 ball overlapping added

FRAME_MIN_X = 1
FRAME_MAX_X = 500
FRAME_MIN_Y = 1
FRAME_MAX_Y = 500

import random
import math

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

    # for class
    def ball_distance(ball_a, ball_b):
        center_dist = math.sqrt((ball_a.x-ball_b.x)**2+(ball_a.y-ball_b.y)**2)
        return center_dist-ball_a.radius-ball_b.radius

    # for class
    def overlap(ball_a, ball_b):
        return Ball.ball_distance(ball_a, ball_b) < 0

    # duplicate of distance function for speed
    def overlaps(self, ball):
        center_dist = math.sqrt((ball.x-self.x)**2+(ball.y-self.y)**2)
        return (center_dist - self.radius - ball.radius) <= 0
    
    
    
    
    
random.seed()
print("Randomization complete.")