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
        self.is_placed: bool = False

        for i in range(self._size):
            self.grid.append([])
            for j in range(self._size):
                self.grid[-1].append(Cell(i, j, self))
                self.addWidget(self.grid[-1][-1], i, j)

    def count_mines_around(self, x, y):
        """
        Counts the number of mines around the cell
        """
        count = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if i >= 0 and i < self._size and j >= 0 and j < self._size:
                    if self.grid[i][j].is_bomb:
                        count += 1
        return count

    def reveal_cells(self, x: int, y: int) -> None:
        """
        Reveals all cells around the cell
        """
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if i >= 0 and i < self._size and j >= 0 and j < self._size:
                    self.grid[i][j].is_revealed = True
                    self.grid[i][j].update()

    def place_mines(self) -> None:
        if self.is_placed:
            return

        placed = 0
        while placed < self.bombs:
            x = QtCore.qrand() % self._size
            y = QtCore.qrand() % self._size
            if not self.grid[x][y].is_bomb and not self.grid[x][y].is_revealed:
                self.grid[x][y].is_bomb = True
                placed += 1
                self.grid[x][y].update()

        self.is_placed = True