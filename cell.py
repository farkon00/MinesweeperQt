from PyQt5 import QtCore, QtGui, QtWidgets
from state import Statuses 


class Cell(QtWidgets.QPushButton):
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
        outer, inner = QtCore.Qt.GlobalColor.gray, QtCore.Qt.GlobalColor.lightGray
        if self.is_revealed:
            if self.is_bomb:
                p.fillRect(r, QtGui.QBrush(QtCore.Qt.GlobalColor.red))
            else:
                p.fillRect(r, QtGui.QBrush(QtCore.Qt.GlobalColor.transparent))
        elif self.is_flagged:
            p.fillRect(r, QtGui.QBrush(QtCore.Qt.GlobalColor.blue))
        else:
            p.fillRect(r, QtGui.QBrush(inner))
        pen = QtGui.QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)

        around = self.grid.count_mines_around(self._x, self._y)
        if self.is_revealed and not self.is_bomb and around > 0:
            self.setStyleSheet("color: black; font-weight: bold;")
            p.drawText(r, QtCore.Qt.AlignmentFlag.AlignCenter, str(around))

        if self.is_revealed and self.is_bomb:
            self.setStyleSheet("color: black; font-weight: bold;")
            p.drawText(r, QtCore.Qt.AlignmentFlag.AlignCenter, "X")

    def mouseReleaseEvent(self, event) -> None:
        """Handler for click event"""

        if self.grid.state.status == Statuses.LOST or self.grid.state.status == Statuses.WON:
            return 

        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if self.is_flagged:
                return

            if self.is_revealed:
                if self.grid.is_flags_right(self._x, self._y):
                    self.grid.reveal_around(self._x, self._y)
                    self.grid.check_win()
            else:
                self.grid.reveal_cells(self._x, self._y)
                if self.is_bomb:
                    self.grid.state.status = Statuses.LOST

                self.grid.place_mines()
        elif event.button() == QtCore.Qt.MouseButton.RightButton:
            if self.is_revealed:
                return

            if not self.is_flagged:
                self.grid.state.flag()
                self.is_flagged = True
            else:
                self.grid.state.unflag()
                self.is_flagged = False

        self.update()