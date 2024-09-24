import pygame
import sys

# Initialize pygame
pygame.init()

# Set the dimensions of the game window
WIDTH, HEIGHT = 300, 600  # Total height is double now
LINE_WIDTH = 5
CELL_SIZE = WIDTH // 3

# Tic-Tac-Toe grid will be drawn in the bottom half
GRID_Y_OFFSET = HEIGHT // 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe with Turn Indicator")

# Initialize board
board = [["" for _ in range(3)] for _ in range(3)]

# Fonts
font = pygame.font.SysFont(None, 100)
small_font = pygame.font.SysFont(None, 50)

# Draw grid in the bottom half of the screen
def draw_grid():
    screen.fill(WHITE)
    
    # Vertical lines
    pygame.draw.line(screen, BLACK, (CELL_SIZE, GRID_Y_OFFSET), (CELL_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, BLACK, (2 * CELL_SIZE, GRID_Y_OFFSET), (2 * CELL_SIZE, HEIGHT), LINE_WIDTH)
    
    # Horizontal lines
    pygame.draw.line(screen, BLACK, (0, GRID_Y_OFFSET + CELL_SIZE), (WIDTH, GRID_Y_OFFSET + CELL_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, BLACK, (0, GRID_Y_OFFSET + 2 * CELL_SIZE), (WIDTH, GRID_Y_OFFSET + 2 * CELL_SIZE), LINE_WIDTH)

# Draw Xs and Os
def draw_marks():
    for row in range(3):
        for col in range(3):
            if board[row][col] == "X":
                mark = font.render("X", True, RED)
                screen.blit(mark, (col * CELL_SIZE + CELL_SIZE // 4, GRID_Y_OFFSET + row * CELL_SIZE + CELL_SIZE // 8))
            elif board[row][col] == "O":
                mark = font.render("O", True, BLUE)
                screen.blit(mark, (col * CELL_SIZE + CELL_SIZE // 4, GRID_Y_OFFSET + row * CELL_SIZE + CELL_SIZE // 8))

# Show the current player's turn
def draw_turn_indicator(current_turn):
    turn_text = small_font.render(f"Turn: {current_turn}", True, BLACK)
    screen.blit(turn_text, (WIDTH // 2 - turn_text.get_width() // 2, HEIGHT // 4 - turn_text.get_height() // 2))

# Check for a mouse click and place mark
def handle_click():
    x, y = pygame.mouse.get_pos()
    
    # Only register clicks within the grid area
    if y >= GRID_Y_OFFSET:
        row = (y - GRID_Y_OFFSET) // CELL_SIZE
        col = x // CELL_SIZE
        if board[row][col] == "":
            return row, col
    return None

# Main game loop
def game_loop():
    current_turn = "X"
    running = True

    while running:
        draw_grid()
        draw_marks()
        draw_turn_indicator(current_turn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_position = handle_click()
                if click_position:
                    row, col = click_position
                    board[row][col] = current_turn
                    current_turn = "O" if current_turn == "X" else "X"
        
        pygame.display.update()

# Start the game
game_loop()
