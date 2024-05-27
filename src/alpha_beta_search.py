from evalFunction import *
from gameserver import *
from scoreConfig_evalFunc import *
from board import *
from game import *
from gui import *

def alpha_beta_search(game: dict):
	print(game["board"])

	init_board(*GameState.createBitBoardFrom(Gui.fenToMatrix(game["board"]), True))
	print_state()
	temp = GameState.createBitBoardFrom(Gui.fenToMatrix(game["board"]), True)
	alpha = -float('inf')
	beta = float('inf')
	depth = 2
	l = dict()
	best_score = alpha_beta_max(alpha, beta, depth, game, l, temp)
	print("best score", best_score)

	return best_score


def alpha_beta_max(alpha, beta, depth_left: int, game: dict, l, temp) -> int:
	m = MoveLib()
	ef = EvalFunction(ScoreConfig.Version1(), Player.Blue)
	if depth_left == 0:
		return 2

	scorelist = ef.computeOverallScore(board.blue_generation(), board=temp)

	for i in range(len(scorelist)):

		move = scorelist.pop()
		board.blue_move_execution(move[0], move[1])
		temp = [board.blue_p, board.blue_k, board.red_p, board.red_k]
		score = alpha_beta_min(alpha, beta, depth_left - 1, game, l, temp)
		init_board(*temp)
		#takeback(*stack.pop())

		l[move] = score
		# rework move
		if score >= beta:
			return beta  # fail hard beta-cutoff
		if score > alpha:
			alpha = score  # alpha acts like max in MiniMax

	return alpha


def alpha_beta_min(alpha, beta, depth_left: int, game: dict, l, temp) -> int:
	m = MoveLib()
	ef = EvalFunction(ScoreConfig.Version1(), Player.Red)
	if depth_left == 0:
		return 3

	scorelist = ef.computeOverallScore(board.red_generation(), board=temp)
	print("2",scorelist)
	for i in range(len(scorelist)):
		move = scorelist.pop()
		#board.red_move_execution(move[0], move[1])
		temp = [board.blue_p, board.blue_k, board.red_p, board.red_k]
		score = alpha_beta_max(alpha, beta, depth_left - 1, game, l, temp)
		init_board(*temp)
		#takeback(*stack.pop())
		# rework move
		l[move] = score
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

	if game["player"] == "b":
		game["player"] = "r"
		return blue_generation()
	elif game["player"] == "r":
		game["player"] = "b"

		return red_generation()
	else:
		raise ValueError("Player must be either b or r")


def takeback(source, dest, hit=False):
	if player == "b":
		blue_takeback(source, dest, hit=False)
	else:
		red_takeback(source, dest, hit=False)
