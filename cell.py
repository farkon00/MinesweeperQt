from dataclasses import dataclass
from PyQt5 import QtCore, QtGui, QtWidgets


class Cell(QtWidgets.QWidget):
    def __init__(self, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._x = x
        self._y = y

        self.is_bomb = self.is_revealed = self.is_flagged = False

    def paintEvent(self, event):
        """
        Renders cell
        """
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        r = event.rect()
        outer, inner = QtCore.Qt.GlobalColor.gray, QtCore.Qt.GlobalColor.lightGray
        p.fillRect(r, QtGui.QBrush(inner))
        pen = QtGui.QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)