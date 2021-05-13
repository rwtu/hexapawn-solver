turn = "b"

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


print(haveWon([["-", "b", "b"],["w", "w", "-"],["w", "b", "-"]], 3, "w"))