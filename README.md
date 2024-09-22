# 1DL251-Group-Project
Game platform

Ideas for design : 

Local, event-driven architecture 

- Single- threaded game loop : 
> updates the game state and provides the output
> , handles player input and manages the turn-based system

- Event queue
> stores players actions as events
> , events are processed sequentially

- Turn-based system 
> determines the active player
> , ensures only the active one can perform actions

Language : common agreement on Python. 

Tools : we can use the Pygame library. Provides functions graphics and sound. Handles user input and system events. Provides a basic structure for a game loop, including updating the game state and rendering the display. 

Data Structures:
1. Board Representation:
   A 2D array (matrix) of size 4x4 represents the board, where each cell holds a stack of pieces.
2. Piece Representation:
   Each piece is an object with the following properties:
  - `color`: "black" or "white"
  - `isStanding`: a boolean indicating if the piece is standing or sitting

Game Logic:
1. Stacking Logic:
   Each cell on the board behaves like a stack. Players can push pieces onto the stack by placing them in a sitting position.
   When a player adds a new piece, it is placed on top of the existing pieces in that cell, preserving the order of placement.
2. Movement Logic:
   Players can move pieces from one cell to another. When moving a stack, the top portion of the stack (one or more pieces) can be shifted to a new cell.
3. Standing Pieces and Blocking:
  Standing pieces cannot be stacked upon and do not count toward the win condition. The standing state is tracked using the isStanding property.
4. Win Condition Check:
   The game checks for a win by verifying if there is a continuous path of sitting pieces of the same color, connecting one side of the board to the opposite side.


