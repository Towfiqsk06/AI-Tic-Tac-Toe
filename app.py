
import math

HUMAN = "X"
AI = "O"
EMPTY = " "

WINNING_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]


def display_board(board):
    print()
    for row in range(3):
        cells = []
        for col in range(3):
            index = row * 3 + col
            value = board[index] if board[index] != EMPTY else str(index + 1)
            cells.append(f" {value} ")
        print("|".join(cells))
        if row < 2:
            print("---+---+---")
    print()


def get_winner(board):
    for a, b, c in WINNING_COMBINATIONS:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_draw(board):
    return get_winner(board) is None and EMPTY not in board


def minimax(board, depth, is_maximizing):
    winner = get_winner(board)

    if winner == AI:
        return 10 - depth
    if winner == HUMAN:
        return depth - 10
    if is_draw(board):
        return 0

    if is_maximizing:
        best_score = -math.inf

        for i in range(9):
            if board[i] == EMPTY:
                board[i] = AI
                score = minimax(board, depth + 1, False)
                board[i] = EMPTY
                best_score = max(best_score, score)

        return best_score

    best_score = math.inf

    for i in range(9):
        if board[i] == EMPTY:
            board[i] = HUMAN
            score = minimax(board, depth + 1, True)
            board[i] = EMPTY
            best_score = min(best_score, score)

    return best_score


def get_ai_move(board):
    best_score = -math.inf
    best_move = None

    for i in range(9):
        if board[i] == EMPTY:
            board[i] = AI
            score = minimax(board, 0, False)
            board[i] = EMPTY

            if score > best_score:
                best_score = score
                best_move = i

    return best_move


def play_game():
    board = [EMPTY] * 9

    print("=" * 32)
    print("       TIC TAC TOE WITH AI")
    print("=" * 32)
    print("You are X | AI is O")
    print("Choose a position from 1 to 9.")

    while True:
        display_board(board)

        # Human player's turn
        try:
            position = int(input("Enter your position (1-9): "))

            if position < 1 or position > 9:
                print("Please enter a number from 1 to 9.")
                continue

            index = position - 1

            if board[index] != EMPTY:
                print("That position is already occupied!")
                continue

            board[index] = HUMAN

        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if get_winner(board) == HUMAN:
            display_board(board)
            print("Congratulations! You win!")
            break

        if is_draw(board):
            display_board(board)
            print("It's a draw!")
            break

        # AI player's turn
        print("AI is thinking...")
        ai_move = get_ai_move(board)
        board[ai_move] = AI
        print(f"AI selected position {ai_move + 1}.")

        if get_winner(board) == AI:
            display_board(board)
            print("AI wins! Try again.")
            break

        if is_draw(board):
            display_board(board)
            print("It's a draw!")
            break

    print("Game over!")


if __name__ == "__main__":
    while True:
        play_game()
        again = input("\nPlay again? (y/n): ").strip().lower()

        if again != "y":
            print("Thanks for playing!")
            break
