from flask import Flask, render_template, request, jsonify
from functools import lru_cache

app = Flask(__name__)

HUMAN = "X"
AI = "O"
EMPTY = ""

WIN_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)

def winner(board):
    for a, b, c in WIN_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None

def game_over(board):
    return winner(board) is not None or EMPTY not in board

@lru_cache(maxsize=100000)
def minimax(board_tuple, maximizing):
    """Return the best achievable score for the AI (O) or human (X)."""
    board = list(board_tuple)
    result = winner(board)
    if result == AI:
        return 1
    if result == HUMAN:
        return -1
    if EMPTY not in board:
        return 0

    if maximizing:
        best = -2
        for i, cell in enumerate(board):
            if cell == EMPTY:
                board[i] = AI
                best = max(best, minimax(tuple(board), False))
                board[i] = EMPTY
        return best

    best = 2
    for i, cell in enumerate(board):
        if cell == EMPTY:
            board[i] = HUMAN
            best = min(best, minimax(tuple(board), True))
            board[i] = EMPTY
    return best

def best_ai_move(board):
    best_score = -2
    best_move = None
    for i, cell in enumerate(board):
        if cell == EMPTY:
            board[i] = AI
            score = minimax(tuple(board), False)
            board[i] = EMPTY
            if score > best_score:
                best_score, best_move = score, i
    return best_move

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/move")
def move():
    data = request.get_json(silent=True) or {}
    board = data.get("board")
    if not isinstance(board, list) or len(board) != 9:
        return jsonify({"error": "Board must be a list of 9 cells."}), 400
    if any(cell not in ("X", "O", "") for cell in board):
        return jsonify({"error": "Invalid board cell."}), 400

    # The server accepts only a valid human turn: X starts and counts must match.
    x_count, o_count = board.count("X"), board.count("O")
    if x_count != o_count + 1:
        return jsonify({"error": "Invalid turn state."}), 400
    if winner(board) or game_over(board):
        return jsonify({"board": board, "winner": winner(board), "game_over": True})

    move_index = best_ai_move(board)
    if move_index is not None:
        board[move_index] = AI

    result = winner(board)
    return jsonify({
        "board": board,
        "winner": result,
        "game_over": game_over(board),
        "draw": game_over(board) and result is None,
        "ai_move": move_index
    })

if __name__ == "__main__":
    app.run(debug=True)
