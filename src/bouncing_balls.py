# first stable version 1.0

from PySide6.QtWidgets import QApplication

import sys

from src.gui import MainWindow
from src.constants import MAX_BALLS, MAX_TRIES

# Constants are in constants.py


def main():
    app = QApplication(sys.argv)

    # Get native screen size and set to full screen
    size = app.screens()[0].size()

    main_window = MainWindow(frame_size=size, max_balls=MAX_BALLS, max_tries=MAX_TRIES)

    main_window.show()
    app.exec()


if __name__ == "__main__":
    main()
