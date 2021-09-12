import math

## -- TOP LEVEL FUNCTION -- ##
# board: list of strings, each representing a row of the board
# size: integer to indicate size of the board
# player: can be either "w" or "b", whose move we want to predict/who the maximizing player is
# depth: integer to indicate how many moves ahead minimax is to look
# returns the optimal next move based on minimax algorithm 
def hexapawn(board, size, player, depth):
    # converts each of the rows in string form to lists so they're mutable 
    newBoard = stringToList(board) 
    (optEval, optBoard) = minimax(newBoard, size, player, depth, player)
    # turn the lists back to strings before returning the answer 
    return listToString(optBoard)


## -- MINIMAX ALGORITHM IMPLEMENTATION -- ##
# board: list with list elements, each of the list elements represents a row in the board
# size: integer to indicate size of the board
# player: can be either "w" or "b", indicates whose move we want to predict/ who the maximizing player is
# depth: integer to indicate how many moves ahead minimax is to look 
# turn: can be either "w" or "b", indicates whose turn it is to move 
# returns tuple containing (evaluation function value, board) for optimal next move
def minimax(board, size, player, depth, turn): 
    # base case - have reached desired depth or cannot make a move
    if depth == 0 or cannotMove(board, size, turn) == True:
        return (staticEval(board, size, player, turn), board)

    # if it's the turn of the maximizing player, want to get highest evaluation value from this position  
    if turn == player:
        maxEval = (-math.inf)
        children = allMoves(board, size, turn)
        for child in children:
            # white is the maximizing player, so next it's black pawn's turn 
            if player == "w":
                # newBoard contains child boards generated from recursive calls 
                (eval, newBoard) = minimax(child, size, player, depth-1, "b")
            # black is the maximizing player, so next it's white pawn's turn 
            else:
                (eval, newBoard) = minimax(child, size, player, depth-1, "w") 
            if eval > maxEval:
                maxEval = eval
                maxBoard = child
        return (maxEval, maxBoard)

    # it's the turn of the minimizing player, want to get lowest evaluation value from this position 
    else:
        minEval = math.inf
        children = allMoves(board, size, turn)
        for child in children:
            # black is the minimizing player, so next it's white pawn's turn 
            if turn == "b": 
                # newBoard contains child boards generated from recursive calls 
                (eval, newBoard) = minimax(child, size, player, depth-1, "w")
            # white is the minimizing player, so next it's black pawn's turn 
            else:
                (eval, newBoard) = minimax(child, size, player, depth-1, "b") 
            if eval < minEval:
                minEval = eval
                minBoard = child
        return (minEval, minBoard)
            

## -- STATIC EVALUATION FUNCTION (from class slides) -- ##
#   +10 if you have won the board 
#   -10 opponent wins
#   num. your pawns - num. opponents pawns if no one wins 
# board: list with list elements,  each of the list elements represents a row in the board
# size: integer to indicate size of the board
# player: can be either "w" or "b", indicates whose move we want to predict/ who the maximizing player is
# returns a single integer - result from static board evaluation 
def staticEval(board, size, player, turn):
    boardVal = 0 
    whiteCoords, blackCoords = findCoords(board, size)
    if player == "w": 
        # white pawns have won the board 
        if haveWon(board, size, player, turn) == True:
            boardVal = 10 
        # black pawns have won the board 
        elif haveWon(board, size, "b", turn) == True:
            boardVal = -10
        # no one's won 
        else: 
            boardVal = len(whiteCoords) - len(blackCoords)
    if player == "b": 
        # black pawns have won the board 
        if haveWon(board, size, player, turn) == True:
            boardVal = 10 
        # white pawns have won the board 
        elif haveWon(board, size, "w", turn) == True:
            boardVal = -10
        # no one's won 
        else: 
            boardVal = len(blackCoords) - len(whiteCoords)
    return boardVal

