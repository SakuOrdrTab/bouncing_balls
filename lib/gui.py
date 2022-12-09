# Version 0.1 Just add graphicScene and graphicView and one ball, test, refractoring
# Version 0.2 Uses Ball_frame for graphic scene for balls

# https://www.pythonguis.com/tutorials/multithreading-pyside-applications-qthreadpool/
# https://stackoverflow.com/questions/68163578/stopping-an-infinite-loop-in-a-worker-thread-in-pyqt5-the-simplest-way

from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QApplication
from PySide6.QtGui import QBrush, QPen, QColor
from PySide6.QtCore import Qt
from PySide6.QtCore import QRunnable, Slot, QThreadPool, Signal, QObject # TLE: import modules needed by threading
import time, traceback, sys # TLE: import other modules used

import Ball_frame
import Ball_window

def main_gui(ball_list, ballframe):
    app = QApplication([])
    ball_window = Ball_window.Ball_window(ballframe, ball_list, maxtries = 100)

    
    Ball_window.show()
    app.exec_()
    print('Stop GUI') 
    
    return None