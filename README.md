# Hexapawn Solver
Finds the optimal next move based on the minimax algorithm

## Inputs
- board: list of strings, each representing a row of the board
- size: integer to indicate size of the board
- player: can be either "w" or "b", whose move we want to predict/who the maximizing player is
- depth: integer to indicate how many moves ahead minimax is to look
- example) hexapawn(["-ww","w--","bbb"], 3, 'b', 2)

## Hexapawn Rules 
### Setup
User specifies how many pawns each player will have (size)
- There are 2 types of pawns: black and white 
- (size) pawns on each side 
- (size) x (size) Board 

### Movement 
- Pawns can move ahead a single space if it is empty 
- Pawns can move diagonally a single space to capture an opponent's pawn 

### How to Win 
- Capture all opponent's pawns 
- One of the pawns reaches the opposite end of the board
- It's the opponent's turn but they can't move 
