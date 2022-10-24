from random import randint

board = []

for x in range(10):
    board.append(["O"] * 10)

def ausgabe(board):
    for row in board:
        print((" ").join(row))

print("Let's play Battleship!")
ausgabe(board)

def random_x(board):
    return randint(0, len(board) - 1)
def random_y(board):
    return randint(0, len(board[0]) - 1)


schiff_x = random_x(board)
schiff_y = random_y(board)

print(schiff_x, schiff_y)

for turn in range(9):
    print ("Versuch"), turn
    rate_x = int(input("X Werte 1-10:"))
    rate_y = int(input("Y Werte 1-10:"))

    if rate_x == schiff_x and rate_y == schiff_y:
        print("Schiff getroffen!")
        break
    else:
        if (rate_x < 0 or rate_x > 9) or (rate_y < 0 or rate_y > 9):
            print("Vieeeeeel zu weit daneben.")
        elif(board[rate_x][rate_y] == "X"):
            print("Da hast du schon hingeschossen.")
        else:
            print("Du hast kein Schiff getroffen!")
            board[rate_x][rate_y] = "X"
    if turn == 8:
        print("Game Over")
    turn =+ 1
    ausgabe(board)
