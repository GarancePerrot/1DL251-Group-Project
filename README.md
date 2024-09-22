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
