import gameserver
from zuggenerator import *
from benchmark import *
import numpy as np
from gameserver import *

bitboard, fen_string, player = gameserver.init()


def alpha_beta_max(alpha: int, beta: int, depth_left: int, player=player) -> int:
    if depth_left == 0:
        return rating()

    for move in generate_moves():
        score = alpha_beta_min(alpha, beta, depth_left - 1)
        if score >= beta:
            return beta  # fail hard beta-cutoff
        if score > alpha:
            alpha = score  # alpha acts like max in MiniMax
    return alpha


def alpha_beta_min(alpha: int, beta: int, depth_left: int) -> int:
    if depth_left == 0:
        score = rating()
        return -score
    for move in generate_moves():
        score = alpha_beta_max(alpha, beta, depth_left - 1)
        if score <= alpha:
            return alpha  # fail hard alpha-cutoff
        if score < beta:
            beta = score  # beta acts like min in MiniMax
    return beta


def generate_moves(player=player):
    # rufe alpha_beta_max mit alpha.generation auf, wenn wir Blau sind
    # und ruf alpha_beta_min mit beta.generation
    # rufe alpha_beta_max mit beta.generation auf, wenn wir rot sind
    # und ruf alpha_beta_min mit alpha.generation
    init_position(*bitboard)
    if player == "b":
        player = "r"
        return alpha_generation()
    elif player == "r":
        player = "b"
        return beta_generation()
    else:
        raise ValueError("Player must be either b or r")


if __name__ == '__main__':
    bitboard, fen_string, player = gameserver.init()
    init_position(*bitboard)
    score = alpha_beta_max(-100000, +100000, 5)
    print(score)
