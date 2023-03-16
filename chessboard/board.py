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
    
    def is_valid_move(self, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        piece = self.board[start_row][start_col]
        if not piece:
            return False
        color, p_type = piece
        
        # Check if the move is valid based on the piece type
        if p_type == "pawn":
            if color == "white":
                if start_col == end_col:
                    if end_row == start_row - 1 and not self.board[end_row][end_col]:
                        # Move one square forward
                        return True
                    elif start_row == 6 and end_row == start_row - 2 and not self.board[end_row][end_col] and not self.board[end_row + 1][end_col]:
                        # Move two squares forward from the starting position
                        return True
                elif abs(end_col - start_col) == 1 and end_row == start_row - 1:
                    # Capture a piece diagonally
                    target_piece = self.board[end_row][end_col]
                    if target_piece and target_piece[0] == "black":
                        return True
            elif color == "black":
                if start_col == end_col:
                    if end_row == start_row + 1 and not self.board[end_row][end_col]:
                        # Move one square forward
                        return True
                    elif start_row == 1 and end_row == start_row + 2 and not self.board[end_row][end_col] and not self.board[end_row - 1][end_col]:
                        # Move two squares forward from the starting position
                        return True
                elif abs(end_col - start_col) == 1 and end_row == start_row + 1:
                    # Capture a piece diagonally
                    target_piece = self.board[end_row][end_col]
                    if target_piece and target_piece[0] == "white":
                        return True
        
        # Add more code for other piece types...

        elif p_type == "rook":
            # Check if the rook is moving along a row or column
            if start_row == end_row or start_col == end_col:
                # Check if there are any pieces blocking the rook's path
                if start_row == end_row:
                    # Check the columns between the start and end positions
                    for col in range(min(start_col, end_col) + 1, max(start_col, end_col)):
                        if self.board[start_row][col] is not None:
                            return False
                else:
                    # Check the rows between the start and end positions
                    for row in range(min(start_row, end_row) + 1, max(start_row, end_row)):
                        if self.board[row][start_col] is not None:
                            return False
                # Check if the end position is empty or has an opponent's piece
                if self.board[end_row][end_col] is None or self.board[end_row][end_col][0] != self.board[start_row][start_col][0]:
                    return True
            return False
        
        return False
    
    def move_piece(self, selected_piece_pos, dest_pos):
        if self.is_valid_move(selected_piece_pos, dest_pos):
            piece = self.board[selected_piece_pos[0]][selected_piece_pos[1]]
            self.board[selected_piece_pos[0]][selected_piece_pos[1]] = None
            self.board[dest_pos[0]][dest_pos[1]] = piece
            return True
        else:
            return False

