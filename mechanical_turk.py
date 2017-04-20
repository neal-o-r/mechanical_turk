import chess
import time
import matplotlib.pyplot as plt
import random

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


def display(board):
	
	print(board)
	print('\n')		
	time.sleep(1)

def play_a_game(players):

	board = chess.Board()
	i = 0
	while not board.is_game_over(claim_draw=True):
				
		player = players[i % 2]	
		move = player(board)
		board.push(move)
		i += 1
	
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
