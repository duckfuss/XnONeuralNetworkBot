import boardController

# initialisations
board = boardController.Board(6,5)
turns = 0

# Variables
nInRow = 3

def askPlayer():
    row = int(input("what row?: "))
    col = int(input("what col?: "))
    return row, col

# game loop:
while True:
    board.fancyPrint()
    if turns % 2 == 0:
        row, col = askPlayer()
        board.editBoard(1,row,col)
        if board.check(nInRow, 1):
            print("X wins")
            break
    else:
        row,col = askPlayer()
        board.editBoard(2,row,col)
        if board.check(nInRow, 2):
            print("O wins")
            break
    turns += 1