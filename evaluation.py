import chess
import random
import numpy as np
from boardvalues import boardvalue
from typing import Tuple, Dict, Callable

Board = chess.Board
Move = chess.Move
Piece = int
Scores = Tuple[float, float]

piecevalues = {
    chess.PAWN: 100,
    chess.BISHOP: 330,
    chess.QUEEN: 900,
    chess.KNIGHT: 320,
    chess.ROOK: 500,
}


def end_result(board: Board) -> int:
    """
    check for draw, if not return 1 for white -1 for black
    """
    return 0 if board.result() == "*" else eval(board.result())


def score_piece(piece: Piece, board: Board) -> Scores:
    """
    compute score for a given piece type
    """
    white_pieces = list(board.pieces(piece, True))  # locations of pieces
    black_pieces = list(board.pieces(piece, False))

    # get piece board values and reverse it for white
    piece_chart = boardvalue[piece]

    white_score = len(white_pieces) * piecevalues[piece] + np.sum(
        piece_chart[::-1][white_pieces]
    )  # reverse board for white

    black_score = len(black_pieces) * piecevalues[piece] + np.sum(
        piece_chart[black_pieces]
    )

    return white_score, black_score


def score(board: Board) -> float:
    """
    evaluate board by summing all opponents pieces
    and checking for mate
    returns a postive value for white adv, neg for black
    """
    # if the game is over, return a large score
    if board.is_game_over(claim_draw=True):
        return end_result(board) * 10000

    diff = lambda scores: scores[0] - scores[1]

    score = random.random() + sum(  # to break ties
        diff(score_piece(p, board)) for p in piecevalues
    )

    return score


def score_move(board: Board, move: Move, score_func: Callable = score) -> float:
    """
    Try move, return the score for each colour (white, black)
    """
    test_board = board.copy()
    test_board.push(move)
    return score_func(test_board)
