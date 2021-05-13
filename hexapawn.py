# intializes global variable to keep track of whose turn it is to move 
turn = "b"

## Top level function 
# board: n-element list with each of the elements representing a row of the board
# size: integer to indicate size of the board
# player: can be either "w" or "b", indicates which color pawn we're playing as/whose move we want to predict 
# lookAhead: integer to indicate how many moves ahead minimax is to look 
def hexapawn(board, size, player, lookAhead):
    # converts each of the rows to a list so they can be mutable 
    newBoard = stringToList(board) 
    turn = player 

## Evaluation Function 
def evalFunct(board, size, player):
    boardVal = 0 
    whiteCoords, blackCoords = findCoords(board, size)
    # playing as white pawn 
    if player == "w": 
        # white pawns have won the board 
        if haveWon(board, size, player) == True:
            boardVal = 10 
        # black pawns have won the board 
        elif haveWon(board, size, "b") == True:
            boardVal = -10
        # no one's won - calculate # of white pawns - # black pawns 
        else: 
            boardVal = len(whiteCoords) - len(blackCoords)
    # playing as black pawn 
    if player == "b": 
        # black pawns have won the board 
        if haveWon(board, size, player) == True:
            boardVal = 10 
        # white pawns have won the board 
        elif haveWon(board, size, "w") == True:
            boardVal = -10
        # no one's won - calculate # of black pawns - # white pawns 
        else: 
            boardVal = len(blackCoords) - len(whiteCoords)
    return boardVal

## Detects if the player passed into the function has won the game 
# board: n-element list with each of the elements representing a row of the board
# size: integer to indicate size of the board
# player: can be either "w" or "b" to indicate whether you're playing as white pawns or black pawns
def haveWon(board, size, player):
    whiteCoords, blackCoords = findCoords(board, size)
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
        if turn == "b" and cannotMove(board,size) == True:
            return True

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

        # it's your opponent's turn but your opponent can't move
        if turn == "w" and cannotMove(board,size) == True:
            return True

    return False 

# Determines if the players whose turn it is to move can move or not 
# returns True if they cannot move, False if the can move 
def cannotMove(board, size):
    whiteCoords, blackCoords = findCoords(board, size)
    # It's white pawns' turn to move 
    if turn == "w":
        for coord in whiteCoords:
            try: 
                # could move down
                if [coord[0]+1, coord[1]] == "-":
                    return False 
            except: pass
            try: 
                # could move diagonally left 
                if [coord[0]+1, coord[1]-1] in blackCoords:
                    return False 
            except: pass
            try: 
                # could move diagonally right
                if [coord[0]+1, coord[1]+1] in blackCoords:
                    return False  
            except: pass
        return True
    else:
        for coord in blackCoords:
            try: 
                # could move up
                if [coord[0]-1, coord[1]] == "-":
                    return False 
            except: pass
            try: 
                # could move diagonally left 
                if [coord[0]-1, coord[1]-1] in whiteCoords:
                    return False 
            except: pass
            try: 
                # could move diagonally right
                if [coord[0]-1, coord[1]+1] in whiteCoords:
                    return False  
            except: pass
        return True 

def moveAll(board, size):
    return moveAhead(board, size) + moveDiagonal(board, size)

## Moves a pawn straight ahead one space if that space is empty 
# board: n-element list with each of the elements representing a row of the board
# size: integer to indicate size of the boards
# returns a list of all possible moves
def moveAhead(board, size):
    # list of moves made 
    moved = []
    # get coordinate positions for where the white and black pawns are 
    whiteCoords, blackCoords = findCoords(board, size)
    # if it's white pawn's turn to move, generate the next moves they can make 
    if (turn == "w"):
        for coord in whiteCoords:
            try: 
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
            except:
                continue
        # now change variable to indicate it's now black pawn's turn to move
        turn = "b"       

    # it's black pawn's player turn to move, generate the moves they can make  
    else:
        for coord in blackCoords: 
            try:
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
            except: 
                continue  
        # now change variable to indicate it's now white pawn's turn to move
        turn = "w"   

    return moved

