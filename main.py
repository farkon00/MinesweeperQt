"""
Minesweeper game in Python pyQt5
"""

import sys

from PyQt5 import QtCore, QtGui, QtWidgets

FIELD_WIDTHS: list[tuple[int, int]] = [
    (8, 16),
    (16, 32),
    (24, 99)
]

class MainWindow(QtWidgets.QMainWindow):
    """
    Main window of minesweeper game
    """
    def __init__(self) -> None:
        super().__init__()
        self.setGeometry(300, 300, 300, 300)

def main() -> None:
    """
    Runs the minesweeper game
    """
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()