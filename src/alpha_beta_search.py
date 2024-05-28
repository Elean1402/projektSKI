from evalFunction import *
from gameserver import *
from scoreConfig_evalFunc import *
from board import *
from game import *
from gui import *

efr = EvalFunction(ScoreConfig.Version1(), Player.Red)
efb = EvalFunction(ScoreConfig.Version1(), Player.Blue)
def alpha_beta_search(game: dict):
	print(game["board"])

	init_board(*GameState.createBitBoardFrom(Gui.fenToMatrix(game["board"]), True))
	print_state()
	temp = get_Board().copy()
	print(temp)
	alpha = -float('inf')
	beta = float('inf')
	depth = 2
	l = dict()
	best_score = alpha_beta_max(alpha, beta, depth, game, l, temp)
	print("best score", best_score)

	return best_score


def alpha_beta_max(alpha, beta, depth_left: int, game: dict, l, temp) -> int:
	m = MoveLib()
	
	if depth_left == 0:
		return 2

	scorelist = efb.computeOverallScore(board.blue_generation(), board=temp)
	print([(m.move(x[0],x[1],3))for x in scorelist])
	for i in range(len(scorelist)):
		
		move = scorelist.pop()
		print("best move for Player Blue=", m.move(move[0],move[1],3))
		print("state before move execution:")
		print(GameState.fromBitBoardToMatrix(temp,True))
		board.blue_move_execution(move[0], move[1])
		newBoard = get_Board()
		gameResponse = isOver()
		print("GameResponse = ", gameResponse)
		if(gameResponse == "c"):
			print("Board after move exec")
			print(GameState.fromBitBoardToMatrix(newBoard,True))
			print(newBoard)
			score = alpha_beta_min(alpha, beta, depth_left - 1, game, l, newBoard)
		
			#takeback(*stack.pop())

			l[move] = score
			# rework move
			if score >= beta:
				return beta  # fail hard beta-cutoff
			if score > alpha:
				alpha = score  # alpha acts like max in MiniMax
		elif(gameResponse == 'Blue Won'):
			print(gameResponse)
			return 1000
		return alpha


def alpha_beta_min(alpha, beta, depth_left: int, game: dict, l, temp) -> int:
	m = MoveLib()
	
	if depth_left == 0:
		return 3

	scorelist = efr.computeOverallScore(board.red_generation(), temp)
	print("Züge:",[(m.move(x[0],x[1],3))for x in scorelist])
	
	for i in range(len(scorelist)):
		
		move = scorelist.pop()
		print("best move for Player red", m.move(move[0],move[1],3))
		print("state before move execution:")
		print(GameState.fromBitBoardToMatrix(temp,True))
		board.red_move_execution(move[0], move[1])
		newBoard = get_Board()
		gameResponse = isOver()
		print("GameResponse = ", gameResponse)
		if(gameResponse == "c"):
			print("Board after move exec")
			print(GameState.fromBitBoardToMatrix(newBoard,True))
			print(newBoard)
			score = alpha_beta_max(alpha, beta, depth_left - 1, game, l, newBoard)
		
			#takeback(*stack.pop())
			# rework move
			l[move] = score
			if score <= alpha:
				return alpha  # fail hard alpha-cutoff
			if score < beta:
				beta = score  # beta acts like min in MiniMax
		elif(gameResponse == "Red Won"):
			print("red Won")
			return 1000

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
	if game['player'] == "b":
		blue_takeback(source, dest, hit=False)
	else:
		red_takeback(source, dest, hit=False)
