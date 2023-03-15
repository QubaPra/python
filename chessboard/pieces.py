import pygame

class ChessPieces:
    def __init__(self, board):
        self.board = board
        self.pieces = []
        self.screen = None
        self.images = {
            "white_pawn": pygame.image.load("white_pawn.png"),
            "white_knight": pygame.image.load("white_knight.png"),
            "white_bishop": pygame.image.load("white_bishop.png"),
            "white_rook": pygame.image.load("white_rook.png"),
            "white_queen": pygame.image.load("white_queen.png"),
            "white_king": pygame.image.load("white_king.png"),
            "black_pawn": pygame.image.load("black_pawn.png"),
            "black_knight": pygame.image.load("black_knight.png"),
            "black_bishop": pygame.image.load("black_bishop.png"),
            "black_rook": pygame.image.load("black_rook.png"),
            "black_queen": pygame.image.load("black_queen.png"),
            "black_king": pygame.image.load("black_king.png")
        }

    def draw(self, screen):
        self.screen = screen
        for i in range(8):
            for j in range(8):
                piece = self.board.board[i][j]
                if piece:
                    color, p_type = piece
                    self.screen.blit(self.images[color + "_" + p_type], (j * 60, i * 60))

