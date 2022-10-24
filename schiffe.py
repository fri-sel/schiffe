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

letters_to_numbers = {
    'A': 1,
    'B': 2,
    'C': 3,
    'D': 4,
    'E': 5,
    'F': 6,
    'G': 7,
    'H': 8,
    'I': 9,
    'J': 10,
}


class Ship(object):

      def __init__(self,lenght):
        self.lenght = lenght


class Player(object):

  def choose_ship_position() -> None:

    print("Platzieren Sie ein Schiff!")

    column = input("Wählen Sie eine Spalte (A bis J):").upper()
    while column not in "ABCDEFGHIJ":
        print("Sie haben eine ungültige Spalte gewählt.")
        column = input("Wählen Sie eine Spalte (A bis J):").upper()

    row = input("Wählen Sie eine Reihe(1 bis 10):").upper()
    while row not in "12345678910":
        print("Sie haben eine ungültige Reihe gewählt.")
        row = input("Wählen Sie eine Reihe(1 bis 10):").upper()

    return int(row) - 1, letters_to_numbers[column] - 1

def print_board(board):
    # Show the board, one row at a time
    print("  A B C D E")
    print(" +-+-+-+-+-+")
    row_number = 1
    for row in board:
        print("%d|%s|" % (row_number, "|".join(row)))
        print(" +-+-+-+-+-+")
        row_number = row_number + 1


feld1 = Spielfeld(10, 10)
feld1.change_field(0, 0)
feld1.print_field()


for n in range(5):
    print("Platiere Schiff", n + 1,"!")
    row_number, column_number = Player.choose_ship_position()

    if board[row_number][column_number] == 'X':
     print("Hier befindet sich bereits ein Schiff!")

    board[row_number][column_number] = 'X'
    print_board(board)
