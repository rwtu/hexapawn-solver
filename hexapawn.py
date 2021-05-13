
## Top level function 
# board: n-element list with each of the elements representing a row of the board
# size: integer to indicate size of the board
# player: can be either "w" or "b" to indicate whether you're playing as white pawns or black paws 
# lookAhead: integer to indicate how many moves ahead minimax is to look 
def hexapawn(board, size, player, lookAhead):
    # converts each of the rows to a list so they can be mutable 
    newBoard = stringToList(board) 


## Evaluation Function 
def evalFunct(board, player):
    pass
    # you have won the board 

    # opponent has won the board 

    # no one's won 

## Detects if the player passed into the function has won the game 
# board: n-element list with each of the elements representing a row of the board
# size: integer to indicate size of the board
# player: can be either "w" or "b" to indicate whether you're playing as white pawns or bl
def haveWon(board, size, player):
    # playing as white pawn 
    if (player == "w"):
        # captured all of opponent's pawns 
        for row in board: 
            if "b" in row:
                break
        else:
            return True
    
        # one of your pawns reach the opposite end of the board
        # which could be any space in last row (size-1)
        if "w" in board[size-1]:
            return True

        # it's your opponent's turn but your opponent can't move 

    # playing as black pawn 
    else:
        # captured all of opponent's pawns 
        for row in board: 
            if "w" in row:
                break
        else:
            return True
    
        # one of your pawns reach the opposite end of the board
        # which could be any space in first row (0)
        if "b" in board[0]:
            return True


## Moves a pawn straight ahead one space if that space is empty 
# board: n-element list with each of the elements representing a row of the board
# size: integer to indicate size of the board
# player: can be either "w" or "b" to indicate whether you're playing as white pawns or bl
# returns a list of all possible moves? 
def moveAhead(board, size, player):
    # list of moves made 
    moved = []
    # get coordinate positions for where the white and black pawns are 
    whiteCoords, blackCoords = findCoords(board, size)
    # playing as white pawn 
    if (player == "w"):
        for coord in whiteCoords:
            # add 1 to the x coordinate to get position if white pawn moved down
            mvDown = [coord[0]+1, coord[1]] 
            # if that position is empty "-", then can move there
            if board[mvDown[0]][mvDown[1]] == "-":
                # copy the board 
                boardCpy = [row[:] for row in board]
                # access the position of where the white pawn was and change it to empty "-"
                boardCpy[coord[0]][coord[1]] = "-"
                # access the position of where the white pawn is going to move and change it to "w"
                boardCpy[mvDown[0]][mvDown[1]] = "w"
                # append this new board state to moved 
                moved.append(boardCpy)
            # else, that position is occupied so we can just keep looking at the other pawns             

    # playing as black pawn 
    else:
        for coord in blackCoords: 
            # subtract 1 to the x coodinate to get position if black pawn moved up 
            mvUp = [coord[0]-1, coord[1]] 
            # if that position is empty "-", then can move there
            if board[mvUp[0]][mvUp[1]] == "-":
                # copy the board 
                boardCpy = [row[:] for row in board]
                # access the position of where the black pawn was and change it to empty "-"
                boardCpy[coord[0]][coord[1]] = "-"
                # access the position of where the black pawn is going to move and change it to "b"
                boardCpy[mvUp[0]][mvUp[1]] = "b"
                # append this new board state to moved 
                moved.append(boardCpy)

            # else, that position is occupied so we can just keep looking at the other pawns          
    return moved


# Finds coordinate positions of players' pawns
# board: n-element list with each of the elements representing a row of the board
# size: integer to indicate size of the board
# Returns 2 lists: whiteCoords and blackCoords - each containing the 
#   coordinate positions of all the pawns with the color indicated in the name
def findCoords(board, size):
    whiteCoords = []
    blackCoords = []
    for x in range(0, size):
        for y in range(0, size):
            if board[x][y] == "w":
                whiteCoords.append([x, y])
            elif board[x][y] == "b":
                blackCoords.append([x, y])
    return whiteCoords, blackCoords 


# Prints out what the board looks like 
# board: n-element list with each of the elements representing a row of the board
def printBoard(board):
    for row in board:
        print("".join(row))
    print("\n")

# Converts the strings representing the rows in the input argument to lists so they can be mutable 
# board: n-element list with each of the elements representing a row of the board
def stringToList(board):
    newBoard = [] 
    for row in board:
        newBoard.append(list(row))
    return newBoard

# -- TESTING -- #
##hexapawn(["www","---","bbb"],3,'w',2)
boards = moveAhead([['w', 'w', 'w'], ['-', 'b', 'b'], ['b', 'b', 'b']], 3, "b") 
for board in boards: printBoard(board)
