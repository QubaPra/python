import pygame

class ChessPieces:
    def __init__(self, board):
        self.board = board
        self.pieces = []
        self.screen = None
        self.images = {
            "white_pawn": pygame.image.load("./images/white_pawn.png"),
            "white_knight": pygame.image.load("./images/white_knight.png"),
            "white_bishop": pygame.image.load("./images/white_bishop.png"),
            "white_rook": pygame.image.load("./images/white_rook.png"),
            "white_queen": pygame.image.load("./images/white_queen.png"),
            "white_king": pygame.image.load("./images/white_king.png"),
            "black_pawn": pygame.image.load("./images/black_pawn.png"),
            "black_knight": pygame.image.load("./images/black_knight.png"),
            "black_bishop": pygame.image.load("./images/black_bishop.png"),
            "black_rook": pygame.image.load("./images/black_rook.png"),
            "black_queen": pygame.image.load("./images/black_queen.png"),
            "black_king": pygame.image.load("./images/black_king.png")
        }

    def draw(self, screen, selected_piece_pos):
        self.screen = screen
        for i in range(8):
            for j in range(8):
                piece = self.board.board[i][j]
                if piece and (i, j) != selected_piece_pos:
                    color, p_type = piece
                    img = self.images[color + "_" + p_type]
                    pos = (j * 60, i * 60)
                    self.screen.blit(img, pos)

        # Draw the selected piece last
        if selected_piece_pos:
            i, j = selected_piece_pos
            piece = self.board.board[i][j]
            if piece:
                color, p_type = piece
                img = self.images[color + "_" + p_type]
                mouse_pos = pygame.mouse.get_pos()
                mouse_x, mouse_y = mouse_pos
                pos = (mouse_x - 60 / 2, mouse_y - 60 / 2)
                self.screen.blit(img, pos)