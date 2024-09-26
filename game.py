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

MAX_STACK_HEIGHT = 4
class Stack():
    def __init__(self, height=0):
        self.stack = [Piece() for _ in range(MAX_STACK_HEIGHT)]
        self.height = height


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
        if not self.is_valid_move(row, col):
            return False

        piece_type = PieceType.BLACK_STANDING if color == PlayerColor.BLACK and is_standing else \
            PieceType.BLACK_LYING if color == PlayerColor.BLACK else \
                PieceType.WHITE_STANDING if is_standing else PieceType.WHITE_LYING

        stack = self.board[row][col]
        stack.stack[stack.height] = Piece(piece_type)
        stack.height += 1

        if color == PlayerColor.BLACK:
            self.black_pieces_left -= 1
        else:
            self.white_pieces_left -= 1

        return True

    def move_piece(self, from_row, from_col, to_row, to_col):
        if not self.is_valid_move(to_row, to_col) or self.board[from_row][from_col].stack[0].type == PieceType.EMPTY:
            return False

        # Move the top piece from the source stack to the destination stack
        source_stack = self.board[from_row][from_col]
        dest_stack = self.board[to_row][to_col]

        # Check if destination stack has space
        if dest_stack.height < self.MAX_STACK_HEIGHT:
            dest_stack.stack[dest_stack.height] = source_stack.stack[source_stack.height - 1]
            dest_stack.height += 1
            source_stack.height -= 1
            source_stack.stack[source_stack.height] = Piece()  # Reset the slot after moving

        return True

    def check_win(self, color):
        target_type = PieceType.BLACK_LYING if color == PlayerColor.BLACK else PieceType.WHITE_LYING

        # Check horizontal and vertical
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE - 3):
                if all(self.board[i][j + k].stack[self.board[i][j + k].height - 1].type == target_type for k in range(4)) or \
                        all(self.board[j + k][i].stack[self.board[j + k][i].height - 1].type == target_type for k in range(4)):
                    return True

        # Check diagonals
        for i in range(self.GRID_SIZE - 3):
            for j in range(self.GRID_SIZE - 3):
                if all(self.board[i + k][j + k].stack[self.board[i + k][j + k].height - 1].type == target_type for k in range(4)) or \
                        all(self.board[i + k][j + 3 - k].stack[self.board[i + k][j + 3 - k].height - 1].type == target_type for k in range(4)):
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

    def is_valid_move(self, row, col):
        return 0 <= row < self.GRID_SIZE and 0 <= col < self.GRID_SIZE and \
            self.board[row][col].height < self.MAX_STACK_HEIGHT and \
            self.board[row][col].stack[self.board[row][col].height - 1].type not in [PieceType.BLACK_STANDING,
                                                                                     PieceType.WHITE_STANDING]
