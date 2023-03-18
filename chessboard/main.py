import pygame
from board import ChessBoard
from pieces import ChessPieces


# Define constants for the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

selected_piece = None
selected_piece_pos = None

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

white_turn = True

game_over = False

# Game Loop
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif board.is_checkmate("black"):          
            winner = "White"
            game_over = True
        elif board.is_checkmate("white"):                     
            winner = "Black"
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            row, col = mouse_pos[1] // 60, mouse_pos[0] // 60
            piece = board.board[row][col]
            if piece and (white_turn and piece[0] == "white" or not white_turn and piece[0] == "black"):
                selected_piece = piece
                selected_piece_pos = (row, col)
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_piece:
                mouse_pos = pygame.mouse.get_pos()
                row, col = mouse_pos[1] // 60, mouse_pos[0] // 60
                if board.is_valid_move(selected_piece_pos, (row, col), "white" if white_turn else "black"):
                    if not (board.move_piece(selected_piece_pos, (row, col), "white" if white_turn else "black")):
                        white_turn = not white_turn                 
                selected_piece = None
                selected_piece_pos = None

    # Draw the board and pieces
    board.draw()
    pieces.draw(screen, selected_piece_pos)

    # Update the display
    pygame.display.update()

    clock.tick(60)

# Game over loop
while game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

    # Display winner
    font = pygame.font.SysFont('Impact', 100)
    text = font.render(f"{winner} won!", True, winner)
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    
    
    

    # Create a surface for the stroke
    stroke = pygame.Surface((600, 110))
    stroke2 = pygame.Surface((600, 120))

    # Fill the stroke with the stroke color
    stroke.fill("black" if winner == "White" else "white")
    stroke2.fill(winner)
    screen.blit(stroke2, stroke2.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2)))
    screen.blit(stroke, stroke.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2)))
    screen.blit(text, text_rect)

    # Update the display
    pygame.display.update()

    clock.tick(60)


