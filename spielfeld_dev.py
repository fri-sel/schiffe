"""Spielfeld"""
from enum import Enum


class State(Enum):
    """Enum Kodierung Spielfeldzeilen"""

    WASSER = 0
    SCHIFF = 1
    BESCHOSSEN = 2
    VERSENKT = 3


class Spielfeld:
    """Klasse zur Repräsentierung des Spielfelds"""

    def __init__(self, hoehe, breite):
        self.hoehe = hoehe
        self.breite = breite
        self.data = [[0 for x in range(hoehe)] for y in range(breite)]

    def change_field(self, posx, posy):
        """Feld an einer Position ändern"""
        self.data[posx][posy] = 1

    def add_ship(self,posx,posy):
        """Schiffe an einer Position adden"""

    def print_field(self):
        """Ausgeben des Feldes und setzen der Schiffe"""
        self.data[1][1] = 1
        self.data[2][2] = 1
        self.data[3][3] = 1
        print("- 1 2 3 4 5 6 7 8 9 10")

        assert self.breite == 10
        for x, label in enumerate("ABCDEFGHIJ"):
            print(label + " ", end="")

            for y in range(self.hoehe):
                if self.data[x][y] == 0:
                    print("_ ", end="")
                elif self.data[x][y] == 1:
                    print("X ", end="")
            print("")


feld1 = Spielfeld(10, 10)
feld1.change_field(0, 0)
feld1.print_field()
