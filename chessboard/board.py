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
