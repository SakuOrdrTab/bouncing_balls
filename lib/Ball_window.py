# Qt GraphicScene for balls to bounce
#
# Ver 0.01 just the scaffold
# Ver 0.1 rename to Ball_window, class for balls' QGraphicScene

from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QApplication
from PySide6.QtGui import QBrush, QPen, QColor
from PySide6.QtCore import Qt

from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QApplication
from PySide6.QtGui import QBrush, QPen, QColor
from PySide6.QtCore import Qt
from PySide6.QtCore import QRunnable, Slot, QThreadPool, Signal, QObject # TLE: import modules needed by threading
import time, traceback, sys # TLE: import other modules used

import Ball
import Ball_frame

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
        # print(self.kwargs)
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

class Ball_window(QGraphicsScene):

    def show_balls(self):
        for ball in self.ball_list:
            self.scene.addItem(ball.ball_ellipse)
        return None

    def set_ball_positions(self):
        for ball in self.ball_list:
            ball.ball_ellipse.setPos(ball.x - ball.radius, ball.y - ball.radius)
        return None

    # TLE: actual function to move balls. Could be any other functions meant to run in parallel thread
    def move_balls(self, ctrl, *args, **kwargs):
        ctrl['break'] = False # TLE: Allow running the function
        while True: # TLE: Run forever
            # print(kwargs)
            # print('asdf')
            # actual move
            # scene = kwargs['scene']
            # ball_list = kwargs['ball_list']
            for ball in self.ball_list:
                ball.move()
                if ball.touches_wa():
                    ball.bounce_w_wall(self.frame)
                for b in self.ball_list:
                    if b != ball:
                        if b.overlaps(ball):
                            b.bounce_w_ball(ball)
                self.set_ball_positions()
            
            if ctrl['break']: # TLE: If ctrl value is set true by main_gui, stop execution of the funtion
                print('break because flag raised')
                break # or in this case: retur
            time.sleep(0.1)    


    def __init__(self, frame, ball_list):
        super().__init__(self, frame.min_x, frame.min_y, frame.max_x, frame.max_y)

        self.ball_list = ball_list
        self.frame = frame

        self.setBackgroundBrush(QColor(0,0,0,255))
        self.scene = QGraphicsScene(frame.min_x, frame.min_y, frame.max_x, frame.max_y)
        self.view = QGraphicsView(self.scene)
        self.scene.setBackgroundBrush(QColor(0,0,0,255))

        threadpool = QThreadPool() # Init multithreading
        ctrl = {} # TLE: define control parameter as dict. I understood this provides a pointer to the variable. Therefore it can be accessed outside the function
        worker = Worker(ctrl, fn=self.move_balls) # create a worker in parallel thread
        threadpool.start(worker) # TLE: Begin parallel process
        self.view.show()
        
        # worker.ctrl['break'] = True # Set ctrl to True which is picked up by the actual function (move_balls()) in parallel thread 
    
        return None