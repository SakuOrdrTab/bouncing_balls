# Ball object class defining python file
# Ver 0.01
# Ver 0.02 ball overlapping added
# Ver 0.03 wall collision added, docstrings
# Ver 0.04 added rudimentary bounces
# Ver 0.05 rudimentary ball drawing with Pyside6
# Ver 0.1 Rudimentary ball physics complete, ball draw, refractoring
# Ver 0.2 Ball_frame added

import random
import math
from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtGui import QBrush, QColor

class Ball:
    """class of Ball, location of the ball, velocities, mass, radius
    """    
    # instance variables:
    # x int
    # y int
    # x_vel (float)
    # y_vel (float)
    # mass (int)
    # radius (int)
    # colour (QColor)
    
    def __init__(self, frame):
        """create Ball Object, initialize random location and speed (0.0 .. 5.0)
        """    
        self.x = random.randint(frame.min_x, frame.max_x)
        self.y = random.randint(frame.min_y, frame.max_y)
        self.radius = random.randint(10, 300)
        self.mass = int(self.radius*self.radius * 3.14)
        self.x_vel = random.random() * 5
        self.y_vel = random.random() * 5
        self.colour = QColor(random.randint(10, 255), random.randint(10, 255),
                             random.randint(10, 255), 255) # totally black not allowed

        ball_render = QGraphicsEllipseItem(0, 0, self.radius * 2, self.radius * 2)
        ball_render.setPos(self.x - self.radius, self.y - self.radius)
 
        brush = QBrush(self.colour)
        ball_render.setBrush(brush)
        self.ball_ellipse = ball_render
        return None

    # simple dist between two coordinates
    def _dist(x1, y1, x2, y2) : return math.sqrt((x1-x2)**2 + (y1-y2**2))
    

    def __str__(self) -> str:
        message = "Ball obj id <{}>\n".format(id(self))
        message += " center x:{0} y:{1}\n v_x:{2:.2f} v_y:{3:.2f}\n radius: {4}, mass: {5}\n".format(
            self.x, self.y, self.x_vel, self.y_vel, self.radius, self.mass)
        message += " Touches wall: "+str(self.touches_wall())
        return message

    def move(self):
        self.x += int(self.x_vel)
        self.y += int(self.y_vel)
        return None

    # for class
    def ball_distance(ball_a, ball_b):
        """Distance between two balls

        Args:
            ball_a (Ball): first ball
            ball_b (Ball): second ball

        Returns:
            float: Distance between the radiuses of the two balls
        """        
        return math.sqrt((ball_a.x - ball_b.x) **2 + (ball_a.y - ball_b.y) **2) - ball_a.radius - ball_b.radius

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
        return (math.sqrt((ball.x - self.x) **2 + (ball.y - self.y) **2) - self.radius - ball.radius) <= 0
    
    # check if touches walls
    def touches_wall(self, frame):
        """Checks if ball radius is over the frame, i.e. touches walls. Uses
        FRAME... constants for boundaries

        Returns:
            Boolean: returns True if ball is even partly outside frame constants
        """        
        if (self.x + self.radius >= frame.max_x) or (self.x - self.radius <= frame.min_x) \
            or (self.y + self.radius >= frame.max_y) or (self.y - self.radius <= frame.min_y):
                return True
        else:
            return False
        

    def bounce_w_wall(self, frame): # rudimentary non-physical wall collision
        # reverse speed
        if self.x <= frame.min_x or self.x >= frame.max_x:
            self.x_vel = -1 * self.x_vel
        if self.y <= frame.min_y or self.y >= frame.max_y:
            self.y_vel = -1 * self.y_vel
        # implement movement of ball away from wall
        # here:
        self.move() # experimental
        return None

    def bounce_w_ball(self, ball2): # rudimentary non-physical collision with balls, just reverse speeds
        # reverse speeds
        self.x_vel = -1 * self.x_vel
        ball2.x_vel = -1 * ball2.x_vel
        self.y_vel = -1 * self.y_vel
        ball2.y_vel = -1 * ball2.y_vel
        # implement movement of both balls from eachother
        # here:
        self.move() # experimental
        ball2.move()
        return None
    
#    def ball_sphere(self, *args, **kwargs):
#        # returns QtEllipse
#        ball_render = QGraphicsEllipseItem(0, 0, self.radius * 2, self.radius * 2)
#        ball_render.setPos(self.x - self.radius, self.y - self.radius)
# 
#        brush = QBrush(self.colour)
#        ball_render.setBrush(brush)
#        self.ball_ellipse = ball_render
#        return None
    

    
random.seed()
print("Randomization complete. (TLE: is random.seet() necessary here? It runs on every import, but maybe rand needs to be initialized?)")