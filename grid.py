from PyQt5 import QtCore, QtGui, QtWidgets
from cell import Cell

class Grid(QtWidgets.QGridLayout):
    """
    Grid of minesweeper game
    """
    def __init__(self, size: int, bombs: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._size = size
        self.bombs = bombs

        self.grid: list[list[Cell]] = []

        for i in range(self._size):
            self.grid.append([])
            for j in range(self._size):
                self.grid[-1].append(Cell(i, j))
                self.addWidget(self.grid[-1][-1], i, j)