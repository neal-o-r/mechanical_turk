import chess
import random
import numpy as np
from movetable import move_table

piece_values = {
    chess.PAWN: 100,
    chess.BISHOP: 330,
    chess.QUEEN: 900,
    chess.KNIGHT: 320,
    chess.ROOK: 500,
}


def end_result(board):
    """
    check for draw, if not return 1 for white -1 for black
    """
    return 0 if board.result() == "*" else eval(board.result())


def score_piece(piece, board, white=True):
    """
    compute score for a given piece type
    """
    pieces = list(board.pieces(piece, white))  # pieces of this kind

    # reverse the board for white
    score_chart = move_table[piece][::-1] if white else move_table[piece]

    return len(pieces) * piece_values[piece] + np.sum(score_chart[pieces])


def score(board):
    """
        evaluate board by summing all opponents pieces
        and checking for mate
        returns a postive value for white adv, neg for black
        """
    # if the game is over, return a large score
    if board.is_game_over(claim_draw=True):
        return end_result(board) * 10000

    score = (
        random.random()  # to break ties
        + sum(score_piece(p, board) for p in piece_values)
        - sum(score_piece(p, board, False) for p in piece_values)
    )

    return score
