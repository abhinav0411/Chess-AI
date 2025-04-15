import chess
import random
import evaluation
from ai import find_best_move

board = chess.Board()

strength_of_pieces = {"p": -1, "n": -3, "b": -3, "r": -5, "q": -9, "k": -10,
                      "P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 10}


running = True

print("Initial position:")
print(board)

while running:
    if board.turn == chess.WHITE:
        print(f"\nWhite's turn (AI thinking...)")
        move = find_best_move(board, 3, strength_of_pieces)
        board.push(move)
        print(f"AI plays: {move.uci()}")
        print(board)
    else:
        print(f"\nBlack's turn (Material: {evaluation.evaluate(board, strength_of_pieces):.1f})")
        while True:
            human = input("Your move > ").strip()
            try:
                move = board.parse_san(human)
                if move in board.legal_moves:
                    board.push(move)
                    print(board)
                    break
                else:
                    print("Illegal move. Try again.")
            except:
                print("Invalid input. Use moves like 'e4' or 'Nf3'.")

    if board.is_game_over():
        if board.is_checkmate():
            winner = "Black" if board.turn == chess.WHITE else "White"
            print(f"Checkmate! {winner} wins!")
        elif board.is_stalemate():
            print("Draw by stalemate")
        else:
            print(f"Game ended: {board.result()}")
        break
