import math
import copy
import time

def print_board(board):
    print()
    for row in [board[i * 3:(i + 1) * 3] for i in range(3)]:
        print("| " + " | ".join(row) + " |")
    print()

def check_winner(board, letter):
    win_combos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    return any(all(board[i] == letter for i in combo) for combo in win_combos)

def is_draw(board):
    return ' ' not in board

def get_available_moves(board):
    return [i for i, spot in enumerate(board) if spot == ' ']

# ------------------ Minimax ------------------
def minimax(board, depth, is_maximizing, player, opponent):
    if check_winner(board, player):
        return 1
    elif check_winner(board, opponent):
        return -1
    elif is_draw(board):
        return 0

    if is_maximizing:
        best = -math.inf
        for move in get_available_moves(board):
            board[move] = player
            val = minimax(board, depth + 1, False, player, opponent)
            board[move] = ' '
            best = max(best, val)
        return best
    else:
        best = math.inf
        for move in get_available_moves(board):
            board[move] = opponent
            val = minimax(board, depth + 1, True, player, opponent)
            board[move] = ' '
            best = min(best, val)
        return best

# ------------------ Alpha-Beta Pruning ------------------
def minimax_ab(board, depth, alpha, beta, is_maximizing, player, opponent, counter):
    counter[0] += 1
    if check_winner(board, player):
        return 1
    elif check_winner(board, opponent):
        return -1
    elif is_draw(board):
        return 0

    if is_maximizing:
        best = -math.inf
        for move in get_available_moves(board):
            board[move] = player
            val = minimax_ab(board, depth + 1, alpha, beta, False, player, opponent, counter)
            board[move] = ' '
            best = max(best, val)
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return best
    else:
        best = math.inf
        for move in get_available_moves(board):
            board[move] = opponent
            val = minimax_ab(board, depth + 1, alpha, beta, True, player, opponent, counter)
            board[move] = ' '
            best = min(best, val)
            beta = min(beta, val)
            if beta <= alpha:
                break
        return best

def find_best_move(board, player, opponent, use_ab=False):
    best_val = -math.inf
    best_move = None
    counter = [0]

    for move in get_available_moves(board):
        board[move] = player
        if use_ab:
            move_val = minimax_ab(board, 0, -math.inf, math.inf, False, player, opponent, counter)
        else:
            move_val = minimax(board, 0, False, player, opponent)
        board[move] = ' '

        if move_val > best_val:
            best_val = move_val
            best_move = move

    return best_move, counter[0] if use_ab else None

# ------------------ Game Modes ------------------

def human_vs_human():
    board = [' ' for _ in range(9)]
    current = 'X'
    print("Welcome to 1 vs 1 Tic-Tac-Toe!")
    print_board([str(i+1) for i in range(9)])

    while True:
        print_board(board)
        try:
            move = int(input(f"Player {current}, enter your move (1-9): ")) - 1
            if move < 0 or move > 8 or board[move] != ' ':
                print("Invalid move. Try again.")
                continue
            board[move] = current
            if check_winner(board, current):
                print_board(board)
                print(f"🎉 Player {current} wins!")
                break
            elif is_draw(board):
                print_board(board)
                print("It's a draw!")
                break
            current = 'O' if current == 'X' else 'X'
        except ValueError:
            print("Enter a number between 1 and 9.")

def human_vs_ai():
    board = [' ' for _ in range(9)]
    print("Play against AI!")
    choice = input("Do you want to use Alpha-Beta Pruning? (y/n): ").lower()
    use_ab = choice == 'y'
    human = input("Choose your letter (X goes first): ").upper()
    ai = 'O' if human == 'X' else 'X'
    current = 'X'

    while True:
        print_board(board)
        if current == human:
            try:
                move = int(input(f"Your move ({human}): ")) - 1
                if move < 0 or move > 8 or board[move] != ' ':
                    print("Invalid move. Try again.")
                    continue
                board[move] = human
            except ValueError:
                print("Enter a number between 1 and 9.")
                continue
        else:
            print("AI is thinking...")
            move, _ = find_best_move(board, ai, human, use_ab)
            board[move] = ai
            print(f"AI chooses position {move + 1}")

        if check_winner(board, current):
            print_board(board)
            if current == human:
                print("🎉 You win!")
            else:
                print("🤖 AI wins!")
            break
        elif is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current = ai if current == human else human

def performance_comparison():
    board = [' ' for _ in range(9)]
    board[0], board[4], board[8] = 'X', 'O', 'X'

    print("Initial Board:")
    print_board(board)

    print("Running standard Minimax...")
    start = time.time()
    move1, _ = find_best_move(board, 'X', 'O', use_ab=False)
    t1 = time.time() - start

    print("Running Alpha-Beta Minimax...")
    start = time.time()
    move2, ab_nodes = find_best_move(board, 'X', 'O', use_ab=True)
    t2 = time.time() - start

    print(f"\nMinimax chose move {move1 + 1} in {t1:.4f}s")
    print(f"Alpha-Beta chose move {move2 + 1} in {t2:.4f}s with {ab_nodes} nodes evaluated")

# ------------------ Main ------------------

def main():
    while True:
        print("\n--- Tic-Tac-Toe Menu ---")
        print("1. Human vs Human")
        print("2. Human vs AI")
        print("3. Compare Minimax vs Alpha-Beta")
        print("4. Exit")
        choice = input("Choose an option (1-4): ")

        if choice == '1':
            human_vs_human()
        elif choice == '2':
            human_vs_ai()
        elif choice == '3':
            performance_comparison()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
