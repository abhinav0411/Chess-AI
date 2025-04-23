import streamlit as st
import chess
import chess.svg
import ai
import evaluation
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("Play Chess vs AI")

# Session state initialization
if "board" not in st.session_state:
    st.session_state.board = chess.Board()
if "player_side" not in st.session_state:
    st.session_state.player_side = "Black"
if "awaiting_ai" not in st.session_state:
    st.session_state.awaiting_ai = False
if "initialized" not in st.session_state:
    st.session_state.initialized = False

# Evaluation strength
evaluation.strength_of_pieces = {
    "p": -1, "n": -3, "b": -3, "r": -5, "q": -9, "k": -10,
    "P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 10
}

# Player side selection
side = st.radio("Choose your side:", ["White", "Black"], horizontal=True)
if side != st.session_state.player_side or not st.session_state.initialized:
    st.session_state.player_side = side
    st.session_state.board = chess.Board()
    st.session_state.awaiting_ai = (side == "White")
    st.session_state.initialized = True

# Difficulty
difficulty = st.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])
depth = {"Easy": 1, "Medium": 2, "Hard": 3}[difficulty]

# Draw board
def show_board():
    board_svg = chess.svg.board(
        st.session_state.board,
        flipped=(st.session_state.player_side == "Black"),
        size=400
    )
    components.html(board_svg, height=450)

# AI move
def make_ai_move():
    with st.spinner("AI is thinking..."):
        move = ai.find_best_move(
            st.session_state.board,
            depth,
            strength_of_pieces=evaluation.strength_of_pieces
        )
        if move:
            st.session_state.board.push(move)
    st.session_state.awaiting_ai = False

# Layout
left, right = st.columns([2, 1])

with left:
    show_board()

    # If it's human's turn
    if st.session_state.board.turn == (st.session_state.player_side == "White") \
            and not st.session_state.board.is_game_over():
        with st.form("move_form", clear_on_submit=True):
            move_input = st.text_input("Your Move (e.g., e2e4):")
            submit = st.form_submit_button("Make Move")
            if submit:
                try:
                    move = chess.Move.from_uci(move_input.strip().lower())
                    if move in st.session_state.board.legal_moves:
                        st.session_state.board.push(move)
                        st.session_state.awaiting_ai = True
                    else:
                        st.error("Illegal move.")
                except:
                    st.error("Invalid move format.")

# Move history
with right:
    st.subheader("Move History")
    history = list(st.session_state.board.move_stack)
    for i in range(0, len(history), 2):
        w = history[i].uci()
        b = history[i + 1].uci() if i + 1 < len(history) else ""
        st.markdown(f"{i//2 + 1}. {w} {b}")

# Trigger AI move outside form
if st.session_state.awaiting_ai and not st.session_state.board.is_game_over() \
        and st.session_state.board.turn != (st.session_state.player_side == "White"):
    make_ai_move()

# Endgame
if st.session_state.board.is_game_over():
    st.success(f"Game Over! Result: {st.session_state.board.result()}")
    if st.button("New Game"):
        st.session_state.board = chess.Board()
        st.session_state.awaiting_ai = (st.session_state.player_side == "Black")
