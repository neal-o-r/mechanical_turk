import chess
import time
import matplotlib.pyplot as plt
import numpy as np


def random_player(board):
	
	if board.is_game_over(): return None

	r = np.random.randint(0, len(board.legal_moves))
	for i, m in enumerate(board.generate_legal_moves()):
		if i == r:
			return m	

def display(board):
	
	print(board)
	print('\n')		


def play_a_game(player1, player2):

	board = chess.Board()
	
	player = player1
	while not board.is_game_over():
	
		move = player(board)
		board.push(move)
		player = player2		

		continue
	
	if board.is_stalemate():
		return 0
	else:
		return 1 + int(board.turn)


def tournament(entrants, rounds):
	
	player1, player2 = entrants[0], entrants[1]

	winners = []
	for i in range(rounds):
		
		winners.append(play_a_game(player1, player2))

	win1 = winners.count(1)
	win2 = winners.count(2)	
	draw = winners.count(0)

	plt.bar([0, 1, 2], [win1, win2, draw])
	plt.show()
