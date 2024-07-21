import boardController
import network
import numpy as np

# variables - can be changed
nInRow = 3
rows, cols = 3,3

# initialisations
board = boardController.Board(rows,cols)

duckX = network.Network([rows*cols, rows*cols], 1)
duckX.generateNetwork()

duckO = network.Network([rows*cols, rows*cols], 2)
duckO.generateNetwork()

duckList = ["padding so index 1 = x etc.", duckX, duckO] # 1 = X, 2 = Y



def askPlayer():
    '''returns chosen row and col of the player'''
    row = int(input("what row?: "))
    col = int(input("what col?: "))
    return row, col


def consultDuck(boardState, player, verbose=False):
    '''picks highest legal move'''
    compressed = np.divide(boardState, 2)
    output = duckList[player].compute(compressed).reshape(rows,cols)
    freeSpaces = np.where(boardState == 0) 
    # 2 arrays, one for xcoord, one for correspinding ycoord
    maxRow, maxCol = freeSpaces[0][0], freeSpaces[1][0]
    for space in range(len(freeSpaces[0])):
        row, col = freeSpaces[0][space], freeSpaces[1][space]
        if output[row][col] > output[maxRow][maxCol]:
            maxRow, maxCol = row, col
    if verbose: print(output, maxRow, maxCol)
    return maxRow, maxCol


def consultEvilDuck(boardState, verbose=False):
    '''This bot chooses next pos completly randomly'''
    freeSpaces = np.where(boardState == 0)
    index = np.random.randint(len(freeSpaces[0]))
    row = freeSpaces[0][index]
    col = freeSpaces[1][index]
    if verbose: print("Row/Col:", row, col, "\nfreeSpaces:", freeSpaces)
    return row,col

def gameLoop(order={1:"duck", 2:"duck"}, verbose=False):
    '''
    plays one match of XnO
    change order{} to:
      "duck"        for an AI
      "player"      for asking the player
      "evilDuck"    for a random choice
    '''
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

def trainAlgorithms(winner, verbose=False):
    '''Post-game training and analysis'''
    duckList[1].trainNetwork(boardHist=board.boardHistory, winner=winner, verbose=verbose)
    duckList[2].trainNetwork(boardHist=board.boardHistory, winner=winner, verbose=verbose)

    

### TRAINING ###
iterations = 10**4
wins, draws = 0, 0
for i in range(iterations):
    # X vs Random
    winner = gameLoop(order={1:"duck", 2:"evilDuck"}, verbose=False)
    trainAlgorithms(winner)
    board.resetBoard()
    if winner == 1: wins += 1
    elif winner == 0: draws += 1

    # O vs Random
    winner = gameLoop(order={1:"evilDuck", 2:"duck"}, verbose=False)
    trainAlgorithms(winner)
    board.resetBoard()


    if i % (iterations/10) == 0:
        gameLoop(order={1:"duck", 2:"duck"}, verbose=False)
        trainAlgorithms(winner, verbose=False)
        board.resetBoard()
        print(i, "games\t", (100*i)/iterations, "%", "complete\n")
        print((100*wins)/(i+1), "%\t won\n", 
              (100*draws)/(i+1), "%\t", " drawn\n", 
              (100*(i-wins-draws))/(i+1), "%\t", " lost\n\n", sep="")

print("FINAL STEP")
for i in range(int(iterations/10)):
    # Ai vs Ai
    winner = gameLoop(order={1:"duck", 2:"duck"}, verbose=False)
    trainAlgorithms(winner)
    board.resetBoard()
print("TRAINING OVER\n\n\n")

## PLAYING ##
while True:
    board.resetBoard()
    gameLoop(order={1:"duck", 2:"player"}, verbose=True)
    # uncoment below to play X
    #gameLoop(order={2:"duck", 1:"player"}, verbose=True)
