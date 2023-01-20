# Ver 0.01
# Ver 0.02 Proto-test for GUI
# Ver 0.1 modules include rudimentary physics, rudimentary graphics, refractoring modules
# Ver 0.1.1 Ball creation added, debugging
# Ver 0.2 Added ball graphic scene frame
# Ver 0.2.1 Directory restructuring
# Ver 0.2.2 added max_tries to kwarg
from PySide6.QtWidgets import QMainWindow, QPushButton

import PySide6
import sys 
import Ball_window


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
            self.ball_window = Ball_window.Ball_window( max_balls=self.kwargs['max_balls'],
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
    app = PySide6.QtWidgets.QApplication(sys.argv)
    main = MainWindow(
                      frame_size=frame_size,
                      max_balls=max_balls_wanted,
                      max_tries=max_tries
                    )
    main.show()
    app.exec()

if __name__ == "__main__":
    main()