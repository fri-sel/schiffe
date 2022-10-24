class Spielfeld(object):
    def __init__(self, hoehe, breite):
        self.hoehe = hoehe
        self.breite = breite

    def changeField(self, posx, posy):
        self[posx][posy] = 1

    def printField(self, hoehe, breite):
        self = [[0 for x in range(hoehe)] for y in range(breite)]
        self[1][1] = 1
        for x in range(hoehe):
            for y in range(breite):
                if self[x][y] == 0:
                    print("O", end="")
                elif self[x][y] == 1:
                    print("X", end="")
            print("")


feld1 = Spielfeld(10, 10)
feld1.printField(10, 10)
# feld1.changeField(0, 0)
