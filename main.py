"""
Minesweeper game in Python pyQt5
"""

import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from grid import Grid
from state import *

MODES: list[tuple[int, int]] = [
    (8, 16),
    (16, 40),
    (24, 99)
]

class MainWindow(QtWidgets.QMainWindow):
    """
    Main window of minesweeper game
    """
    def __init__(self) -> None:
        super().__init__()

        self.level = MODES[0]
        self.level_index = 0

        self._timer = QtCore.QTimer() 
        self._timer.timeout.connect(self.update_timer) # type: ignore
        self._timer.start(1000)

        self.timer_value = 0 

        self.init_ui()

        self.setWindowTitle("Minesweeper")
        self.setFixedSize(600, 600)
        self.show()

    def init_ui(self) -> None:
        """
        Initializes the UI
        """
        self.toolbar_widget = QtWidgets.QWidget()
        self.toolbar_layout = QtWidgets.QHBoxLayout()

        self.mines_label = QtWidgets.QLabel(f"Mines left: {self.level[1]}")
        self.mines_label.setFont(QtGui.QFont("Arial", 20))
        self.mines_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.toolbar_layout.addWidget(self.mines_label)

        self.restart_button = QtWidgets.QPushButton()
        self.restart_button.setFixedSize(32, 32)
        self.restart_button.setIconSize(QtCore.QSize(32, 32))
        self.restart_button.setIcon(QtGui.QIcon("images/smiley.png"))
        self.restart_button.setFlat(True)
        self.toolbar_layout.addWidget(self.restart_button)

        self.state = State(self.level, self.restart_button, self.mines_label)

        self.clock = QtWidgets.QLabel("Timer: 0")
        self.clock.setFont(QtGui.QFont("Arial", 20))
        self.clock.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.toolbar_layout.addWidget(self.clock)

        self.toolbar_widget.setLayout(self.toolbar_layout)

        self.grid_widget = QtWidgets.QWidget()
        self.grid_layout = Grid(self.state, self.level[0], self.level[1])
        self.grid_widget.setLayout(self.grid_layout)

        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.toolbar_widget)
        self.main_layout.addWidget(self.grid_widget)
        self.main_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.main_widget)

    def update_timer(self):
        """Updates clock text and timer value"""
        if self.state.status == Statuses.PLAYING:
            self.timer_value += 1
            self.clock.setText(f"Timer: {self.timer_value}")

    def reset_grid(self):
        """Creates new grid"""
        self.grid_layout = Grid(self.level[0], self.level[1])
        self.grid_layout.update()

def main() -> None:
    """
    Runs the minesweeper game
    """
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    app.exec_()

if __name__ == "__main__":
    main()