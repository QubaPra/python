import pygame
from board import ChessBoard
from pieces import ChessPieces
import aichess

pygame.mixer.init()
draw_sound = pygame.mixer.Sound("./sounds/draw.wav")
checkmate_sound = pygame.mixer.Sound("./sounds/checkmate.wav")
start_sound = pygame.mixer.Sound("./sounds/start.wav")
promo_sound = pygame.mixer.Sound("./sounds/promo.wav")

start_sound.play()

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
def fen_to_board(fen):
    board = [[None]*8 for _ in range(8)]
    piece_map = {'r': 'rook', 'n': 'knight', 'b': 'bishop', 'q': 'queen', 'k': 'king', 'p': 'pawn'}
    rows = fen.split("/")
    for i, row in enumerate(rows):
        j = 0
        for char in row:
            if char.isdigit():
                j += int(char)
            else:
                color = "white" if char.isupper() else "black"
                piece = piece_map[char.lower()]
                board[i][j] = (color, piece)
                j += 1
    return board

fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
board.board = fen_to_board(fen)

game_over = False
player_move = True
winner=None

def check_for_end():
    global winner
    if board.is_checkmate("black"):          
        winner = "White"            
        checkmate_sound.play()
        return True
    elif board.is_checkmate("white"):                     
        winner = "Black"        
        checkmate_sound.play()
        return True
    elif board.is_stalemate("white"):                     
        winner = "Stalemate"        
        draw_sound.play() 
        return True           
    elif board.draw_material() or board.move_50_rule():
        winner = "Draw"        
        draw_sound.play()
        return True

def save_result(winner, moves):
    with open("lastgame.txt", "w") as file:
        if winner == "Draw":
            file.write("Draw after " + str(len(moves)*2) + " moves")
        else:
            file.write(winner + " wins after " + str(len(moves)*2) + " moves")

# Game Loop
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif not player_move:      
            ai_move = aichess.ai_move(player_last_move)               
            board.move_piece(ai_move[0], ai_move[1], "black",True)
            game_over = check_for_end()
            player_move=True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            row, col = mouse_pos[1] // 60, mouse_pos[0] // 60
            piece = board.board[row][col]
            if piece and piece[0]=="white":
                selected_piece = piece
                selected_piece_pos = (row, col)
        elif event.type == pygame.MOUSEBUTTONUP:            
            if selected_piece:
                mouse_pos = pygame.mouse.get_pos()
                row, col = mouse_pos[1] // 60, mouse_pos[0] // 60
                if board.is_valid_move(selected_piece_pos, (row, col), "white",True): 
                    if not (board.move_piece(selected_piece_pos, (row, col), "white",True)):
                        player_move = False
                        player_last_move = (selected_piece_pos,(row, col))                       
                        if board.repetition(selected_piece_pos,row, col):
                            winner = "Draw"                            
                            game_over = True                        
                        if piece[1] == "pawn" and (row==0 or row==7):
                            color="white"                        
                            queen_rect = pieces.images[color + "_queen"].get_rect(topleft=(30, 210))
                            rook_rect = pieces.images[color + "_rook"].get_rect(topleft=(150, 210))
                            bishop_rect = pieces.images[color + "_bishop"].get_rect(topleft=(270, 210))
                            knight_rect = pieces.images[color + "_knight"].get_rect(topleft=(390, 210))
                            promo=True
                            while promo:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        quit()
                                    elif event.type == pygame.MOUSEBUTTONDOWN:
                                        # Get the mouse position
                                        mouse_pos = pygame.mouse.get_pos()
                                        # Check if the mouse position is within the bounds of any image
                                        if queen_rect.collidepoint(mouse_pos):
                                            board.board[row][col] = (color, "queen")
                                            promo=False
                                        elif rook_rect.collidepoint(mouse_pos):
                                            board.board[row][col] = (color, "rook")
                                            promo=False
                                        elif bishop_rect.collidepoint(mouse_pos):
                                            board.board[row][col] = (color, "bishop")
                                            promo=False
                                        elif knight_rect.collidepoint(mouse_pos):
                                            board.board[row][col] = (color, "knight")
                                            promo=False                                        
                                pieces.promoui(screen,color)
                                # Update the display
                                pygame.display.update()
                                clock.tick(60)
                            promo_sound.play()                            
                selected_piece = None
                selected_piece_pos = None
            check_for_end()                     

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
    save_result(winner, board.returnAllMoves())
    if winner != "White" and winner != "Black":        
        text = font.render(f"{winner}", True, (128,128,128))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

        # Create a surface for the stroke
        stroke = pygame.Surface((600, 110))
        stroke2 = pygame.Surface((600, 120))

        # Fill the stroke with the stroke color
        stroke.fill((200,200,200))
        stroke2.fill((128,128,128))        
    else:
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