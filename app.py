import streamlit as st
import chess
import chess.svg
import ai  # your AI logic
import evaluation
import random

st.set_page_config(layout="wide")
st.title("Play Chess vs AI")

# Session state to keep the board persistent
if "board" not in st.session_state:
    st.session_state.board = chess.Board()

# Show board
st.image(chess.svg.board(st.session_state.board), width=500)

# Input move from the user
user_move = st.text_input("Your Move (e.g. e2e4):")

if st.button("Make Move"):
    try:
        move = chess.Move.from_uci(user_move)
        if move in st.session_state.board.legal_moves:
            st.session_state.board.push(move)

            # AI move
            ai_move = ai.find_best_move(
                st.session_state.board, depth=2, strength_of_pieces=evaluation.strength_of_pieces
            )
            if ai_move:
                st.session_state.board.push(ai_move)
        else:
            st.error("Illegal move.")
    except:
        st.error("Invalid move format.")

if st.session_state.board.is_game_over():
    st.success(f"Game Over! Result: {st.session_state.board.result()}")
