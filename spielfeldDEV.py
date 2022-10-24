class Spielfeld(object):
    def __init__(self, hoehe, breite):
        self.hoehe = hoehe
        self.breite = breite

    def changeField(self, posx, posy):
        return 0

    def printField(self, hoehe, breite):
        self = [[0 for x in range(hoehe)] for y in range(breite)]
        self[1][1] = 1
        self[2][2] = 1
        self[3][3] = 1
        print("- 1 2 3 4 5 6 7 8 9 10")
        for x in range(breite):
            if x == 0:
                print("A ", end="")
            elif x == 1:
                print("B ", end="")
            elif x == 2:
                print("C ", end="")
            elif x == 3:
                print("D ", end="")
            elif x == 4:
                print("E ", end="")
            elif x == 5:
                print("F ", end="")
            elif x == 6:
                print("G ", end="")
            elif x == 7:
                print("H ", end="")
            elif x == 8:
                print("I ", end="")
            elif x == 9:
                print("J ", end="")

            for y in range(hoehe):
                if self[x][y] == 0:
                    print("O ", end="")
                elif self[x][y] == 1:
                    print("X ", end="")
            print("")


feld1 = Spielfeld(10, 10)
feld1.printField(10, 10)
feld1.changeField(0, 0)
