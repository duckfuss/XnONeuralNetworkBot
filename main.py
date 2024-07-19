import boardController
import network
import numpy as np
import time

# initialisations
rows, cols = 6,5
board = boardController.Board(rows,cols)

duckX = network.Network([rows*cols, 10, rows*cols], 1)
duckX.generateNetwork()

duckO = network.Network([rows*cols, 10, rows*cols], 2)
duckO.generateNetwork()

duckList = ["padding so index 1 = x etc.", duckX, duckO]


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


def computerGameLoop(turns=0, maxTurns=100):
    '''
    Plays one game of duckX vs duckY
    Changing turns to 1 will allow O to go first
    '''
    while turns < maxTurns:
        time.sleep(0.1) # debug
        turns += 1
        board.fancyPrint()
        print("turns taken:", turns)
        if turns % 2 == 0:  activePlayer = 1
        else:               activePlayer = 2
        row, col = consultDuck(board.boardState, activePlayer)
        board.editBoard(activePlayer,row,col)
        if board.check(nInRow, activePlayer):
            if activePlayer == 1:   print("X wins")
            else:                   print("O wins")
            return activePlayer
    return 0 # timeout -> nobody won :(



### TRAINING ###
computerGameLoop()
