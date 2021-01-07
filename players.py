import time
import random
import chess
import evaluation
from timeout import timeout
from strategies import (
    alpha_beta_iterative_deepen,
    minimax_iterative_deepen,
    alpha_beta,
    minimax,
)


Board = chess.Board
Move = chess.Move
Scores = evaluation.Scores
"""
All 'players' have a standard API, they take a board and return a move
"""


def random_player(board: Board) -> Move:
    """
        makes a random move each time.
        """
    return random.choice(list(board.generate_legal_moves()))


def human_player(board: Board) -> Move:
    """
        if you want to play
        """
    print(board)
    uci = input("Your Move  ")
    move = chess.Move.from_uci(uci)
    if move not in list(board.generate_legal_moves()):
        print("Not a valid move, try again")
        human_player(board)

    return move


def eval_player(board: Board) -> Move:
    """
    this player evaluates the board after each legal move
    and makes the move that is worst for the opponent.
    """
    # take the highest score if white, lowest if black
    agg = max if board.turn else min
    moves = list(board.generate_legal_moves())

    score = lambda m: evaluation.score_move(board, m)

    return agg(moves, key=score)


def minimax_player(board: Board, depth: int = 1) -> Move:
    """
    This player plays a minimax strategy,
    and looks `depth` ahead
    """
    agg = max if board.turn else min
    moves = list(board.generate_legal_moves())

    score = lambda m: evaluation.score_move(
        board, m, score_func=lambda b: minimax(b, depth)
    )

    return agg(moves, key=score)


def alpha_beta_player(board: Board, depth: int = 2, iterative: bool = False) -> Move:
    """
    This player plays alpha beta strategy,
    and looks `depth` ahead.
    Iterative deepens if iterative = True
    """
    agg = max if board.turn else min
    ab = alpha_beta_iterative_deepen if iterative else alpha_beta

    moves = list(board.generate_legal_moves())

    score = lambda m: evaluation.score_move(
            board, m, score_func=lambda b: ab(b, depth))

    return agg(moves, key=score)
