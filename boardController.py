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

    def check(self, nInRow):
        '''
        checks for n in a row
        nInRow MUST be < self.rows and self.cols
        '''
        
        for row in range(self.rows):
                for col in range(self.cols):
                    active = self.boardState[row][col]

                    pass
        print(self.boardState)

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
bob.fancyPrint()