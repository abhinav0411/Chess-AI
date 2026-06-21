# ♟️ Chess AI with Minimax & Alpha-Beta Pruning

A modern web-based Chess application where you can play against an intelligent Chess AI. The project is built using **Python**, **Streamlit**, and the **python-chess** library, showcasing a custom-built AI engine based on the Minimax algorithm enhanced with Alpha-Beta pruning, move ordering, and detailed positional heuristics.

---

## 🚀 Key Features

*   **Play as White or Black**: Select your side and the board automatically flips to your perspective.
*   **Three Difficulty Levels**:
    *   **Easy** (Depth 1): Quick, lightweight moves suitable for beginners.
    *   **Medium** (Depth 2): Balanced play evaluating moves further down the tree.
    *   **Hard** (Depth 3): A challenging mode searching multiple moves ahead.
*   **Interactive Streamlit Web UI**: Beautifully rendered board using SVG, side-by-side move history, and live game status updates (win, lose, draw).
*   **Intelligent Chess AI**:
    *   **Search Engine**: Minimax tree search.
    *   **Alpha-Beta Pruning**: Prunes unpromising branches early to significantly speed up calculations.
    *   **Move Ordering**: Sorts moves (prioritizing captures and checks) to maximize pruning efficiency.
    *   **Positional Heuristics**: Goes beyond simple piece counting to evaluate board safety, center control, passed/isolated pawns, and piece development.

---

## 🛠️ Project Structure

The project is structured into modular components:

*   [board.py](file:///Users/anantjain/Downloads/Chess-AI/board.py) — The main Streamlit web application. Manages session state, handles user moves in Universal Chess Interface (UCI) format, runs the game loop, and displays the board and move history.
*   [ai.py](file:///Users/anantjain/Downloads/Chess-AI/ai.py) — The core AI logic, containing the Minimax algorithm with Alpha-Beta pruning and move-sorting routines.
*   [evaluation.py](file:///Users/anantjain/Downloads/Chess-AI/evaluation.py) — The board evaluation engine. Computes a static score for a given board position based on material balance and advanced heuristics.
*   [requirements.txt](file:///Users/anantjain/Downloads/Chess-AI/requirements.txt) — Project dependencies.

---

## 🧠 How the AI Works

The Chess AI evaluates positions from the perspective of both players, attempting to maximize its own score while minimizing the opponent's options.

### 1. Minimax & Alpha-Beta Pruning
At each turn, the AI constructs a game tree up to a specified depth. **Alpha-beta pruning** keeps track of two values:
*   `alpha`: The minimum score the maximizing player is assured of.
*   `beta`: The maximum score the minimizing player is assured of.

If the algorithm finds a branch that is worse than an already evaluated path, it discards (prunes) that branch immediately, dramatically reducing the number of nodes evaluated.

### 2. Move Ordering
To prune the search tree as early as possible, legal moves are sorted before evaluation:
1.  **Captures** are evaluated first.
2.  **Checks** are evaluated next.
3.  Other legal moves follow.

This ordering ensures that "good" moves are checked early, allowing alpha-beta pruning to cut off large sections of the tree.

### 3. Positional Evaluation
Rather than relying solely on material values (e.g., Pawn = 1, Queen = 9), [evaluation.py](file:///Users/anantjain/Downloads/Chess-AI/evaluation.py) analyzes the state of the game:
*   **Material Counts**: Basic piece value summation.
*   **Mobility**: The number of legal moves available to a player.
*   **King Safety & Activity**: Calculates pawn shields/guards around the King during the opening and middlegame, and encourages the King to move to the center in the endgame.
*   **Piece Development & Activity**: Penalizes minor pieces (Knights, Bishops) left on starting squares and rewards active placement on central squares.
*   **Rook Positioning**: Rewards rooks occupying open files or control of the 7th rank.
*   **Pawn Structure**: Penalizes isolated pawns and rewards passed pawns.
*   **Early Queen Penalty**: Discourages early, reckless queen movements in the opening.
*   **Repetition Draw Penalty**: Penalizes the AI for repeating board states to prevent infinite loop draw states unless forced.

---

## 🔧 Installation & Setup

Ensure you have Python 3.8+ installed on your system.

1. **Clone or navigate to the project directory**:
   ```bash
   cd /Users/anantjain/Downloads/Chess-AI
   ```

2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit application**:
   ```bash
   streamlit run board.py
   ```

---

## 🎮 How to Play

1. Run the app and open the local URL in your web browser (typically `http://localhost:8501`).
2. Select your preferred color side (White or Black) and choose a difficulty level.
3. Enter your moves in **UCI format** (e.g., `e2e4` for pawn to e4, `g1f3` for knight to f3, or `e7e8q` for promoting a pawn to queen).
4. Click **Make Move** to submit. The AI will calculate its response and play its move.
5. Track the step-by-step game history on the right-hand panel.
