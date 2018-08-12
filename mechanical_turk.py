import chess
import time
import matplotlib.pyplot as plt
import random
import players


def display(board):

        s = str(board)
        s = [str(8-i) + '. '+v for i, v in enumerate(s.split('\n'))]
        s = '\n'.join(s)

        print(s)
        print('   A B C D E F G H')
        print('\n')
        time.sleep(0.5)


def play_a_game(players, show=False):

        board = chess.Board()
        i = 0
        while not board.is_game_over(claim_draw=True):

                player = players[i % 2]
                move = player(board, not(i % 2))
                board.push(move)
                i += 1
                if show: display(board)

        return 0 if board.result() == '*' else eval(board.result())


def plot_wins(winners):

        win1 = winners.count(1)
        win2 = winners.count(-1)
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
                print("Game No. {}".format(i))
                winners.append(play_a_game(entrants))
                print('Winner,', winners[-1])

        plot_wins(winners)

#play_a_game([players.mm_player, players.random_player], show=True)
