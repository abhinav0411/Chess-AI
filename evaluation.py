import chess


# Define directions manually
NORTH = 8
SOUTH = -8
EAST = 1
WEST = -1
NORTHEAST = NORTH + EAST
NORTHWEST = NORTH + WEST
SOUTHEAST = SOUTH + EAST
SOUTHWEST = SOUTH + WEST


def king_safety(board, square):
    """Evaluate how safe the king is by checking nearby friendly pieces."""
    safety = 0
    directions = [NORTH, NORTHEAST, EAST, SOUTHEAST,
                  SOUTH, SOUTHWEST, WEST, NORTHWEST]
    for direction in directions:
        adjacent = square + direction
        if 0 <= adjacent < 64 and chess.square_distance(square, adjacent) == 1:
            piece = board.piece_at(adjacent)
            if piece and piece.color == board.color_at(square):
                safety += 0.3
            else:
                safety -= 0.2
    return safety


# Function to check the phase of the game (opening, middlegame, endgame)
def state_of_board(board):
    count_minor = 0
    count_queen = 0
    for i in board.board_fen():
        if (i != "q" and i != "Q") and (i != "p" and i != "P"):
            count_minor += 1
        elif i == "q" or i == "Q":
            count_queen += 1
    if (count_queen == 0 and count_minor <= 4) or (count_queen == 1 and count_minor <= 2):
        return "endgame"
    else:
        return "middlegame"

# Function for king's activity based on the phase of the game
def king_activity(board, square, is_endgame):
    rank = chess.square_rank(square)
    file = chess.square_file(square)

    if is_endgame:
        # Bonus for being near center
        center_distance = abs(3.5 - rank) + abs(3.5 - file)
        return (4 - center_distance) * 0.2  # max 0.8 bonus
    else:
        # Penalize kings far from back rank (0 for white, 7 for black)
        back_rank = 0 if board.color_at(square) == chess.WHITE else 7
        rank_penalty = abs(rank - back_rank)
        return -0.4 * rank_penalty

# Function to evaluate knight and bishop activity
def minor_piece_activity(square):
    rank = chess.square_rank(square)
    file = chess.square_file(square)
    # Bonus for central control
    return 0.1 * (4 - abs(3.5 - rank)) * (4 - abs(3.5 - file)) / 4

# Function to evaluate rook positioning
def rook_positioning(board, square):
    file = chess.square_file(square)
    rank = chess.square_rank(square)
    color = board.color_at(square)
    bonus = 0.0

    # Check for open/semi-open file
    file_has_own_pawn = False
    file_has_enemy_pawn = False
    for r in range(8):
        sq = chess.square(file, r)
        piece = board.piece_at(sq)
        if piece and piece.piece_type == chess.PAWN:
            if piece.color == color:
                file_has_own_pawn = True
            else:
                file_has_enemy_pawn = True
    if not file_has_own_pawn:
        bonus += 0.3 if not file_has_enemy_pawn else 0.15

    # Bonus for 7th rank pressure
    if (color == chess.WHITE and rank == 6) or (color == chess.BLACK and rank == 1):
        bonus += 0.2

    return bonus

# Function to evaluate isolated pawns
def isolated_pawns(board, square):
    not_isolated = 0
    file = chess.square_file(square)
    for f_offset in [-1, 1]:
        if 0 <= file + f_offset < 8:
            adj_square = chess.square(file + f_offset, chess.square_rank(square))
            if board.piece_at(adj_square) == chess.PAWN:
                not_isolated += 0.3
    return not_isolated

# Function to count material strength
def count_pieces(board, strength_of_pieces):
    strength = 0
    for i in board.board_fen():
        if i.isalpha():
            strength += strength_of_pieces[i]
    return strength


def piece_development(board):
    development_score = 0
    starting_positions = {
        chess.KNIGHT: [chess.B1, chess.G1, chess.B8, chess.G8],
        chess.BISHOP: [chess.F1, chess.C1, chess.F8, chess.C8],
        chess.QUEEN: [chess.D1, chess.D8],
        chess.ROOK: [chess.A1, chess.H1, chess.A8, chess.H8],
    }

    # Iterate over pieces on the board
    for square, piece in board.piece_map().items():
        if piece.color == chess.WHITE:
            piece_type = piece.piece_type
            if piece_type in starting_positions:
                if square not in starting_positions[piece_type]:
                    development_score += 0.1  # Reward for moving out of the starting position
            else:
                development_score += 0.1  # Reward for moving any piece
        elif piece.color == chess.BLACK:
            piece_type = piece.piece_type
            if piece_type in starting_positions:
                if square not in starting_positions[piece_type]:
                    development_score -= 0.1  # Penalize Black for not developing early
            else:
                development_score -= 0.1  # Penalize Black for not developing early

    return development_score

def piece_activity(board):
    activity_score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            # Give minor pieces a bonus for being on central squares
            if piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
                if square in [chess.D4, chess.D5, chess.E4, chess.E5]:
                    activity_score += 0.2 if piece.color == chess.WHITE else -0.2
            # Encourage the Queen to be developed later in the game
            if piece.piece_type == chess.QUEEN:
                if square in [chess.D1, chess.D8]:  # Queen on starting squares
                    activity_score -= 0.5  # Penalize for underdeveloped Queen
                else:
                    activity_score += 0.1  # Bonus for Queen's activity
    return activity_score

# Updated evaluate function
def evaluate(board, strength_of_pieces):
    score = count_pieces(board, strength_of_pieces)
    
    # Check game status
    if board.is_checkmate():
        return float('-inf') if board.turn == chess.WHITE else float('inf')
    if board.is_game_over():
        return 0
    
    # Determine the phase of the game
    game_state = state_of_board(board)
    is_endgame = game_state == "endgame"
    
    # Mobility calculation
    def get_mobility(color):
        temp_board = board.copy()
        temp_board.turn = color
        return len(list(temp_board.legal_moves))
    
    white_mobility = get_mobility(chess.WHITE)
    black_mobility = get_mobility(chess.BLACK)
    score += 0.1 * (white_mobility - black_mobility)

    # Central squares bonus
    CENTRAL_SQUARES = [chess.D4, chess.D5, chess.E4, chess.E5]
    for square in CENTRAL_SQUARES:
        piece = board.piece_at(square)
        if piece and piece != chess.KING:
            score += 0.3 * (1 if piece.color == chess.WHITE else -1)
        
        # King safety
        if piece == chess.KING:
            safety = king_safety(board, piece)
            score += 0.4 * safety if piece.color == chess.WHITE else -0.4

        # Isolated pawns
        if piece == chess.PAWN:
            not_isolated = isolated_pawns(board, piece)
            score += 0.3 * not_isolated if piece.color == chess.WHITE else -0.3
    
    # King activity in the endgame
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            color_sign = 1 if piece.color == chess.WHITE else -1

            # Positional features
            if piece.piece_type == chess.KING:
                score += 0.4 * color_sign * king_safety(board, square)
                score += 0.6 * color_sign * king_activity(board, square, is_endgame)
            elif piece.piece_type in [chess.BISHOP, chess.KNIGHT]:
                score += 0.2 * color_sign * minor_piece_activity(square)
            elif piece.piece_type == chess.ROOK:
                score += 0.3 * color_sign * rook_positioning(board, square)
    
    # Add Piece Development and Activity bonuses
    score += piece_development(board)
    score += piece_activity(board)
    
    # Repetition penalty
    if board.is_repetition(2):
        score -= 0.8  
    elif board.is_repetition(1):
        score -= 0.2

    return score
