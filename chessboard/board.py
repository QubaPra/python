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
    
    def is_valid_move(self, start_pos, end_pos, color):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        piece = self.board[start_row][start_col]
        if not piece or piece[0] != color:
            return False
        p_type = piece[1]

        if p_type == "pawn":
            if start_col == end_col:
                if color == "white" and end_row == start_row - 1 and not self.board[end_row][end_col]:
                    return True
                elif color == "white" and start_row == 6 and end_row == start_row - 2 and not self.board[end_row][end_col] and not self.board[end_row + 1][end_col]:
                    return True
                elif color == "black" and end_row == start_row + 1 and not self.board[end_row][end_col]:
                    return True
                elif color == "black" and start_row == 1 and end_row == start_row + 2 and not self.board[end_row][end_col] and not self.board[end_row - 1][end_col]:
                    return True
            elif abs(end_col - start_col) == 1 and end_row == start_row + (-1 if color == "white" else 1):
                target_piece = self.board[end_row][end_col]
                if target_piece and target_piece[0] != color:
                    return True

        elif p_type == "rook":
            if start_row == end_row:
                for col in range(start_col + 1, end_col) if start_col < end_col else range(start_col - 1, end_col, -1):
                    if self.board[start_row][col]:
                        return False
                return not self.board[end_row][end_col] or self.board[end_row][end_col][0] != color
            elif start_col == end_col:
                for row in range(start_row + 1, end_row) if start_row < end_row else range(start_row - 1, end_row, -1):
                    if self.board[row][start_col]:
                        return False
                return not self.board[end_row][end_col] or self.board[end_row][end_col][0] != color

        elif p_type == "queen":
            if start_row == end_row:
                for col in range(start_col + 1, end_col) if start_col < end_col else range(start_col - 1, end_col, -1):
                    if self.board[start_row][col]:
                        return False
                return not self.board[end_row][end_col] or self.board[end_row][end_col][0] != color
            elif start_col == end_col:
                for row in range(start_row + 1, end_row) if start_row < end_row else range(start_row - 1, end_row, -1):
                    if self.board[row][start_col]:
                        return False
                return not self.board[end_row][end_col] or self.board[end_row][end_col][0] != color
            elif abs(end_col - start_col) == abs(end_row - start_row):
                for i in range(1, abs(end_col - start_col)):
                    row = start_row + i * (-1 if end_row < start_row else 1)
                    col = start_col + i * (-1 if end_col < start_col else 1)
                    if self.board[row][col]:
                        return False
                return not self.board[end_row][end_col] or self.board[end_row][end_col][0] != color

        return False

    
    def move_piece(self, selected_piece_pos, dest_pos,color):
        if self.is_valid_move(selected_piece_pos, dest_pos,color):
            piece = self.board[selected_piece_pos[0]][selected_piece_pos[1]]
            self.board[selected_piece_pos[0]][selected_piece_pos[1]] = None
            self.board[dest_pos[0]][dest_pos[1]] = piece
            return True
        else:
            return False

