import time
import random
import chess
import evaluation
from timeout import timeout
import mechanical_turk
from strategies import (ab_iterative_deepen,
        mm_iterative_deepen, alpha_beta, minimax)


"""
All 'players' have a standard API, they take a board,
and a binary flag indicating if they are playing as white (True) or black
"""

def random_player(board, white):
    """
        makes a random move each time.
        doesn't matter if it's black or white
        """
    return random.choice(list(board.generate_legal_moves()))


def human_player(board, white):
    """
        if you want to play the turk
        """
    print(board)
    uci = input("Your Move  ")
    move = chess.Move.from_uci(uci)
    if move not in list(board.generate_legal_moves()):
        print("Not a valid move, try again")
        human_player(board, white)
    return move


def eval_player(board, white):
    """
        this player evaluates the board after each legal move
        and makes the move that is worst for the opponent.
        it only differs from the random player in that it will take
        a piece or force a mate where possible.
        """
    t = 1 if white else -1
    top_score = -99999
    move = None
    for m in board.generate_legal_moves():
        test_board = board.copy()
        test_board.push(m)
        score = t * evaluation.score(test_board)
        if score > top_score:
            top_score = score
            move = m

    return move


def minimax_player(board, white, depth=1):
    """
    This player plays a minimax strategy,
    and looks $depth / 2 moves ahead
    """
    t = 1 if white else -1
    best_score = -99999
    move = None
    for m in board.generate_legal_moves():
        new_board = board.copy()
        new_board.push(m)
        score = t * minimax(new_board, depth)
        if score > best_score:
            best_score = score
            move = m

    return move


def alpha_beta_player(board, white, depth=1):
    # AB pruned minimax player
    t = 1 if white else -1
    best_score = -99999
    move = None
    n_moves = board.legal_moves.count()
    i = 0
    for m in board.generate_legal_moves():
        new_board = board.copy()
        new_board.push(m)
        score = t * ab_iterative_deepen(new_board, (not white))
        if score > best_score:
            best_score = score
            move = m

    return move
