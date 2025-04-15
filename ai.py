import evaluation
import chess

def minimax(board, depth, alpha, beta, maximizing_player, strength_of_pieces):
    if depth == 0 or board.is_game_over():
        return evaluation.evaluate(board, strength_of_pieces), None 
    
    best_move = None
    legal_moves = sorted(board.legal_moves, 
                        key=lambda m: (board.is_capture(m), board.gives_check(m)),
                        reverse=True)

    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth-1, alpha, beta, False, strength_of_pieces)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move  # Return move here
    else:
        # Similar logic for minimizing
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth-1, alpha, beta, True, strength_of_pieces)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def find_best_move(board, depth, strength_of_pieces):
    _, best_move = minimax(board, depth, float('-inf'), float('inf'), 
                          board.turn == chess.WHITE, strength_of_pieces)
    return best_move


