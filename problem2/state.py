from enum import Enum, auto 

from PyQt5 import QtGui, QtWidgets

class Statuses(Enum):
    """
    Enum of statuses for the game.
    """
    READY   = auto()
    PLAYING = auto()
    WON     = auto()
    LOST    = auto()



class State:
    icons = {
        Statuses.READY:   "images/plus.png",
        Statuses.PLAYING: "images/smiley.png",
        Statuses.WON:     "images/smiley-lol.png",
        Statuses.LOST:    "images/cross.png"
    }

    def __init__(self, mode: tuple[int, int], icon : QtWidgets.QPushButton, mines_left_label : QtWidgets.QLabel):
        self.icon = icon
        self.mines_left_label = mines_left_label
        self.mines_left = mode[1]

        self.status = Statuses.READY

    def flag(self):
        """
        Decrements mines left.
        """
        self.mines_left -= 1
        self.mines_left_label.setText(f"Mines left: {self.mines_left}")

    def unflag(self):
        """
        Decrements mines left.
        """
        self.mines_left += 1
        self.mines_left_label.setText(f"Mines left: {self.mines_left}")

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

        self.icon.setIcon(QtGui.QIcon(State.icons[self._status]))