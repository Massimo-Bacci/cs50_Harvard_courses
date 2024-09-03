"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    Nx = sum(cell == "X" for row in board for cell in row)
    No = sum(cell == "O" for row in board for cell in row)
    
    return O if Nx > No else X
    
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(row, col) for row in range(len(board)) for col in range(len(board[0])) if board[row][col] == EMPTY}

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Not possible")
    
    board1 = copy.deepcopy(board)
    board1[action[0]][action[1]] = player(board)
    return board1

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    def check_line(line):
        return line[0] if all(cell == line[0] and cell is not None for cell in line) else None

    for row in board:
        result = check_line(row)
        if result == "X":
            return X
        if result == "O":
            return O

    for col in range(len(board[0])):
        result = check_line([row[col] for row in board])
        if result == "X":
            return X
        if result == "O":
            return O

    diagonal1 = check_line([board[i][i] for i in range(len(board))])
    diagonal2 = check_line([board[i][len(board) - 1 - i] for i in range(len(board))])
    if diagonal1 == "X":
            return X
    if diagonal1 == "O":
            return O
        
    if diagonal2 == "X":
            return X
    if diagonal2 == "O":
            return O

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) in (X, O) or all(cell != EMPTY for row in board for cell in row):
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return 1 if winner(board) == X else (-1 if winner(board) == O else 0)


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    def max_value(board):
        if terminal(board):
            return (None, utility(board))
        v = float('-inf')
        best_action = None
        for action in actions(board):
            _, min_val = min_value(result(board, action))
            if min_val > v:
                v = min_val
                best_action = action
        return best_action, v

    def min_value(board):
        if terminal(board):
            return (None, utility(board))
        v = float('inf')
        best_action = None
        for action in actions(board):
            _, max_val = max_value(result(board, action))
            if max_val < v:
                v = max_val
                best_action = action
        return best_action, v

    if terminal(board):
        return None

    if player(board) == X:
        best_action, _ = max_value(board)
        return best_action
    else:
        best_action, _ = min_value(board)
        return best_action
