import boardController
import network
import numpy as np
import time

# initialisations
rows, cols = 3,3
board = boardController.Board(rows,cols)

duckX = network.Network([rows*cols, 10, rows*cols], 1)
duckX.generateNetwork()

duckO = network.Network([rows*cols, 10, rows*cols], 2)
duckO.generateNetwork()

duckList = ["padding so index 1 = x etc.", duckX, duckO]
# 1 = X, 2 = Y

# Variables :)
nInRow = 3

def askPlayer():
    row = int(input("what row?: "))
    col = int(input("what col?: "))
    return row, col

def consultDuck(boardState, player):
    output = duckList[player].compute(boardState).reshape(rows,cols)
    (row,col) = np.unravel_index(output.argmax(), output.shape) # take the highest valued coord
    print(output)
    return row, col


def computerGameLoop(maxTurns=10):
    '''
    Plays one game of duckX vs duckY
    Changing turns to 1 will allow O to go first
    '''
    for turns in range(maxTurns):
        time.sleep(0.1) # debug
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

def trainAlgorithm(winner):
    '''Post-game training and analysis'''
    duckList[1].trainNetwork(boardHist=board.boardHistory, winner=winner)
    duckList[2].trainNetwork(boardHist=board.boardHistory, winner=winner)

### TRAINING ###
winner = computerGameLoop()
trainAlgorithm(winner)
