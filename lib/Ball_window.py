# Qt GraphicScene for balls to bounce
#
# Ver 0.01 just the scaffold
# Ver 0.1 rename to Ball_window, class for balls' QGraphicScene

from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QApplication
from PySide6.QtGui import QColor
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
# to stop running threads at window exit with ctrl, adapted from https://stackoverflow.com/questions/68163578/stopping-an-infinite-loop-in-a-worker-thread-in-pyqt5-the-simplest-way
# The stopping is left to the actual function running by passing ctrl. Might be more elegant to handle stopping from Worker class (?)
class Worker(QRunnable):
    '''
    Parallel thread for running functions passed with control signals
    '''
    def __init__(self, class_ctrl, worker_ctrl, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.class_ctrl = class_ctrl # Setting true stops all threads of class
        self.worker_ctrl = worker_ctrl # Setting true stops only this thread 

    @Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(self.class_ctrl, self.worker_ctrl, *self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            if result == False: # Had to hack False as return if the worker is killed by Ball_window. Otherwise self.signals is deleted and emit() results in error
                return
            else:
                self.signals.finished.emit()  # Don

class Ball_window(QGraphicsScene):

    def __init__(self, *args, **kwargs):
        super(Ball_window, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.worker_list = []
        self.ball_list = []
        self.ballframe = Ball_frame.Ball_frame(
            self.kwargs['frame_size']['min_x'],
            self.kwargs['frame_size']['min_y'],
            self.kwargs['frame_size']['max_x'],
            self.kwargs['frame_size']['max_y'],
            )
        for i in range(0, self.kwargs['max_balls']):
            if 'max_tries' in kwargs:
                self.create_ball(max_tries = kwargs['max_tries'])
            else:
                self.create_ball()
        print("Balls in list: ", len(self.ball_list))
        self.scene = QGraphicsScene(
            self.kwargs['frame_size']['min_x'],
            self.kwargs['frame_size']['min_y'],
            self.kwargs['frame_size']['max_x'],
            self.kwargs['frame_size']['max_y'],
            )        
        self.view = QGraphicsView(self.scene)
        self.view.closeEvent = self.closeEvent # Add close event of the window to stop worker threads
        self.scene.setBackgroundBrush(QColor(0,0,0,255))
        self.class_ctrl = { 
            'break': False, # Setting this True stops all worker threads of the class
        }
        self.show_balls()
        self.start_worker('pallinsiirtelijä', self.move_balls)

    def closeEvent(self,event):
        print('Close event')
        self.class_ctrl['break'] = True

    # start_worker written as to start multiple workers as needed. However, it is not clear if the implementation is correct for this purpose.
    # For example, it is not clear if a new threadpool should be instantiated here, or in the init block of class
    def start_worker(self, name, fn):
        max_thread_count = QThreadPool.globalInstance().maxThreadCount() # Maximum number of possible threads
        current_thread_count = QThreadPool.globalInstance().activeThreadCount()
        if current_thread_count >= max_thread_count:
            print(f'Max thread count reached, cannot start worker') 
            return
        # self.label.setText(f"Running {threadCount} Threads")
        pool = QThreadPool.globalInstance()
        worker_ctrl = {} # Setting this control to True stops only this worker thread
        worker = Worker(self.class_ctrl, worker_ctrl, fn=fn)
        worker_dict = {
            'name': name,
            'worker_ctrl': worker_ctrl,
            'handle': worker,
        }
        self.worker_list.append(worker_dict) # Keep track of threads
        pool.start(worker)
        print(f'worker "{name}" started')

    def create_ball(self, max_tries = 10):
        if len(self.ball_list) < 1:
            creation = Ball.Ball(self.ballframe)
            if not creation.touches_wall(self.ballframe):
                self.ball_list.append(creation)
        for tries in range(0, max_tries):
            creation = Ball.Ball(self.ballframe)
            ball_free_of_walls = ~creation.touches_wall(self.ballframe) #?
            ball_doesnt_touch_another_ball = True
            if ball_free_of_walls:
                for ball in self.ball_list:
                    if ball.overlaps(creation):
                        ball_doesnt_touch_another_ball = False
                        break # Another iteration might set above True
            if ball_free_of_walls & ball_doesnt_touch_another_ball:
                self.ball_list.append(creation)

    def show_balls(self):
        for ball in self.ball_list:
            self.scene.addItem(ball.ball_ellipse)
        return None

    def set_ball_positions(self):
        for ball in self.ball_list:
            ball.ball_ellipse.setPos(ball.x - ball.radius, ball.y - ball.radius)
        return None

    def move_balls(self, class_ctrl, worker_ctrl, *args, **kwargs):
        worker_ctrl['break'] = False # TLE: Allow running the function
        while True: # TLE: Run forever
            for ball in self.ball_list:
                ball.move()
                if ball.touches_wall(self.ballframe):
                    ball.bounce_w_wall(self.ballframe)
                for b in self.ball_list:
                    if b != ball:
                        if b.overlaps(ball):
                            b.bounce_w_ball(ball)
                # THE LINE BELOW SEEMS TO CREATE ERROR: 
                # QObject::startTimer: Timers cannot be started from another thread.
                # Maybe set_ball_positions() has another timer 
                self.set_ball_positions() 
            stop_worker = ( # Check if this thread or all threads of the class are set to stop
                    (worker_ctrl['break'] == True)
                    | (class_ctrl['break'] == True)
                )
            if stop_worker:
                print('break because flag raised')
                print(f'''class_ctrl['break'] = {class_ctrl['break']}''')
                print(f'''worker_ctrl['break'] = {worker_ctrl['break']}''')
                return False
            time.sleep(0.01)    
        return None

def main():
    # TLE: For easier debugging, the ball window can be started here directly without going through the main application / main window bouncing_balls.main()
    max_balls = 100
    frame_size = {
        'min_x': 1,
        'min_y': 1,
        'max_x': 1080,
        'max_y': 780,
    }
    app = QApplication(sys.argv)
    main = Ball_window(frame_size=frame_size, max_balls=max_balls)
    main.view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()