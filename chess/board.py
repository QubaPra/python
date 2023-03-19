import pygame

pygame.mixer.init()
move_sound = pygame.mixer.Sound("./sounds/move.mp3")

# Define constants for the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

check = False
castle = {"white": False, "black": False}
qcastle = {"white": False, "black": False}
kcastle = {"white": False, "black": False}
en_passant_target = None
passant = True

class ChessBoard:
    def __init__(self, width=480, height=480, square_size=60):
        self.board = [[0] * 8 for _ in range(8)]
        self.width, self.height, self.square_size = width, height, square_size
        self.background_color, self.board_color = WHITE, GRAY
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.draw()

    def draw(self):    
        for row in range(8):
            for col in range(8):
                color = WHITE if (row + col) % 2 == 0 else GRAY
                if self.check_check("white") and self.board[row][col] == ("white", "king"):
                    color = (255, 0, 0)
                elif self.check_check("black") and self.board[row][col] == ("black", "king"):
                    color = (255, 0, 0)
                pygame.draw.rect(self.screen, color, [col * self.square_size, row * self.square_size, self.square_size, self.square_size])
    
    def draw_material(self):
        pieces = {}
        for row in self.board:
            for piece in row:
                if piece:
                    color, name = piece
                    pieces[(color, name)] = pieces.get((color, name), 0) + 1

        white_pieces = [(name, count) for (color, name), count in pieces.items() if color == 'white']
        black_pieces = [(name, count) for (color, name), count in pieces.items() if color == 'black']

        white_pieces.sort()
        black_pieces.sort()

        if (white_pieces, black_pieces) in [([('king', 1)], [('king', 1)]),
                                            ([('king', 1)], [('king', 1), ('knight', 1)]),
                                            ([('king', 1), ('knight', 1)], [('king', 1)]),
                                            ([('king', 1)], [('bishop', 1), ('king', 1)]),
                                            ([('bishop', 1), ('king', 1)], [('king', 1)])]:
            return True
        return False

    def is_valid_move(self, start_pos, end_pos, color):
        global check, castle, qcastle, kcastle, en_passant_target, passant
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
            return False
        piece = self.board[start_row][start_col]
        if not piece or piece[0] != color:
            return False        
        p_type = piece[1]

        if p_type == "pawn":
            if start_col == end_col:
                if color == "white":
                    if end_row == start_row - 1 and not self.board[end_row][end_col]:
                        return True
                    elif start_row == 6 and end_row == start_row - 2 and not self.board[end_row][end_col] and not self.board[end_row + 1][end_col]:
                        en_passant_target = (end_row, end_col)
                        passant = True
                        #print(en_passant_target)
                        return True
                elif color == "black":
                    if end_row == start_row + 1 and not self.board[end_row][end_col]:
                        return True
                    elif start_row == 1 and end_row == start_row + 2 and not self.board[end_row][end_col] and not self.board[end_row - 1][end_col]:
                        en_passant_target = (end_row, end_col)
                        passant = True
                        #print(en_passant_target)
                        return True
            elif abs(end_col - start_col) == 1 and end_row == start_row + (-1 if color == "white" else 1):
                target_piece = self.board[end_row][end_col]
                if target_piece and target_piece[0] != color:
                    return True
                # Check for en passant capture
                
                elif (end_row + (1 if color == "white" else -1), end_col )== en_passant_target:
                    self.board[en_passant_target[0]][en_passant_target[1]] = None
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
                    if self.board[start_row + i * (-1 if end_row < start_row else 1)][start_col + i * (-1 if end_col < start_col else 1)]:
                        return False
                return not self.board[end_row][end_col] or self.board[end_row][end_col][0] != color

        elif p_type == "bishop":
            if abs(end_col - start_col) == abs(end_row - start_row):
                for i in range(1, abs(end_col - start_col)):
                    if self.board[start_row + i * (-1 if end_row < start_row else 1)][start_col + i * (-1 if end_col < start_col else 1)]:
                        return False
                return not self.board[end_row][end_col] or self.board[end_row][end_col][0] != color
        
        elif p_type == "king":            
            if not castle[color]:           
                if color == "white":
                    if (not kcastle[color] and end_pos == (7,6)) or (not qcastle[color] and end_pos==(7,2)):
                        for i in range(1, 3):
                            col = start_col + (1 if end_col > start_col else -1) * i
                            if self.board[start_row][col] or self.check_square(7,col-1, "black"):
                                return False
                        if self.check_square(7,start_col + (1 if end_col > start_col else -1) * 3, "black"):
                            return False
                        return True
                elif color == "black":
                    if (not kcastle[color] and end_pos == (0,6)) or (not qcastle[color] and end_pos==(0,2)):
                        for i in range(1, 3):
                            col = start_col + (1 if end_col > start_col else -1) * i
                            if self.board[start_row][col] or self.check_square(0,col, "white"):
                                return False                            
                        if self.check_square(0,start_col + (1 if end_col > start_col else -1) * 3, "white"):
                            return False
                        return True
                
            return abs(end_col - start_col) <= 1 and abs(end_row - start_row) <= 1 and (not self.board[end_row][end_col] or self.board[end_row][end_col][0] != color)
        
        elif p_type == "knight":
            if abs(end_col - start_col) == 2 and abs(end_row - start_row) == 1:
                target_piece = self.board[end_row][end_col]
                return not target_piece or target_piece[0] != color
            elif abs(end_col - start_col) == 1 and abs(end_row - start_row) == 2:
                target_piece = self.board[end_row][end_col]
                return not target_piece or target_piece[0] != color
            else:
                return False

        return False

    def check_check(self,color):
        # Check for check
        king_row, king_col = None, None
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece == (color, "king"):
                    king_row, king_col = row, col
                    break
            if king_row is not None:
                break
            
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece[0] != color and self.is_valid_move((row, col), (king_row, king_col), "black" if color == "white" else "white"):
                    #print("in check")
                    return True
            else:
                continue
        return False

    def is_checkmate(self, color):
        # Find the king
        
        king_pos = None
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == (color, "king"):
                    king_pos = (row, col)
                    break
            if king_pos:
                break

        # Check if the king is in check
        if not self.check_check(color):
            return False

        #print(king_pos)        

        # Check if the king can move out of check

        
        for row in range(king_pos[0]-1, king_pos[0]+1):
            for col in range(king_pos[1]-1, king_pos[1]+1):                     
                if not self.check_square(row, col, color) and (0 <= row < 8 and 0 <= col < 8) and (row,col)!=king_pos and self.is_valid_move(king_pos, (row, col), color):
                    #print(not self.is_valid_move(king_pos, (row, col), color))
                    #print(row, col, color)
                    return False
        #print(2)
        # Check if any other piece can block the check
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if not piece or piece[0] != color:
                    continue
                for r in range(8):
                    for c in range(8):
                        if self.is_valid_move((row, col), (r, c), color):
                            # Make the move and see if the king is still in check
                            piece_taken = self.board[r][c]
                            self.board[r][c] = piece
                            self.board[row][col] = None
                            if not self.check_check(color):
                                #print(3)
                                self.board[row][col] = piece
                                self.board[r][c] = piece_taken
                                return False
                            self.board[row][col] = piece
                            self.board[r][c] = piece_taken
                            #print(4)

        # The king is in checkmate
        return True

    def is_stalemate(self, color):
        # Find the king        
        king_pos = None
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == (color, "king"):
                    king_pos = (row, col)
                    break
            if king_pos:
                break        
        #print(king_pos)        

        # Check if the king can move out of check        
        for row in range(king_pos[0]-1, king_pos[0]+1):
            for col in range(king_pos[1]-1, king_pos[1]+1):                     
                if not self.check_square(row, col, color) and (0 <= row < 8 and 0 <= col < 8) and (row,col)!=king_pos and self.is_valid_move(king_pos, (row, col), color):
                    #print(not self.is_valid_move(king_pos, (row, col), color))
                    #print(row, col, color)
                    return False
        #print(2)
        # Check if any other piece can block the check
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if not piece or piece[0] != color:
                    continue
                for r in range(8):
                    for c in range(8):
                        if self.is_valid_move((row, col), (r, c), color):
                            # Make the move and see if the king is still in check
                            piece_taken = self.board[r][c]
                            self.board[r][c] = piece
                            self.board[row][col] = None
                            if not self.check_check(color):
                                #print(3)
                                self.board[row][col] = piece
                                self.board[r][c] = piece_taken
                                return False
                            self.board[row][col] = piece
                            self.board[r][c] = piece_taken
                            #print(4)

        # The king is in checkmate
        return True

    def move_piece(self, selected_piece_pos, dest_pos,color):
        global castle, qcastle, kcastle, passant, en_passant_target 

        if self.is_valid_move(selected_piece_pos, dest_pos,color):                                    
            prev_piece = self.board[dest_pos[0]][dest_pos[1]]
            piece = self.board[selected_piece_pos[0]][selected_piece_pos[1]]         
            self.board[selected_piece_pos[0]][selected_piece_pos[1]] = None
            self.board[dest_pos[0]][dest_pos[1]] = piece

            if self.check_check(color):               
                
                self.board[selected_piece_pos[0]][selected_piece_pos[1]] = piece
                self.board[dest_pos[0]][dest_pos[1]] = prev_piece
                if en_passant_target!=None and not passant:
                    self.board[en_passant_target[0]][en_passant_target[1]] = ("black" if color == "white" else "white", "pawn")                              
                return True
            
            move_sound.play()

            if en_passant_target!=None and passant:
                passant = False
                
            elif en_passant_target!=None and not passant:
                passant = True                
                en_passant_target=None           
            
            #print (en_passant_target, passant)   

            # Check for pawn promotion
            if piece[1] == "pawn" and (dest_pos[0] == 0 or dest_pos[0] == 7):
                self.board[dest_pos[0]][dest_pos[1]] = (color, "queen")
            
            # Check for castle       
            if piece[1] == "king" and abs(dest_pos[1]-selected_piece_pos[1]) == 2:                
                if dest_pos == (7,6) or dest_pos == (0,6):
                    self.board[dest_pos[0]][dest_pos[1]-1] = (color, "rook")
                    self.board[dest_pos[0]][7] = None
                elif dest_pos == (7,2) or dest_pos == (0,2):
                    self.board[dest_pos[0]][dest_pos[1]+1] = (color, "rook")
                    self.board[dest_pos[0]][0] = None

            if piece[1] == "king":
                castle[color]= True
            if piece[1] == "rook":                
                if self.board[7][7] == None:
                    kcastle[color]=True
                elif self.board[7][0] == None:
                    qcastle[color]=True
                elif self.board[0][7] == None:
                    kcastle[color]=True
                elif self.board[0][0] == None:
                    qcastle[color]=True
        
        return False
    
    def check_square(self,row, col, color):

        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece and piece[0] == color:
                    # Check if the piece can move to the square
                    if self.is_valid_move((r, c), (row, col), piece[0]):
                        return True
        return False
    
    

