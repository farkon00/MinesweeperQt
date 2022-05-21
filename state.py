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

    def __init__(self, icon : QtWidgets.QPushButton):
        self.icon = icon

        self.status = Statuses.READY

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

        self.icon.setIcon(QtGui.QIcon(State.icons[self._status]))