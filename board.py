import streamlit as st
import chess
import chess.svg
import ai
import evaluation
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("Play Chess vs AI")

# Initialize session state
if "board" not in st.session_state:
    st.session_state.board = chess.Board()
if "player_side" not in st.session_state:
    st.session_state.player_side = "Black"
if "last_move_by_human" not in st.session_state:
    st.session_state.last_move_by_human = False
if "initialized" not in st.session_state:
    st.session_state.initialized = False

# Evaluation strength
evaluation.strength_of_pieces = {
    "p": -1, "n": -3, "b": -3, "r": -5, "q": -9, "k": -10,
    "P": 1, "N": 3, "B": 3, "R": 5, "Q": 9, "K": 10
}

# Side selection (resets game if changed)
side = st.radio("Choose your side:", ["White", "Black"], horizontal=True)
if side != st.session_state.player_side or not st.session_state.initialized:
    st.session_state.player_side = side
    st.session_state.board = chess.Board()
    st.session_state.initialized = True
    st.session_state.last_move_by_human = False

# Select difficulty
difficulty = st.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])
depth = {"Easy": 1, "Medium": 2, "Hard": 3}[difficulty]

# Show board
def show_board():
    board_svg = chess.svg.board(
        st.session_state.board,
        size=400,
        flipped=(st.session_state.player_side == "Black")
    )
    components.html(board_svg, height=450)

# Layout
left_col, right_col = st.columns([2, 1])

# Left column: board and player move
with left_col:
    show_board()
    if st.session_state.board.turn == (st.session_state.player_side == "White") \
            and not st.session_state.board.is_game_over():
        with st.form("move_form", clear_on_submit=True):
            human_move = st.text_input("Your Move (UCI format, e.g. e2e4):", key="move_input")
            submitted = st.form_submit_button("Make Move")
            if submitted:
                try:
                    move = chess.Move.from_uci(human_move.strip().lower())
                    if move in st.session_state.board.legal_moves:
                        st.session_state.board.push(move)
                        st.session_state.last_move_by_human = True
                    else:
                        st.error("Illegal move.")
                except ValueError:
                    st.error("Invalid UCI format.")

# Right column: move history
with right_col:
    st.subheader("Move History")
    moves = list(st.session_state.board.move_stack)
    move_list = []
    for i in range(0, len(moves), 2):
        white = moves[i].uci()
        black = moves[i + 1].uci() if i + 1 < len(moves) else ""
        move_list.append(f"{i//2 + 1}. {white} {black}")
    st.markdown("\n".join(move_list))

# AI move logic — only after human has moved
def make_ai_move():
    if st.session_state.last_move_by_human and not st.session_state.board.is_game_over():
        if st.session_state.board.turn != (st.session_state.player_side == "White"):
            with st.spinner("AI is thinking..."):
                ai_move = ai.find_best_move(
                    st.session_state.board,
                    depth,
                    strength_of_pieces=evaluation.strength_of_pieces
                )
                if ai_move:
                    st.session_state.board.push(ai_move)
                    st.session_state.last_move_by_human = False

make_ai_move()

# End game display
if st.session_state.board.is_game_over():
    st.success(f"Game Over! Result: {st.session_state.board.result()}")
    if st.button("New Game"):
        st.session_state.board = chess.Board()
        st.session_state.last_move_by_human = False
