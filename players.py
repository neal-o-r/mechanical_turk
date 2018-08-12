import time
import random
import chess
import evaluation
from timeout import timeout
import mechanical_turk

'''
All 'players' have a standard API, they take a board,
and a binary flag indicating if they are playing as white (True) or black
'''

def random_player(board, white):
        '''
        makes a random move each time.
        doesn't matter if it's black or white
        '''
        return random.choice(list(board.generate_legal_moves()))


def human_player(board, white):
        '''
        if you want to play the turk
        '''
        mechanical_turk.display(board)
        uci = input('Your Move  ')
        move = chess.Move.from_uci(uci)
        if move not in list(board.generate_legal_moves()):
                print('Not a valid move, try again')
                human_player(board, white)
        return move


def eval_player(board, white):
        '''
        this player evaluates the board after each legal move
        and makes the move that is worst for the opponent.
        it only differs from the random player in that it will take
        a piece or force a mate where possible.
        '''
        t = 1 if white else -1
        top_score = -99999
        move = None
        for m in board.generate_legal_moves():
                test_board = board.copy()
                test_board.push(m)
                score = t * evaluation.piece_evaluate(test_board)
                if score > top_score:
                        top_score = score
                        move = m

        return move


def mm_player(board, white):
        # minimax player
        t = 1 if white else -1
        best_score = -99999
        move = None
        n_moves = board.legal_moves.count()
        for m in board.generate_legal_moves():
                new_board = board.copy()
                new_board.push(m)
                score = t * mm_iterative_deepen(new_board, n_moves)
                if score > best_score:
                        best_score = score
                        move = m

        return move


def ab_player(board, white):
        # AB pruned minimax player
        t = 1 if white else -1
        best_score = -99999
        move = None
        n_moves = board.legal_moves.count()
        i = 0
        for m in board.generate_legal_moves():
                new_board = board.copy()
                new_board.push(m)
                score = t * ab_iterative_deepen(new_board, n_moves)
                if score > best_score:
                        best_score = score
                        move = m

        return move


def ab_iterative_deepen(board, n):

        score = alpha_beta(board, 1, -99999, 99999, True)

        d = 5
        with timeout(seconds=2/n):
                for i in range(2, d):
                        try:
                                s = alpha_beta(board, i, -99999, 99999, True)
                        except:
                                break
                        score = s
        return score


def mm_iterative_deepen(board, n):

        score = minimax(board, 1, True)

        d = 5
        with timeout(seconds=1/n):
                for i in range(2, d):
                        try:
                                s = minimax(board, i, True)
                        except:
                                break
                        score = s
        return score

def minimax(board_in, depth, turn):


        if (depth == 0) or (board_in.is_game_over(claim_draw=True)):
                return evaluation.piece_evaluate(board_in)

        if turn:
                best_value = -99999
                for m in board_in.generate_legal_moves():
                        board = board_in.copy()
                        board.push(m)
                        v = minimax(board, depth-1, False)
                        best_value = max(best_value, v)

                return best_value

        else:

                best_value = 99999
                for m in board_in.generate_legal_moves():
                        board = board_in.copy()
                        board.push(m)
                        v = minimax(board, depth-1, True)
                        best_value = min(best_value, v)

                return best_value


def alpha_beta(board_in, depth, alpha, beta, turn):

        if (depth == 0) or (board_in.is_game_over(claim_draw=True)):
                return evaluation.piece_evaluate(board_in)

        if turn:
                v = -99999
                for m in board_in.generate_legal_moves():
                        board = board_in.copy()
                        board.push(m)

                        v = max(v, alpha_beta(board, depth-1, alpha, beta, False))
                        alpha = max(alpha, v)
                        if beta <= alpha:
                                break

                return v

        else:
                v = 99999
                for m in board_in.generate_legal_moves():
                        board = board_in.copy()
                        board.push(m)

                        v = min(v, alpha_beta(board, depth-1, alpha, beta, True))
                        beta = min(beta, v)
                        if beta <= alpha:
                                break

                return v
