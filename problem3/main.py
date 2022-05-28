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
        self.restart_button.clicked.connect(self.restart) # type: ignore
        self.toolbar_layout.addWidget(self.restart_button)

        self.state = State(self)

        self.clock = QtWidgets.QLabel("Timer: 0")
        self.clock.setFont(QtGui.QFont("Arial", 20))
        self.clock.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.toolbar_layout.addWidget(self.clock)

        self.toolbar_widget.setLayout(self.toolbar_layout)

        self.grid_widget = QtWidgets.QWidget()
        self.grid_layout = Grid(self.state, self.level[0], self.level[1])
        self.grid_widget.setLayout(self.grid_layout)

        self.level_layout = QtWidgets.QHBoxLayout()
        self.level_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.levels_group = QtWidgets.QButtonGroup()
        
        self.level_easy = QtWidgets.QRadioButton("Easy")
        self.level_easy.setChecked(True)
        self.levels_group.addButton(self.level_easy)
        self.level_layout.addWidget(self.level_easy)
        
        self.level_medium = QtWidgets.QRadioButton("Medium")
        self.levels_group.addButton(self.level_medium)
        self.level_layout.addWidget(self.level_medium)

        self.level_hard = QtWidgets.QRadioButton("Hard")
        self.levels_group.addButton(self.level_hard)
        self.level_layout.addWidget(self.level_hard)

        self.levels_group.buttonToggled.connect(self.change_level) # type: ignore
        self.levels_widget = QtWidgets.QWidget()
        self.levels_widget.setLayout(self.level_layout)

        self.best_label = QtWidgets.QLabel("Best: 0")
        self.best_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.best_label.setFont(QtGui.QFont("Arial", 25))

        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.levels_widget)
        self.main_layout.addWidget(self.best_label)
        self.main_layout.addWidget(self.toolbar_widget)
        self.main_layout.addWidget(self.grid_widget)
        self.main_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.main_widget)

        self.state.load_bests()
        self.best_label.setText(f"Best: {self.state.bests[self.level_index]}")

    def update_timer(self):
        """Updates clock text and timer value"""
        if self.state.status == Statuses.PLAYING:
            self.timer_value += 1
            self.clock.setText(f"Timer: {self.timer_value}")

    def restart(self):
        """Restarts game"""
        self.grid_layout = Grid(self.state, self.level[0], self.level[1])
        new_grid_widget = QtWidgets.QWidget()
        new_grid_widget.setLayout(self.grid_layout)
        self.main_layout.removeWidget(self.grid_widget)
        self.main_layout.addWidget(new_grid_widget)
        self.grid_widget = new_grid_widget

        self.state.status = Statuses.READY
        self.state.mines_left = self.level[1]
        self.state.mines_left_label.setText(f"Mines left: {self.level[1]}")
        self.timer_value = 0
        self.clock.setText(f"Timer: {self.timer_value}")

    def change_level(self, button: QtWidgets.QAbstractButton):
        """Changes level of game"""
        if button.text() == "Easy":
            self.level = MODES[0]
            self.level_index = 0
        elif button.text() == "Medium":
            self.level = MODES[1]
            self.level_index = 1
        elif button.text() == "Hard":
            self.level = MODES[2]
            self.level_index = 2

        self.best_label.setText(f"Best: {self.state.bests[self.level_index]}")
        self.restart()

def main() -> None:
    """
    Runs the minesweeper game
    """
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    app.exec_()

if __name__ == "__main__":
    main()