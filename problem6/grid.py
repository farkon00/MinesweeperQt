import random
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from cell import Cell
from state import *

sys.setrecursionlimit(100000000)

class Grid(QtWidgets.QGridLayout):
    """
    Grid of minesweeper game
    """
    def __init__(self, state: State, size: int, bombs: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.state = state

        self._size = size
        self.bombs = bombs

        self.grid: list[list[Cell]] = []
        self.is_placed: bool = False

        for i in range(self._size):
            self.grid.append([])
            for j in range(self._size):
                self.grid[-1].append(Cell(j, i, self))
                self.addWidget(self.grid[-1][-1], i, j)

    def count_mines_around(self, x, y):
        """
        Counts the number of mines around the cell
        """
        count = 0
        for i in range(y-1, y+2):
            for j in range(x-1, x+2):
                if i >= 0 and i < self._size and j >= 0 and j < self._size:
                    if self.grid[i][j].is_bomb:
                        count += 1
        return count

    def is_flags_right(self, x: int, y: int) -> bool:
        """
        Checks if flags around the cell is right
        """
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if i >= 0 and i < self._size and j >= 0 and j < self._size:
                    if self.grid[i][j].is_bomb and not self.grid[i][j].is_flagged:
                        return False
                    elif not self.grid[i][j].is_bomb and self.grid[i][j].is_flagged:
                        return False
        return True

    def check_win(self):
        flag = []
        for i in self.grid:
            for j in i:
                if not (j.is_bomb or j.is_revealed):
                    return
                elif j.is_revealed and not j.is_flagged:
                    flag.append(j)

        self.state.win()
        for i in flag:
            j.is_flagged = True    
            j.update() 

    def reveal_around(self, x: int, y: int) -> None:
        """Reveals all cells around the cell"""
        self.place_mines(x, y)

        queue = [(x, y)]
        while queue:
            x, y = queue.pop()
            cell = self.grid[y][x]
            if not cell.is_revealed or cell.is_flagged:  
                cell.is_revealed = True
                if self.count_mines_around(x, y) != 0:
                    continue
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if x+i < 0 or y+j < 0 or x+i >= self._size or y+j >= self._size:
                            continue
                        cell = self.grid[y+j][x+i]
                        if not any((cell.is_revealed, cell.is_flagged, cell.is_bomb)):
                            queue.append((x+i, y+j))

        for i in self.grid:
            for j in i:
                j.update()

        self.check_win()

    def place_mines(self, opened_x: int, opened_y: int) -> None:
        """Places mines on the grid, will make all checks by itself"""
        if self.is_placed:
            return

        self.state.status = Statuses.PLAYING
        placed = 0
        while placed < self.bombs:
            x = random.randint(0, self._size-1)
            y = random.randint(0, self._size-1)
            if not self.grid[x][y].is_bomb and\
                (opened_x-1 < x or x > opened_x+1) and\
                (opened_y-1 < y or y > opened_y+1):
                self.grid[x][y].is_bomb = True
                placed += 1
                self.grid[x][y].update()

        self.is_placed = True