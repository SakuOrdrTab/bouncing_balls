# Ball object class defining python file
# Ver 0.01
# Ver 0.02 ball overlapping added
# Ver 0.03 wall collision added, docstrings


FRAME_MIN_X = 1
FRAME_MAX_X = 500
FRAME_MIN_Y = 1
FRAME_MAX_Y = 500

import random
import math

class Ball:
    """class of Ball, location of the ball, velocities, mass, radius
    """    
    # instance variables:
    # radius = 1
    # x = 0
    # y = 0
    # x_vel = 0.0
    # y_vel = 0.0
    # mass = 100
    
    def __init__(self):
        """create Ball Object, initialize random location and speed (0.0 .. 5.0)
        """    
        self.x = random.randint(FRAME_MIN_X, FRAME_MAX_X)
        self.y = random.randint(FRAME_MIN_Y, FRAME_MAX_Y)
        self.radius = random.randint(10,50)
        self.mass = int(self.radius*self.radius*3.14)
        self.x_vel = random.random() * 5
        self.y_vel = random.random() * 5
        return None

    def __str__(self) -> str:
        message = "Ball obj id <{}>\n".format(id(self))
        message += " center x:{0} y:{1}\n v_x:{2:.2f} v_y:{3:.2f}\n radius: {4}, mass: {5}\n".format(
            self.x, self.y, self.x_vel, self.y_vel, self.radius, self.mass)
        message += " Touches wall: "+str(self.touches_wall())
        return message

    # for class
    def ball_distance(ball_a, ball_b):
        """Distance between two balls

        Args:
            ball_a (Ball): first ball
            ball_b (Ball): second ball

        Returns:
            int: Distance between the radiuses of the two balls
        """        
        center_dist = math.sqrt((ball_a.x-ball_b.x)**2+(ball_a.y-ball_b.y)**2)
        return center_dist - ball_a.radius - ball_b.radius

    # for class
    def overlap(ball_a, ball_b):
        """Checks if two balls overlap

        Args:
            ball_a (Ball): first ball
            ball_b (Ball): second ball

        Returns:
            Boolean: Returns True if balls overlap
        """        
        return Ball.ball_distance(ball_a, ball_b) < 0

    # duplicate of distance function for speed
    def overlaps(self, ball):
        """Class method for ball to check if another ball overlaps, i.e. collides

        Args:
            ball (Ball): the Ball to check possible collision for

        Returns:
            Boolean: Returns True if the arg ball is overlapping i.e. colliding
        """        
        center_dist = math.sqrt((ball.x-self.x)**2+(ball.y-self.y)**2)
        return (center_dist - self.radius - ball.radius) <= 0
    
    # check if touches walls
    def touches_wall(self):
        """Checks if ball radius is over the frame, i.e. touches walls. Uses
        FRAME... constants for boundaries

        Returns:
            Boolean: returns True if ball is even partly outside frame constants
        """        
        if (self.x + self.radius >= FRAME_MAX_X) or (self.x - self.radius <= FRAME_MIN_X) \
            or (self.y + self.radius >= FRAME_MAX_Y) or (self.y - self.radius <= FRAME_MIN_Y):
                return True
        else:
            return False
    
    
    
    
    
random.seed()
print("Randomization complete.")