import pygame
import sys

# Initialize Pygame
pygame.init()

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

# Set the window size
WINDOW_SIZE = 400
GRID_SIZE = 4
CELL_SIZE = WINDOW_SIZE // GRID_SIZE

# Create window
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 100))  # Add space for the text and restart button
pygame.display.set_caption("4x4 Board Game")

# Initialize the board with 0 for empty, 1 for player 1 (black), and 2 for player 2 (white)
board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
current_player = 1  # Player 1 starts (black)
game_over = False  # Track game state
winner = None  # To track the winning player
draw = False  # Track if it's a draw

# Font for the text
font = pygame.font.SysFont(None, 36)

# Draw a chessboard
def draw_board():
    screen.fill(WHITE)
    # Draw the grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)
            # Draw the player's pieces as squares
            if board[row][col] == 1:  # Black piece
                pygame.draw.rect(screen, BLACK, rect.inflate(-10, -10))  # Smaller black square
            elif board[row][col] == 2:  # White piece
                pygame.draw.rect(screen, GRAY, rect.inflate(-10, -10))  # Smaller white square

    # Draw the current player turn text if the game is not over
    if not game_over and not draw:
        text = font.render(f"Player {current_player}'s Turn ({'Black' if current_player == 1 else 'White'})", True, BLACK)
        screen.blit(text, (10, WINDOW_SIZE + 10))

# Depth First Search to check if the player has a valid path connecting two sides
def dfs(player, row, col, visited, side_flags):
    visited[row][col] = True

    # Check if the piece is on one of the four sides
    if row == 0:
        side_flags['top'] = True
    if row == GRID_SIZE - 1:
        side_flags['bottom'] = True
    if col == 0:
        side_flags['left'] = True
    if col == GRID_SIZE - 1:
        side_flags['right'] = True

    # Check only within a continuous path of the player's pieces
    if (side_flags['top'] and side_flags['bottom']) or (side_flags['left'] and side_flags['right']):
        return True

    # Define the directions for DFS: right, left, down, up
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE and not visited[new_row][new_col] and board[new_row][new_col] == player:
            if dfs(player, new_row, new_col, visited, side_flags):
                return True

    return False

# Check if the player has won using DFS
def check_win_dfs(player):
    visited = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    # Initialize flags to track which sides are connected
    side_flags = {'top': False, 'bottom': False, 'left': False, 'right': False}

    # Traverse the board to find all positions for current player
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == player and not visited[row][col]:
                side_flags = {'top': False, 'bottom': False, 'left': False, 'right': False}  # Reset for each path
                if dfs(player, row, col, visited, side_flags):
                    return True
    return False

# Check if the board is full
def is_board_full():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 0:
                return False
    return True

# Draw the restart button and the winner or draw message
def draw_restart_button():
    pygame.draw.rect(screen, GREEN, (150, WINDOW_SIZE + 50, 100, 40))
    text = font.render("Restart", True, BLACK)
    screen.blit(text, (160, WINDOW_SIZE + 50))
    # Display the winner or draw message
    if winner:
        winner_text = font.render(f"Player {winner} Wins!", True, BLACK)
        screen.blit(winner_text, (120, WINDOW_SIZE + 70))
    elif draw:
        draw_text = font.render("It's a Draw!", True, BLACK)
        screen.blit(draw_text, (140, WINDOW_SIZE + 70))

# Restart the game
def restart_game():
    global board, current_player, game_over, winner, draw
    board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    current_player = 1  # Reset to player 1
    game_over = False
    winner = None  # Reset winner
    draw = False  # Reset draw flag

# Main game loop
def main():
    global current_player, game_over, winner, draw
    running = True
    while running:
        draw_board()

        # If the game is over, draw the restart button and winner message
        if game_over or draw:
            draw_restart_button()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse click position
                mouseX, mouseY = pygame.mouse.get_pos()

                # If game is over or draw, check if the restart button is clicked
                if game_over or draw:
                    if 150 <= mouseX <= 250 and WINDOW_SIZE + 50 <= mouseY <= WINDOW_SIZE + 90:
                        restart_game()

                # If the game is not over and click is inside the grid, place the piece
                if not game_over and not draw and mouseY < WINDOW_SIZE:
                    col = mouseX // CELL_SIZE
                    row = mouseY // CELL_SIZE

                    # If the clicked grid is empty, place the piece
                    if board[row][col] == 0:
                        board[row][col] = current_player

                        # Check if the current player wins using DFS
                        if check_win_dfs(current_player):
                            print(f"Player {current_player} wins!")
                            game_over = True
                            winner = current_player  # Store the winning player
                        # Check for a draw if the board is full
                        elif is_board_full():
                            print("It's a Draw!")
                            draw = True

                        # Switch players if game is not over
                        if not game_over and not draw:
                            current_player = 2 if current_player == 1 else 1

if __name__ == "__main__":
    main()
