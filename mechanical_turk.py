import chess
import time
import matplotlib.pyplot as plt
import players
import evaluation
from itertools import cycle
from typing import List, Callable

Players = List[Callable]


def play_a_game(players: Players, show: bool = False) -> int:

    board = chess.Board()
    player_cycle = cycle(players)

    while not board.is_game_over(claim_draw=True):

        player = next(player_cycle)
        move = player(board)
        board.push(move)

        if show:
            print(board, "\n")
            time.sleep(0.5)

    return evaluation.end_result(board)


def tournament(entrants: Players, rounds: int):

    winners = []
    for i in range(rounds):
        winners.append(play_a_game(entrants))
        print(f"Game No. {i}: Winner = {int(winners[-1])}")

    plot_wins(winners)


def plot_wins(winners: List[int]):

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
    play_a_game([players.minimax_player, players.alpha_beta_player], show=True)
    #tournament([players.eval_player, players.minimax_player], 10)
