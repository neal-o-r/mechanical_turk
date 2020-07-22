from evaluation import score as score_func

import numpy as np

def minimax(board_in, depth, turn=True):

    if (depth is 0) or (board_in.is_game_over(claim_draw=True)):
        return score_func(board_in)

    t = -1 if turn else 1

    best_value = t * 99999
    for m in board_in.generate_legal_moves():
        board = board_in.copy()
        board.push(m)
        v = minimax(board, depth - 1, (not t))
        best_value = max(best_value, v) if t else min(best_value, v)

    return best_value


def alpha_beta(board_in, depth, turn, alpha=-np.inf, beta=np.inf):

    if (depth == 0) or (board_in.is_game_over(claim_draw=True)):
        return score_func(board_in)

    t = -1 if turn else 1
    agg = max if turn else min
    v = t * 99999
    for m in board_in.generate_legal_moves():
        board = board_in.copy()
        board.push(m)

        v = agg(v, alpha_beta(board, depth - 1, alpha, beta, (not turn)))
        alpha = agg(alpha, v)
        if beta <= alpha:
            break

    return v


def ab_iterative_deepen(board, turn, n=2):

    score = alpha_beta(board, 1, -99999, 99999, turn)

    d = 5
    with timeout(seconds=2 / n):
        for i in range(2, d):
            try:
                s = alpha_beta(board, i, -99999, 99999, turn)
            except:
                break
            score = s
    return score


def mm_iterative_deepen(board, n):

    score = minimax(board, 1, True)

    d = 5
    with timeout(seconds=1 / n):
        for i in range(2, d):
            try:
                s = minimax(board, i, True)
            except:
                break
            score = s
    return score


