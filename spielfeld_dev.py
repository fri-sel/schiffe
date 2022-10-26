"""Spielfeld"""
import sys
import time
from enum import Enum
from random import randint
from typing import List, Tuple

from colors import bcolors
from direction import Direction
from schiffe import Schiff, letters_to_numbers


# from schiessen import Schuss
class State(Enum):
    """Enum Kodierung Spielfeldzeilen"""

    WASSER = 0
    SCHIFF = 1
    BESCHOSSEN = 2
    GETROFFEN = 3


class Statistics:
    rounds: int = 0
    ships_hitted: int = 0
    missed_shots: int = 0


class Settings:
    ship_anz: int = 1


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

    def check_if_free(self, x: int, y: int) -> bool:
        """Check ob Schiff bereits am Ort"""
        return self.data[x][y] == State.WASSER

    def is_in_field(self, posx, posy) -> bool:
        """Check ob Schiff im Feld platziert wird"""
        if posx < 0 or posx > self.breite:
            raise IndexError(
                f"\n{bcolors.RED}-> Schiff konnte nicht erstellt werden{bcolors.RESET}\n"
            )
        if posy < 0 or posy > self.hoehe:
            raise IndexError(
                f"\n{bcolors.RED}-> Schiff konnte nicht erstellt werden{bcolors.RESET}\n"
            )
        return True

    def berechne_positionen(self, ship, posx, posy) -> List[Tuple[int, int]]:
        """Positionen berechnen für Schiffsplatzierung"""
        posx -= 1
        posy -= 1
        positions = []

        for i in range(ship.laenge):
            if Direction.LINKS == ship.richtung:
                x = posx - i
                y = posy
            if Direction.RECHTS == ship.richtung:
                x = posx + i
                y = posy
            if Direction.OBEN == ship.richtung:
                x = posx
                y = posy - i
            if Direction.UNTEN == ship.richtung:
                x = posx
                y = posy + i

            if self.is_in_field(x, y):
                positions.append((x, y))
            else:
                raise IndexError(
                    f"\n{bcolors.RED}Fehler: Schiff kann nicht außerhalb des Feldes platziert werden!\n{bcolors.RESET}\n"
                )
        return positions

    def add_ship(self, ship: Schiff, posx: int, posy: int):
        """Schiffe an einer Position adden"""

        positions = self.berechne_positionen(ship, posx, posy)

        for position in positions:
            if not self.check_if_free(*position):
                raise IndexError(
                    f"\n{bcolors.RED}Fehler: An der Stelle ist bereits ein Schiff{bcolors.RESET}\n"
                )

        for x, y in positions:
            self.data[x][y] = State.SCHIFF

    def auto_add_ships(self):
        """Computer added Schiffe an zufälligen Positionen"""
        anz = Settings.ship_anz
        success = 0

        while success != anz:
            try:
                feld1.auto_create_ship()
                success += 1
            except:
                pass

    def lese_position(self):
        """Einlesen einer Position"""

        print(
            f"{bcolors.UNDERLINE}Wo soll das Schiff platziert werden?{bcolors.RESET}"
        )
        eingabe = str(input("Y-Pos (Buchstabe) eingeben: "))

        y = letters_to_numbers[eingabe]

        eingabe = int(input("X-Pos (Zahl) eingeben: "))

        x = eingabe

        if not self.is_in_field(x, y):
            raise KeyError(
                f"\n{bcolors.RED}Fehler: Ungültige Position angegeben{bcolors.RESET}\n"
            )

        return (x, y)

    def create_ship(self):
        """Schiffe zusammenstellen"""

        schiff = Schiff(Schiff.einlesen(), Direction.einlesen())
        try:
            x, y = self.lese_position()
            feld1.add_ship(schiff, x, y)
        except Exception as e:
            raise RuntimeError(
                f"\n{bcolors.RED}Fehler: Schiff konnte nicht erstellt werden{bcolors.RESET}\n"
            ) from e

    def auto_create_ship(self):
        """Schiffe random zusammenstellen durch Computer"""
        randLength = randint(1, 4)
        randNr = randint(1, 4)
        if randNr == 1:
            randDirection = Direction.RECHTS
        elif randNr == 2:
            randDirection = Direction.LINKS
        elif randNr == 3:
            randDirection = Direction.OBEN
        elif randNr == 4:
            randDirection = Direction.UNTEN

        schiff = Schiff(randLength, randDirection)
        try:
            x = randint(1, 10)
            y = randint(1, 10)
            feld1.add_ship(schiff, x, y)
        except Exception as e:
            raise RuntimeError(
                f"\n{bcolors.RED}Fehler: Schiff konnte nicht erstellt werden{bcolors.RESET}\n"
            ) from e

    def shoot_x(self) -> int:
        """Einlesen X-Position Schuss"""
        eingabe = int(input("X-Pos (Zahl) eingeben: "))

        if eingabe < 1 or eingabe > self.breite:
            raise KeyError(
                f"{bcolors.RED}Fehler: Ungültige Länge angegeben{bcolors.RESET}"
            )

        return eingabe

    def shoot_y(self) -> int:
        """Einlesen Y-Position Schuss"""
        print(
            f"{bcolors.UNDERLINE}Wohin soll geschossen werden?{bcolors.RESET}"
        )
        eingabe = str(input("Y-Pos (Buchstabe) eingeben: "))

        return letters_to_numbers[eingabe]

    def single_shot(self):
        """Einzelner Schuss auf Map"""

        y = self.shoot_y() - 1
        x = self.shoot_x() - 1

        if self.data[x][y] == State.SCHIFF:
            self.data[x][y] = State.GETROFFEN
            print(f"\n{bcolors.GREEN}-> Treffer!{bcolors.RESET}\n")
            Statistics.ships_hitted += 1
        elif self.data[x][y] == State.GETROFFEN:
            self.data[x][y] = State.GETROFFEN
            Statistics.missed_shots += 1
            print(
                f"\n{bcolors.RED}-> Du hast dieses Schiff bereits getroffen!{bcolors.RESET}\n"
            )
        elif self.data[x][y] == State.BESCHOSSEN:
            Statistics.missed_shots += 1
            print(
                f"\n{bcolors.RED}-> Du hast hier bereits hingezielt!{bcolors.RESET}\n"
            )
        else:
            self.data[x][y] = State.BESCHOSSEN
            Statistics.missed_shots += 1
            print(
                f"\n{bcolors.YELLOW}-> Du hast ins Wasser getroffen...{bcolors.RESET}\n"
            )

    def auto_shooter(self):
        """Automatisch random Schüsse auf Map"""

        x = randint(1, 10) - 1
        y = randint(1, 10) - 1

        if self.data[x][y] == State.SCHIFF:
            self.data[x][y] = State.GETROFFEN
            Statistics.ships_hitted += 1
        elif self.data[x][y] == State.GETROFFEN:
            self.data[x][y] = State.GETROFFEN
            Statistics.missed_shots += 1
        else:
            self.data[x][y] = State.BESCHOSSEN
            Statistics.missed_shots += 1
        Statistics.rounds += 1
        feld1.print_field()

    def print_menu(self):
        eingabe = 0
        print(
            f"{bcolors.TUERKIS_UNDERLINE_BOLD}WILLKOMMEN BEI SCHIFFE VERSENKEN{bcolors.RESET}\n"
        )
        print(
            f"{bcolors.BOLD}[1] Singleplayer\n[2] Spielvorführung\n[3] Anleitung\n[4] Einstellungen\n{bcolors.RESET}\n"
        )

        eingabe = int(
            input(f"{bcolors.BOLD}Wählen sie eine Option: {bcolors.RESET}")
        )
        if eingabe == 1:
            feld1.game_normal_run()
            print(
                f"{bcolors.BOLD}\n[1] Zurück zum Menü\n[2] Beenden{bcolors.RESET}\n"
            )
            ende_auswahl = int(
                input(f"{bcolors.BOLD}Wählen sie eine Option: {bcolors.RESET}")
            )
            if ende_auswahl == 1:
                feld1.clear_Field()
                feld1.print_menu()
            else:
                sys.exit()

        elif eingabe == 2:
            feld1.game_speedrun()
            print(
                f"{bcolors.BOLD}\n[1] Zurück zum Menü\n[2] Beenden{bcolors.RESET}\n"
            )
            ende_auswahl = int(
                input(f"{bcolors.BOLD}Wählen sie eine Option: {bcolors.RESET}")
            )
            if ende_auswahl == 1:
                feld1.clear_Field()
                feld1.print_menu()
            else:
                sys.exit()

        elif eingabe == 3:
            print("folgt")

        elif eingabe == 4:
            Settings.ship_anz = input(
                f"{bcolors.BOLD}Anzahl der Schiffe eingeben: {bcolors.RESET}"
            )
            print("Fehler fixen")

        else:
            raise KeyError(
                f"{bcolors.RED}Fehler: Ungültige Auswahl{bcolors.RESET}"
            )

    def print_field(self):
        """Ausgeben des Feldes und setzen der Schiffe"""

        print("+ 1 2 3 4 5 6 7 8 9 10")

        assert self.hoehe == 10
        for y, label in enumerate("ABCDEFGHIJ"):
            print(label + " ", end="")

            for x in range(self.breite):
                if self.data[x][y] == State.WASSER:
                    print(f"{bcolors.BLUE_BG}〰️{bcolors.RESET}", end="")
                elif self.data[x][y] == State.SCHIFF:
                    print(f"{bcolors.BLUE_BG}🚢{bcolors.RESET}", end="")
                elif self.data[x][y] == State.BESCHOSSEN:
                    print(f"{bcolors.BLUE_BG}  {bcolors.RESET}", end="")
                elif self.data[x][y] == State.GETROFFEN:
                    print(f"{bcolors.BLUE_BG}❌{bcolors.RESET}", end="")
            print("")
        print("\n")

    def clear_Field(self):
        """Leeren des Feldes (Alles zu Wasser)"""
        for y in range(self.hoehe):
            for x in range(self.breite):
                self.data[x][y] = State.WASSER
        feld1.reset_statistics()

    def reset_statistics(self):
        Statistics.rounds = 0
        Statistics.missed_shots = 0
        Statistics.ships_hitted = 0

    def print_statistics(self):

        print("Schüsse Gesamt:", Statistics.rounds)
        print("Treffer bei Schiffen:", Statistics.ships_hitted)
        print("Verfehlte Schüsse:", Statistics.missed_shots)

    def victory_check(self):
        """Checken ob alle Schiffe versenkt wurden"""
        for y in range(self.hoehe):
            for x in range(self.breite):
                if self.data[x][y] == State.SCHIFF:
                    return 1
        print(
            f"{bcolors.TUERKIS_UNDERLINE}Glückwunsch - Du hast alle Schiffe versenkt!{bcolors.RESET}"
        )
        feld1.print_statistics()
        return 0

    def game_speedrun(self):
        """Schnelldurchlauf des Spiels zum Testen"""
        print(
            f"{bcolors.BOLD_UNDERLINE}Schiffe versenken: Spielvorführung{bcolors.RESET}\n"
        )
        feld1.auto_add_ships()
        feld1.print_field()
        time.sleep(3)
        while feld1.victory_check() != 0:
            feld1.auto_shooter()
            time.sleep(0.5)

    def game_normal_run(self):
        """Normaler Ablauf des Spiels bis Sieg"""
        print(
            f"{bcolors.BOLD_UNDERLINE}Schiffe versenken: Singleplayer{bcolors.RESET}\n"
        )
        feld1.auto_add_ships()
        feld1.print_field()
        while feld1.victory_check() != 0:
            feld1.single_shot()
            Statistics.rounds += 1
            feld1.print_field()


# Spielfeld erstellen
feld1 = Spielfeld(10, 10)
# feld1.change_field(5, 5)

# Schiffe per Code adden und platzieren
schiff1 = Schiff(2, Direction.LINKS)
schiff2 = Schiff(2, Direction.RECHTS)
schiff3 = Schiff(3, Direction.OBEN)
schiff4 = Schiff(3, Direction.UNTEN)
schiff5 = Schiff(4, Direction.OBEN)

# feld1.add_ship(schiff1, 8, 8)
# feld1.add_ship(schiff2, 2, 2)
# feld1.add_ship(schiff3, 10, 10)
# feld1.add_ship(schiff4, 8, 2)
# feld1.add_ship(schiff5, 5, 9)

# Schiffe per Nutzereingabe erstellen und platzieren
# feld1.create_ship()
# feld1.auto_add_ships()

# Ausgabe Feld
# feld1.print_field()

# Schießen
# feld1.single_shot()
# feld1.auto_shooter()

# Spielablauf und Ende
# feld1.game_speedrun()
# feld1.game_normal_run()

# Menü printen
feld1.print_menu()
