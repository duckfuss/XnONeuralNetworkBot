import numpy as np


class Board():
    def __init__(self, rows, cols) -> None:
        self.rows = rows
        self.cols = cols
        self.boardState = np.zeros((self.rows, self.cols), dtype=int)
        print(self.boardState)
    def editBoard(self, value, row, col):
        print(self.boardState[row][col])
        self.boardState[row][col] = value

    def check(self, nInRow, value):
        '''
        checks for n in a row
        nInRow MUST be < self.rows and self.cols
        ''' 
        Tv,Th,TdU,TdD = 0,0,0,0 # totals for vert, horiz., ...
        for row in range(self.rows):
            for col in range(self.cols):
                if self.boardState[row][col] == value:
                    Tv  += self.searchAhead("Vert", row, col, nInRow, value)
                    Th  += self.searchAhead("Hor", row, col, nInRow, value)
                    TdU += self.searchAhead("diagUp", row, col, nInRow, value)
                    TdD += self.searchAhead("diagDo", row, col, nInRow, value)
        print(Tv, Th, TdU, TdD)
    
    def searchAhead(self, direc, row, col, n, positive):
        nD = {"Vert":[1,0], "Hor":[0,1], "diagUp":[1,-1], "diagDo":[1,1]} # neighbour data
        for i in range(n-1):
            row += nD[direc][0]
            col += nD[direc][1]
            if col < self.cols and row < self.rows:
                if self.boardState[row][col] != positive:
                    return 0
            else:
                return 0
        return 1


    def fancyPrint(self, charDict = {0:"  ", 1:"❌", 2:"⭕️"}):
        '''prints self.boardState using nice ascii grid chars'''
        for row in range(self.rows):
            print(" ", end="")
            for col in range(self.cols-1):
                print(charDict[self.boardState[row][col]], end="┃ ")
            print(charDict[self.boardState[row][col+1]])
            if row != self.rows-1:
                print("━", end="")
                for i in range(self.cols-1):
                    print("━━╋━", end="")
                print("━━")

bob = Board(6,5)
bob.editBoard(1,2,2)
bob.editBoard(1,1,3)
bob.editBoard(1,0,4)
bob.fancyPrint()
bob.check(3, 1)