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
import Ball_graphic_scene

# TLE: Copy-pasted from https://www.pythonguis.com/tutorials/multithreading-pyside-applications-qthreadpool/
# to convey information about worker state
class WorkerSignals(QObject): 
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    '''
    finished = Signal()  # QtCore.Signal
    error = Signal(tuple)
    result = Signal(object)

# TLE: Mostly copy-pasted from https://www.pythonguis.com/tutorials/multithreading-pyside-applications-qthreadpool/
# to kill running functions at window exit with ctrl, adapted from https://stackoverflow.com/questions/68163578/stopping-an-infinite-loop-in-a-worker-thread-in-pyqt5-the-simplest-way
# The killing is left to the actual function wunning by passing ctrl. Might be more elegant to handle killing from Worker class
class Worker(QRunnable):
    '''
    Parallel thread for running functions passed with control signals
    '''
    def __init__(self, ctrl, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.ctrl = ctrl # TLE: Control variable passed on to the actual function running in thread

    @Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(self.ctrl, *self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Don

def draw_balls(ball_list, scene):
    for ball in ball_list:
        scene.addItem(ball.ball_sphere())
    return None

# TLE: actual function to move balls. Could be any other functions meant to run in parallel thread
def move_balls(ctrl, *args, **kwargs):
    ctrl['break'] = False # TLE: Allow running the function
    while True: # TLE: Run forever
       print("Move ball, move!")
       if ctrl['break']: # TLE: If ctrl value is set true by main_gui, stop execution of the funtion
            print('break because flag raised')
            break # or in this case: retur
       time.sleep(0.1)

# class Ball_graphicscene
def main_gui(ball_list, ballframe):
    app = QApplication([])
    # scene = Ball_graphic_scene.Ball_graphic_scene(ballframe.min_x, ballframe.min_y, ballframe.max_x, ballframe.max_y)
    scene = QGraphicsScene(ballframe.min_x, ballframe.min_y, ballframe.max_x, ballframe.max_y)
    view = QGraphicsView(scene)

    scene.setBackgroundBrush(QColor(0,0,0,255))

    draw_balls(ball_list, scene) # ball physics keep balls in frame
    threadpool = QThreadPool() # Init multithreading
    ctrl = {} # TLE: define control parameter as dict. I understood this provides a pointer to the variable. Therefore it can be accessed outside the function
    worker = Worker(ctrl, fn=move_balls) # create a worker in parallel thread
    threadpool.start(worker) # TLE: Begin parallel process
    view.show()
    app.exec_()
    print('Stop GUI') 
    worker.ctrl['break'] = True # Set ctrl to True which is picked up by the actual function (move_balls()) in parallel thread 
    
    return None