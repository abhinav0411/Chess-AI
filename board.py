import streamlit as st
import chess
import chess.svg
import ai 
import evaluation
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("Play Chess vs AI")

# Initialize board and piece values
if "board" not in st.session_state:
    st.session_state.board = chess.Board()
    evaluation.strength_of_pieces = {
        "p": -1, "n": -3, "b": -3, "r": -5, "q": -9, "k": -10,
        "P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 10
    }

# Display board
def show_board():
    board_svg = chess.svg.board(st.session_state.board, size=400)
    components.html(board_svg, height=450)

# AI move logic
def make_ai_move():
    if st.session_state.board.turn == chess.WHITE and not st.session_state.board.is_game_over():
        with st.spinner("AI is thinking..."):
            ai_move = ai.find_best_move(
                st.session_state.board,
                depth=3,
                strength_of_pieces=evaluation.strength_of_pieces
            )
            if ai_move:
                st.session_state.board.push(ai_move)
                st.experimental_rerun()

# Human move handling (UCI input)
def handle_human_move():
    human_move = st.text_input("Your Move (UCI format, e.g. e7e5):", key="move_input")
    if st.button("Make Move"):
        try:
            move = chess.Move.from_uci(human_move.strip().lower())
            if move in st.session_state.board.legal_moves:
                st.session_state.board.push(move)
                st.experimental_rerun()
            else:
                st.error("Illegal move. Check possible moves.")
        except ValueError:
            st.error("Invalid UCI format. Use like 'e7e5' or 'g1f3'")

# Main flow
show_board()

# Handle AI move first if it's White's turn
if st.session_state.board.turn == chess.WHITE:
    make_ai_move()
else:
    handle_human_move()

# Game status
if st.session_state.board.is_game_over():
    st.success(f"Game Over! Result: {st.session_state.board.result()}")
    if st.button("New Game"):
        st.session_state.board = chess.Board()
        st.experimental_rerun()
