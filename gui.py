# Version 0.1 Just add graphicScene and graphicView and one ball, test, refractoring
# Version 0.2 Uses Ball_frame for graphic scene for balls

from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QApplication
from PySide6.QtGui import QBrush, QPen, QColor
from PySide6.QtCore import Qt

import Ball_frame

def draw_balls(ball_list, scene):
    for ball in ball_list:
        scene.addItem(ball.ball_sphere())
    return None

def main_gui(ball_list, ballframe):
    app = QApplication([])
    scene = QGraphicsScene(ballframe.min_x, ballframe.min_y, ballframe.max_x, ballframe.max_y)
    view = QGraphicsView(scene)

    scene.setBackgroundBrush(QColor(0,0,0,255))

    draw_balls(ball_list, scene)
    view.show()
    app.exec_()

    return None
