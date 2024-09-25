# TEST FEEL FREE TO DELETE ONLY FOR FOLDER STRUCTUREfrom enum import Enum

class PieceType(Enum):
    EMPTY = 0
    BLACK_LYING = 1
    BLACK_STANDING = 2
    WHITE_LYING = 3
    WHITE_STANDING = 4

class PlayerColor(Enum):
    BLACK = 0
    WHITE = 1

class Piece:
    def __init__(self, type=PieceType.EMPTY, height=0):
        self.type = type
        self.height = height

class Game:
    def __init__(self):
        self.GRID_SIZE = 4
        self.MAX_STACK_HEIGHT = 4
        self.board = [[Piece() for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)] #inner and outer list
        self.current_player = PlayerColor.BLACK
        self.black_pieces_left = 15
        self.white_pieces_left = 15

    def place_piece(self, row, col, color, is_standing):
        if not self.is_valid_move(row, col):
            return False

        piece_type = PieceType.BLACK_STANDING if color == PlayerColor.BLACK and is_standing else \
                     PieceType.BLACK_LYING if color == PlayerColor.BLACK else \
                     PieceType.WHITE_STANDING if is_standing else PieceType.WHITE_LYING

        self.board[row][col] = Piece(piece_type, self.board[row][col].height + 1)

        if color == PlayerColor.BLACK:
            self.black_pieces_left -= 1
        else:
            self.white_pieces_left -= 1

        return True

    def move_piece(self, from_row, from_col, to_row, to_col):
        if not self.is_valid_move(to_row, to_col) or self.board[from_row][from_col].type == PieceType.EMPTY:
            return False

        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = Piece()
        return True

    def check_win(self, color):
        target_type = PieceType.BLACK_LYING if color == PlayerColor.BLACK else PieceType.WHITE_LYING

        # Check horizontal and vertical
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE - 3):
                if all(self.board[i][j+k].type == target_type for k in range(4)) or \
                   all(self.board[j+k][i].type == target_type for k in range(4)):
                    return True

        # Check diagonals
        for i in range(self.GRID_SIZE - 3):
            for j in range(self.GRID_SIZE - 3):
                if all(self.board[i+k][j+k].type == target_type for k in range(4)) or \
                   all(self.board[i+k][j+3-k].type == target_type for k in range(4)):
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
               self.board[row][col].type not in [PieceType.BLACK_STANDING, PieceType.WHITE_STANDING]

