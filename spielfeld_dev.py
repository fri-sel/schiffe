"""Spielfeld"""
import os
import re
import sys
import time
from enum import Enum
from multiprocessing.sharedctypes import Value
from random import randint
from typing import List, Tuple

from colors import bcolors
from direction import Direction
from schiessen import letters_to_numbers, numbers_to_letters
from schiffe import Schiff

clear = lambda: os.system("clear")

# from schiessen import Schuss
class State(Enum):
    """Enum Kodierung Spielfeldzeilen"""

    WASSER = 0
    SCHIFF = 1
    BESCHOSSEN = 2
    GETROFFEN = 3


class Statistics:
    rounds: int = 0
    rounds_player1: int = 0
    rounds_player2: int = 0
    ships_hitted: int = 0
    ships_hitted_player1: int = 0
    ships_hitted_player2: int = 0
    missed_shots: int = 0
    missed_shots_player1: int = 0
    missed_shots_player2: int = 0
    last_x: int = 0
    last_y: int = 0


class Settings:
    ship_anz: int = 5
    animation_time: float = 0.5
    difficulty: int = 1
    modus: int = 1
    treffer: list = []


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

    def remove_ship(self, ship: Schiff, posx: int, posy: int):
        """Schiffe an einer Position löschen"""

        positions = self.berechne_positionen(ship, posx, posy)

        for position in positions:
            if self.check_if_free(*position):
                raise IndexError(
                    f"\n{bcolors.RED}Fehler: An der Stelle ist bereits ein Schiff{bcolors.RESET}\n"
                )

        for x, y in positions:
            self.data[x][y] = State.WASSER

    def auto_add_ships(self):
        """Computer added Schiffe an zufälligen Positionen"""
        anz = Settings.ship_anz
        success = 0

        while success != anz:
            try:
                self.auto_create_ship()
                success += 1
            except:
                pass

    def auto_add_ships_on_both_maps(self):
        """Computer added Schiffe an zufälligen Positionen auf beiden Feldern"""
        anz = Settings.ship_anz
        success = 0

        while success != anz:
            try:
                self.auto_create_ships_on_both_maps()
                success += 1
            except:
                pass

    def lese_position(self):
        """Einlesen einer Position"""

        print(
            f"{bcolors.UNDERLINE}Wo soll das Schiff platziert werden?{bcolors.RESET}"
        )
        eingabe = str(input("Y-Pos (Buchstabe) eingeben: "))

        y = letters_to_numbers[eingabe.upper()]

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
            self.add_ship(schiff, x, y)
        except Exception as e:
            raise RuntimeError(
                f"\n{bcolors.RED}Fehler: Schiff konnte nicht erstellt werden{bcolors.RESET}\n"
            ) from e

    def create_ships_on_both_maps(self):
        """Schiffsdaten kopieren und random auf Feld 2 platzieren"""
        randNr = randint(1, 4)
        if randNr == 1:
            randDirection = Direction.RECHTS
        elif randNr == 2:
            randDirection = Direction.LINKS
        elif randNr == 3:
            randDirection = Direction.OBEN
        elif randNr == 4:
            randDirection = Direction.UNTEN

        randx = randint(1, 10)
        randy = randint(1, 10)

        schiff1 = Schiff(Schiff.einlesen(), Direction.einlesen())
        schiff2 = Schiff(schiff1.laenge, randDirection)

        try:
            x, y = self.lese_position()
            feld1.add_ship(schiff1, x, y)
            feld2.add_ship(schiff2, randx, randy)
        except:
            feld1.remove_ship(schiff1, x, y)
            pass

    def place_ships_on_both_maps_manually(self):
        """Schiffsdaten kopieren und Schiffe nacheinander auf beiden Feldern per Hand platzieren"""
        length = Schiff.einlesen()
        print(
            f"{bcolors.TUERKIS}Spieler 1 - Platziere Schiff:{bcolors.RESET}\n"
        )

        try:
            schiff1 = Schiff(length, Direction.einlesen())
            x, y = self.lese_position()
            feld1.add_ship(schiff1, x, y)
        except:
            pass

        try:
            print(
                f"{bcolors.TUERKIS}Spieler 2 - Platziere Schiff:{bcolors.RESET}\n"
            )
            schiff2 = Schiff(length, Direction.einlesen())
            x, y = self.lese_position()
            feld2.add_ship(schiff2, x, y)
        except:
            feld1.remove_ship(schiff1, x, y)
            feld2.remove_ship(schiff2, x, y)
            pass

    def auto_create_ships_on_both_maps(self):
        """Schiffsdaten kopieren und random auf Feld 2 platzieren"""
        randLength = randint(1, 4)
        randNr = randint(1, 4)
        if randNr == 1:
            randDirection1 = Direction.RECHTS
        elif randNr == 2:
            randDirection1 = Direction.LINKS
        elif randNr == 3:
            randDirection1 = Direction.OBEN
        elif randNr == 4:
            randDirection1 = Direction.UNTEN

        randNr2 = randint(1, 4)
        if randNr2 == 1:
            randDirection2 = Direction.RECHTS
        elif randNr2 == 2:
            randDirection2 = Direction.LINKS
        elif randNr2 == 3:
            randDirection2 = Direction.OBEN
        elif randNr2 == 4:
            randDirection2 = Direction.UNTEN

        schiff1 = Schiff(randLength, randDirection1)
        schiff2 = Schiff(schiff1.laenge, randDirection2)

        randx1 = randint(1, 10)
        randy1 = randint(1, 10)
        randx2 = randint(1, 10)
        randy2 = randint(1, 10)

        try:
            feld1.add_ship(schiff1, randx1, randy1)
            feld2.add_ship(schiff2, randx2, randy2)

        except Exception as e:
            feld1.remove_ship(schiff1, randx1, randy1)
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
            self.add_ship(schiff, x, y)
        except Exception as e:
            raise RuntimeError(
                f"\n{bcolors.RED}Fehler: Schiff konnte nicht erstellt werden{bcolors.RESET}\n"
            ) from e

    def set_all_ship(self):
        for y in range(self.hoehe):
            for x in range(self.breite):
                self.data[x][y] = State.SCHIFF

    def shoot_x(self) -> int:
        """Einlesen X-Position Schuss"""

        while True:
            eingabe = input("X-Pos (Zahl) eingeben: ")
            try:
                if int(eingabe) > 0 and int(eingabe) <= 10:
                    break
                print(f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}")
                continue
            except ValueError:
                print(f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}")
        return int(eingabe)

    def shoot_y(self) -> int:
        """Einlesen Y-Position Schuss"""
        while True:
            print(
                f"{bcolors.UNDERLINE}Wohin soll geschossen werden?{bcolors.RESET}"
            )
            eingabe = str(input("Y-Pos (Buchstabe) eingeben: ")).upper()
            if eingabe in "ABCDEFGHIJ":
                break

            print(f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}")
            continue

        return letters_to_numbers[eingabe]

    def single_shot(self):
        """Einzelner Schuss auf Map"""

        y = self.shoot_y() - 1
        x = self.shoot_x() - 1

        Statistics.last_x = x + 1
        Statistics.last_y = numbers_to_letters[y + 1]

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

    def auto_shooter_normal(self):
        """Automatisch random Schüsse auf Map"""
        time.sleep(Settings.animation_time)
        x = randint(1, 10) - 1
        y = randint(1, 10) - 1

        while (x, y) in Settings.treffer:
            x = randint(1, 10) - 1
            y = randint(1, 10) - 1

        if self.data[x][y] == State.SCHIFF:
            self.data[x][y] = State.GETROFFEN
            print(f"\n{bcolors.GREEN}-> Treffer!{bcolors.RESET}\n")
            Statistics.ships_hitted += 1
        elif self.data[x][y] == State.GETROFFEN:
            self.data[x][y] = State.GETROFFEN
            print(
                f"\n{bcolors.RED}-> Dieses Schiff wurde bereits getroffen!{bcolors.RESET}\n"
            )
            Statistics.missed_shots += 1
        else:
            self.data[x][y] = State.BESCHOSSEN
            Statistics.missed_shots += 1
            print(
                f"\n{bcolors.YELLOW}-> Ins Wasser getroffen...{bcolors.RESET}\n"
            )

        Statistics.rounds += 1
        Settings.treffer.append((x, y))
        self.print_field()
        print(
            f"{bcolors.UNDERLINE}Letzter Schuss:{bcolors.RESET} {numbers_to_letters[y + 1]}{x + 1}\n"
        )

    def auto_shooter_medium(self):
        """Automatisch random Schüsse auf Map"""
        time.sleep(Settings.animation_time)
        x = randint(1, 10) - 1
        y = randint(1, 10) - 1

        while self.data[x][y] != State.SCHIFF:
            extra_shot = randint(1, 100)
            if extra_shot >= 11:
                x = randint(1, 10) - 1
                y = randint(1, 10) - 1
            else:
                break
        while (x, y) in Settings.treffer:
            x = randint(1, 10) - 1
            y = randint(1, 10) - 1

        if self.data[x][y] == State.SCHIFF:
            self.data[x][y] = State.GETROFFEN
            print(f"\n{bcolors.GREEN}-> Treffer!{bcolors.RESET}\n")
            Statistics.ships_hitted += 1
        elif self.data[x][y] == State.GETROFFEN:
            self.data[x][y] = State.GETROFFEN
            print(
                f"\n{bcolors.RED}-> Dieses Schiff wurde bereits getroffen!{bcolors.RESET}\n"
            )
            Statistics.missed_shots += 1
        else:
            self.data[x][y] = State.BESCHOSSEN
            Statistics.missed_shots += 1
            print(
                f"\n{bcolors.YELLOW}-> Ins Wasser getroffen...{bcolors.RESET}\n"
            )

        Settings.treffer.append((x, y))
        Statistics.rounds += 1
        self.print_field()
        print(
            f"{bcolors.UNDERLINE}Letzter Schuss:{bcolors.RESET} {numbers_to_letters[y + 1]}{x + 1}\n"
        )

    def auto_shooter_hard(self):
        """Automatisch random Schüsse auf Map"""
        time.sleep(Settings.animation_time)

        x = randint(1, 10) - 1
        y = randint(1, 10) - 1

        while self.data[x][y] != State.SCHIFF:
            extra_shot = randint(1, 100)
            if extra_shot >= 8:
                x = randint(1, 10) - 1
                y = randint(1, 10) - 1
            else:
                break

        while (x, y) in Settings.treffer:
            x = randint(1, 10) - 1
            y = randint(1, 10) - 1

        if self.data[x][y] == State.SCHIFF:
            self.data[x][y] = State.GETROFFEN
            print(f"\n{bcolors.GREEN}-> Treffer!{bcolors.RESET}\n")
            Statistics.ships_hitted += 1
        elif self.data[x][y] == State.GETROFFEN:
            self.data[x][y] = State.GETROFFEN
            print(
                f"\n{bcolors.RED}-> Dieses Schiff wurde bereits getroffen!{bcolors.RESET}\n"
            )
            Statistics.missed_shots += 1
        else:
            self.data[x][y] = State.BESCHOSSEN
            Statistics.missed_shots += 1
            print(
                f"\n{bcolors.YELLOW}-> Ins Wasser getroffen...{bcolors.RESET}\n"
            )

        Settings.treffer.append((x, y))
        Statistics.rounds += 1
        self.print_field()
        print(
            f"{bcolors.UNDERLINE}Letzter Schuss:{bcolors.RESET} {numbers_to_letters[y + 1]}{x + 1}\n"
        )

    def print_menu(self):
        ask_menu_option = True
        while ask_menu_option:
            eingabe = 0
            print(
                f"{bcolors.TUERKIS_UNDERLINE_BOLD}WILLKOMMEN BEI SCHIFFE VERSENKEN{bcolors.RESET}\n"
            )
            print(
                f"{bcolors.BOLD}[1] Singleplayer\n[2] Player vs. Bot\n[3] Player vs. Player\n[4] Sandkasten-Modus\n[5] Spielvorführung\n[6] Anleitung\n[7] Einstellungen\n[8] Beenden\n{bcolors.RESET}\n"
            )

            Settings.modus = input(
                f"{bcolors.BOLD}Wählen sie eine Option: {bcolors.RESET}"
            )
            try:
                Settings.modus = int(Settings.modus)
                if Settings.modus == 1:
                    self.game_normal_run()
                    ask_end_game = True
                    while ask_end_game:
                        print(
                            f"{bcolors.BOLD}\n[1] Zurück zum Menü\n[2] Beenden{bcolors.RESET}\n"
                        )
                        ende_auswahl = int(
                            input(
                                f"{bcolors.BOLD}Wählen sie eine Option: {bcolors.RESET}"
                            )
                        )
                        try:
                            if int(ende_auswahl) > 0 and int(ende_auswahl) <= 2:
                                if int(ende_auswahl) == 1:
                                    ask_end_game = False
                                    self.clear_Field()
                                    self.print_menu()
                                elif int(ende_auswahl) == 2:
                                    ask_end_game = False
                                    break
                                print(
                                    f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}"
                                )
                                continue
                            print(
                                f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}"
                            )
                            continue
                        except:
                            print(
                                f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}"
                            )
                            continue
                    ask_menu_option = False

                elif Settings.modus == 2:
                    feld1.game_player_vs_bot()
                    ask_end_game = True
                    while ask_end_game:
                        print(
                            f"{bcolors.BOLD}\n[1] Zurück zum Menü\n[2] Beenden{bcolors.RESET}\n"
                        )
                        ende_auswahl = input(
                            f"{bcolors.BOLD}Wählen sie eine Option: {bcolors.RESET}"
                        )

                        try:
                            if int(ende_auswahl) > 0 and int(ende_auswahl) <= 2:
                                if int(ende_auswahl) == 1:
                                    ask_end_game = False
                                    self.clear_Field()
                                    self.print_menu()
                                elif int(ende_auswahl) == 2:
                                    ask_end_game = False
                                    break
                                print(
                                    f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}"
                                )
                                continue
                            print(
                                f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}"
                            )
                            continue
                        except:
                            print(
                                f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}"
                            )
                            continue
                    ask_menu_option = False

                elif Settings.modus == 3:
                    feld1.game_player_vs_player()
                    ask_end_game = True
                    while ask_end_game:
                        print(
                            f"{bcolors.BOLD}\n[1] Zurück zum Menü\n[2] Beenden{bcolors.RESET}\n"
                        )
                        ende_auswahl = input(
                            f"{bcolors.BOLD}Wählen sie eine Option: {bcolors.RESET}"
                        )

                        try:
                            if int(ende_auswahl) > 0 and int(ende_auswahl) <= 2:
                                if int(ende_auswahl) == 1:
                                    ask_end_game = False
                                    self.clear_Field()
                                    self.print_menu()
                                elif int(ende_auswahl) == 2:
                                    ask_end_game = False
                                    break
                                print(
                                    f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}"
                                )
                                continue
                            print(
                                f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}"
                            )
                            continue
                        except:
                            print(
                                f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}"
                            )
                            continue
                    ask_menu_option = False

                elif Settings.modus == 4:
                    self.game_sandbox_mode()
                    ask_end_game = True
                    while ask_end_game:
                        print(
                            f"{bcolors.BOLD}\n[1] Zurück zum Menü\n[2] Beenden{bcolors.RESET}\n"
                        )
                        ende_auswahl = input(
                            f"{bcolors.BOLD}Wählen sie eine Option: {bcolors.RESET}"
                        )

                        try:
                            if int(ende_auswahl) > 0 and int(ende_auswahl) <= 2:
                                if int(ende_auswahl) == 1:
                                    ask_end_game = False
                                    self.clear_Field()
                                    self.print_menu()
                                elif int(ende_auswahl) == 2:
                                    ask_end_game = False
                                    break
                                print(
                                    f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}"
                                )
                                continue
                            print(
                                f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}"
                            )
                            continue
                        except:
                            print(
                                f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}"
                            )
                            continue
                    ask_menu_option = False

                elif Settings.modus == 5:
                    self.game_speedrun()
                    ask_end_game = True
                    while ask_end_game:
                        print(
                            f"{bcolors.BOLD}\n[1] Zurück zum Menü\n[2] Beenden{bcolors.RESET}\n"
                        )
                        ende_auswahl = input(
                            f"{bcolors.BOLD}Wählen sie eine Option: {bcolors.RESET}"
                        )

                        try:
                            if int(ende_auswahl) > 0 and int(ende_auswahl) <= 2:
                                if int(ende_auswahl) == 1:
                                    ask_end_game = False
                                    self.clear_Field()
                                    self.print_menu()
                                elif int(ende_auswahl) == 2:
                                    ask_end_game = False
                                    break
                                print(
                                    f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}"
                                )
                                continue
                            print(
                                f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}"
                            )
                            continue
                        except:
                            print(
                                f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}"
                            )
                            continue
                    ask_menu_option = False

                elif Settings.modus == 6:
                    anleitung = open("anleitung.html")
                    for line in anleitung:
                        print(line.rstrip())
                    anleitung.close()
                    ask_end_game = True
                    while ask_end_game:
                        print(
                            f"{bcolors.BOLD}\n[1] Zurück zum Menü\n[2] Beenden{bcolors.RESET}\n"
                        )
                        ende_auswahl = input(
                            f"{bcolors.BOLD}Wählen sie eine Option: {bcolors.RESET}"
                        )

                        try:
                            if int(ende_auswahl) > 0 and int(ende_auswahl) <= 2:
                                if int(ende_auswahl) == 1:
                                    ask_end_game = False
                                    self.clear_Field()
                                    self.print_menu()
                                elif int(ende_auswahl) == 2:
                                    ask_end_game = False
                                    break
                                print(
                                    f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}"
                                )
                                continue
                            print(
                                f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}"
                            )
                            continue
                        except:
                            print(
                                f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}"
                            )
                            continue
                    ask_menu_option = False

                elif Settings.modus == 7:
                    option = 0
                    print(
                        f"{bcolors.BOLD}[1] Anzahl Schiffe\n[2] Animationsgeschwindigkeit\n[3] Bot Schwierigkeit{bcolors.RESET}\n"
                    )
                    option = int(
                        input(
                            f"{bcolors.TUERKIS}Einstellung wählen: {bcolors.RESET}"
                        )
                    )

                    if option == 1:
                        anz = int(
                            input(
                                f"{bcolors.BOLD}Anzahl der Schiffe eingeben: {bcolors.RESET}"
                            )
                        )
                        Settings.ship_anz = anz
                        self.print_menu()
                    if option == 2:
                        ani_time = float(
                            input(
                                f"{bcolors.BOLD}Animationsgeschwindigkeit: {bcolors.RESET}"
                            )
                        )
                        Settings.animation_time = ani_time
                        self.print_menu()
                    if option == 3:
                        print(
                            f"{bcolors.BOLD}[1] Einfach\n[2] Mittel\n[3] Schwer{bcolors.RESET}"
                        )
                        difficulty = int(
                            input(
                                f"{bcolors.BOLD}Bot Schwierigkeit wählen: {bcolors.RESET}"
                            )
                        )
                        Settings.difficulty = difficulty
                    else:
                        break

                elif Settings.modus == 8:
                    ask_menu_option = False

                else:
                    raise ValueError(
                        f"{bcolors.RED}Fehler: Ungültige Auswahl{bcolors.RESET}"
                    )
            except ValueError:
                print(f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}")
        sys.exit()

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

    def clear_Field(self):
        """Leeren des Feldes (Alles zu Wasser)"""
        for y in range(self.hoehe):
            for x in range(self.breite):
                self.data[x][y] = State.WASSER
        self.reset_statistics()

    def reset_statistics(self):
        Statistics.rounds = 0
        Statistics.rounds_player1 = 0
        Statistics.rounds_player2 = 0
        Statistics.ships_hitted = 0
        Statistics.ships_hitted_player1 = 0
        Statistics.ships_hitted_player2 = 0
        Statistics.missed_shots = 0
        Statistics.missed_shots_player1 = 0
        Statistics.missed_shots_player2 = 0
        Statistics.last_x = 0
        Statistics.last_y = 0
        Settings.treffer.clear()

    def print_statistics(self):

        print("Schüsse Gesamt:", Statistics.rounds)
        print("Treffer bei Schiffen:", Statistics.ships_hitted)
        print("Verfehlte Schüsse:", Statistics.missed_shots)

    def print_statistics_multiplayer(self):
        print(f"{bcolors.BLUE}Spieler Statistiken:{bcolors.RESET}")
        print("Schüsse Gesamt:", Statistics.rounds_player1)
        print("Treffer bei Schiffen:", Statistics.ships_hitted)
        print("Verfehlte Schüsse:", Statistics.missed_shots)

        print(f"\n{bcolors.BLUE}Gegner Statistiken:{bcolors.RESET}")
        print("Schüsse Gesamt:", Statistics.rounds_player2)
        print("Treffer bei Schiffen:", Statistics.ships_hitted)
        print("Verfehlte Schüsse:", Statistics.missed_shots)

    def victory_check(self):
        """Checken ob alle Schiffe versenkt wurden"""
        for y in range(self.hoehe):
            for x in range(self.breite):
                if self.data[x][y] == State.SCHIFF:
                    return 1
        print(
            f"{bcolors.TUERKIS_UNDERLINE}Gewonnen - Du hast alle Schiffe versenkt!{bcolors.RESET}"
        )
        self.print_statistics()
        print(Settings.treffer)
        return 0

    def victory_check_player(self):
        """Checken ob Spieler zuerst alle Schiffe versenkt hat im Multiplayer"""
        for y in range(feld2.hoehe):
            for x in range(feld2.breite):
                if feld2.data[x][y] == State.SCHIFF:
                    return 1

        if Settings.modus == 3:
            print(
                f"{bcolors.TUERKIS_UNDERLINE}Spieler 1 hat gewonnen!{bcolors.RESET}"
            )
        else:
            print(
                f"{bcolors.TUERKIS_UNDERLINE}Gewonnen - Du hast alle Schiffe versenkt!{bcolors.RESET}"
            )

        self.print_statistics_multiplayer()
        return 0

    def victory_check_enemy(self):
        """Checken ob Gegner zuerst alle Schiffe versenkt hat im Multiplayer"""
        for y in range(feld1.hoehe):
            for x in range(feld1.breite):
                if feld1.data[x][y] == State.SCHIFF:
                    return 1
        if Settings.modus == 3:
            print(
                f"{bcolors.TUERKIS_UNDERLINE}Spieler 2 hat gewonnen!{bcolors.RESET}"
            )
        else:
            print(
                f"{bcolors.TUERKIS_UNDERLINE}Gewonnen - Du hast alle Schiffe versenkt!{bcolors.RESET}"
            )

        self.print_statistics_multiplayer()
        return 0

    def game_speedrun(self):
        """Schnelldurchlauf des Spiels zum Testen"""
        print(
            f"{bcolors.BOLD_UNDERLINE}Schiffe versenken: Spielvorführung{bcolors.RESET}\n"
        )
        self.auto_add_ships()
        self.print_field()
        time.sleep(3)
        while self.victory_check() != 0:
            if Settings.difficulty == 1:
                self.auto_shooter_normal()
            if Settings.difficulty == 2:
                self.auto_shooter_medium()
            if Settings.difficulty == 3:
                self.auto_shooter_hard()
            time.sleep(Settings.animation_time)

    def game_normal_run(self):
        """Normaler Ablauf des Spiels bis Sieg"""
        print(
            f"{bcolors.BOLD_UNDERLINE}Schiffe versenken: Singleplayer{bcolors.RESET}\n"
        )
        self.auto_add_ships()
        self.print_field()
        while self.victory_check() != 0:
            self.single_shot()
            Statistics.rounds += 1
            self.print_field()
            print(
                f"{bcolors.UNDERLINE}Letzter Schuss:{bcolors.RESET} {Statistics.last_y}{Statistics.last_x}\n"
            )

    def game_sandbox_mode(self):
        """Sandkastenmodus: Selbst Schiffe platzieren"""
        ship_anz = int(
            input(
                f"{bcolors.BOLD}Wie viele Schiffe sollen platziert werden?: {bcolors.RESET}"
            )
        )
        for ship_anz in range(ship_anz):
            self.create_ship()
        print(
            f"{bcolors.BOLD_UNDERLINE}Schiffe versenken: Sandkastenmodus{bcolors.RESET}\n"
        )
        self.print_field()
        while self.victory_check() != 0:
            self.single_shot()
            Statistics.rounds += 1
            self.print_field()
            print(
                f"{bcolors.UNDERLINE}Letzter Schuss:{bcolors.RESET} {Statistics.last_y}{Statistics.last_x}\n"
            )

    def game_player_vs_bot(self):
        """Spieler gegen Computer Spielmodus"""
        ask_way_of_adding_ships = True
        while ask_way_of_adding_ships:
            print(f"{bcolors.BOLD_UNDERLINE}Spielart wählen{bcolors.RESET}\n")
            auswahl = input(
                f"{bcolors.UNDERLINE}Wie sollen die Schiffe platziert werden?{bcolors.RESET}\n[1] Selber hinzufügen\n[2] Automatisch hinzufügen\nEingabe: "
            )
            try:
                if int(auswahl) > 0 and int(auswahl) <= 2:
                    if int(auswahl) == 1:
                        ask_number_ships = True
                        while ask_number_ships:
                            anz = input(
                                f"{bcolors.UNDERLINE}Wie viele Schiffe sollen platziert werden?: {bcolors.RESET}"
                            )
                            try:
                                if int(anz) >= 0 and int(anz) <= 25:
                                    print("Richtige Anzahl ausgewählt!")
                                    anz = int(anz)
                                    Settings.ship_anz = anz
                                    for anz in range(anz):
                                        self.create_ships_on_both_maps()
                                    ask_number_ships = False
                                print(
                                    f"{bcolors.RED}Fehler: Max. 25 Schiffe erlaubt!{bcolors.RESET}"
                                )
                                continue
                            except:
                                print(
                                    f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}"
                                )
                        ask_way_of_adding_ships = False
                    elif int(auswahl) == 2:
                        self.auto_add_ships_on_both_maps()
                        break
                    print(
                        f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}"
                    )
                    continue
                print(f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}")
                continue

            except ValueError:
                print(f"{bcolors.RED}Fehler: Ungültige Eingabe{bcolors.RESET}")
        clear()
        print(
            f"{bcolors.BOLD_UNDERLINE}Schiffe versenken: Spieler vs. Bot{bcolors.RESET}\n"
        )
        print(f"{bcolors.TUERKIS_UNDERLINE}Dein Feld:{bcolors.RESET}\n")
        feld1.print_field()
        print(
            f"\n{bcolors.TUERKIS_UNDERLINE}Gegner Feld (Bot):{bcolors.RESET}\n"
        )
        feld2.print_field()
        time.sleep(5)
        clear()

        while feld2.victory_check() != 0:
            print(f"\n{bcolors.TUERKIS_UNDERLINE}Dein Zug:{bcolors.RESET}\n")
            feld2.print_field()
            feld2.single_shot()
            feld2.print_field()
            print(
                f"{bcolors.UNDERLINE}Letzter Schuss:{bcolors.RESET} {Statistics.last_y}{Statistics.last_x}\n"
            )
            Statistics.rounds_player1 += 1
            time.sleep(5)
            clear()
            if self.victory_check_player() == 0:
                break

            if Settings.difficulty == 1:
                print(
                    f"\n{bcolors.TUERKIS_UNDERLINE}Gegner (Bot) spielt:{bcolors.RESET}\n"
                )
                feld1.print_field()
                feld1.auto_shooter_normal()
                Statistics.rounds_player2 += 1
                time.sleep(7)
                clear()
                if self.victory_check_enemy() == 0:
                    break
            if Settings.difficulty == 2:
                print(
                    f"\n{bcolors.TUERKIS_UNDERLINE}Gegner (Bot) spielt:{bcolors.RESET}\n"
                )
                feld1.print_field()
                feld1.auto_shooter_medium()
                Statistics.rounds_player2 += 1
                time.sleep(7)
                clear()
                if self.victory_check_enemy() == 0:
                    break
            if Settings.difficulty == 3:
                print(
                    f"\n{bcolors.TUERKIS_UNDERLINE}Gegner (Bot) spielt:{bcolors.RESET}\n"
                )
                feld1.print_field()
                feld1.auto_shooter_hard()
                Statistics.rounds_player2 += 1
                time.sleep(7)
                clear()
                if self.victory_check_enemy() == 0:
                    break

    def game_player_vs_player(self):
        """Spieler gegen Spieler Spielmodus"""
        print(f"{bcolors.BOLD_UNDERLINE}Spielart wählen:{bcolors.RESET}\n")
        auswahl = int(
            input(
                f"{bcolors.UNDERLINE}Wie sollen die Schiffe platziert werden?{bcolors.RESET}\n[1] Selber hinzufügen\n[2] Automatisch hinzufügen\nEingabe: "
            )
        )
        if auswahl == 1:
            anz = int(
                input(
                    f"{bcolors.UNDERLINE}Wie viele Schiffe sollen platziert werden?: {bcolors.RESET}"
                )
            )
            Settings.ship_anz = anz
            for anz in range(anz):
                self.place_ships_on_both_maps_manually()
                feld1.print_field()
                feld2.print_field()

        elif auswahl == 2:
            self.auto_add_ships_on_both_maps()

        else:
            raise KeyError(
                f"{bcolors.RED}Fehler: Ungültige Auswahl{bcolors.RESET}"
            )
        clear()
        print(
            f"{bcolors.BOLD_UNDERLINE}Schiffe versenken: Spieler vs. Spieler{bcolors.RESET}\n"
        )
        print(f"{bcolors.TUERKIS_UNDERLINE}Feld Spieler 1:{bcolors.RESET}\n")
        feld1.print_field()
        print(f"\n{bcolors.TUERKIS_UNDERLINE}Feld Spieler 2:{bcolors.RESET}\n")
        feld2.print_field()
        time.sleep(5)
        clear()

        while feld2.victory_check() != 0:
            print(
                f"\n{bcolors.TUERKIS_UNDERLINE}Zug Spieler 1:{bcolors.RESET}\n"
            )
            feld2.print_field()
            feld2.single_shot()
            feld2.print_field()
            print(
                f"{bcolors.UNDERLINE}Letzter Schuss:{bcolors.RESET} {Statistics.last_y}{Statistics.last_x}\n"
            )
            Statistics.rounds_player1 += 1
            time.sleep(5)
            clear()
            if self.victory_check_player() == 0:
                break

            print(
                f"\n{bcolors.TUERKIS_UNDERLINE}Zug Spieler 2:{bcolors.RESET}\n"
            )
            feld1.print_field()
            feld1.single_shot()
            feld1.print_field()
            print(
                f"{bcolors.UNDERLINE}Letzter Schuss:{bcolors.RESET} {Statistics.last_y}{Statistics.last_x}\n"
            )
            Statistics.rounds_player2 += 1
            time.sleep(5)
            clear()
            if self.victory_check_enemy() == 0:
                break


# Spielfeld erstellen
feld1 = Spielfeld(10, 10)
feld2 = Spielfeld(10, 10)
# feld1.change_field(5, 5)

# Schiffe per Code adden und platzieren
# s1 = Schiff(2, Direction.LINKS)
# s2 = Schiff(2, Direction.RECHTS)
# s3 = Schiff(3, Direction.OBEN)
# s4 = Schiff(3, Direction.UNTEN)
# s5 = Schiff(4, Direction.OBEN)

# feld1.add_ship(s1, 8, 8)
# feld1.add_ship(s2, 2, 2)
# feld1.add_ship(s3, 10, 10)
# feld1.add_ship(s4, 8, 2)
# feld1.add_ship(s5, 5, 9)

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
