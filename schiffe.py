"""Schiffe"""

from enum import Enum

from colors import bcolors
from direction import Direction
from schiessen import letters_to_numbers


class Schiff:
    """Klasse zur Repräsentierung der Schiffe"""

    def __init__(self, laenge: int, richtung: Direction):
        self.laenge = laenge
        self.richtung = richtung

    @staticmethod
    def einlesen() -> int:
        """Einlesen Schiffslänge"""
        ask_ship_lenght = True
        while ask_ship_lenght:
            print(
                f"{bcolors.UNDERLINE}Was für ein Schiff soll hinzugefügt werden?{bcolors.RESET}\n 1: 1er Schiff\n 2: 2er Schiff\n 3: 3er Schiff\n 4: 4er Schiff"
            )
            eingabe = input("Schifflänge eingeben: ")
            try:
                if int(eingabe) > 0 and int(eingabe) < 5:
                    ask_ship_lenght = False
                    break
                print(f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}")
                continue
            except ValueError:
                print(f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}")

        return int(eingabe)

    def posy(self) -> int:
        """Einlesen Y-Position Schiff"""

        while True:
            print(
                f"{bcolors.UNDERLINE}Wo soll das Schiff platziert werden?{bcolors.RESET}\n"
            )
            eingabe = str(input("Y-Pos (Buchstabe) eingeben: ")).upper()
            if eingabe in "ABCDEFGHIJ":
                break
            else:
                print(f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}")
                continue

        return letters_to_numbers[eingabe] - 1

    def posx(self) -> int:
        """Einlesen X-Position Schiff"""

        while True:
            eingabe = int(input("X-Pos (Zahl) eingeben: "))
            if eingabe > 0 and eingabe <= 10:
                break
            else:
                print(f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}")
                continue

        return eingabe - 1
