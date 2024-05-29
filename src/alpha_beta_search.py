from src.evalFunction import *
from src.gameserver import *
from src.scoreConfig_evalFunc import *
from src.board import *
from src.game import *
from src.gui import *

depth = 3

def alpha_beta_search(game: dict):
	print(game["board"])
	player = game["player"]
	temp = GameState.createBitBoardFrom(Gui.fenToMatrix(game["board"]), True)
	init_board(*temp)
	print("Start Position")
	print_state()
	alpha = -float('inf')
	beta = float('inf')
	l = dict()
	best_score = alpha_beta_max(alpha, beta, depth, game, l, temp)
	print("best score", best_score)

	return best_score


def alpha_beta_max(alpha, beta, depth_left: int, game: dict, l, temp) -> int:
	m = MoveLib()
	efblue = EvalFunction(ScoreConfig.Version1(), Player.Blue)
	if depth_left == 0:
		return 2

	gen = board.blue_generation()
	print(moves_to_string(gen))
	if len(gen) == 0:

		scorelist = []
	else:
		scorelist = efblue.computeOverallScore(gen, board=temp)
		print([(m.BitsToPosition(x[0]),m.BitsToPosition(x[1])) for x in scorelist])


	for i in range(len(scorelist)):

		move = scorelist.pop()
		temp = [board.red_p, board.red_k, board.blue_p, board.blue_k].copy()
		board.blue_move_execution(move[0], move[1])

		print(f'Depth: {depth-depth_left+1}')
		print_state("Blue")
		input("Cont: ")

		temp2 = [board.red_p, board.red_k, board.blue_p, board.blue_k].copy()
		# print("before alpha_beta_min")
		# print_state()
		score = alpha_beta_min(alpha, beta, depth_left - 1, game, l, temp2)
		#init_board(*temp)
		# print("before takeback")
		# print_state()

		
		last_move =stack.pop()
		# print("to take back")
		# print("source")
		# print_board(last_move[0])
		# print("dest")
		# print_board(last_move[1])
		blue_takeback(*last_move)

		# takeback(*last_move,game)
		print("Blue takeback")
		print_state()
		input("Cont: ")


		l[move] = score
		# rework move
		if score >= beta:
			return beta  # fail hard beta-cutoff
		if score > alpha:
			alpha = score  # alpha acts like max in MiniMax

	return alpha


def alpha_beta_min(alpha, beta, depth_left: int, game: dict, l, temp) -> int:
	m = MoveLib()
	efred = EvalFunction(ScoreConfig.Version1(), Player.Red)
	if depth_left == 0:
		return 3
	gen = board.red_generation()
	print(moves_to_string(gen))
	if len(gen) == 0:
		scorelist = []

	else:
		scorelist = efred.computeOverallScore(gen, board=temp)
		print([(m.BitsToPosition(x[0]), m.BitsToPosition(x[1])) for x in scorelist])
	
	for i in range(len(scorelist)):

		move = scorelist.pop()
		temp = [board.red_p, board.red_k, board.blue_p, board.blue_k].copy()
		board.red_move_execution(move[0], move[1])

		print(f'Depth: {depth-depth_left+1}')
		print_state("Red")
		input("Cont: ")



		temp2 = [board.red_p, board.red_k,board.blue_p, board.blue_k].copy()

		# print("before alpha_beta_max")
		# print_state()
		score = alpha_beta_max(alpha, beta, depth_left - 1, game, l, temp2)
		# init_board(*temp)
		# print("before takeback")
		# print_state()

		last_move =stack.pop()
		# print("to take back")
		# print("source")
		# print_board(last_move[0])
		# print("dest")
		# print_board(last_move[1])
		red_takeback(*last_move)

		print("Red takeback")
		print_state()
		input("Cont: ")
		
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



