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
    countX = 0
    countO = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == "X":
                countX += 1
            elif board[i][j] == "O":
                countO += 1
    return X if countX <= countO else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    plays = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                plays.add((i,j))
    return plays


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    tempBoard = copy.deepcopy(board)
    currPlayer = player(board)
    try:
        if tempBoard[action[0]][action[1]] == EMPTY:
            tempBoard[action[0]][action[1]] = currPlayer
        else:
            raise Exception
    except:
        raise Exception
    else:
        return tempBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Horizontal
    for i in range(3):
        if board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]

    # Vertical
    for i in range(3):
        if board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]

    # Diagonal
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[2][0]

    return None
    

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    acts = actions(board)
    if len(acts) == 0 or winner(board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    # Functions based on the lecture
    def max_val(board):
        v = -9999

        if terminal(board):
            return utility(board)

        for action in actions(board):
            v = max(v, min_val(result(board, action)))

        return v

    def min_val(board):
        v = 9999

        if terminal(board):
            return utility(board)

        for action in actions(board):
            v = min(v, max_val(result(board, action)))

        return v
    # Variables for comparison and best action found
    bestAction = None
    bestScore, current = 0, 0

    if player(board) == X:
        # Set variables for X
        bestScore = -5
        current = -1
        for act in actions(board):
            # Pruning actions that give me the same score in the first board, as the one I got in the first min_val
            if utility(result(board, act)) <= current:
                pass
            else:
                # Saving the best value I get
                current = min_val(result(board, act))
                if bestScore < current:
                    bestScore = current
                    bestAction = act
    else:
        # Set variables for O
        bestScore = 5
        current = 1
        for act in actions(board):
            # Pruning actions that give me the same score in the first board, as the one I got in the first max_val
            if utility(result(board, act)) >= current:
                pass
            else:
                # Saving the best value I get
                current = max_val(result(board, act))
                if bestScore > current:
                    bestScore = current
                    bestAction = act

    return bestAction

