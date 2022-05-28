from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import *
from state import Statuses 


class Cell(QtWidgets.QPushButton):
    MINE_COLORS = [
        Qt.GlobalColor.blue, Qt.GlobalColor.darkGreen, Qt.GlobalColor.red, Qt.GlobalColor.darkBlue,
        Qt.GlobalColor.darkRed , Qt.GlobalColor.green, Qt.GlobalColor.black, Qt.GlobalColor.lightGray
    ]

    def __init__(self, x, y, grid, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._x = x
        self._y = y

        self.grid = grid 

        self.is_bomb = self.is_revealed = self.is_flagged = False

    def paintEvent(self, event):
        """
        Renders cell
        """
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        r = event.rect()
        outer, inner = Qt.GlobalColor.gray, Qt.GlobalColor.lightGray
        if self.is_revealed:
            if self.is_bomb:
                p.fillRect(r, QtGui.QBrush(Qt.GlobalColor.red))
            else:
                p.fillRect(r, QtGui.QBrush(Qt.GlobalColor.transparent))
        elif self.is_flagged:
            p.fillRect(r, QtGui.QBrush(Qt.GlobalColor.blue))
        else:
            p.fillRect(r, QtGui.QBrush(inner))
        pen = QtGui.QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)

        around = self.grid.count_mines_around(self._x, self._y)
        if self.is_revealed and not self.is_bomb and around > 0:
            self.setStyleSheet(f"font-weight: bold;")
            pen = QtGui.QPen(self.MINE_COLORS[around - 1])
            pen.setWidth(1)
            p.setPen(pen)
            p.drawText(r, Qt.AlignmentFlag.AlignCenter, str(around))

        if self.is_revealed and self.is_bomb:
            self.setStyleSheet("font-weight: bold;")
            p.drawText(r, Qt.AlignmentFlag.AlignCenter, "X")

    def mouseReleaseEvent(self, event) -> None:
        """Handler for click event"""

        if self.grid.state.status == Statuses.LOST or self.grid.state.status == Statuses.WON:
            return 

        if event.button() == Qt.MouseButton.LeftButton:
            if self.is_flagged:
                return

            if self.is_revealed:
                if self.grid.is_flags_right(self._x, self._y):
                    self.grid.reveal_around(self._x, self._y)
                    self.grid.check_win()
            else:
                self.grid.reveal_around(self._x, self._y)
                if self.is_bomb:
                    self.grid.state.status = Statuses.LOST
        elif event.button() == Qt.MouseButton.RightButton and not self.grid.state.pro_mode_enabled:
            if self.is_revealed:
                return

            if not self.is_flagged:
                self.grid.state.flag()
                self.is_flagged = True
            else:
                self.grid.state.unflag()
                self.is_flagged = False

        self.update()