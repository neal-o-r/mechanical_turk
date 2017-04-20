import time
import random
import chess


def random_player(board):
        # makes a random move each time.        
        r = random.randint(0, len(board.legal_moves)-1)
        for i, m in enumerate(board.generate_legal_moves()):
                if i == r:
                        return m

def human_player(board):
        # if you want to play the turk
        display(board)
        uci = input('Your Move  ')
        return chess.Move.from_uci(uci)


def eval_player(board):
        # this player evaluates the board after each legal move
        # and makes the move that is worst for the opponent.
        # it only differs from the random player in that it will take
        # a piece or force a mate where possible. 

        top_score = 9999
        move = None
        for m in board.generate_legal_moves():

                test_board = board.copy()
                test_board.push(m)
                score = piece_evaluate(test_board)
                if score <= top_score:
                        top_score = score
                        move = m

        return move


def mm_player(board):
	# minimax player

	depth = 3

	best_score = -9999
	move = None
	for m in board.generate_legal_moves():
		
		new_board = board.copy()
		new_board.push(m)
		score = minimax(new_board, depth, True)
		if score > best_score:
			score = best_score
			move = m

	return move 


def minimax(board, depth, turn):

	
	if (depth == 0) or (board.is_game_over(claim_draw=True)):
		return piece_evaluate(board)		

	if turn:
		best_value = -9999
		for m in board.generate_legal_moves():
			board.push(m)
			v = minimax(board, depth-1, False)
			best_value = max(best_value, v)
		return best_value

	else:
		best_value = 9999
		for m in board.generate_legal_moves():
			board.push(m)
			v = minimax(board, depth-1, True)
			best_value = min(best_value, v)
		return best_value


def piece_evaluate(board):

        # evaluate board by summing all opponents pieces
        # and checking for mate
        if board.is_checkmate(): return -100

        score = random.random() #to break ties
        for piece, value in [(chess.PAWN, 1),
                                (chess.BISHOP, 4),
                                (chess.QUEEN, 10),
                                (chess.KNIGHT, 5),
                                (chess.ROOK, 3)]:

                score += len(board.pieces(piece, True)) * value

        return score

