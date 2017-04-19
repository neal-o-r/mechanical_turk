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

def human_player(board):

	display(board)
	uci = input('Your Move  ')
	return chess.Move.from_uci(uci)


def display(board):
	
	print(board)
	print('\n')		


def play_a_game(players):

	board = chess.Board()
	i = 0
	while not board.is_game_over():
				
		player = players[i % 2]	
		move = player(board)
		board.push(move)
		i += 1
		
	if board.is_stalemate():
		return 0
	else:
		return 1 + int(board.turn)

def plot_wins(winners):

	win1 = winners.count(1)
	win2 = winners.count(2)	
	draw = winners.count(0)

	fig = plt.figure()
	ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

	ax.bar([0, 1, 2], [win1, win2, draw], align='center')
	ax.set_xticks([0, 1, 2])
	ax.set_xticklabels(('Player1', 'Player2', 'Draw'))
	plt.show()


def tournament(entrants, rounds):
	
	winners = []
	for i in range(rounds):
		
		winners.append(play_a_game(entrants))

	plot_wins(winners)
