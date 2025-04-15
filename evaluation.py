# Evaluating the position

import chess


Centre_Pieces = [chess.D4, chess.D5, chess.E4, chess.E5]


# Function for king safety
def king_safety(board, square):
    safety = 0
    for direction in [chess.NORTH, chess.NE, chess.EAST, chess.SE, chess.SOUTH, chess.SW, chess.WEST, chess.NW]:
        adjacent_square = square+direction
        if 0 <= adjacent_square < 64:
            piece = board.piece_at(adjacent_square)
            if piece:
                if piece.color == board.color_at(square):
                    safety += 0.3
            else:
                safety -= 0.2
    return safety


# Function to look at isolated pawns
def isolated_pawns(board, square):
    not_isolated = 0
    file = chess.square_file(square)
    for f_offset in [-1, 1]:
        if 0 <= file + f_offset < 8:
            adj_square = chess.square(file + f_offset, chess.square_rank(square))
            if board.piece_at(adj_square) == chess.PAWN:
                not_isolated += 0.3
    return not_isolated

def count_pieces(board, strength_of_pieces):
    strength = 0
    for i in board.board_fen():
        if i.isalpha():
            strength += strength_of_pieces[i]
    return strength

#
def evaluate(board, strength_of_pieces):
    strength = count_pieces(board, strength_of_pieces)
    
    if board.is_checkmate():
        return float('-inf') if board.turn == chess.WHITE else float('inf')
    if board.is_game_over():
        return 0
    
    # Mobility calculation for both colors
    def get_mobility(color):
        temp_board = board.copy()
        temp_board.turn = color
        return len(list(temp_board.legal_moves))
    
    white_mobility = get_mobility(chess.WHITE)
    black_mobility = get_mobility(chess.BLACK)
    strength += 0.1 * (white_mobility - black_mobility)
    
    # Central squares bonus
    CENTRAL_SQUARES = [chess.D4, chess.D5, chess.E4, chess.E5]
    for square in CENTRAL_SQUARES:
        piece = board.piece_at(square)
        if piece and piece != chess.KING:
            strength += 0.3 * (1 if piece.color == chess.WHITE else -1)
        
        # King safety
        if piece == chess.KING:
            safety = king_safety(board, piece)
            strength += 0.4 * safety if piece.color == chess.WHITE else -0.4

        # Isolated pawns
        if piece == chess.PAWN:
            not_isolated = isolated_pawns(board, piece)
            strength += 0.3 * not_isolated if piece.colore == chess.WHITE else -0.3
    
    # Repetition penalty
    if board.is_repetition(2):
        strength -= 0.8  
    elif board.is_repetition(1):
        strength -= 0.2
    
    return strength


