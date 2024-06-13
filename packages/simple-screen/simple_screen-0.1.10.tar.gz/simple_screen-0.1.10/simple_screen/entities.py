from collections import namedtuple
from dataclasses import dataclass


def minmax(_min, _max, value):
    return min(max(_min, value), _max)


class Color:
    def __init__(self, r: int = 0, g: int = 0, b: int = 0):
        self.r = int(minmax(0, 1000, int(r)/255 * 1000))
        self.g = int(minmax(0, 1000, int(g)/255 * 1000))
        self.b = int(minmax(0, 1000, int(b)/255 * 1000))

    def __repr__(self) -> str:
        return f"Color: {self.r}, {self.g}, {self.b}"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.r == other.r and self.g == other.g and self.b == other.b
        return False

    def __hash__(self):
        return hash((self.r, self.g, self.b))

    @property
    def value(self):
        return self.r, self.g, self.b


@dataclass
class Position:
    y: int
    x: int


@dataclass
class Dimensions:
    h: int
    w: int
