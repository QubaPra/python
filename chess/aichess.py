import chess
import chess.engine

def get_ai_move(board):
    # Start the Stockfish engine
    engine = chess.engine.SimpleEngine.popen_uci("stockfish.exe")

    # Ask the engine to analyze the position and suggest a move
    result = engine.play(board, chess.engine.Limit(time=0.5))
    ai_move = result.move

    # Stop the engine
    engine.quit()

    return ai_move

# Start a new game
board = chess.Board()


def to_chess_notation(move):
    row1, col1 = move[0]
    row2, col2 = move[1]
    
    # Convert rows and columns to chess notation
    col1 = chr(ord('a') + col1)
    col2 = chr(ord('a') + col2)
    row1 = 8 - row1
    row2 = 8 - row2
    
    return f"{col1}{row1}{col2}{row2}"

def from_chess_notation(chess_move):
    # Convert columns to numbers
    col1 = ord(chess_move[0]) - ord('a')
    col2 = ord(chess_move[2]) - ord('a')
    
    # Convert rows to numbers
    row1 = 8 - int(chess_move[1])
    row2 = 8 - int(chess_move[3])
    
    return ((row1, col1), (row2, col2))

def ai_move(player_move):   

    player_move = to_chess_notation(player_move)

    player_move = chess.Move.from_uci(player_move)
    
    board.push(player_move)

    # Get the AI's move and make it
    ai_move = get_ai_move(board)
    board.push(ai_move)
    return from_chess_notation(ai_move.uci())