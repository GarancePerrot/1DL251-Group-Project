import pygame
import sys
from game import Game, PlayerColor, PieceType #importing classes from game file 

# Initialize pygame
pygame.init() #init for pygame package 

# Set the dimensions of the game window
WIDTH, HEIGHT = 1000, 800
LINE_WIDTH = 3
CELL_SIZE = WIDTH // 8  # cell size 100
GRID_Y_OFFSET = HEIGHT - CELL_SIZE * 4 # place grid at the bottom
GRID_X_OFFSET = CELL_SIZE * 2

# Colors rgb value 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CREME = (249, 228, 188)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("4-in-a-Row Stacking Game")

# Initialize game
game = Game() #creating an object for Game class

# Fonts
font = pygame.font.SysFont(None, 80)
small_font = pygame.font.SysFont(None, 40)

def draw_grid():
    screen.fill(CREME)

    # Draw grid lines                            X1                 Y1                   X2           Y2
    for i in range(5):
        pygame.draw.line(screen, BLACK, ((i + 2) * CELL_SIZE, GRID_Y_OFFSET), ((i + 2) * CELL_SIZE, HEIGHT), LINE_WIDTH) # vertical lines
        pygame.draw.line(screen, BLACK, (2 * CELL_SIZE, GRID_Y_OFFSET + i * CELL_SIZE), (WIDTH - 2 * CELL_SIZE, GRID_Y_OFFSET + i * CELL_SIZE), LINE_WIDTH) # horizontal lines


def draw_pieces():
    
    for row in range(4):
        for col in range(4):
            piece = game.board[row][col]
            if piece.type != PieceType.EMPTY:
                color = BLACK if piece.type in [PieceType.BLACK_LYING, PieceType.BLACK_STANDING] else WHITE
                x = GRID_X_OFFSET + col * CELL_SIZE + CELL_SIZE // 2 # middle of x axis
                y = GRID_Y_OFFSET + row * CELL_SIZE + CELL_SIZE // 2 # middle of y axis
                if piece.type in [PieceType.BLACK_LYING, PieceType.WHITE_LYING]:
                    pygame.draw.circle(screen, color, (x, y), CELL_SIZE // 3)
                else:
                    pygame.draw.rect(screen, color, (x - CELL_SIZE // 4, y - CELL_SIZE // 4, CELL_SIZE // 2, CELL_SIZE // 2))
                # Draw stack height
                if piece.height > 1:
                    height_text = small_font.render(str(piece.height), True, RED if color == BLACK else BLUE)
                    screen.blit(height_text, (x - height_text.get_width() // 2, y - height_text.get_height() // 2))

def draw_turn_indicator():
    current_player = "Black" if game.get_current_player() == PlayerColor.BLACK else "White"
    turn_text = small_font.render(f"Turn: {current_player}", True, BLACK)
    screen.blit(turn_text, (WIDTH // 2 - turn_text.get_width() // 2, HEIGHT // 4 - turn_text.get_height() // 2))

def draw_piece_counts():
    black_count = game.get_remaining_pieces(PlayerColor.BLACK)
    white_count = game.get_remaining_pieces(PlayerColor.WHITE)
    black_text = small_font.render(f"Black: {black_count} pcs", True, BLACK)
    white_text = small_font.render(f"White: {white_count} pcs", True, BLACK)
    screen.blit(black_text, (10, 10))
    screen.blit(white_text, (WIDTH - white_text.get_width() - 10, 10))

def draw_mode_indicator(place_mode):
    mode_text = small_font.render("Mode: Place" if place_mode else "Mode: Move", True, BLACK)
    screen.blit(mode_text, (WIDTH // 2 - mode_text.get_width() // 2, HEIGHT // 4 + 30))

def draw_game(place_mode):
    draw_grid()
    draw_pieces()
    draw_turn_indicator()
    draw_piece_counts()
    draw_mode_indicator(place_mode)

def handle_click():
    x, y = pygame.mouse.get_pos()
    if y >= GRID_Y_OFFSET:
        row = (y - GRID_Y_OFFSET) // CELL_SIZE
        col = (x - GRID_X_OFFSET) // CELL_SIZE
        return row, col
    return None

def game_loop():
    place_mode = True
    selected_piece = None

    while True:
        draw_game(place_mode)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_position = handle_click()
                if click_position:
                    row, col = click_position
                    current_player = game.get_current_player()
                    
                    if place_mode:
                        # Place a piece
                        is_standing = event.button == 3  # Right-click for standing piece
                        if game.place_piece(row, col, current_player, is_standing):
                            game.switch_turn()
                    else:
                        # Move a piece
                        if selected_piece:
                            from_row, from_col = selected_piece
                            if game.move_piece(from_row, from_col, row, col):
                                game.switch_turn()
                            selected_piece = None
                        else:
                            selected_piece = (row, col)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    place_mode = not place_mode
                    selected_piece = None

        if game.check_win(PlayerColor.BLACK):
            print("Black wins!")
            break
        elif game.check_win(PlayerColor.WHITE):
            print("White wins!")
            break
        elif game.is_draw():
            print("It's a draw!")
            break

        pygame.display.update()

# Start the game
game_loop()
