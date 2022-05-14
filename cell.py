from dataclasses import dataclass
from PyQt5 import QtCore, QtGui, QtWidgets


class Cell(QtWidgets.QPushButton):
    def __init__(self, x, y, grid, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._x = x
        self._y = y

        self.grid = grid 

        self.is_bomb = self.is_revealed = self.is_flagged = False

        self.clicked.connect(self.on_click)

    def paintEvent(self, event):
        """
        Renders cell
        """
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        r = event.rect()
        outer, inner = QtCore.Qt.GlobalColor.gray, QtCore.Qt.GlobalColor.lightGray
        p.fillRect(r, QtGui.QBrush(inner if not self.is_bomb else QtCore.Qt.GlobalColor.red))
        pen = QtGui.QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)

        if self.is_revealed and not self.is_bomb:
            self.setStyleSheet("color: black; font-weight: bold;")
            p.drawText(r, QtCore.Qt.AlignmentFlag.AlignCenter, str(self.grid.count_mines_around(self._x, self._y)))

    def on_click(self) -> None:
        self.is_revealed = True
        self.update()