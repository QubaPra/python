import pygame

# Define constants for the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

class ChessBoard:
    def __init__(self):
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.screen = None
        self.square_size = 60
        self.width = self.height = self.square_size * 8

    def draw(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(WHITE)
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    pygame.draw.rect(self.screen, GRAY, [col * self.square_size, row * self.square_size, self.square_size, self.square_size])
                else:
                    pygame.draw.rect(self.screen, WHITE, [col * self.square_size, row * self.square_size, self.square_size, self.square_size])
        pygame.display.flip()

    def put_piece(self, piece, row, col):
        self.board[row][col] = piece
    
    def is_valid_move(self, selected_piece_pos, move_to_pos):
        # Check if the selected piece is a valid piece
        selected_piece = self.board[selected_piece_pos[0]][selected_piece_pos[1]]
        if not selected_piece:
            return False

        # Check if the move is within the bounds of the board
        if move_to_pos[0] < 0 or move_to_pos[0] > 7 or move_to_pos[1] < 0 or move_to_pos[1] > 7:
            return False

        # Check if the move is valid for the selected piece
        piece_type = selected_piece[1]
        if piece_type == "pawn":
            # ... pawn move validation ...
            pass
        elif piece_type == "rook":
            # ... rook move validation ...
            pass
        elif piece_type == "knight":
            # ... knight move validation ...
            pass
        elif piece_type == "bishop":
            # ... bishop move validation ...
            pass
        elif piece_type == "queen":
            # ... queen move validation ...
            pass
        elif piece_type == "king":
            # ... king move validation ...
            pass

        return True
    
    def move_piece(self, selected_piece_pos, dest_pos):
        if self.is_valid_move(selected_piece_pos, dest_pos):
            piece = self.board[selected_piece_pos[0]][selected_piece_pos[1]]
            self.board[selected_piece_pos[0]][selected_piece_pos[1]] = None
            self.board[dest_pos[0]][dest_pos[1]] = piece
            return True
        else:
            return False

