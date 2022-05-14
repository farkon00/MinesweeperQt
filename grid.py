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

        placed = 0
        while placed < self.bombs:
            x = QtCore.qrand() % self._size
            y = QtCore.qrand() % self._size
            if not self.grid[x][y].is_bomb and not self.grid[x][y].is_revealed:
                self.grid[x][y].is_bomb = True
                placed += 1
                self.grid[x][y].update()