"""Schiessen"""

from colors import bcolors

letters_to_numbers = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
    "H": 8,
    "I": 9,
    "J": 10,
}

numbers_to_letters = {
    1: "A",
    2: "B",
    3: "C",
    4: "D",
    5: "E",
    6: "F",
    7: "G",
    8: "H",
    9: "I",
    10: "J",
}


class Schuss:
    """Klasse zur Implementierung der Schießfunktionen"""

    def __init__(self, posx: str, posy: int):
        self.posx = posx
        self.posy = posy

    def shoot_x(self) -> int:
        """Einlesen X-Position Schuss"""
        print(f"{bcolors.UNDERLINE}Wohin soll geschossen werden{bcolors.RESET}")
        eingabe = str(input("X-Pos (Buchstabe) eingeben: "))

        return letters_to_numbers[eingabe.upper()]

    def shoot_y(self) -> int:
        """Einlesen Y-Position Schuss"""
        eingabe = int(input("Y-Pos (Zahl) eingeben: "))

        return eingabe
