import gameserver
from zuggenerator import *
from benchmark import *
import numpy as np
from gameserver import *
from gamestate import *
from moveLib import *

def alpha_beta_max(alpha: int, beta: int, depth_left: int, game: dict) -> int:
	if depth_left == 0:
		return rating()

	for move in generate_moves(game):
		score = alpha_beta_min(alpha, beta, depth_left - 1, game)
		if score >= beta:
			return beta  # fail hard beta-cutoff
		if score > alpha:
			alpha = score  # alpha acts like max in MiniMax
	return alpha


def alpha_beta_min(alpha: int, beta: int, depth_left: int, game: dict) -> int:
	if depth_left == 0:
		return - rating()
	for move in generate_moves(game):
		score = alpha_beta_max(alpha, beta, depth_left - 1, game)
		if score <= alpha:
			return alpha  # fail hard alpha-cutoff
		if score < beta:
			beta = score  # beta acts like min in MiniMax
	return beta


def generate_moves(game: dict) -> list:
	# rufe alpha_beta_max mit alpha.generation auf, wenn wir Blau sind
	# und ruf alpha_beta_min mit beta.generation
	# rufe alpha_beta_max mit beta.generation auf, wenn wir rot sind
	# und ruf alpha_beta_min mit alpha.generation
	m = MoveLib()
	board, player = game["board"].split(" ")
	init_position(*GameState.createBitBoardFrom(Gui.fenToMatrix(board), True))
	if player == "b":
		player = "r"
		gen = moves_to_string(alpha_generation())
		source, dest = gen[0].split("-")
		#print(gen[0])
		#print(m.move(source, dest, mode=1))
		print(alpha_generation())
		alpha_p_move_execution(*m.move(source, dest, mode=1))
		print(alpha_generation())
		return alpha_generation()
	elif player == "r":
		player = "b"
		return beta_generation()
	else:
		raise ValueError("Player must be either b or r")
