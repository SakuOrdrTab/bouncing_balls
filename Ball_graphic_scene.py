# Version 0.01 Just add graphicScene and graphicView and one ball, test

from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QApplication
from PySide6.QtGui import QBrush, QPen
from PySide6.QtCore import Qt


def main_gui():
    app = QApplication([])

    scene = QGraphicsScene(1, 1, 500, 500)

    view = QGraphicsView(scene)



    # Define the brush (fill).
    #
    #brush = QBrush(Qt.red)
    #
    #rect.setBrush(brush)



    # Define the pen (line)
    #
    # pen = QPen(Qt.cyan)
    #
    # pen.setWidth(10)
    #
    # rect.setPen(pen)

    ## ellipsi:

    test_ball = QGraphicsEllipseItem(0, 0, 100, 100)
    test_ball.setPos(75, 30)

    brush = QBrush(Qt.blue)
    test_ball.setBrush(brush)

    # pen = QPen(Qt.green)
    # pen.setWidth(5)
    # test_ball.setPen(pen)

    scene.addItem(test_ball)

    view.show()

    app.exec_()

    return None