## Moves a pawn diagonally once space forward if opponent is occupying that space
# board: n-element list with each of the elements representing a row of the board
# size: integer to indicate size of the board
# returns a list of all possible moves
def moveDiagonal(board, size):
    # list of moves made 
    moved = []
    # get coordinate positions for where the white and black pawns are 
    whiteCoords, blackCoords = findCoords(board, size)
    # if it's white pawn's player to move, generate the next moves they can make  
    if (turn == "w"):
        for coord in whiteCoords:
            try: 
                # position if white pawn moved diagonally to left 
                mvDiagLeft = [coord[0]+1, coord[1]-1]
                # if that position is in the blackCoords list, we can move there 
                if mvDiagLeft in blackCoords:
                    boardCpy = [row[:] for row in board]
                    # access the position of where the white pawn was and change it to empty "-"
                    boardCpy[coord[0]][coord[1]] = "-"
                    # access the position of where the white pawn is going to move and change it to "w"
                    boardCpy[mvDiagLeft[0]][mvDiagLeft[1]] = "w"
                    # append the new board state to moved
                    moved.append(boardCpy) 
            except:
                pass
            try:
                # position if white pawn moved diagonally to the right 
                mvDiagRight = [coord[0]+1, coord[1]+1]
                # if that position is in the blackCoords list, we can move there 
                if mvDiagRight in blackCoords:
                    boardCpy = [row[:] for row in board]
                    # access the position of where the white pawn was and change it to empty "-"
                    boardCpy[coord[0]][coord[1]] = "-"
                    # access the position of where the white pawn is going to move and change it to "w"
                    boardCpy[mvDiagRight[0]][mvDiagRight[1]] = "w"
                    # append the new board state to moved
                    moved.append(boardCpy) 
            except:
                continue
        # now change variable to indicate it's now black pawn's turn to move
        turn = "b"   

    # it's black pawn's player turn to move, generate the moves they can make  
    else:
        for coord in blackCoords:
            try: 
                # position if black pawn moved diagonally to left 
                mvDiagLeft = [coord[0]-1, coord[1]-1]
                # if that position is in the whiteCoords list, we can move there 
                if mvDiagLeft in whiteCoords:
                    boardCpy = [row[:] for row in board]
                    # access the position of where the black pawn was and change it to empty "b"
                    boardCpy[coord[0]][coord[1]] = "-"
                    # access the position of where the black pawn is going to move and change it to "b"
                    boardCpy[mvDiagLeft[0]][mvDiagLeft[1]] = "b"
                    # append the new board state to moved
                    moved.append(boardCpy) 
            except:
                pass
            try: 
                # position if black pawn moved diagonally to the right 
                mvDiagRight = [coord[0]-1, coord[1]+1]
                # if that position is in the whiteCoords list, we can move there 
                if mvDiagRight in whiteCoords:
                    boardCpy = [row[:] for row in board]
                    # access the position of where the black pawn was and change it to empty "-"
                    boardCpy[coord[0]][coord[1]] = "-"
                    # access the position of where the black pawn is going to move and change it to "b"
                    boardCpy[mvDiagRight[0]][mvDiagRight[1]] = "b"
                    # append the new board state to moved
                    moved.append(boardCpy) 
            except:
                continue
        # now change variable to indicate it's now white pawn's turn to move
        turn = "w"   
    return moved 

# Finds coordinate positions of players' pawns
# board: n-element list with each of the elements representing a row of the board
# size: integer to indicate size of the board
# returns 2 lists: whiteCoords and blackCoords - each containing the 
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
result = evalFunct([["-","w","-"],["w","b","w"],["b","-","b"]], 3, "b")
print(result)
#for board in boards: printBoard(board)
