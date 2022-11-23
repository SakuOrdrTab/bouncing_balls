# Version 0.1 Just add graphicScene and graphicView and one ball, test, refractoring

from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QApplication
from PySide6.QtGui import QBrush, QPen, QColor
from PySide6.QtCore import Qt

def draw_balls(ball_list, scene):
    for ball in ball_list:
        scene.addItem(ball.ball_sphere())
    return None

def main_gui(ball_list):
    app = QApplication([])
    scene = QGraphicsScene(1, 1, 500, 500)
    view = QGraphicsView(scene)

    draw_balls(ball_list, scene)
    view.show()
    app.exec_()

    return None
