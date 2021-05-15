import math

## Top level function 
# board: n-element list with each of the elements representing a row of the board
# size: integer to indicate size of the board
# player: can be either "w" or "b", whose move we want to predict/ who the maximizing player is
# depth: integer to indicate how many moves ahead minimax is to look 
def hexapawn(board, size, player, depth):
    # converts each of the rows to a list so they can be mutable 
    newBoard = stringToList(board) 
    # --TWO SITUATIONS -- # 
    # 1) game has just begun: no one has moved yet 
    # 2) game in progress
    #   - either white is the maximizing player:  black pawns have just moved so now it's white pawns' turn to move 
    #   - or black is the maximizing player: white pawns have just moved so now it's black pawns' turn to move 
    return minimax(newBoard, size, player, depth, player)


## Implementation of the Minimax algorithm 
# board: n-element list with each of the elements representing a row of the board
# size: integer to indicate size of the board
# player: can be either "w" or "b", indicates whose move we want to predict/ who the maximizing player is
# depth: integer to indicate how many moves ahead minimax is to look 
# turn: can be either "w" or "b", indicates whose turn it is to move 
# returns tuple list containing (evaluation function value, board) 
def minimax(board, size, player, depth, turn): 
    if depth == 0:
        return (staticEval(board, size, player, turn), board)
    # if it's the turn of the maximizing player, want to get highest eval in this position  
    if turn == player:
        maxEval = (-math.inf)
        maxBoard = board # variable used to store the board with maximum evaluation function value
        children = allMoves(board, size, turn)
        for child in children: printBoard(child)
        for child in children:
            # white is the maximizing player, so next it's black pawn's turn 
            if player == "w": 
                (eval, newBoard) = minimax(child, size, player, depth-1, "b")
            # black is the maximizing player, so next it's white pawn's turn 
            else:
                (eval, newBoard) = minimax(child, size, player, depth-1, "w") 
            if eval > maxEval:
                maxEval = eval 
                maxBoard = child
        return (maxEval, maxBoard) 

    # it's the turn of the minimizing player, want to get lowest eval in this position 
    else:
        minEval = math.inf
        minBoard = board # variable used to store the board with minimum evaluation function value
        children = allMoves(board, size, turn)
        for child in children:
            # black is the minimizing player, so next it's white pawn's turn 
            if turn == "b": 
                (eval, newBoard) = minimax(child, size, player, depth-1, "w")
            # white is the minimizing player, so next it's black pawn's turn 
            else:
                (eval, newBoard) = minimax(child, size, player, depth-1, "b") 
            if eval < minEval:
                minEval = eval 
                minBoard = child
        return (minEval, minBoard)
            
## Evaluation Function (the one from class slides): 
#   +10 if you have won the board 
#   -10 opponent wins
#   num. your pawns - num. opponents pawns if no one wins 
# board: n-element list with each of the elements representing a row of the board
# size: integer to indicate size of the board
# player: can be either "w" or "b", indicates whose move we want to predict/ who the maximizing player is
# returns a single integer - result from static board evaluation 
def staticEval(board, size, player, turn):
    boardVal = 0 
    whiteCoords, blackCoords = findCoords(board, size)
    # white pawn is the maximizing player
    if player == "w": 
        # white pawns have won the board 
        if haveWon(board, size, player, turn) == True:
            boardVal = 10 
        # black pawns have won the board 
        elif haveWon(board, size, "b", turn) == True:
            boardVal = -10
        # no one's won - calculate # of white pawns - # black pawns 
        else: 
            boardVal = len(whiteCoords) - len(blackCoords)
    # black pawn is the maximizing player
    if player == "b": 
        # black pawns have won the board 
        if haveWon(board, size, player, turn) == True:
            boardVal = 10 
        # white pawns have won the board 
        elif haveWon(board, size, "w", turn) == True:
            boardVal = -10
        # no one's won - calculate # of black pawns - # white pawns 
        else: 
            boardVal = len(blackCoords) - len(whiteCoords)
    return boardVal

## Detects if the player passed into the function has won the game 
# board: n-element list with each of the elements representing a row of the board
# size: integer to indicate size of the board
# player: can be either "w" or "b", indicates whose move we want to predict/ who the maximizing player is
def haveWon(board, size, player, turn):
    # white pawn is the maximizing player
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
        if turn == "b" and cannotMove(board,size, turn) == True:
            return True

    # black pawn is the maximizing player 
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
        if turn == "w" and cannotMove(board,size, turn) == True:
            return True

    return False 

# Determines if the players whose turn it is to move can move or not 
# board: n-element list with each of the elements representing a row of the board
# size: integer to indicate size of the board
# returns True if they cannot move, False if the can move 
def cannotMove(board, size, turn):
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

def allMoves(board, size, turn):
    return moveAhead(board, size,turn) + moveDiagonal(board, size, turn)

## Moves a pawn straight ahead one space if that space is empty 
# board: n-element list with each of the elements representing a row of the board
# size: integer to indicate size of the boards
# returns a list of all possible moves
def moveAhead(board, size, turn):
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
    return moved

## Moves a pawn diagonally once space forward if opponent is occupying that space
# board: n-element list with each of the elements representing a row of the board
# size: integer to indicate size of the board
# returns a list of all possible moves
def moveDiagonal(board, size, turn):
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
result = hexapawn(["-ww","w--","bbb"],3,'b',2)
print(result)
#for board in boards: printBoard(board)
