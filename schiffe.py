"""Schiffe"""
from enum import Enum


class Direction(Enum):
    """Enum Kodierung Schiffrichtungen"""

    RECHTS = "r"
    LINKS = "l"
    OBEN = "o"
    UNTEN = "u"

    @staticmethod
    def einlesen() -> "Direction":
        """Einlesen Schiffsdaten"""
        print(
            "In welche Richtung soll das Schiff platziert werden?\n r: rechts\n l: links\n o: oben\n u: unten"
        )
        eingabe = str(input("Richtung eingeben: "))
        if eingabe == "l":
            return Direction.LINKS
        if eingabe == "r":
            return Direction.RECHTS
        if eingabe == "o":
            return Direction.OBEN
        if eingabe == "u":
            return Direction.UNTEN

class Schiff:
    """Klasse zur Repräsentierung der Schiffe"""

    def __init__(self, laenge: int, richtung: Direction):
        self.laenge = laenge
        self.richtung = richtung

    @staticmethod
    def einlesen():
        """Einlesen Schiffsdaten"""
        print(
            "Was für ein Schiff soll hinzugefügt werden?\n 1: 1er Schiff\n 2: 2er Schiff\n 3: 3er Schiff\n 4: 4er Schiff"
        )
        self.laenge = int(input("Zahl eingeben: "))

        self.richtung = Direction.einlesen()
