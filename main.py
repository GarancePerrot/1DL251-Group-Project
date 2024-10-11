import pygame
import sys
from time import time
import math
from game import Game, PlayerColor, PieceType  # importing classes from game file
from time import time

# Initialize pygame
pygame.init()  # init for pygame package

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600  # The overall dimensions of the game window
GRID_ROWS, GRID_COLS = 4, 4  # 4x4 grid on the game board

# Calculate cell size based on window width
CELL_SIZE = WINDOW_WIDTH // (GRID_COLS + 4)  # Each cell size, leaves margin on both sides
GRID_WIDTH = CELL_SIZE * GRID_COLS  # Total width of the grid (4 cells)
GRID_HEIGHT = CELL_SIZE * GRID_ROWS  # Total height of the grid (4 cells)

# Margins and offsets
MARGIN_BOTTOM = 20  # Margin between the bottom of the grid and the window bottom
LINE_WIDTH = 3  # Line width for the grid lines

# Offsets to center the grid horizontally and place it near the bottom
GRID_X_OFFSET = (WINDOW_WIDTH - GRID_WIDTH) // 2  # Center the grid horizontally
GRID_Y_OFFSET = WINDOW_HEIGHT - GRID_HEIGHT - MARGIN_BOTTOM  # Place the grid near the bottom

# for info
BORDER_RADIUS = 5

# Colors rgb value
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CREME = (249, 228, 188)
DARKER_CREME = (220, 190, 140)
GREEN = (0, 255, 0)
GRAY = (80, 80, 80)

# Set up display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("4-in-a-Row Stacking Game")

# Initialize game
game = Game()  # creating an object for Game class

# Fonts
font = pygame.font.SysFont(None, 80)
small_font = pygame.font.SysFont(None, 40)
error_font = pygame.font.SysFont(None, 30)

selected_piece = None  # Stores the last clicked square
valid_moves = []  # Stores valid adjacent moves



# Draw grid function
def draw_grid(place_mode):
    global selected_piece, valid_moves
    screen.fill(CREME)

    # Draw grid lines and highlight clicked square
    for i in range(5):
        pygame.draw.line(screen, BLACK, ((i + 2) * CELL_SIZE, GRID_Y_OFFSET),
                         ((i + 2) * CELL_SIZE, WINDOW_HEIGHT - MARGIN_BOTTOM), LINE_WIDTH)  # vertical lines
        pygame.draw.line(screen, BLACK, (2 * CELL_SIZE, GRID_Y_OFFSET + i * CELL_SIZE),
                         (WINDOW_WIDTH - 2 * CELL_SIZE, GRID_Y_OFFSET + i * CELL_SIZE), LINE_WIDTH)  # horizontal lines


    # Highlight the clicked square if it exists
    if selected_piece is not None and not place_mode:
        row, col = selected_piece
        x = GRID_X_OFFSET + col * CELL_SIZE
        y = GRID_Y_OFFSET + row * CELL_SIZE

        # Draw a rectangle to highlight the clicked square
        highlight_color = (97, 74, 47)  # Less vibrant brown
        pygame.draw.rect(screen, highlight_color, (x, y, CELL_SIZE, CELL_SIZE), 5)  # 5 pixel border

    # Highlight valid adjacent moves
    if not place_mode:
        for row, col in valid_moves:
            x = GRID_X_OFFSET + col * CELL_SIZE
            y = GRID_Y_OFFSET + row * CELL_SIZE
            pygame.draw.rect(screen, (144, 238, 144), (x, y, CELL_SIZE, CELL_SIZE), 5)  # Light green for valid moves




# Info button
info_button_rect = None  # Global variable
changeView_button_rect = None
Timer_button_rect = None


