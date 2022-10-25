"""Spielfeld"""
from enum import Enum
from random import randint

from schiessen import Schuss
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

        if ship.laenge == 1:
            self.data[posx][posy] = State.SCHIFF

        # for Schleife (if für Fälle)
        elif ship.laenge == 2:

            # Rechts
            if ship.richtung == Direction.RECHTS:
                self.data[posx][posy] = State.SCHIFF
                self.data[posx][posy + 1] = State.SCHIFF

            # Links
            if ship.richtung == Direction.LINKS:
                self.data[posx][posy] = State.SCHIFF
                self.data[posx][posy - 1] = State.SCHIFF

            # Oben
            if ship.richtung == Direction.OBEN:
                self.data[posx][posy] = State.SCHIFF
                self.data[posx - 1][posy] = State.SCHIFF

            # Unten
            if ship.richtung == Direction.UNTEN:
                self.data[posx][posy] = State.SCHIFF
                self.data[posx + 1][posy] = State.SCHIFF

        elif ship.laenge == 3:

            # Rechts
            if ship.richtung == Direction.RECHTS:
                self.data[posx][posy] = State.SCHIFF
                self.data[posx][posy + 1] = State.SCHIFF
                self.data[posx][posy + 2] = State.SCHIFF

            # Links
            if ship.richtung == Direction.LINKS:
                self.data[posx][posy] = State.SCHIFF
                self.data[posx][posy - 1] = State.SCHIFF
                self.data[posx][posy - 2] = State.SCHIFF
            # Oben
            if ship.richtung == Direction.OBEN:
                self.data[posx][posy] = State.SCHIFF
                self.data[posx - 1][posy] = State.SCHIFF
                self.data[posx - 2][posy] = State.SCHIFF

            # Unten
            if ship.richtung == Direction.UNTEN:
                self.data[posx][posy] = State.SCHIFF
                self.data[posx + 1][posy] = State.SCHIFF
                self.data[posx + 2][posy] = State.SCHIFF

        elif ship.laenge == 4:

            # Rechts
            if ship.richtung == Direction.RECHTS:
                self.data[posx][posy] = State.SCHIFF
                self.data[posx][posy + 1] = State.SCHIFF
                self.data[posx][posy + 2] = State.SCHIFF
                self.data[posx][posy + 3] = State.SCHIFF

            # Links
            if ship.richtung == Direction.LINKS:
                self.data[posx][posy] = State.SCHIFF
                self.data[posx][posy - 1] = State.SCHIFF
                self.data[posx][posy - 2] = State.SCHIFF
                self.data[posx][posy - 3] = State.SCHIFF

            # Oben
            if ship.richtung == Direction.OBEN:
                self.data[posx][posy] = State.SCHIFF
                self.data[posx - 1][posy] = State.SCHIFF
                self.data[posx - 2][posy] = State.SCHIFF
                self.data[posx - 3][posy] = State.SCHIFF

            # Unten
            if ship.richtung == Direction.UNTEN:
                self.data[posx][posy] = State.SCHIFF
                self.data[posx + 1][posy] = State.SCHIFF
                self.data[posx + 2][posy] = State.SCHIFF
                self.data[posx + 3][posy] = State.SCHIFF

    def single_shot(self):
        """Einzelner Schuss auf Map"""

        x = Schuss.posx() - 1
        y = Schuss.posy() - 1

        if self.data[x][y] == State.SCHIFF:
            self.data[x][y] = State.GETROFFEN
        elif self.data[x][y] == State.GETROFFEN:
            self.data[x][y] = State.GETROFFEN
        else:
            self.data[x][y] = State.BESCHOSSEN

    def auto_shooter(self):
        """Automatisch random Schüsse auf Map"""
        anz = 100
        for i in range(anz):
            x = randint(1, 10) - 1
            y = randint(1, 10) - 1

            if self.data[x][y] == State.SCHIFF:
                self.data[x][y] = State.GETROFFEN
            elif self.data[x][y] == State.GETROFFEN:
                self.data[x][y] = State.GETROFFEN
            else:
                self.data[x][y] = State.BESCHOSSEN

    def create_ship(self):
        """Schiffe zusammenstellen"""

        schiff = Schiff(Schiff.einlesen(), Direction.einlesen())
        feld1.add_ship(schiff, Schiff.posx(), Schiff.posy())

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
                    print("  ", end="")
                elif self.data[x][y] == State.GETROFFEN:
                    print("X ", end="")
            print("")


"""Spielfeld erstellen"""
feld1 = Spielfeld(10, 10)
# feld1.change_field(5, 5)

"""Schiffe per Code adden und platzieren"""
schiff1 = Schiff(2, Direction.LINKS)
schiff2 = Schiff(2, Direction.RECHTS)
schiff3 = Schiff(3, Direction.OBEN)
schiff4 = Schiff(3, Direction.UNTEN)
schiff5 = Schiff(4, Direction.OBEN)

feld1.add_ship(schiff1, 8, 8)
feld1.add_ship(schiff2, 2, 2)
feld1.add_ship(schiff3, 10, 10)
feld1.add_ship(schiff4, 8, 2)
feld1.add_ship(schiff5, 5, 9)

"""Schiffe per Nutzereingabe erstellen und platzieren"""
# feld1.create_ship()


"""Ausgabe Feld"""
feld1.print_field()

"""Schießen"""
# feld1.single_shot()
feld1.auto_shooter()

"""Ausgabe Feld"""
feld1.print_field()
