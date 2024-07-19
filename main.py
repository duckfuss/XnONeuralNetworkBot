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

def consultDuck(boardState, player, verbose=False):
    output = duckList[player].compute(boardState).reshape(rows,cols)
    (row,col) = np.unravel_index(output.argmax(), output.shape) # take the highest valued coord
    if verbose: print(output, row, col)
    return row, col

def playerGameLoop(order={1:"network", 2:"player"}):
    for i in range((rows * cols)+5):
        if i % 2 == 0:  activePlayer, turn = order[1], 1
        else:           activePlayer, turn = order[2], 2
        if activePlayer == "network":
            print("\nCOMPUTER TURN")
            board.fancyPrint()
            row, col = consultDuck(board.boardState, turn, verbose=True)
        elif activePlayer == "player":
            print("\nPLAYER TURN")
            board.fancyPrint()
            row, col = askPlayer()
        board.editBoard(turn,row,col)
        if board.check(nInRow, turn):
            board.fancyPrint()
            if turn == 1:   print("----------------------------X wins\n")
            else:           print("----------------------------O wins\n")
            return activePlayer
    print("nobody wins")

def multiplayerGameLoop():
    for i in range((rows * cols)+5):
        board.fancyPrint()
        if i % 2 == 0:
            print("Xs turn")
            player = 1
        else:
            print("Os turn")
            player = 2
        row, col = askPlayer()
        board.editBoard(player, row, col)
        if board.check(nInRow, player):
            board.fancyPrint()
            if player == 1: print("----------------------------X wins\n")
            else:           print("----------------------------O wins\n")
            return

def computerGameLoop(maxTurns=10, verbose=False, wait=False):
    '''
    Plays one game of duckX vs duckY
    Changing turns to 1 will allow O to go first
    '''
    for turns in range(maxTurns):
        if turns % 2 == 0:  activePlayer = 1
        else:               activePlayer = 2
        row, col = consultDuck(board.boardState, activePlayer)
        if verbose: 
            if wait: time.sleep(1) # debug
            board.fancyPrint()
            print("turns taken:", turns)
            print("next coords:", row, col)
        board.editBoard(activePlayer, row, col)
        if board.check(nInRow, activePlayer):
            if verbose:
                board.fancyPrint()
                if activePlayer == 1:   print("---------------------------- X wins\n")
                else:                   print("---------------------------- O wins\n")
            return activePlayer
    if verbose: print("---------------------------- DRAW\n")
    return 0 # timeout -> nobody won :(

def trainAlgorithms(winner):
    '''Post-game training and analysis'''
    duckList[1].trainNetwork(boardHist=board.boardHistory, winner=winner)
    duckList[2].trainNetwork(boardHist=board.boardHistory, winner=winner)

    

### TRAINING ###
iterations = 10**6
for i in range(iterations):
    winner = computerGameLoop()
    trainAlgorithms(winner)
    board.resetBoard()
    if i % (iterations/10) == 0:
        computerGameLoop(verbose=True)
        print(i, (100*i)/iterations, "%")


computerGameLoop(verbose=True, wait=True)
board.fancyPrint()
print("\n\n\n")
while True:
    board.resetBoard()
    #multiplayerGameLoop()
    playerGameLoop()