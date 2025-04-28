import chess

# Directions
NORTH = 8
SOUTH = -8
EAST = 1
WEST = -1
NORTHEAST = NORTH + EAST
NORTHWEST = NORTH + WEST
SOUTHEAST = SOUTH + EAST
SOUTHWEST = SOUTH + WEST

# Helper Functions
def king_safety(board, square):
    safety = 0
    directions = [NORTH, NORTHEAST, EAST, SOUTHEAST,
                  SOUTH, SOUTHWEST, WEST, NORTHWEST]
    for direction in directions:
        adjacent = square + direction
        if 0 <= adjacent < 64 and chess.square_distance(square, adjacent) == 1:
            piece = board.piece_at(adjacent)
            if piece and piece.color == board.color_at(square):
                safety += 0.2
            else:
                safety -= 0.2
    return safety

def state_of_board(board):
    minor_pieces = sum(1 for p in board.piece_map().values() if p.piece_type in [chess.BISHOP, chess.KNIGHT, chess.ROOK])
    queens = sum(1 for p in board.piece_map().values() if p.piece_type == chess.QUEEN)
    total_pieces = len(board.piece_map())
    if total_pieces > 24:  # Opening phase
        return "opening"
    elif queens == 0 or (queens == 1 and minor_pieces <= 2):
        return "endgame"
    return "middlegame"

def king_activity(board, square, is_endgame):
    rank = chess.square_rank(square)
    file = chess.square_file(square)
    if is_endgame:
        center_distance = abs(3.5 - rank) + abs(3.5 - file)
        return (4 - center_distance) * 0.2
    else:
        back_rank = 0 if board.color_at(square) == chess.WHITE else 7
        rank_penalty = abs(rank - back_rank)
        return -0.3 * rank_penalty

def minor_piece_activity(square):
    rank = chess.square_rank(square)
    file = chess.square_file(square)
    center_bonus = (4 - abs(3.5 - rank)) * (4 - abs(3.5 - file)) / 4
    return 0.1 * center_bonus

def rook_positioning(board, square):
    file = chess.square_file(square)
    rank = chess.square_rank(square)
    color = board.color_at(square)
    bonus = 0.0
    own_pawn, enemy_pawn = False, False
    for r in range(8):
        sq = chess.square(file, r)
        piece = board.piece_at(sq)
        if piece and piece.piece_type == chess.PAWN:
            if piece.color == color:
                own_pawn = True
            else:
                enemy_pawn = True
    if not own_pawn:
        bonus += 0.3 if not enemy_pawn else 0.15
    if (color == chess.WHITE and rank == 6) or (color == chess.BLACK and rank == 1):
        bonus += 0.2
    return bonus

def isolated_pawn(board, square):
    file = chess.square_file(square)
    for offset in [-1, 1]:
        if 0 <= file + offset < 8:
            adjacent = chess.square(file + offset, chess.square_rank(square))
            piece = board.piece_at(adjacent)
            if piece and piece.piece_type == chess.PAWN and piece.color == board.color_at(square):
                return 0
    return -0.3  # Penalty for being isolated

def passed_pawn(board, square):
    file = chess.square_file(square)
    rank = chess.square_rank(square)
    color = board.color_at(square)
    direction = 1 if color == chess.WHITE else -1

    for r in range(rank + direction, 8 if color == chess.WHITE else -1, direction):
        sq = chess.square(file, r)
        piece = board.piece_at(sq)
        if piece and piece.piece_type == chess.PAWN and piece.color != color:
            return 0  # Blocked by an opposing pawn

    return 0.5 if (rank == 6 and color == chess.WHITE) or (rank == 1 and color == chess.BLACK) else 0.2

def mobility(board, color):
    temp_board = board.copy()
    temp_board.turn = color
    return len(list(temp_board.legal_moves))

def material_count(board, strength_table):
    strength = 0
    for piece in board.piece_map().values():
        symbol = piece.symbol()
        strength += strength_table[symbol]
    return strength

def piece_development(board, is_endgame):
    dev_score = 0
    starting = {
        chess.KNIGHT: [chess.B1, chess.G1, chess.B8, chess.G8],
        chess.BISHOP: [chess.C1, chess.F1, chess.C8, chess.F8],
    }
    for square, piece in board.piece_map().items():
        if piece.piece_type in starting and square not in starting[piece.piece_type]:
            dev_score += (0.2 if not is_endgame else 0.1) * (1 if piece.color == chess.WHITE else -1)
    return dev_score

def piece_activity(board):
    act_score = 0
    center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
    for square, piece in board.piece_map().items():
        if piece.piece_type in [chess.KNIGHT, chess.BISHOP] and square in center_squares:
            act_score += 0.2 if piece.color == chess.WHITE else -0.2
    return act_score

def queen_activity(board, square, is_endgame):
    if not is_endgame and square not in [chess.D1, chess.D8]:
        return -0.5  # Heavy penalty for early queen moves
    elif is_endgame and square in [chess.D4, chess.D5, chess.E4, chess.E5]:
        return 0.2  # Small bonus for active queens in endgame
    return 0

# Final evaluation function
def evaluate(board, strength_table):
    if board.is_checkmate():
        return -9999 if board.turn == chess.WHITE else 9999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = material_count(board, strength_table)
    
    is_endgame = (state_of_board(board) == "endgame")

    score += 0.1 * (mobility(board, chess.WHITE) - mobility(board, chess.BLACK))

    for square, piece in board.piece_map().items():
        color_sign = 1 if piece.color == chess.WHITE else -1

        if piece.piece_type == chess.KING:
            score += color_sign * (0.4 * king_safety(board, square) + 0.6 * king_activity(board, square, is_endgame))
        elif piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
            score += 0.2 * color_sign * minor_piece_activity(square)
        elif piece.piece_type == chess.ROOK:
            score += 0.3 * color_sign * rook_positioning(board, square)
        elif piece.piece_type == chess.PAWN:
            score += 0.2 * color_sign * (isolated_pawn(board, square) + passed_pawn(board, square))
        elif piece.piece_type == chess.QUEEN:
            score += color_sign * queen_activity(board, square, is_endgame)

    score += piece_development(board, is_endgame)
    score += piece_activity(board)

    if board.is_repetition(2):
        score -= 0.8
    elif board.is_repetition(1):
        score -= 0.2

    return score if board.turn == chess.WHITE else -score
