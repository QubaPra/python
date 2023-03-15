import pygame
from board import ChessBoard
from pieces import ChessPieces

# Define constants for the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize Pygame
pygame.init()

# Set up the window
WINDOW_SIZE = (480, 480)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

# Set up the board and pieces
board = ChessBoard()
pieces = ChessPieces(board)

# Set up the initial position of the pieces
board.board[0] = [("black", "rook"), ("black", "knight"), ("black", "bishop"), ("black", "queen"), ("black", "king"), ("black", "bishop"), ("black", "knight"), ("black", "rook")]
board.board[1] = [("black", "pawn") for _ in range(8)]
board.board[6] = [("white", "pawn") for _ in range(8)]
board.board[7] = [("white", "rook"), ("white", "knight"), ("white", "bishop"), ("white", "queen"), ("white", "king"), ("white", "bishop"), ("white", "knight"), ("white", "rook")]

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    # Draw the board and pieces
    board.draw()
    pieces.draw(screen)

    # Update the display
    pygame.display.update()

    clock.tick(60)
