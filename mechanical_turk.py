import chess
import time
import matplotlib.pyplot as plt
import random
import players


def display(board):
	
	print(board)
	print('\n')		
	time.sleep(1)


def play_a_game(players, show=False):

	board = chess.Board()
	i = 0
	while not board.is_game_over(claim_draw=True):
				
		player = players[i % 2]	
		move = player(board)
		board.push(move)
		i += 1
		if show: display(board)
	
	return board.result()


def plot_wins(winners):

	win1 = winners.count('1-0')
	win2 = winners.count('0-1')	
	draw = winners.count('1/2-1/2')

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

play_a_game([players.random_player, players.mm_player], show=True)
