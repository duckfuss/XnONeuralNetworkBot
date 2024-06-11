import numpy as np
class Board():
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.boardState = np.zeros((self.width, self.height))
    def check(self):
        print(self.boardState)