## Detects if the player passed into the function has won the game 
# board: list with list elements,  each of the list elements represents a row in the board
# size: integer to indicate size of the board
# player: can be either "w" or "b", indicates whose move we want to predict/ who the maximizing player is
def haveWon(board, size, player, turn):
    if (player == "w"):
        # checks to see if captured all black pawns
        for row in board: 
            if "b" in row:
                break
        else:
            return True
        # one of the white pawns reach the opposite end of the board
        if "w" in board[size-1]:
            return True
        # it's black pawns' turn but they can't move
        if turn == "b" and cannotMove(board,size, turn) == True:
            return True
    else:
        # checks to see if captured all white pawns
        for row in board: 
            if "w" in row:
                break
        else:
            return True
        # black pawn has reached the opposite end of the board
        if "b" in board[0]:
            return True
        # it's white pawns' turn but they can't move
        if turn == "w" and cannotMove(board,size,turn) == True:
            return True

    return False 

## Determines if the players whose turn it is to move can make a valid move
# board: list with list elements,  each of the list elements represents a row in the board
# size: integer to indicate size of the board
# returns True if they cannot move, False if the can move 
def cannotMove(board, size, turn):
    whiteCoords, blackCoords = findCoords(board, size)
    if turn == "w":
        for coord in whiteCoords:
            try: 
                # test if white pawn can move down
                if board[coord[0]+1][coord[1]] == "-":
                    return False 
            except: pass
            try: 
                # test if white pawn can move diagonally left
                if [coord[0]+1, coord[1]-1] in blackCoords:
                    return False 
            except: pass
            try: 
                # test if white pawn can move diagonally right 
                if [coord[0]+1, coord[1]+1] in blackCoords:
                    return False  
            except: pass
        return True
    else:
        for coord in blackCoords:
            try: 
                # test if black pawn can move move up
                if board[coord[0]-1][coord[1]] == "-":
                    return False 
            except: pass
            try: 
                # test if black pawn can move diagonally left 
                if [coord[0]-1, coord[1]-1] in whiteCoords:
                    return False 
            except: pass
            try: 
                # test if black pawn can move diagonally right
                if [coord[0]-1, coord[1]+1] in whiteCoords:
                    return False  
            except: pass
        return True 

## -- MOVE GENERATOR -- ##
# board: list with list elements,  each of the list elements represents a row in the board
# size: integer to indicate size of the board
# turn: can be either "w" or "b", indicates whose turn it is to move 
# returns all the possible next moves from the given board 
def allMoves(board, size, turn):
    return moveAhead(board, size,turn) + moveDiagonal(board, size, turn)

## Moves a pawn straight ahead one space if that space is empty 
# board: list with list elements,  each of the list elements represents a row in the board
# size: integer to indicate size of the boards
# returns a list of all valid moves that can be made by moving pawns one space ahead
def moveAhead(board, size, turn):
    # list of moves made 
    moved = []
    # get coordinate positions for where the white and black pawns are 
    whiteCoords, blackCoords = findCoords(board, size)
    # if it's white pawns' turn to move, generate the next moves they can make 
    if (turn == "w"):
        for coord in whiteCoords:
            try: 
                # position if white pawn moved down
                mvDown = [coord[0]+1, coord[1]] 
                # if that position is empty, then can move there
                if board[mvDown[0]][mvDown[1]] == "-":
                    boardCpy = [row[:] for row in board]
                    # access the position of where the white pawn was and change it to empty
                    boardCpy[coord[0]][coord[1]] = "-"
                    # "move" pawn 
                    boardCpy[mvDown[0]][mvDown[1]] = "w"
                    moved.append(boardCpy)
            except:
                continue      

    # it's black pawns' turn to move, generate the moves they can make  
    else:
        for coord in blackCoords: 
            try:
                # position if black pawn moved up 
                mvUp = [coord[0]-1, coord[1]] 
                # if that position is empty, then can move there
                if board[mvUp[0]][mvUp[1]] == "-":
                    boardCpy = [row[:] for row in board]
                    # access the position of where the black pawn was and change it to empty 
                    boardCpy[coord[0]][coord[1]] = "-"
                    # "move" pawn
                    boardCpy[mvUp[0]][mvUp[1]] = "b"
                    moved.append(boardCpy)
            except: 
                continue  
    return moved

