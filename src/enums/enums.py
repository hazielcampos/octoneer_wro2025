from enum import Enum

class Direction(Enum):
    RIGHT = 0
    LEFT = 1

class Orientation(Enum):
    CLOCKWISE = 0
    COUNTERCLOCKWISE = 1
    NO_SET = 2
    
class Lane(Enum):
    RIGHT = 0
    LEFT = 1
    CENTER = 2