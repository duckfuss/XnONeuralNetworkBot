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

        pass
    def check(self):
        print(self.boardState)

    def fancyPrint(self):
        '''prints self.boardState using nice ascii grid chars'''
        for row in range(self.rows):
            print(" ", end="")
            for col in range(self.cols-1):
                print(self.boardState[row][col], end=" ┃ ")
            print(self.boardState[row][col+1])
            if row != self.rows-1:
                print("━", end="")
                for i in range(self.cols-1):
                    print("━━╋━", end="")
                print("━━")
bob = Board(6,5)
bob.editBoard(1,4,4)
bob.fancyPrint()