import evaluation
import numpy as np
from typing import Tuple, Callable
from timeout import timeout

Board = evaluation.Board
Move = evaluation.Move
Score = float


def move(board: Board, move: Move) -> Board:
    new_board = board.copy()
    new_board.push(move)
    return new_board


def minimax(board: Board, depth: int) -> Score:

    if (depth is 0) or (board.is_game_over(claim_draw=True)):
        return evaluation.score(board)

    agg = max if board.turn else min

    return agg(minimax(move(board, m), depth - 1)
            for m in board.generate_legal_moves())



def alpha_beta(
    board: Board, depth: int, alpha: float = -np.inf, beta: float = np.inf
) -> Score:

    if (depth is 0) or (board.is_game_over(claim_draw=True)):
        val = evaluation.score(board)
        if board.turn:
            if alpha < val:
                alpha = val
            return alpha
        else:
            if beta > val:
                beta = val
            return beta

    if not board.turn:
        for m in board.generate_legal_moves():
            if alpha < beta:
                val = alpha_beta(move(board, m), depth - 1, alpha, beta)
                if beta > val:
                    beta = val
        return beta

    else:
        for m in board.generate_legal_moves():
            if alpha < beta:
                val = alpha_beta(move(board, m), depth - 1, alpha, beta)
                if alpha < val:
                    alpha = val
        return alpha



def iterative_deepen(evaluator: Callable, board: Board, time: int) -> Score:

    score = evaluator(board, 1)

    max_depth = 5
    with timeout(seconds=time):
        for i in range(2, max_depth):
            try:
                score = evaluator(board, i)
            except:
                break
    return score


def minimax_iterative_deepen(board: Board, time: int = 2) -> Score:
    return iterative_deepen(minimax, board, time)


def alpha_beta_iterative_deepen(board: Board, time: int = 2) -> Score:
    return iterative_deepen(alpha_beta, board, time)
