import pygame
import sys
from game import Game, PlayerColor, PieceType  # importing classes from game file

# Initialize pygame
pygame.init()  # init for pygame package

# Set the dimensions of the game window
WIDTH, HEIGHT = 800, 600
MARGIN_BOTTOM = 20
LINE_WIDTH = 3
CELL_SIZE = WIDTH // 8  # cell size 100
GRID_Y_OFFSET = HEIGHT - CELL_SIZE * 4 - MARGIN_BOTTOM  # place grid at the bottom
GRID_X_OFFSET = CELL_SIZE * 2

# Colors rgb value
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CREME = (249, 228, 188)
DARKER_CREME = (220, 190, 140)
GREEN = (0, 255, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("4-in-a-Row Stacking Game")

# Initialize game
game = Game()  # creating an object for Game class

# Fonts
font = pygame.font.SysFont(None, 80)
small_font = pygame.font.SysFont(None, 40)


# Draw grid function
def draw_grid():
    screen.fill(CREME)

    # Draw grid lines                            X1                 Y1                   X2           Y2
    for i in range(5):
        pygame.draw.line(screen, BLACK, ((i + 2) * CELL_SIZE, GRID_Y_OFFSET),
                         ((i + 2) * CELL_SIZE, HEIGHT - MARGIN_BOTTOM), LINE_WIDTH)  # vertical lines
        pygame.draw.line(screen, BLACK, (2 * CELL_SIZE, GRID_Y_OFFSET + i * CELL_SIZE),
                         (WIDTH - 2 * CELL_SIZE, GRID_Y_OFFSET + i * CELL_SIZE), LINE_WIDTH)  # horizontal lines


# Info button
info_button_rect = None  # Global variable
changeView_button_rect = None

def draw_info_button():
    global info_button_rect  # Use the global variable
    info_button_rect = pygame.Rect(WIDTH // 2 - 50, 10, 100, 40)  # Create a rectangle for the button
    pygame.draw.rect(screen, DARKER_CREME, info_button_rect)  # Draw the button
    # Draw border rect
    pygame.draw.rect(screen, BLACK, info_button_rect, 3)
    info_text = small_font.render("Info", True, BLACK)  # Add text to the button
    screen.blit(info_text, (
    info_button_rect.centerx - info_text.get_width() // 2, info_button_rect.centery - info_text.get_height() // 2))


def draw_changeView_button():
    global changeView_button_rect  # Use the global variable
    changeView_button_rect = pygame.Rect(WIDTH - 250, 100, 200, 50)  # Create a rectangle for the button
    pygame.draw.rect(screen, DARKER_CREME, changeView_button_rect)  # Draw the button
    # Draw border rect
    pygame.draw.rect(screen, BLACK, changeView_button_rect, 3)
    changeView_text = small_font.render("Change View", True, BLACK)  # Add text to the button
    screen.blit(changeView_text, (
    changeView_button_rect.centerx - changeView_text.get_width() // 2, changeView_button_rect.centery - changeView_text.get_height() // 2))

# Draw pieces function
def draw_pieces(change_view):
    for row in range(4):
        for col in range(4):
            # piece = game.board[row][col]
            # if piece.type != PieceType.EMPTY:
            #     color = BLACK if piece.type in [PieceType.BLACK_LYING, PieceType.BLACK_STANDING] else WHITE
            #     x = GRID_X_OFFSET + col * CELL_SIZE + CELL_SIZE // 2  # middle of x axis
            #     y = GRID_Y_OFFSET + row * CELL_SIZE + CELL_SIZE // 2  # middle of y axis
            #     if piece.type in [PieceType.BLACK_LYING, PieceType.WHITE_LYING]:
            #         pygame.draw.circle(screen, color, (x, y), CELL_SIZE // 3)
            #     else:
            #         pygame.draw.rect(screen, color,
            #                          (x - CELL_SIZE // 4, y - CELL_SIZE // 4, CELL_SIZE // 2, CELL_SIZE // 2))
            #     # Draw stack height
            #     if piece.height > 1:
            #         height_text = small_font.render(str(piece.height), True, RED if color == BLACK else BLUE)
            #         screen.blit(height_text, (x - height_text.get_width() // 2, y - height_text.get_height() // 2))
            stack = game.board[row][col]
            if stack.height != 0:
                if change_view:
                    x = GRID_X_OFFSET + col * CELL_SIZE + 15
                    y = GRID_Y_OFFSET + row * CELL_SIZE + CELL_SIZE - 15
                    for i,piece in enumerate(stack.stack):
                        if stack.stack[i].type == PieceType.EMPTY:
                            continue
                        color = BLACK if stack.stack[i].type in [PieceType.BLACK_LYING,
                                PieceType.BLACK_STANDING] else WHITE
                        type = stack.stack[i].type
                        if type in [PieceType.BLACK_LYING, PieceType.WHITE_LYING]:
                            pygame.draw.rect(screen, color,
                                             (x, y, CELL_SIZE // 2 + 20, CELL_SIZE // 2 - 40))
                            y -= CELL_SIZE // 2 - 40 + 5
                        else:
                            pygame.draw.rect(screen, color,
                                             (x +25, y - 20, CELL_SIZE // 2 - 30, CELL_SIZE // 2 - 20))
                            y -= CELL_SIZE // 2 - 40 + 5
                else:
                    color = BLACK if stack.stack[stack.height - 1].type in [PieceType.BLACK_LYING,
                                                                            PieceType.BLACK_STANDING] else WHITE
                    x = GRID_X_OFFSET + col * CELL_SIZE + CELL_SIZE // 2  # middle of x axis
                    y = GRID_Y_OFFSET + row * CELL_SIZE + CELL_SIZE // 2  # middle of y axis
                    if stack.stack[stack.height - 1].type in [PieceType.BLACK_LYING, PieceType.WHITE_LYING]:
                            pygame.draw.circle(screen, color, (x, y), CELL_SIZE // 3)
                    else:
                        pygame.draw.rect(screen, color,
                                         (x - CELL_SIZE // 4, y - CELL_SIZE // 4, CELL_SIZE // 2, CELL_SIZE // 2))
                    # Draw stack height
                    if stack.height > 1:
                        height_text = small_font.render(str(stack.height), True, RED if color == BLACK else BLUE)
                        screen.blit(height_text,
                                    (x - height_text.get_width() // 2, y - height_text.get_height() // 2))


# Draw turn indicator function
def draw_turn_indicator():
    current_player = "Black" if game.get_current_player() == PlayerColor.BLACK else "White"
    turn_text = small_font.render(f"Turn: {current_player}", True, BLACK)
    screen.blit(turn_text, (WIDTH // 2 - turn_text.get_width() // 2, HEIGHT // 5 - turn_text.get_height() // 2))


# Draw piece counts function
def draw_piece_counts():
    black_count = game.get_remaining_pieces(PlayerColor.BLACK)
    white_count = game.get_remaining_pieces(PlayerColor.WHITE)
    black_text = small_font.render(f"Black: {black_count} pcs", True, BLACK)
    white_text = small_font.render(f"White: {white_count} pcs", True, BLACK)
    screen.blit(black_text, (10, 10))
    screen.blit(white_text, (WIDTH - white_text.get_width() - 10, 10))


# Draw mode indicator function
def draw_mode_indicator(place_mode):
    mode_text = small_font.render("Mode: Place" if place_mode else "Mode: Move", True, BLACK)
    screen.blit(mode_text, (WIDTH // 2 - mode_text.get_width() // 2, HEIGHT // 5 + 30))

def draw_mode_indicator(place_mode):
    mode_text = small_font.render("Mode: Place" if place_mode else "Mode: Move", True, BLACK)
    screen.blit(mode_text, (WIDTH // 2 - mode_text.get_width() // 2, HEIGHT // 5 + 30))

# Draw game function
def draw_game(place_mode,change_view):
    draw_grid()
    draw_info_button()
    draw_pieces(change_view)
    draw_turn_indicator()
    draw_piece_counts()
    draw_mode_indicator(place_mode)
    draw_changeView_button()


# Handle mouse click function
def handle_click():
    x, y = pygame.mouse.get_pos()

    # Check if the click is on the grid
    if y >= GRID_Y_OFFSET:
        row = (y - GRID_Y_OFFSET) // CELL_SIZE
        col = (x - GRID_X_OFFSET) // CELL_SIZE
        return row, col

    # Check if the click is on the Info button
    global info_button_rect  # Access the global variable
    global changeView_button_rect
    if info_button_rect and info_button_rect.collidepoint(x, y):
        return "Info Button"
    if changeView_button_rect and changeView_button_rect.collidepoint(x, y):
        return "ChangeView Button"

    return None


# Draw popup with rules
def draw_popup():
    # Draw a slightly less transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))  # Less transparent black
    screen.blit(overlay, (0, 0))

    # Increase the size of the popup box
    popup_rect = pygame.Rect(WIDTH // 6, HEIGHT // 6, WIDTH * 2 // 3, HEIGHT * 2 // 3)
    pygame.draw.rect(screen, WHITE, popup_rect)

    # Adjust the size of the popup title
    title_font = pygame.font.SysFont(None, 60)  # Smaller header size
    title = title_font.render("Game Rules", True, BLACK)
    screen.blit(title, (popup_rect.centerx - title.get_width() // 2, popup_rect.y + 20))

    # Reduce text size and wrap it within the popup
    rule_font = pygame.font.SysFont(None, 30)  # Smaller text size for readability
    rules = [
        "• The goal is to create a path from one side of the board to the other.",
        "• Each player has 15 pieces to place on the 4x4 grid.",
        "• Players can either move or place a piece each turn.",
        "• Players can place pieces either lying down or standing.",
        "• Left-click to place a lying piece, right-click for standing.",
        "• Pieces can stack up to 4 high, but only lying pieces can form a row.",
        "• After placing all pieces, players can move their pieces to continue playing."
    ]

    # Render and wrap text within the popup window
    y_offset = 100  # Start y position for rules
    for rule in rules:
        wrapped_text = wrap_text(rule, rule_font, popup_rect.width - 40)  # Wrap text manually
        for line in wrapped_text:
            rule_text = rule_font.render(line, True, BLACK)
            screen.blit(rule_text, (popup_rect.x + 20, popup_rect.y + y_offset))
            y_offset += rule_text.get_height() + 10  # Add spacing between lines

    # Draw the Close button
    button_rect = pygame.Rect(popup_rect.centerx - 100, popup_rect.y + popup_rect.height - 80, 200, 50)
    pygame.draw.rect(screen, GREEN, button_rect)
    button_text = rule_font.render("Close", True, BLACK)
    screen.blit(button_text, (
    button_rect.centerx - button_text.get_width() // 2, button_rect.centery - button_text.get_height() // 2))

    return button_rect


# Helper function to wrap text into lines
def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "

    if current_line:
        lines.append(current_line.strip())

    return lines


# Game loop function
def game_loop():
    place_mode = True
    selected_piece = None
    popup_open = False  # Popup state
    change_view = False

    while True:
        draw_game(place_mode,change_view)

        if popup_open:
            button_rect = draw_popup()  # Draw the popup and get the button rect

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not popup_open:  # Don't process game events when popup is open
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_position = handle_click()
                    print(click_position)

                    if click_position == "Info Button":
                        print("Info button clicked")
                        popup_open = not popup_open
                    elif click_position == "ChangeView Button":
                        print("Change View button clicked")
                        change_view = not change_view
                    elif click_position != "Info Button" and click_position is not None:
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
                    elif event.key == pygame.K_p:  # Press 'P' to open the popup
                        popup_open = True

            else:  # When popup is open
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        popup_open = False  # Close the popup when button is clicked

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
