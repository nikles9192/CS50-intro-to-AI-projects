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

    state=board
    count_x=0
    count_o=0
    for list_i in state:
        for x in list_i:
            if x==X:
                count_x+=1
            if x==O:
                count_o+=1
    if count_x==count_o:
        return "X"
    else:
        return "O"






def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_set=set()
    for i,list_i in enumerate(board):
        for j,x in enumerate(list_i):
             if x==EMPTY:
                 actions_set.add((i,j))
    return actions_set



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Lets find the player
    i,j=action
    player_decided=player(board)
    if board[i][j]!=EMPTY:
        raise Exception(f"Move is forbidden as already there is {board[i][j]} on it")
    board_cp=copy.deepcopy(board)
    board_cp[i][j]=player_decided
    return board_cp

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    def check_horiz(board,player):
        """Checks if player has win in horizontal way"""
        for list_i in board:
            if list_i==[player,player,player]:
                return True
        return False
    def check_vert(board,player):
        """Checks if player has win in vertical way"""
        # is_winner=False
        for i in range(len(board)):
            list_i=[row[i] for row in board]
            if list_i==[player,player,player]:
                return True
        return False
    def check_diag(board,player):
        is_player=True
        for i in range(3):
            if board[i][i]!=player:
                is_player=False
                break
        if is_player:
            return True
        is_player=True
        for i in range(3):
            if board[2-i][i]!=player:
                is_player=False
                break
        if is_player:
            return True
        return False
    if check_diag(board,X) or check_horiz(board,X) or check_vert(board,X):
        return X
    if check_diag(board,O) or check_horiz(board,O) or check_vert(board,O):
        return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True
    



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_got=winner(board)
    if winner_got==X:
        return 1
    elif winner_got==O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    current_player=player(board) 
    if current_player==X:
        opt_move=None
        opt_value=-2
        for  action in actions(board):
            value=min_play(result(board,action))
            if value>opt_value:
                opt_value=value
                opt_move=action
        return opt_move
    else:
        opt_move=None
        opt_value=2
        for  action in actions(board):
            value=max_play(result(board,action))
            if value<opt_value:
                opt_value=value
                opt_move=action
        return opt_move


def max_play(board):
    if terminal(board):
        return utility(board)
    v=-2
    for action in actions(board):
        v=max(v,min_play(result(board=board,action=action)))
    return v


def min_play(board):
    if terminal(board):
        return utility(board)
    v=2
    for action in actions(board):
        v=min(v,max_play(result(board=board,action=action)))
    return v

    