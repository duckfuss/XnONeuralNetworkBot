import boardController
import network
import numpy as np

# initialisations
rows, cols = 6,5
board = boardController.Board(rows,cols)
duckX = network.Network([rows*cols, 20, rows*cols], 1)
duckX.generateNetwork()
duckO = network.Network([rows*cols, 20, rows*cols], 2)
duckO.generateNetwork()
duckList = ["padding so index 1 = x etc.", duckX, duckO]
turns = 0

# Variables :)
nInRow = 3

def askPlayer():
    row = int(input("what row?: "))
    col = int(input("what col?: "))
    return row, col

def consultDuck(boardState, turn):
    output = duckList[turn].compute(boardState).reshape(rows,cols)
    (row,col) = np.unravel_index(output.argmax(), output.shape)
    return row, col

# training game loop:
while True:
    board.fancyPrint()
    if turns % 2 == 0:
        row, col = consultDuck(board.boardState, 1)
        board.editBoard(1,row,col)
        if board.check(nInRow, 1):
            print("X wins")
            break
    else:
        row,col = consultDuck(board.boardState, 2)
        board.editBoard(2,row,col)
        if board.check(nInRow, 2):
            print("O wins")
            break
    turns += 1
# assume game is over