import boardController
import network
import numpy as np
import time

# initialisations
rows, cols = 3,3
board = boardController.Board(rows,cols)

duckX = network.Network([rows*cols, 16, rows*cols], 1)
duckX.generateNetwork()

duckO = network.Network([rows*cols, 16, rows*cols], 2)
duckO.generateNetwork()

duckList = ["padding so index 1 = x etc.", duckX, duckO]
# 1 = X, 2 = Y

# Variables :)
nInRow = 3

def askPlayer():
    row = int(input("what row?: "))
    col = int(input("what col?: "))
    return row, col
'''
def consultDuck(boardState, player, verbose=False):
    compressed = np.divide(boardState, 2)
    output = duckList[player].compute(compressed).reshape(rows,cols)
    (row,col) = np.unravel_index(output.argmax(), output.shape) # take the highest valued coord
    if verbose: print(output, row, col)
    return row, col
'''

def consultDuck(boardState, player, verbose=False):
    compressed = np.divide(boardState, 2)
    output = duckList[player].compute(compressed).reshape(rows,cols)
    freeSpaces = np.where(boardState == 0) 
    # 2 arrays, one for xcoord, one for correspinding ycoord
    freeOutputList, freeCoordsList = [], []
    maxRow, maxCol = 0, 0
    for space in range(len(freeSpaces[0])):
        row, col = freeSpaces[0][space], freeSpaces[1][space]
        if output[row][col] > output[maxRow][maxCol]:
            maxRow, maxCol = row, col
    return row, col


def consultEvilDuck(boardState, verbose=False):
    '''This bot chooses next pos completly randomly'''
    #if np.count_nonzero(boardState) == rows * cols:
    freeSpaces = np.where(boardState == 0)
    index = np.random.randint(len(freeSpaces[0]))
    row = freeSpaces[0][index]
    col = freeSpaces[1][index]
    if verbose: print("Row/Col:", row, col, "\nfreeSpaces:", freeSpaces)
    return row,col

def gameLoop(order={1:"duck", 2:"duck"}, verbose=False):
    for i in range(rows*cols):
        if verbose: board.fancyPrint()
        if i % 2 == 0:  active = 1
        else:           active = 2
        if order[active] == "duck":
            if verbose: print("\nCOMPUTER", active, "TURN")
            row, col = consultDuck(board.boardState, active, verbose=verbose)
        elif order[active] == "player":
            if verbose: print("\nPLAYER TURN")
            row, col = askPlayer()
        elif order[active] == "evilDuck":
            if verbose: print("\nEVIL DUCK TURN")
            row,col = consultEvilDuck(board.boardState, verbose=verbose)
        board.editBoard(active,row,col)
        if board.check(nInRow, active):
            if verbose:
                board.fancyPrint()
                if active == 1: print("---------------------------- X wins\n\n")
                else:           print("---------------------------- O wins\n\n")
            return active
    if verbose: print("---------------------------- DRAW\n\n")
    return 0

def trainAlgorithms(winner):
    '''Post-game training and analysis'''
    duckList[1].trainNetwork(boardHist=board.boardHistory, winner=winner)
    duckList[2].trainNetwork(boardHist=board.boardHistory, winner=winner)

    

### TRAINING ###
iterations = 10**6
for i in range(iterations):
    winner = gameLoop(order={1:"duck", 2:"evilDuck"}, verbose=False)
    trainAlgorithms(winner)
    board.resetBoard()
    if i % (iterations/10) == 0:
        gameLoop(order={1:"duck", 2:"evilDuck"}, verbose=True)
        board.resetBoard()
        print(i, (100*i)/iterations, "%")

print("\n\n\n")
while True:
    board.resetBoard()
    #multiplayerGameLoop()
    gameLoop(order={1:"duck", 2:"player"}, verbose=True)