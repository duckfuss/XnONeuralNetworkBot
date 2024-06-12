import boardController

board = boardController.Board(6,5)
turns = 0

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
    else:
        row,col = askPlayer()
        board.editBoard(2,row,col)
