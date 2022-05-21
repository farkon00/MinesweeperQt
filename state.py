from enum import Enum, auto 

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
        Statuses.WON:     "images/cross.png",
        Statuses.LOST:    "images/smiley_lol.png"
    }
    def __init__(self):
        self.status = Statuses.READY