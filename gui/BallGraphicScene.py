# Qt GraphicScene for balls to bounce
#
# Ver 0.01 just the scaffold

from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QApplication
from PySide6.QtGui import QBrush, QPen, QColor
from PySide6.QtCore import Qt

import lib.Ball_frame as Ball_frame

class Ball_scene(QGraphicsScene):

    def __init__(self, min_x, min_y, max_x, max_y):
        super().__init__(self, min_x, min_y, max_x, max_y)
        self.setBackgroundBrush(QColor(0,0,0,255))
        return None