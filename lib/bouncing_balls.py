# Started whole new refactoring of code to get bugs fixed, all the classes are in the same script

from PySide6.QtWidgets import QMainWindow, QPushButton, QApplication, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem
from PySide6.QtGui import QColor, QBrush
from PySide6.QtCore import QRunnable, Slot, QThreadPool, Signal, QObject

import sys, time, traceback, math, random


class Ball:
    """
    class of Ball, location of the ball, velocities, mass, radius, holds also QEllipseItem to draw the ball
    """        
    def __init__(self, frame):
        """Constructor for Ball, sets random speed, colour and position.

        Args:
            frame (Ball_frame): frame for balls and physics

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
        self.frame = frame

    # simple dist between two coordinates
    def _dist(x1, y1, x2, y2) : return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def __str__(self) -> str:
        # string representation if needed
        message = "Ball obj id <{}>\n".format(id(self))
        message += " center x:{0} y:{1}\n v_x:{2:.2f} v_y:{3:.2f}\n radius: {4}, mass: {5}\n".format(
            self.x, self.y, self.x_vel, self.y_vel, self.radius, self.mass)
        message += " Touches wall: "+str(self.touches_wall())
        return message

    def move(self):
        """moves ball according to its speed, does not refresh QEllipseItem position

        Returns:
            None
        """        
        self.x += int(self.x_vel)
        self.y += int(self.y_vel)
        return None

    # for class
    @staticmethod
    def ball_distance(ball_a, ball_b):
        """Distance between two balls

        Args:
            ball_a (Ball): first ball
            ball_b (Ball): second ball

        Returns:
            float: Distance between the radiuses of the two balls
        """        
        return math.sqrt((ball_a.x - ball_b.x) ** 2 + (ball_a.y - ball_b.y) ** 2) - ball_a.radius - ball_b.radius

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
    def touches_wall(self):
        """Checks if ball radius is over the frame, i.e. touches walls. Uses
        FRAME... constants for boundaries

        Returns:
            Boolean: returns True if ball is even partly outside frame constants
        """        
        if (self.x + self.radius >= self.frame.max_x) or (self.x - self.radius <= self.frame.min_x) \
            or (self.y + self.radius >= self.frame.max_y) or (self.y - self.radius <= self.frame.min_y):
                return True
        else:
            return False

    def bounce_w_wall(self): # rudimentary non-physical wall collision
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
        # implement movement of ball away from wall
        # here:
        self.move() # experimental
        return None

    def bounce_w_ball(self, ball2):
        """Bounces two balls.
        Simplistic physical, 1-dim collisions calculated
        separately for x and y
        
        Args:
            ball2 (Ball): second ball, first is self

        Returns:
            None
        """        
        # rudimentary version: reverse speeds
        # self.x_vel = -1 * self.x_vel
        # ball2.x_vel = -1 * ball2.x_vel
        # self.y_vel = -1 * self.y_vel
        # ball2.y_vel = -1 * ball2.y_vel
        
        # Okay, this is still a simplistication. It is considered that
        # momentum is preserved in both x and y dimensions, so they are
        # calculated separately. Temporary variables needed, *_temp
        x_vel_self_temp = ((self.mass - ball2.mass) * self.x_vel + 2 * ball2.mass * ball2.x_vel) / (self.mass + ball2.mass)
        x_vel_ball2_temp = self.x_vel + x_vel_self_temp - ball2.x_vel
        y_vel_self_temp = ((self.mass - ball2.mass) * self.y_vel + 2 * ball2.mass * ball2.y_vel) / (self.mass + ball2.mass)
        y_vel_ball2_temp = self.y_vel + y_vel_self_temp - ball2.y_vel
        self.x_vel = x_vel_self_temp # now implement speeds according to above
        self.y_vel = y_vel_self_temp
        ball2.x_vel = x_vel_ball2_temp
        ball2.y_vel = y_vel_ball2_temp
        
        # implement movement of both balls from eachother
        # here:
        self.move() # experimental
        ball2.move()
        return None

class Ball_frame():
    """
    Class to hold the wanted dimensions of frame to hold the balls and physics
    """    
    def __init__(self, min__x, min__y, max__x, max__y):
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
    update_positions = Signal(list)

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
        self.signals = kwargs.get('signals', WorkerSignals())  # Use provided signals or create a new one
        self.class_ctrl = class_ctrl # Setting true stops all threads of class
        self.worker_ctrl = worker_ctrl # Setting true stops only this thread 

    @Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        # Retrieve args/kwargs here; and fire processing using them
        result = None # Assign a default value to avoid UnbounlocalError
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
                self.signals.finished.emit()  # Done

class Ball_window(QGraphicsScene):
    """
    A Window (QGraphicsscene) to show the balls within GUI. Ballframe sets the size
    """    

    def __init__(self, *args, **kwargs):
        super(Ball_window, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.ball_list = []
        
        # create a ball_frame
        self.ballframe = Ball_frame(
            self.kwargs['frame_size']['min_x'],
            self.kwargs['frame_size']['min_y'],
            self.kwargs['frame_size']['max_x'],
            self.kwargs['frame_size']['max_y'],
            )
        
         # Initialize WorkerSignals instance
        self.worker_signals = WorkerSignals()

        # Connecting the signal to the slot
        self.worker_signals.update_positions.connect(self.update_ball_positions)        
        
        # create a ball_list
        self.worker_list = []
        for i in range(0, self.kwargs['max_balls']):
            if 'max_tries' in kwargs:
                self.create_ball(max_tries = kwargs['max_tries'])
            else:
                self.create_ball()
        print("Balls in list: ", len(self.ball_list))
        
        # create scene
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
        # print(f'Ball count in window = {len(self.scene.items())}')
        self.show_balls()
        self.start_worker('ballmover', self.move_balls)

    def update_ball_positions(self, positions):
        for ball, pos in zip(self.ball_list, positions):
            ball.ball_ellipse.setPos(*pos)

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
        worker_ctrl = {}  # Setting this control to True stops only this worker thread
        worker = Worker(self.class_ctrl, worker_ctrl, fn=fn, signals=self.worker_signals)
        worker_dict = {
            'name': name,
            'worker_ctrl': worker_ctrl,
            'handle': worker,
        }
        self.worker_list.append(worker_dict) # Keep track of threads
        pool.start(worker)
        print(f'worker "{name}" started')

    def create_ball(self, max_tries = 10):
        """Tries to create ball within a free space in scene. 
        Has maximum tries, so that it doesn't try forever if scene is almost full

        Args:
            max_tries (int, optional): Maximum tries to make a new ball. Defaults to 10.
        """        
        for tries in range(0, max_tries):
            creation = Ball(self.ballframe)
            ball_free_of_walls = ~creation.touches_wall() #?
            ball_doesnt_touch_another_ball = True
            if ball_free_of_walls:
                for ball in self.ball_list:
                    if ball.overlaps(creation):
                        ball_doesnt_touch_another_ball = False
                        break # Another iteration might set above True
            if ball_free_of_walls & ball_doesnt_touch_another_ball:
                self.ball_list.append(creation)
                return None # bugfix: has to return not to fill ball_list
        return None

    def show_balls(self):
        """Add all QEllipseitems(Ball Obj) to the scene in ballwindow. Goes through ball_list

        Returns:
            None
        """        
        for ball in self.ball_list:
            self.scene.addItem(ball.ball_ellipse)
        return None

    def set_ball_positions(self):
        """Set positions in QEllipseitems in Ball objects to match x and y within the Ball object instance
        that are derived from physics

        Returns:
            None
        """        
        for ball in self.ball_list:
            ball.ball_ellipse.setPos(ball.x - ball.radius, ball.y - ball.radius)
        return None

    def move_balls(self, class_ctrl, worker_ctrl, signals, *args, **kwargs):
        worker_ctrl['break'] = False
        while True:
            ball_positions = []
            for ball in self.ball_list:
                ball.move()
                if ball.touches_wall():
                    ball.bounce_w_wall()
                for other_ball in self.ball_list:
                    if other_ball != ball and other_ball.overlaps(ball):
                        other_ball.bounce_w_ball(ball)
                ball_positions.append((ball.x - ball.radius, ball.y - ball.radius))
            signals.update_positions.emit(ball_positions)  # Emitting the signal with positions
            if class_ctrl['break'] or worker_ctrl['break']:
                return False
            time.sleep(0.01)

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args 
        self.kwargs = kwargs
        self.button = QPushButton("Start balls")
        self.button.clicked.connect(self.start_ball_window)
        self.setCentralWidget(self.button)
        self.show()
        self.ball_window = None
        # print('Forced starting of ball_window')
        # self.start_ball_window()

    def start_ball_window(self):
        if self.ball_window is None: # Check if window is already created not to create multiple child windows
            self.ball_window = Ball_window( max_balls=self.kwargs['max_balls'],
                                            frame_size = self.kwargs['frame_size'],
                                            max_tries=self.kwargs['max_tries'])
        self.ball_window.view.show() # If window is created and then closed, it will reappear because of this

def main():

    max_balls_wanted = 100 # seems to work best
    max_tries = 100
    frame_size = {
        'min_x': 1,
        'min_y': 1,
        'max_x': 1080,
        'max_y': 780,
    }
    app = QApplication(sys.argv)
    main = MainWindow(
                      frame_size=frame_size,
                      max_balls=max_balls_wanted,
                      max_tries=max_tries
                    )
    main.show()
    app.exec()

if __name__ == "__main__":
    main()