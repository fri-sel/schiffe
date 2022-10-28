"""Schiffe"""

from enum import Enum

from colors import bcolors
from direction import Direction
from schiessen import letters_to_numbers


# from typing import List, Tuple
class Schiff:
    """Klasse zur Repräsentierung der Schiffe"""

    def __init__(self, laenge: int, richtung: Direction):
        self.laenge = laenge
        self.richtung = richtung

    @staticmethod
    def einlesen() -> int:
        """Einlesen Schiffslänge"""
        print(
            f"{bcolors.UNDERLINE}Was für ein Schiff soll hinzugefügt werden?{bcolors.RESET}\n 1: 1er Schiff\n 2: 2er Schiff\n 3: 3er Schiff\n 4: 4er Schiff"
        )
        eingabe = int(input("Schifflänge eingeben: "))
        if eingabe < 1 or eingabe > 4:
            raise KeyError(
                f"{bcolors.RED}Fehler: Ungültige Länge angegeben{bcolors.RESET}"
            )

        return eingabe

    def posy(self) -> int:
        """Einlesen Y-Position Schiff"""
        print(
            f"{bcolors.UNDERLINE}Wo soll das Schiff platziert werden?{bcolors.RESET}\n"
        )
        eingabe = str(input("Y-Pos (Buchstabe) eingeben: "))
        if not isinstance(eingabe, str):
            raise KeyError(
                f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}"
            )
        return letters_to_numbers[eingabe] - 1

    def posx(self) -> int:
        """Einlesen X-Position Schiff"""
        eingabe = int(input("X-Pos (Zahl) eingeben: "))
        if not isinstance(eingabe, int):
            raise KeyError(
                f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}"
            )
        return eingabe - 1
