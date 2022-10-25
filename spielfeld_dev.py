"""Spielfeld"""
from enum import Enum

from schiffe import Direction, Schiff


class State(Enum):
    """Enum Kodierung Spielfeldzeilen"""

    WASSER = 0
    SCHIFF = 1
    BESCHOSSEN = 2
    GETROFFEN = 3


class Spielfeld:
    """Klasse zur Repräsentierung des Spielfelds"""

    def __init__(self, hoehe, breite):
        self.hoehe = hoehe
        self.breite = breite
        self.data = [
            [State.WASSER for x in range(hoehe)] for y in range(breite)
        ]

    def change_field(self, posx, posy):
        """Feld an einer Position ändern"""
        posx -= 1
        posy -= 1
        self.data[posx][posy] = State.SCHIFF

    def add_ship(self, ship: Schiff, posx: int, posy: int):
        """Schiffe an einer Position adden"""
        posx -= 1
        posy -= 1
        if (
            self.data[posx][posy] == State.SCHIFF
            or self.data[posx][posy] == State.GETROFFEN
        ):
            print("An der Stelle ist bereits ein Schiff.")

        # schiff = Schiff.einlesen() selbst eingeben

        if ship.laenge == 1:
            self.data[posx][posy] = 1

        elif ship.laenge == 2:
            self.data[posx][posy] = 1

            # Rechts
            if Direction == "r":
                self.data[posx][posy] = 1
                self.data[posx][posy + 1] = 1

            # Links
            if Direction == "l":
                self.data[posx][posy] = 1
                self.data[posx][posy - 1] = 1

            # Oben
            if Direction == "o":
                self.data[posx][posy] = 1
                self.data[posx - 1][posy] = 1

            # Unten
            if Direction == "u":
                self.data[posx][posy] = 1
                self.data[posx + 1][posy] = 1

    def print_field(self):
        """Ausgeben des Feldes und setzen der Schiffe"""

        print("- 1 2 3 4 5 6 7 8 9 10")

        assert self.breite == 10
        for x, label in enumerate("ABCDEFGHIJ"):
            print(label + " ", end="")

            for y in range(self.hoehe):
                if self.data[x][y] == State.WASSER:
                    print("_ ", end="")
                elif self.data[x][y] == State.SCHIFF:
                    print("S ", end="")
                elif self.data[x][y] == State.BESCHOSSEN:
                    print("O ", end="")
                elif self.data[x][y] == State.GETROFFEN:
                    print("X ", end="")
            print("")


feld1 = Spielfeld(10, 10)
feld1.change_field(5, 5)

schiff1 = Schiff(10, Direction.LINKS)
feld1.add_ship(schiff1,8,8)
feld1.print_field()
