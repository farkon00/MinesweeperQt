import pickle

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

    def __init__(self, game):
        self.game = game
        self.icon = game.restart_button
        self.mines_left_label = game.mines_label
        self.mines_left = game.level[1]

        self.status = Statuses.READY
        self.pro_mode_enabled = False

        self.bests = [None] * 3

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

    def load_bests(self):
            try:
                self.bests = pickle.load(open("bests", "rb"))
            except FileNotFoundError:
                pass

    def dump_bests(self):
        pickle.dump(self.bests, open("bests", "wb"))

    def win(self):
        self.status = Statuses.WON

        if (self.bests[self.game.level_index] > self.game.timer_value) if \
          self.bests[self.game.level_index] is not None else True:
            self.bests[self.game.level_index] = self.game.timer_value
            self.game.best_label.setText(f"Best: {self.bests[self.level_index] if self.bests[self.level_index] is not None else '-'}")

        self.dump_bests()

    def pro_mode(self, value):
        self.pro_mode_enabled = bool(value)
        self.game.restart()

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

        self.icon.setIcon(QtGui.QIcon(State.icons[self._status]))