import chess
import time
import matplotlib.pyplot as plt
import random
from itertools import cycle
import players


def play_a_game(players, show=False):

    board = chess.Board()
    # make a cycle of players and colours (white, black)
    player_cycle = cycle(zip(players, [True, False]))

    while not board.is_game_over(claim_draw=True):

        player, color = next(player_cycle)
        move = player(board, color)
        board.push(move)
        if show:
            print(board)
            time.sleep(0.5)

    return 0 if board.result() == "*" else eval(board.result())


def tournament(entrants, rounds):

    winners = []
    for i in range(rounds):
        winners.append(play_a_game(entrants))
        print(f"Game No. {i}: Winner = {int(winners[-1])}")

    plot_wins(winners)


def plot_wins(winners):

    win1 = winners.count(1)
    win2 = winners.count(-1)
    draw = winners.count(0)

    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    ax.bar([0, 1, 2], [win1, win2, draw], align="center")
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(("Player1", "Player2", "Draw"))
    plt.show()


if __name__ == "__main__":
    tournament([players.eval_player, players.minimax_player], 10)
