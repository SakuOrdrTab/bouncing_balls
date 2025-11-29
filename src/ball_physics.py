"""Ball class for physics etc"""

from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtGui import QColor, QBrush

import math
import random

from src.constants import MAX_SPEED


class Ball:
    """
    class of Ball, location of the ball, velocities, mass, radius, holds also QEllipseItem to draw the ball
    """

    def __init__(self, min_radius: int, max_radius: int, frame: "Ball_frame") -> None:
        """Constructor for Ball, sets random speed, colour and position.

        Args:
            frame (Ball_frame): frame for balls and physics

        """
        self.x = random.randint(frame.min_x, frame.max_x)
        self.y = random.randint(frame.min_y, frame.max_y)
        self.radius = random.randint(min_radius, max_radius)
        self._mass = int(self.radius * self.radius * 3.14)
        self.x_vel = random.random() * MAX_SPEED * 2 - 0.5 * MAX_SPEED
        self.y_vel = random.random() * MAX_SPEED * 2 - 0.5 * MAX_SPEED
        self.colour = QColor(
            random.randint(10, 255),
            random.randint(10, 255),
            random.randint(10, 255),
            255,
        )  # totally black not allowed

        ball_render = QGraphicsEllipseItem(0, 0, self.radius * 2, self.radius * 2)
        ball_render.setPos(self.x - self.radius, self.y - self.radius)

        brush = QBrush(self.colour)
        ball_render.setBrush(brush)
        self.ball_ellipse = ball_render
        self.frame = frame

    @property
    def mass(self):
        return self._mass

    def _dist(self, x1: int, y1: int, x2: int, y2: int) -> float:
        # simple geometric distance between two coordinates
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def __str__(self) -> str:
        # string representation if needed
        message = "Ball obj id <{}>\n".format(id(self))
        message += " center x:{0} y:{1}\n v_x:{2:.2f} v_y:{3:.2f}\n radius: {4}, mass: {5}\n".format(
            self.x, self.y, self.x_vel, self.y_vel, self.radius, self.mass
        )
        message += " Touches wall: " + str(self.touches_wall())
        return message

    def move(self):
        """moves ball according to its speed, does not refresh QEllipseItem position

        Returns:
            None
        """
        self.x += self.x_vel
        self.y += self.y_vel
        return None

    # for class
    @staticmethod
    def ball_distance(ball_a: "Ball", ball_b: "Ball") -> float:
        """Distance between two balls

        Args:
            ball_a (Ball): first ball
            ball_b (Ball): second ball

        Returns:
            float: Distance between the radiuses of the two balls
        """
        return (
            math.sqrt((ball_a.x - ball_b.x) ** 2 + (ball_a.y - ball_b.y) ** 2)
            - ball_a.radius
            - ball_b.radius
        )

    def overlaps(self, ball: "Ball") -> bool:
        """Class method for ball to check if another ball overlaps, i.e. collides

        Args:
            ball (Ball): the Ball to check possible collision for

        Returns:
            Boolean: Returns True if the arg ball is overlapping i.e. colliding
        """
        return (
            math.sqrt((ball.x - self.x) ** 2 + (ball.y - self.y) ** 2)
            - self.radius
            - ball.radius
        ) <= 0

    def touches_wall(self) -> bool:
        """Checks if ball radius is over the frame, i.e. touches walls. Uses
        FRAME... constants for boundaries

        Returns:
            Boolean: returns True if ball is even partly outside frame constants
        """
        if (
            (self.x + self.radius >= self.frame.max_x)
            or (self.x - self.radius <= self.frame.min_x)
            or (self.y + self.radius >= self.frame.max_y)
            or (self.y - self.radius <= self.frame.min_y)
        ):
            return True
        else:
            return False

    def bounce_w_wall(self) -> None:
        """Bounces ball with frame, i.e. reverses according speed.
        Rudimentary yet, nonphysical

        Args:
            frame (Ball_frame): the frame for physics

        Returns:
            None
        """
        # reverse speed
        if self.x <= self.frame.min_x or self.x >= self.frame.max_x:
            self.x_vel = -1 * self.x_vel
        if self.y <= self.frame.min_y or self.y >= self.frame.max_y:
            self.y_vel = -1 * self.y_vel
        # Move away
        self.move()
        return None

    def bounce_w_ball(self, ball2: "Ball") -> None:
        """Bounces two balls.
        Simplistic physical, 1-dim collisions calculated
        separately for x and y

        Args:
            ball2 (Ball): second ball, first is self

        Returns:
            None
        """
        # Okay, this is still a simplistication. It is considered that
        # momentum is preserved in both x and y dimensions, so they are
        # calculated separately. Temporary variables needed, *_temp
        x_vel_self_temp = (
            (self.mass - ball2.mass) * self.x_vel + 2 * ball2.mass * ball2.x_vel
        ) / (self.mass + ball2.mass)
        x_vel_ball2_temp = self.x_vel + x_vel_self_temp - ball2.x_vel
        y_vel_self_temp = (
            (self.mass - ball2.mass) * self.y_vel + 2 * ball2.mass * ball2.y_vel
        ) / (self.mass + ball2.mass)
        y_vel_ball2_temp = self.y_vel + y_vel_self_temp - ball2.y_vel
        self.x_vel = x_vel_self_temp  # now implement speeds according to above
        self.y_vel = y_vel_self_temp
        ball2.x_vel = x_vel_ball2_temp
        ball2.y_vel = y_vel_ball2_temp

        # implement movement of both balls from eachother here:
        self.move()
        ball2.move()
        return None


class Ball_frame:
    """
    Class to hold the wanted dimensions of frame to hold the balls and physics
    """

    def __init__(self, min__x: int, min__y: int, max__x: int, max__y: int) -> None:
        """constructor for Ball_frame.

        Args:
            min__x (int): minimum x of frame
            min__y (int): min y
            max__x (int): maximum x of frame
            max__y (int): max y

        Returns:
            None
        """
        self.min_x = min__x
        self.min_y = min__y
        self.max_x = max__x
        self.max_y = max__y
        return None