def draw_unused_pieces():
    # Set the initial position for the unused pieces stack
    stack_x = GRID_X_OFFSET - CELL_SIZE - 20  # Place on the left of the board, leaving a bit of space
    stack_y = GRID_Y_OFFSET + CELL_SIZE * 4 - 5 # Start stacking from the bottom of the board
    piece_height = CELL_SIZE // 2 - 40  # Ensure each piece has the appropriate height (adjusted)
    piece_width = CELL_SIZE // 2 + 20  # Ensure the width matches the side view of the pieces in the grid
    piece_margin = 0  # Set spacing between each piece

    black_unused_count = game.get_remaining_pieces(PlayerColor.BLACK)
    white_unused_count = game.get_remaining_pieces(PlayerColor.WHITE)

    # There are 30 pieces in total, alternating between black and white
    for i in range(30):
        if i < black_unused_count + white_unused_count:
            # Alternate between black and white pieces
            color = WHITE if i % 2 == 0 else BLACK
            # Draw the actual piece with the same width as the side-view pieces in the grid
            pygame.draw.rect(screen, color, (stack_x, stack_y, piece_width, piece_height))
            stack_y -= piece_height + piece_margin  # Move upward to place the next piece




def draw_info_button():
    global info_button_rect  # Use the global variable
    info_button_rect = pygame.Rect(WINDOW_WIDTH - 50, 10, 30, 30)  # Create a rectangle for the button
    pygame.draw.rect(screen, DARKER_CREME, info_button_rect, border_radius=50)  # Draw the button
    # Draw border rect
    pygame.draw.rect(screen, BLACK, info_button_rect, 3, border_radius=50)
    info_text = small_font.render("i", True, BLACK)  # Add text to the button
    screen.blit(info_text, (
    info_button_rect.centerx - info_text.get_width() // 2, info_button_rect.centery - info_text.get_height() // 2))


def draw_restart_button():
    global restart_button_rect  # Use the global variable

    # Align Restart button vertically below the Info button
    restart_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 60, 10, 120, 45) # Below Info button (same size and style)

    pygame.draw.rect(screen, DARKER_CREME, restart_button_rect)  # Same color as Info button
    # Draw border rect
    pygame.draw.rect(screen, BLACK, restart_button_rect, 3, border_radius=BORDER_RADIUS)  
    restart_text = small_font.render("Restart", True, BLACK)  # Same text color as Info button
    screen.blit(restart_text, (restart_button_rect.centerx - restart_text.get_width() // 2, restart_button_rect.centery - restart_text.get_height() // 2))
    
def draw_timer_button(timer):
    global Timer_button_rect # Use the global variable
    Timer_button_rect = pygame.Rect(10, 10, 140, 45) 
    # changeView_button_rect = pygame.Rect(WIDTH - 250, 100, 200, 50) 
    pygame.draw.rect(screen, DARKER_CREME, Timer_button_rect)  # Draw the button
    # Draw border rect
    pygame.draw.rect(screen, BLACK, Timer_button_rect, 3, border_radius=BORDER_RADIUS)
    if timer == "inf":
        string = "Timer: "+timer
    else: 
        string = "Timer: "+timer+"\'"
    Timer_text = small_font.render(string, True, BLACK)  # Add text to the button
    screen.blit(Timer_text, (
    Timer_button_rect.centerx - Timer_text.get_width() // 2, Timer_button_rect.centery - Timer_text.get_height() // 2))



def draw_end_message(winner):
    # Only show "Black Wins" or "White Wins"
    if winner == "Black":
        end_message = "Black Wins!"
    elif winner == "White":
        end_message = "White Wins!"
    else:
        end_message = "It's a Draw!"  # In case of a draw, though it's less likely with your conditions

    # Render the end message
    end_text = small_font.render(end_message, True, BLACK)

    # Place the text to the left of the Restart button
    text_x = restart_button_rect.x - end_text.get_width() - 20  # 20 pixels padding to the left of the Restart button
    text_y = restart_button_rect.centery - end_text.get_height() // 2  # Center vertically with the Restart button

    # Blit the text onto the screen
    screen.blit(end_text, (text_x, text_y))


def draw_changeView_button():
    global changeView_button_rect  # Use the global variable
    changeView_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, 60, 200, 50)  # Create a rectangle for the button
    pygame.draw.rect(screen, DARKER_CREME, changeView_button_rect)  # Draw the button
    # Draw border rect
    pygame.draw.rect(screen, BLACK, changeView_button_rect, 3, border_radius=BORDER_RADIUS)
    changeView_text = small_font.render("Change View", True, BLACK)  # Add text to the button
    screen.blit(changeView_text, (
    changeView_button_rect.centerx - changeView_text.get_width() // 2, changeView_button_rect.centery - changeView_text.get_height() // 2))

# Draw pieces function
def draw_pieces(change_view):
    for row in range(4):
        for col in range(4):
            stack = game.board[row][col].stack

            if len(stack) != 0:
                if change_view:
                    # Side view logic: only show the top 5 pieces
                    game.max_display_pieces = min(len(stack), 5)
                    x = GRID_X_OFFSET + col * CELL_SIZE + 15
                    y = GRID_Y_OFFSET + row * CELL_SIZE + CELL_SIZE - 15

                    # If there are more than 5 pieces, only show the top 5
                    start_index = max(0, len(stack) - 5)

                    # Draw the top 5 pieces starting from the latest one
                    for i in range(start_index, len(stack)):
                        piece = stack[i]
                        color = BLACK if piece.type in [PieceType.BLACK_LYING, PieceType.BLACK_STANDING] else WHITE

                        # Draw lying pieces
                        if piece.type in [PieceType.BLACK_LYING, PieceType.WHITE_LYING]:
                            pygame.draw.rect(screen, color, (x, y, CELL_SIZE // 2 + 20, CELL_SIZE // 2 - 40))
                        else:  # Draw standing pieces with width 1/3 of lying pieces, height is the same
                            standing_width = (CELL_SIZE // 2 + 20) // 3  # Width is 1/3 of lying piece
                            pygame.draw.rect(screen, color, (
                                x + ((CELL_SIZE // 2 + 20) - standing_width) // 2,  # Center the standing piece
                                y, standing_width, CELL_SIZE // 2 - 40))  # Keep the same height

                        y -= CELL_SIZE // 2 - 40  # Move upward for the next piece

                    # If there are more than 5 pieces, show "+n" for the remaining pieces
                    if len(stack) > 5:
                        remaining_pieces = len(stack) - 5
                        text = small_font.render(f"+{remaining_pieces}", True, RED)
                        screen.blit(text, (x, GRID_Y_OFFSET + (row + 1) * CELL_SIZE - text.get_height()))

                else:
                    # Top-down view logic: draw circular pieces and show stack height
                    x = GRID_X_OFFSET + col * CELL_SIZE + CELL_SIZE // 2  # X position
                    y = GRID_Y_OFFSET + row * CELL_SIZE + CELL_SIZE // 2  # Y position

                    # Draw the top piece
                    piece = stack[len(stack) - 1]
                    color = BLACK if piece.type in [PieceType.BLACK_LYING, PieceType.BLACK_STANDING] else WHITE

                    # Draw a circular piece for the top-down view
                    pygame.draw.circle(screen, color, (x, y), CELL_SIZE // 3)

                    # If there is more than one piece, show the stack height
                    if len(stack) > 1:
                        height_text = small_font.render(str(len(stack)), True, RED)
                        screen.blit(height_text, (x - height_text.get_width() // 2, y - height_text.get_height() // 2))

def draw_hovered_stack(mouse_pos):
    hovered_cell = game.get_hovered_cell(mouse_pos, GRID_X_OFFSET, CELL_SIZE)

    if hovered_cell:
        row, col = hovered_cell
        stack = game.board[row][col].stack

        if len(stack) > 0:
            # Display the stack on the right side of the screen, aligned with the unused pieces on the left
            stack_x = WINDOW_WIDTH - CELL_SIZE - 50  # Leave a 50-pixel margin on the right side
            stack_y = GRID_Y_OFFSET + CELL_SIZE * 4 - 5 # Start stacking from the bottom of the board, aligned with the left side

            # Ensure the piece size is consistent with the unused pieces
            piece_height = CELL_SIZE // 2 - 40  # Keep the height consistent with the left side
            piece_width = CELL_SIZE // 2 + 20   # Ensure the width matches the lying pieces in the grid
            piece_margin = 0  # Set the margin between each piece

            # Display pieces in stack order, from bottom to top
            for i in range(len(stack)):
                piece = stack[i]
                color = BLACK if piece.type in [PieceType.BLACK_LYING, PieceType.BLACK_STANDING] else WHITE

                # Display lying pieces
                if piece.type in [PieceType.BLACK_LYING, PieceType.WHITE_LYING]:
                    pygame.draw.rect(screen, color, (stack_x, stack_y, piece_width, piece_height))
                else:  # Handle standing pieces
                    # Standing pieces have 1/3 of the width of lying pieces, with the same height
                    standing_width = piece_width // 3  # Standing piece width is 1/3 of lying piece
                    standing_height = piece_height  # Standing piece height is the same as lying piece

                    # Center the standing piece horizontally and draw it
                    pygame.draw.rect(screen, color, 
                                     (stack_x + (piece_width - standing_width) // 2,  # Center horizontally
                                      stack_y,  # Place it at the correct Y-axis position
                                      standing_width, 
                                      standing_height))

                stack_y -= piece_height + piece_margin  # Move upward and leave space between pieces

            
# Draw turn indicator function
def draw_turn_indicator():
    current_player = "Black" if game.get_current_player() == PlayerColor.BLACK else "White"
    turn_text = small_font.render(f"Turn: {current_player}", True, BLACK)
    screen.blit(turn_text, (WINDOW_WIDTH // 2 - turn_text.get_width() // 2, (WINDOW_HEIGHT + 50) // 5 - turn_text.get_height() // 2))


# Draw piece counts function
def draw_piece_counts():
    black_count = game.get_remaining_pieces(PlayerColor.BLACK)
    white_count = game.get_remaining_pieces(PlayerColor.WHITE)
    black_text = small_font.render(f"Black: {black_count} pcs", True, BLACK)
    white_text = small_font.render(f"White: {white_count} pcs", True, BLACK)
    screen.blit(black_text, (10, 100))
    screen.blit(white_text, (WINDOW_WIDTH - white_text.get_width() - 10, 100))


# Draw mode indicator function
def draw_mode_indicator(place_mode):
    mode_text = small_font.render("Mode: Place" if place_mode else "Mode: Move", True, BLACK)
    screen.blit(mode_text, (WINDOW_WIDTH // 2 - mode_text.get_width() // 2, WINDOW_HEIGHT // 5 + 30))


# TIMER : 
# - User clicks on the "Timer" button (by default set to "inf" = no time limit)
# - A popup displays with choices of inf, 1, 2 , ... , 10 min and user clicks on one
# - The timer value is updated on the button
# - The round begins and the time left for the round is shown under the Timer button (e.g "Time left: 54 s")
# - When time left reaches 0, the current player loses 
#           -> (possible improvements : give option of what happens e.g penalty, random move etc...)
# - The time left is reset to the timer value when :
#           -> A turn changes (other player starts playing)
#           -> Player clicks on "Restart" button
#           -> Player sets a NEW value to the Timer value in the Timer popup
# - The time left is UNCHANGED when:
#           -> Player clicks on "Info" and exits the info popup
#           -> Player clicks on "Timer" and does NOT choose a new value for timer (clicks on "Cancel" button)


#helper for time left
def seconds_to_minutes_seconds(seconds):
  minutes = int(seconds) // 60
  remaining_seconds = int(seconds) % 60
  return str(minutes), str(remaining_seconds)

#draw indicator for time left for the round 
def draw_time_left_indicator(time_left):
    if time_left == "inf" or time_left == "0":
        string = "Time left: "+ time_left
    else : 
        min, sec = seconds_to_minutes_seconds(time_left)
        if min == "0":
            string = "Time left: "+sec+"\'"
        elif sec == "0":
            string = "Time left: "+ min +"\""
        else:
            string = "Time left: "+  min + "\' "+sec+"\""
    font = pygame.font.Font(None, 30) 
    mode_text = font.render(string, True, GRAY)
    # screen.blit(mode_text, (WINDOW_WIDTH // 2 - mode_text.get_width() // 2 - 250 , WINDOW_HEIGHT // 5 + 35))
    screen.blit(mode_text, (14, 60))
    
    

# Draw game function
def draw_game(place_mode,change_view, timer, time_left):
    draw_grid(place_mode)  # This now includes the selected square and valid moves
    draw_unused_pieces()
    draw_hovered_stack(game.mouse_pos)
    draw_info_button()
    draw_timer_button(timer)
    draw_pieces(change_view)
    draw_turn_indicator()
    draw_piece_counts()
    draw_mode_indicator(place_mode)
    draw_changeView_button()
    draw_time_left_indicator(time_left)
    


def draw_error(text, color, row, col, t, text_position=(10, 50)):


    #Get the coordinates for the current cell
    # cell_row, cell_col = current_cell 
    rect_x = GRID_X_OFFSET + col * CELL_SIZE
    rect_y = GRID_Y_OFFSET + row * CELL_SIZE 

    #Split the text at every line break
    lines = text.split("\n")

    # text_position_x = text_position[0]
    # text_position_y = text_position[1]
    text_position_x = 10
    text_position_y = 150

    #Calculate fade factor
    t_delta = time() - t

    f = max(0, min(1, 1 - (t_delta/2)))
    alpha = int(f*255)
    alpha_square = int(f*225)

    #Create transparent surface to draw the red rectangle
    rect_surface = pygame.Surface((CELL_SIZE,CELL_SIZE),pygame.SRCALPHA)
    rect_surface.fill((0,0,0,0))

    #Draw the red rectangle 
    pygame.draw.rect(rect_surface,(255,0,0,alpha_square), (0,0,CELL_SIZE,CELL_SIZE),7)
    screen.blit(rect_surface,(rect_x,rect_y))

    #Draw every line of text on top of each other
    for line in lines:
        msg = error_font.render(line,True,color)
        msg.set_alpha(alpha)
        screen.blit(msg,(text_position_x,text_position_y))
        text_position_y+=msg.get_height()


error_position = None
error_msg = None
error_time = None

def handle_move_click(row, col):
    global selected_piece, valid_moves, error_position, error_msg, error_time


    if selected_piece is None:

        # om vi trycker på en enstaka vit ruta som svart. Gör ingenting (flasha Tommys röda)
        if game.get_top_piece_opposite_color(row, col) or game.board[row][col].stack == []:
            print("Top piece opposite color")

            error_msg = "Invalid move,\nread instructions"
            error_position = (row,col)
            error_time = time()
        else:
            # Select the piece
            selected_piece = (row, col)
            valid_moves = game.get_valid_moves(row, col)
    elif selected_piece == (row, col):
        # Deselect the piece if the same square is clicked again
        reset_moves_preview_visuals()
    elif (row, col) in valid_moves:
        # Move the piece if the destination is valid
        from_row, from_col = selected_piece
        if game.move_piece(from_row, from_col, row, col):

            # Potential problem when moving with stacks. Make a check first. Right now we use booleans. 
            # Could return remaining pieces instead. Switch turns if zero.
            game.switch_turn()
            reset_moves_preview_visuals()
    elif (row, col) not in valid_moves:
        print("Square not in valid moves")

        error_msg = "Invalid move,\nread instructions"
        error_position = (row,col)
        error_time = time()


def reset_moves_preview_visuals():
    global selected_piece, valid_moves
    selected_piece = None
    valid_moves = []


# Handle mouse click function
def handle_click():
    global selected_piece, valid_moves
    x, y = pygame.mouse.get_pos()

    # Check if the click is on the grid
    if y >= GRID_Y_OFFSET and x >= GRID_X_OFFSET and y <= WINDOW_HEIGHT - MARGIN_BOTTOM and x <= WINDOW_WIDTH - GRID_X_OFFSET:
        row = (y - GRID_Y_OFFSET) // CELL_SIZE
        col = (x - GRID_X_OFFSET) // CELL_SIZE
        return row, col

    
    # Check if the click is on the Info, Change View, or Restart buttons
    global info_button_rect, changeView_button_rect, restart_button_rect
    
    global Timer_button_rect
    
    if info_button_rect and info_button_rect.collidepoint(x, y):
        return "Info Button"
    if changeView_button_rect and changeView_button_rect.collidepoint(x, y):
        return "ChangeView Button"
    if Timer_button_rect and Timer_button_rect.collidepoint(x, y):
        return "Timer Button"
    if restart_button_rect and restart_button_rect.collidepoint(x, y):
        return "Restart Button"

    return None




# Draw popup with rules
def draw_popup():
    # Draw a slightly less transparent overlay
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))  # Less transparent black
    screen.blit(overlay, (0, 0))

        # Increase the size of the popup box (make it larger to fit the text better)
    popup_rect = pygame.Rect(WINDOW_WIDTH // 8, WINDOW_HEIGHT // 8, WINDOW_WIDTH * 3 // 4, WINDOW_HEIGHT * 3 // 4)
    pygame.draw.rect(screen, WHITE, popup_rect)

   # Adjust the size of the popup title
    title_font = pygame.font.SysFont(None, 50)  # Smaller header size for better fitting
    title = title_font.render("GAME RULES", True, BLACK)
    # screen.blit(title, (popup_rect.centerx - title.get_width() // 2 , popup_rect.y + 20))
    screen.blit(title, (popup_rect.centerx - title.get_width() // 2 , popup_rect.y + 12))

    # Reduce text size and wrap it within the popup
    rule_font = pygame.font.SysFont(None, 25)  # Smaller text size for better readability
    rules = [
        "• Goal: Create a path from one side of the board to the opposite side.",
        "• Setup: Each player has 15 pieces to place on the 4x4 grid.",
        "• Gameplay:                                              ",
        "  - Players take turns placing or moving pieces.",
        "  - Pieces can be placed either lying or standing.",
        "  - Left-click to place a lying piece, right-click to place a standing piece.",
        "  - Pieces can stack up to 4 high, but only lying pieces can form a path.",
        "  - After placing all pieces, players can move their pieces to continue playing.",
    ]

    # Render and wrap text within the popup window
    y_offset = 55  # Start y position for rules
    line_spacing = 12  # Decrease line spacing for better readability
    for rule in rules:
        wrapped_text = wrap_text(rule, rule_font, popup_rect.width - 40)  # Wrap text manually
        for line in wrapped_text:
            rule_text = rule_font.render(line, True, BLACK)
            screen.blit(rule_text, (popup_rect.x + 20, popup_rect.y + y_offset))
            y_offset += rule_text.get_height() + line_spacing  # Add reduced line spacing between lines

    # Draw the Close button (change color to cream, with black text and border)
    # button_rect = pygame.Rect(popup_rect.centerx - 100, popup_rect.y + popup_rect.height - 80, 200, 50)
    button_rect = pygame.Rect(popup_rect.centerx - 55, popup_rect.y + popup_rect.height - 48, 110, 32)
    pygame.draw.rect(screen, CREME, button_rect)  # Change button color to cream
    pygame.draw.rect(screen, BLACK, button_rect, 3)  # Add black border around the button
    button_text = rule_font.render("Close", True, BLACK)  # Set font color to black
    screen.blit(button_text, (
    button_rect.centerx - button_text.get_width() // 2, button_rect.centery - button_text.get_height() // 2))

    return button_rect

# Draw popup for optional timer
def draw_popup_timer():
    # The button title will have the current timer (default inf) "Timer: inf"
    
    # Draw a slightly less transparent overlay
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))  # Less transparent black
    screen.blit(overlay, (0, 0))
    

    # Increase the size of the popup box
    popup_rect = pygame.Rect(WINDOW_WIDTH // 6, WINDOW_HEIGHT // 6, WINDOW_WIDTH * 2// 3, WINDOW_HEIGHT * 2 // 3)
    pygame.draw.rect(screen, WHITE, popup_rect)

    # Adjust the size of the popup title
    title_font = pygame.font.SysFont(None, 50)  
    title = title_font.render("SET TIMER", True, BLACK)
    screen.blit(title, (popup_rect.centerx - title.get_width() // 2, popup_rect.y + 12))

    text_font = pygame.font.SysFont(None, 30)
    text = text_font.render("Select a timer (in minutes) for each game round:", True, BLACK)
    screen.blit(text, (popup_rect.centerx - text.get_width() // 2, popup_rect.y + 100))

    #array with 0 to 10 minute buttons aligned in a row:
    button_width = 40  
    button_height = 40  
    spacing = 8  
    total_width = 11 * button_width + 10 * spacing  # Total width of all buttons and spaces
    
    start_x = popup_rect.centerx - total_width // 2  # Starting x-position to center the buttons
    button_y = popup_rect.y + popup_rect.height // 2  # Adjust the y-position of the buttons

    # Timer buttons (0 to 10 minutes)
    timer_array = [pygame.Rect(start_x + i * (button_width + spacing), button_y, button_width, button_height) for i in range(11)]
    
    #handle first button (infinity):
    pygame.draw.rect(screen, CREME, timer_array[0])
    pygame.draw.rect(screen, BLACK, timer_array[0], 3)  # Add black border around the button
    nb = text_font.render("inf", True, BLACK)
    screen.blit(nb, (timer_array[0].centerx - nb.get_width() // 2, timer_array[0].centery - nb.get_height() // 2))
    
    for i in range(1,11):
        pygame.draw.rect(screen, CREME, timer_array[i])
        pygame.draw.rect(screen, BLACK, timer_array[i], 3)  # Add black border around the button
        nb = text_font.render(str(i), True, BLACK)
        screen.blit(nb, (timer_array[i].centerx - nb.get_width() // 2, timer_array[i].centery - nb.get_height() // 2))
    

    # Draw the Cancel button below the timer buttons
    button_rect = pygame.Rect(popup_rect.centerx - 55, popup_rect.y + popup_rect.height - 48, 110, 32)
    pygame.draw.rect(screen, CREME, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 3)  # Add black border around the button
    button_text = text_font.render("Cancel", True, BLACK)
    screen.blit(button_text, (
        button_rect.centerx - button_text.get_width() // 2, button_rect.centery - button_text.get_height() // 2))
    

    return button_rect, timer_array




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
    popup_open = False  # Popup state (for info button)
    popup_2_open = False # popup state (for setting optional timer)
    change_view = True  # Default view is side view
    game_end = False  # Track if the game is over
    winner = None  # Track the winner
    global selected_piece
    global valid_moves
    global error_msg,error_position,error_time
    global valid_moves
    timer = "inf" #infinity  = no timer by default
    
    start = time() 
    print("START: ", + start)
    flag = 0  

    while True:
        
        game.mouse_pos = pygame.mouse.get_pos()  # Gets the current mouse position

        #setting a timer for the round :
                    
        if timer == "inf":
            duration = math.inf
        else : 
            duration = float(timer) * 60 #convert in seconds
        
        
        #print("time() - start : " , time()- start, " < ? , duration : ", duration)
        if time() - start >= duration and winner == None: #and time exceeded
            #current player loses :
            current_player = game.current_player
            print(current_player)
            if current_player == PlayerColor.BLACK:
                winner = "White"
            else:
                winner = "Black"
            game_end = True
            time_left = "0"
            
        #simplify time left for the round to show user
        if timer == "inf" and winner == None:
            time_left = "inf"
        elif winner == None:
            time_left = str(int(duration - time()+start))
            
                
        draw_game(place_mode,change_view, timer, time_left)
        draw_restart_button()
        
        if error_msg:
            draw_error(error_msg,BLACK,error_position[0],error_position[1],error_time)

            if time() - error_time > 2:
                error_msg = None
                error_position = None
                error_time = None

        if game_end:
            draw_end_message(winner)  # Displays a prompt at the end of the game
            time_left = "0"


        if popup_open:
            button_rect = draw_popup()  # Draw the popup for rules and get the button rect
            
        if popup_2_open:
            button_rect_2, timer_array = draw_popup_timer()
            
        # Check the grid over which the mouse hovers and display all the pieces in the stack in the specified area
        draw_hovered_stack(game.mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
                
            # Detect the Restart button click (even when the game is over)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Click the Restart button to restart the game at any time
                if restart_button_rect.collidepoint(mouse_x, mouse_y):
                    game.restart_game()  
                    game_end = False  # Reset the game end state
                    winner = None  # Reset winner
                    time_left = "0"
                    start = time()
                    continue  # Restart the game loop

                # If the game is over, the placement or movement of pieces is no longer handled
                if game_end:
                    time_left = "0"
                    continue


            if not popup_open and not popup_2_open:  # Don't process game events when popup is open
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_position = handle_click()

                    if click_position == "Info Button":
                        print("Info button clicked")
                        popup_open = not popup_open
                        
                    elif click_position == "Restart Button":
                        print("Restart button clicked")
                        game.restart_game()  # Reset the game
                        reset_moves_preview_visuals()
                        print("Game restarted")
                        
                    elif click_position == "ChangeView Button":
                        print("Change View button clicked")
                        change_view = not change_view
                        
                    elif click_position == "Timer Button":
                        print("Timer button clicked")
                        popup_2_open = not popup_2_open
                        
                    elif click_position != "Info Button" and click_position is not None:
                        row, col = click_position
                        current_player = game.get_current_player()
                        
                        #current player makes an action : 
                        if place_mode:
                            # Place a piece
                            is_standing = event.button == 3  # Right-click for standing piece
                            if game.place_piece(row, col, current_player, is_standing):
                                game.switch_turn()
                                reset_moves_preview_visuals()
                                start = time()  #restart counter
                        else:
                            start = time()
                            handle_move_click(row, col)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        place_mode = not place_mode
                        selected_piece = None
                    elif event.key == pygame.K_p:  # Press 'P' to open the popup
                        popup_open = True

            elif popup_open:  # When popup for rules is open
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        popup_open = False  # Close the popup when button is clicked
                #PRESS ESC TO CLOSE DOWN POPUP
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        popup_open = False

            else: #popup for timer is open
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    #1) here we search which time button does input_rect correspond to
                    #2) store it in current timer
                    #3) then close the popup
                    
                    if timer_array[0].collidepoint(mouse_x, mouse_y):
                            timer = "inf"
                            start = time() #restart counter after closing popup
                    
                    for i in range(1,11):
                        if timer_array[i].collidepoint(mouse_x, mouse_y):
                            timer = str(i)
                            start = time() #restart counter after closing popup
                    
                    popup_2_open = False
                    
                            
                    # else : user clicks on cancel button
                    if button_rect_2.collidepoint(mouse_x, mouse_y):
                        popup_2_open = False  
                        
                
                    
                

        if not game_end:
            if game.check_win_dfs(PlayerColor.BLACK):
                winner = "Black"
                game_end = True
                time_left = "0"
            elif game.check_win_dfs(PlayerColor.WHITE):
                winner = "White"
                game_end = True
                time_left = "0"
            elif game.is_draw():
                game_end = True
                time_left = "0"

        pygame.display.update()


# Start the game
game_loop()
