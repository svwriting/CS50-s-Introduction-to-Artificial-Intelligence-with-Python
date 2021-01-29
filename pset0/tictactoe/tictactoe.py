"""
Tic Tac Toe Player
"""

import math

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
    count_=0
    for i in range(3):
        for j in range(3):
            if board[i][j]==EMPTY:
                count_+=1
    if count_%2:
        return X
    else:
        return O
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions=set()
    for i in range(3):
        for j in range(3):
            if board[i][j]==EMPTY:
                possible_actions.add((i,j))
    return possible_actions
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    nowplayer=player(board)
    nboard=initial_state()
    for i in range(3):
        nboard[i]=board[i].copy()
    if board[action[0]][action[1]]==EMPTY:
        nboard[action[0]][action[1]]=nowplayer
        return nboard
    else:
        raise NameError('valid action!')
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0]==board[i][1]==board[i][2]:
            return board[i][0]
        elif board[0][i]==board[1][i]==board[2][i]:
            return board[0][i]
    if board[0][0]==board[1][1]==board[2][2] or board[0][2]==board[1][1]==board[2][0]:
        return board[1][1]
    return None
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    for i in range(3):
        for j in range(3):
            if board[i][j]==EMPTY:
                return False
    return True
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board)==X:
        return 1
    elif winner(board)==O:
        return -1
    else:
        return 0
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    """
    def maxv(board,V=20):
        actionsSet=actions(board)
        v,v_=-2,0
        for action in actionsSet:
            temp_b=result(board,action)
            if terminal(temp_b):
                v_+=utility(temp_b)
            else:
                v_=minv(temp_b,v)
            if v_>v:
                v=v_
        return v
    def minv(board,V=-20):
        actionsSet=actions(board)
        v,v_=2,0
        for action in actionsSet:
            temp_b=result(board,action)
            if terminal(temp_b):
                v_+=utility(temp_b)
            else:
                v_=maxv(temp_b,v)
            if v_<v:
                v=v_
        return v
    """
    def sumv(board,w=1): # calculate score of a state =sigma(w*utility(terminal board))
        actionsSet=actions(board)
        temp_=len(actionsSet)
        if temp_>0:
            w/=len(actionsSet)
        sum_=0
        for action in actionsSet:
            temp_b=result(board,action)
            if terminal(temp_b):
                sum_+=utility(temp_b)*w
            else:
                sum_+=sumv(temp_b,w)
        return sum_
    ############################################
    if terminal(board):
        return None
    elif board[1][1]==EMPTY:
        return (1,1)
    elif board[0][0]==EMPTY:
        return (0,0)
    else:
        actionsSet=actions(board)
        move=None
        if player(board)=='X':
            V=-2
            for action in actionsSet:
                #V_=minv(result(board,action))
                V_=sumv(result(board,action))
                if V<V_:
                    V=V_
                    move=action
        else:
            V=2
            for action in actionsSet:
                #V_=maxv(result(board,action))
                V_=sumv(result(board,action))
                if V>V_:
                    V=V_
                    move=action
        return move
    raise NotImplementedError