## Moves a pawn diagonally once space forward if opponent is occupying that space
# board: list with list elements,  each of the list elements represents a row in the board
# size: integer to indicate size of the board
# returns a list of all valid moves that can be made by moving pawns diagonally left or right 
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
                    # access the position of where the white pawn was and change it to empty
                    boardCpy[coord[0]][coord[1]] = "-"
                    # "move" pawn
                    boardCpy[mvDiagLeft[0]][mvDiagLeft[1]] = "w"
                    moved.append(boardCpy) 
            except:
                pass
            try:
                # position if white pawn moved diagonally to the right 
                mvDiagRight = [coord[0]+1, coord[1]+1]
                # if that position is in the blackCoords list, we can move there 
                if mvDiagRight in blackCoords:
                    boardCpy = [row[:] for row in board]
                    # access the position of where the white pawn was and change it to empty 
                    boardCpy[coord[0]][coord[1]] = "-"
                    # "move" pawn
                    boardCpy[mvDiagRight[0]][mvDiagRight[1]] = "w"
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
                    # access the position of where the black pawn was and change it to empty
                    boardCpy[coord[0]][coord[1]] = "-"
                    # "move" pawn
                    boardCpy[mvDiagLeft[0]][mvDiagLeft[1]] = "b"
                    moved.append(boardCpy) 
            except:
                pass
            try: 
                # position if black pawn moved diagonally to the right 
                mvDiagRight = [coord[0]-1, coord[1]+1]
                # if that position is in the whiteCoords list, we can move there 
                if mvDiagRight in whiteCoords:
                    boardCpy = [row[:] for row in board]
                    # access the position of where the black pawn was and change it to empty 
                    boardCpy[coord[0]][coord[1]] = "-"
                    # "move" pawn
                    boardCpy[mvDiagRight[0]][mvDiagRight[1]] = "b"
                    moved.append(boardCpy) 
            except:
                continue
    return moved 

## --  HELPER FUNCTIONS -- ##

## Finds coordinate positions of players' pawns
# board: list with list elements,  each of the list elements represents a row in the board
# size: integer to indicate size of the board
# returns 2 lists: whiteCoords and blackCoords - each containing the 
#   coordinate positions of all the pawns with the associated color
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

## Prints out what the board looks like in readable form - for quick debugging 
# board: list with list elements,  each of the list elements represents a row in the board
def printBoard(board):
    for row in board:
        print("".join(row))
    print("\n")

## Converts the strings representing the rows to lists so they can be mutable 
# board: list of strings, each representing a row of the board
# returns given board but with each of the elements as lists instead of strings 
def stringToList(board):
    newBoard = [] 
    for row in board:
        newBoard.append(list(row))
    return newBoard

## Converts the lists representing the rows back into strings for proper format
#board: list with list elements,  each of the list elements represents a row in the board
# returns list of strings, each representing a row of the board
def listToString(board): 
    joined = []
    for row in board:
        joined.append("".join(row))
    return joined

# -- TESTING -- #
#result = hexapawn(["-ww","w--","bbb"],3,'b',2) #['-ww', 'b--', 'b-b']
#print(result)

#result = hexapawn(['wwwww','-----','-----','-----','bbbbb'], 5, 'w', 5) #['-wwww', 'w----', '-----', '-----', 'bbbbb']
#print(result)

#result = hexapawn(["www","---","bbb"],3,'w',2) #["-ww", "w--" , "bbb"]
#print(result)

#result = hexapawn(["w-w","-w-","b-b"],3,'b',2) #["w-w","-b-","--b"]
#print(result)

# tests unable to move base case
#result = hexapawn(["-w-","wbw","b-b"],3,'w',2) #["-w-","wbw","b-b"]
#print(result)
