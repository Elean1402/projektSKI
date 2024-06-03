from board import *
from game import *
from gameserver import *
from gui import *
from scoreConfig_evalFunc import *
from evalFunction import *
import time

GET_PLAYER_INDEX = 1
GET_BOARD_INDEX = 0


class AlphaBetaSearch:
	def __init__(self, game, time_limit=2):
		self.moveLib = MoveLib()
		self.eval = EvalFunction(ScoreConfig.Version1(), Player.Blue)
		self.game = game
		self.player = self.game[GET_PLAYER_INDEX]
		self.gameOver = False  # or some other initial state
		self.bitboards = self.game[GET_BOARD_INDEX]  # Set this to the initial bitboards
		self.eval = EvalFunction(ScoreConfig.Version1(),
								 self.player)  # Set this to an instance of your evaluation function
		self.best_move = None
		self.time_limit = time_limit 

	
	def search(self, iterative_deepening=False):
		start_time = time.time()
		init_board(*self.bitboards)
		if iterative_deepening:
			depth = 1
			while True:
				result, temp_move = self.alphaBetaMax(-1000000, 1000000, depth, self.bitboards, start_time)
				if temp_move is not None:
					self.best_move = [self.moveLib.BitsToPosition(temp_move[0]),
										self.moveLib.BitsToPosition(temp_move[1])]
				if self.is_game_over() or time.time() - start_time > self.time_limit:
					break
				depth += 1
		else:
			result, temp_move = self.alphaBetaMax(-1000000, 1000000, 2, self.bitboards, start_time)
			if temp_move is not None:
				self.best_move = [self.moveLib.BitsToPosition(temp_move[0]),
									self.moveLib.BitsToPosition(temp_move[1])]
		return self.best_move


	def alphaBetaMax(self, alpha, beta, depthleft, bitboard_copy, start_time):
		self.player = Player.Blue
		if depthleft == 0:
			etc = generate_moves(self.player)
			if len(etc) != 0:
				points = self.eval.computeOverallScore(etc, board=bitboard_copy)[0][3]
			else:
				points = -10000

			return points, None
		moves = generate_moves(self.player)
		if len(moves) == 0:
			scorelist = []
		else:
			moves_string = moves_to_string(moves)
			print("moves", moves_string)
			scorelist = self.eval.computeOverallScore(moves, board=bitboard_copy)

		for i in range(len(scorelist)):
			if time.time() - start_time > self.time_limit:
				return None, None
			move = scorelist.pop()
			bitboard_copy = [red_p, red_k, blue_p, blue_k]
			execute_move(self.player, move)
			score, _ = self.alphaBetaMin(alpha, beta, depthleft - 1, bitboard_copy, start_time)
			self.player = Player.Blue
			takeback(self.player, move)

			if score >= beta:
				return beta, None

			if score > alpha:
				temp_move = move
				alpha = score

		return alpha, temp_move


	def alphaBetaMin(self, alpha, beta, depthleft, bitboard_copy, start_time):
		self.player = Player.Red
		if depthleft == 0:
			etc = generate_moves(self.player)
			points = -self.eval.computeOverallScore(etc, board=bitboard_copy)[0][3]
			print("points", points)
			return points, None
		moves = generate_moves(self.player)
		if len(moves) == 0:
			scorelist = []
		else:
			moves_string = moves_to_string(moves)
			print("moves", moves_string)
			scorelist = self.eval.computeOverallScore(moves,board=bitboard_copy)

		for i in range(len(scorelist)):
			if time.time() - start_time > self.time_limit:
				return None, None
			move = scorelist.pop()
			bitboard_copy = [red_p, red_k, blue_p, blue_k]
			execute_move(self.player, move)
			score, _ = self.alphaBetaMax(alpha, beta, depthleft - 1, bitboard_copy, start_time)
			print(score)
			self.player = Player.Red
			takeback(self.player, move)
			if score <= alpha:
				return alpha, None
			if score < beta:
				beta = score

		return beta, None


def generate_moves(player) -> list:
	# rufe alpha_beta_max mit alpha.generation auf, wenn wir Blau sind
	# und ruf alpha_beta_min mit beta.generation
	# rufe alpha_beta_max mit beta.generation auf, wenn wir rot sind
	# und ruf alpha_beta_min mit alpha.generation

	if player == Player.Blue:
		return blue_generation()
	elif player == Player.Red:
		return red_generation()
	else:
		raise ValueError("Player must be either b or r")


def execute_move(player, move):
	if player == Player.Blue:
		blue_move_execution(move[0], move[1])
	elif player == Player.Red:
		red_move_execution(move[0], move[1])


def takeback(player, move):
	if player == Player.Blue:
		blue_takeback(move[0], move[1])
	elif player == Player.Red:
		red_takeback(move[0], move[1])


def search(state):
	search_instance = AlphaBetaSearch(state)
	result = search_instance.search()
	print(result)
	return result


if __name__ == '__main__':
	test7 = "6/8/8/8/1r01b04/8/8/6 b"
	fen, player = test7.split(" ")
	player = Player.Blue if player == "b" else Player.Red
	bitboard = GameState.createBitBoardFrom(Gui.fenToMatrix(fen), True)
	gameArray = [bitboard, player, True, False]
	search(gameArray)