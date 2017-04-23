import time
import random
import chess
import numpy as np
import evaluation
from timeout import timeout

def random_player(board):
	# makes a random move each time.	
	r = random.randint(0, len(board.legal_moves)-1)
	for i, m in enumerate(board.generate_legal_moves()):
		if i == r:
			return m

def human_player(board):
	# if you want to play the turk
	display(board)
	uci = input('Your Move	')
	return chess.Move.from_uci(uci)


def eval_player(board):
	
	# this player evaluates the board after each legal move
	# and makes the move that is worst for the opponent.
	# it only differs from the random player in that it will take
	# a piece or force a mate where possible. 

	top_score = -99999
	move = None
	for m in board.generate_legal_moves():

		test_board = board.copy()
		test_board.push(m)
		score = evaluation.piece_evaluate(test_board)
		if score > top_score:
			top_score = score
			move = m

	return move


def mm_player(board):
	# minimax player

	best_score = 99999
	move = None
	n_moves = len(board.legal_moves)
	i = 0
	for m in board.generate_legal_moves():
		new_board = board.copy()
		new_board.push(m)
		score = mm_iterative_deepen(new_board, n_moves)
		#score = minimax(new_board, 1, True)
		if score < best_score:
			best_score = score
			move = m

	return move 


def ab_player(board):
	# minimax player

	best_score = 99999
	move = None
	n_moves = len(board.legal_moves)
	i = 0
	for m in board.generate_legal_moves():
		new_board = board.copy()
		new_board.push(m)
		score = ab_iterative_deepen(new_board, n_moves)
		#score = minimax(new_board, 1, True)
		if score < best_score:
			best_score = score
			move = m

	return move


def ab_iterative_deepen(board, n):

	score = alpha_beta(board, 1, -99999, 99999, True)

	d = 5
	with timeout(seconds=1/n):
		for i in range(2, d):
			try:
				s = alpha_beta(board, i, -99999, 99999, True)
			except:
				break
			print(i)
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






