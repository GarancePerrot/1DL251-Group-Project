from enum import Enum


class PieceType(Enum):
    EMPTY = 0
    BLACK_LYING = 1
    BLACK_STANDING = 2
    WHITE_LYING = 3
    WHITE_STANDING = 4


class PlayerColor(Enum):
    BLACK = 0
    WHITE = 1

MAX_STACK_HEIGHT = 30
class Stack():
    def __init__(self):
        self.stack = []


class Piece:
    def __init__(self, type=PieceType.EMPTY):
        self.type = type
        


class Game:
    def __init__(self):
        self.GRID_SIZE = 4
        self.MAX_STACK_HEIGHT = 4
        self.board = [[Stack() for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        self.current_player = PlayerColor.BLACK
        self.black_pieces_left = 15
        self.white_pieces_left = 15

    def place_piece(self, row, col, color, is_standing):
        if not self.is_valid_placement(row, col):
            return False

        piece_type = PieceType.BLACK_STANDING if color == PlayerColor.BLACK and is_standing else \
            PieceType.BLACK_LYING if color == PlayerColor.BLACK else \
                PieceType.WHITE_STANDING if is_standing else PieceType.WHITE_LYING

        stack = self.board[row][col]
        stack.stack.append(Piece(piece_type))

        if color == PlayerColor.BLACK:
            self.black_pieces_left -= 1
        else:
            self.white_pieces_left -= 1

        return True

    def get_top_piece_opposite_color(self, row, col):
        current_player = self.get_current_player()

        if len(self.board[row][col].stack) > 0:
            top_piece = self.board[row][col].stack[-1]
            if current_player == PlayerColor.BLACK:
                return top_piece.type in [PieceType.WHITE_LYING, PieceType.WHITE_STANDING]
            else:
                return top_piece.type in [PieceType.BLACK_LYING, PieceType.BLACK_STANDING]


    def move_piece(self, from_row, from_col, to_row, to_col):
        stack = self.board[from_row][from_col].stack
        if len(stack) > 0:
            if not self.is_valid_move(from_row, from_col, to_row, to_col) or stack[0].type == PieceType.EMPTY:
                return False

        # Move the top piece from the source stack to the destination stack
        source_stack = self.board[from_row][from_col].stack
        dest_stack = self.board[to_row][to_col].stack

        # Check if destination stack has space
        if len(dest_stack) < MAX_STACK_HEIGHT:
            for i in range(len(source_stack) - 1, -1, -1):
                if source_stack[i].type == PieceType.BLACK_STANDING and self.current_player == PlayerColor.BLACK:
                    break
                    #FIXFIXFIX

            """ PieceType.BLACK_STANDING if color == PlayerColor.BLACK and is_standing else \
            PieceType.BLACK_LYING if color == PlayerColor.BLACK else \
                PieceType.WHITE_STANDING if is_standing else PieceType.WHITE_LYING """
            #förut
            dest_stack.append(source_stack[-1])
            source_stack.pop()

        return True

    # Depth First Search to check if the player has a valid path connecting two sides
    def dfs(self, player, row, col, visited, side_flags):
        visited[row][col] = True

        # Get the top piece type at the current position
        top_piece = self.board[row][col].stack[-1] if len(self.board[row][col].stack) > 0 else None

        # Check if the piece is the correct type (only lying pieces count for win condition)
        if top_piece is None or (player == PlayerColor.BLACK and top_piece.type != PieceType.BLACK_LYING) or \
        (player == PlayerColor.WHITE and top_piece.type != PieceType.WHITE_LYING):
            return False

        # Check if the piece is on one of the four sides
        if row == 0:
            side_flags['top'] = True
        if row == self.GRID_SIZE - 1:
            side_flags['bottom'] = True
        if col == 0:
            side_flags['left'] = True
        if col == self.GRID_SIZE - 1:
            side_flags['right'] = True

        # If either top-bottom or left-right are connected, the player wins
        if (side_flags['top'] and side_flags['bottom']) or (side_flags['left'] and side_flags['right']):
            return True

        # Define the directions for DFS: right, left, down, up
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.GRID_SIZE and 0 <= new_col < self.GRID_SIZE and not visited[new_row][new_col]:
                if self.dfs(player, new_row, new_col, visited, side_flags):
                    return True

        return False


    # Check if the player has won using DFS
    def check_win_dfs(self, player):
        visited = [[False for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
    
        # Initialize flags to track which sides are connected
        side_flags = {'top': False, 'bottom': False, 'left': False, 'right': False}

        # Traverse the board to find all positions for current player
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                if len(self.board[row][col].stack) > 0:  # Check if there is any piece on this position
                    top_piece = self.board[row][col].stack[-1]
                    if (player == PlayerColor.BLACK and top_piece.type in [PieceType.BLACK_LYING, PieceType.BLACK_STANDING]) or \
                        (player == PlayerColor.WHITE and top_piece.type in [PieceType.WHITE_LYING, PieceType.WHITE_STANDING]):
                        if not visited[row][col]:
                            side_flags = {'top': False, 'bottom': False, 'left': False, 'right': False}  # Reset for each path
                            if self.dfs(player, row, col, visited, side_flags):
                                return True
        return False


    def is_draw(self):
        return self.black_pieces_left == 0 and self.white_pieces_left == 0

    def switch_turn(self):
        self.current_player = PlayerColor.WHITE if self.current_player == PlayerColor.BLACK else PlayerColor.BLACK

    def get_current_player(self):
        return self.current_player

    def get_remaining_pieces(self, color):
        return self.black_pieces_left if color == PlayerColor.BLACK else self.white_pieces_left

    def get_valid_moves(self, row, col):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up
        moves = []

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.GRID_SIZE and 0 <= new_col < self.GRID_SIZE:
                # Check if the move is within bounds and if the stack height is less than MAX_STACK_HEIGHT
                if len(self.board[new_row][new_col].stack) < MAX_STACK_HEIGHT:
                    # Check if there is any piece in the stack and if it's not a standing piece
                    if len(self.board[new_row][new_col].stack) > 0:
                        top_piece = self.board[new_row][new_col].stack[-1].type
                        if top_piece in [PieceType.BLACK_STANDING, PieceType.WHITE_STANDING]:
                            continue  # Skip adding this move if it's a standing piece
                    moves.append((new_row, new_col))

        return moves

    def is_valid_move(self, from_row, from_col, to_row, to_col):
        # Check if the target move is in the list of valid moves from the starting position
        return (to_row, to_col) in self.get_valid_moves(from_row, from_col)

    
    def is_valid_placement(self, row, col):
        # Check if the stack height is less than MAX_STACK_HEIGHT
        if len(self.board[row][col].stack) >= MAX_STACK_HEIGHT:
            return False

        # Check if the top piece is not a standing piece
        if len(self.board[row][col].stack) > 0:
            top_piece = self.board[row][col].stack[-1].type
            if top_piece in [PieceType.BLACK_STANDING, PieceType.WHITE_STANDING]:
                return False

        return True

    def restart_game(self):
        self.board = [[Stack() for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]  # Reset the board to Stack objects
        self.current_player = PlayerColor.BLACK  # Reset to player 1
        self.black_pieces_left = 15  # Reset black pieces
        self.white_pieces_left = 15  # Reset white pieces
        print("Game reset successful")
        
    def get_hovered_cell(self, mouse_pos, grid_x_offset, cell_size):
        x, y = mouse_pos
        col = (x - grid_x_offset) // cell_size  # Evaluates the mouse column using the passed grid_x_offset and cell_size
        row = (y - grid_x_offset) // cell_size  # Calculate the mouse row using the passed grid_x_offset and cell_size

        # Check that the mouse is within range of the board
        if 0 <= row < 4 and 0 <= col < 4:
            return row, col
        else:
            return None

    
  