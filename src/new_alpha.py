from board import *
from game import *
from gameserver import *
from gui import *
from scoreConfig_evalFunc import *

GET_PLAYER_INDEX = 1  # Replace with the actual index
GET_BOARD_INDEX = 0


class AlphaBetaSearch:
	def __init__(self, game):
		self.moveLib = MoveLib()
		self.eval = EvalFunction(ScoreConfig.Version1(), Player.Blue)
		self.game = game
		self.player = self.game[GET_PLAYER_INDEX]
		self.gameOver = False  # or some other initial state
		self.bitboards = self.game[GET_BOARD_INDEX]  # Set this to the initial bitboards
		self.eval = EvalFunction(ScoreConfig.Version1(),
								 self.player)  # Set this to an instance of your evaluation function
		self.best_move = None

	def search(self):

		init_board(*self.bitboards)
		result = self.alphaBetaMax(-1000000, 1000000, 4, self.bitboards)
		self.best_move = [self.moveLib.BitsToPosition(self.best_move[0]),
						  self.moveLib.BitsToPosition(self.best_move[1])]
		return self.best_move

	def alphaBetaMax(self, alpha, beta, depthleft, bitboard_copy):
		self.player = Player.Blue
		if depthleft == 0:
			etc = generate_moves(self.player)
			if len(etc) != 0:
				points = self.eval.computeOverallScore(etc, board=bitboard_copy)[0][3]
			else:
				points = -10000

			return points
		moves = generate_moves(self.player)
		if len(moves) == 0:
			scorelist = []
		else:
			scorelist = self.eval.computeOverallScore(moves, board=bitboard_copy)

		for i in range(len(scorelist)):
			move = scorelist.pop()
			bitboard_copy = [board.red_p, board.red_k, board.blue_p, board.blue_k]
			execute_move(self.player, move)
			score = self.alphaBetaMin(alpha, beta, depthleft - 1, bitboard_copy)
			print(score)
			self.player = Player.Blue
			takeback(self.player, move)
			if score >= beta:
				return beta

			if score > alpha:
				self.best_move = move
				alpha = score

		return alpha

	def alphaBetaMin(self, alpha, beta, depthleft, bitboard_copy):
		self.player = Player.Red
		if depthleft == 0:
			# print("rating",self.rating(generate_moves(self.player), bitboard_copy))
			etc = generate_moves(self.player)
			points = -self.eval.computeOverallScore(etc, board=bitboard_copy)[0][3]
			print("points", points)
			return points
		moves = generate_moves(self.player)
		if len(moves) == 0:
			scorelist = []
		else:
			scorelist = self.eval.computeOverallScore(moves,board=bitboard_copy)

		for i in range(len(scorelist)):
			move = scorelist.pop()
			bitboard_copy = [board.red_p, board.red_k, board.blue_p, board.blue_k]
			execute_move(self.player, move)
			score = self.alphaBetaMax(alpha, beta, depthleft - 1, bitboard_copy)
			print(score)
			self.player = Player.Red
			takeback(self.player, move)
			if score <= alpha:
				return alpha
			if score < beta:
				self.best_move = move
				beta = score

		return beta

	def rating(moves, board):
		return eval.computeOverallScore(moves, board=board)


def generate_moves(player) -> list:
	# rufe alpha_beta_max mit alpha.generation auf, wenn wir Blau sind
	# und ruf alpha_beta_min mit beta.generation
	# rufe alpha_beta_max mit beta.generation auf, wenn wir rot sind
	# und ruf alpha_beta_min mit alpha.generation

	if player == Player.Blue:
		return board.blue_generation()
	elif player == Player.Red:
		return board.red_generation()
	else:
		raise ValueError("Player must be either b or r")


def execute_move(player, move):
	if player == Player.Blue:
		board.blue_move_execution(move[0], move[1])
	elif player == Player.Red:
		board.red_move_execution(move[0], move[1])


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
	test7 = "6/8/8/8/2r0b04/1b06/8/6 b"
	fen, player = test7.split(" ")
	player = Player.Blue if player == "b" else Player.Red
	bitboard = GameState.createBitBoardFrom(Gui.fenToMatrix(fen), True)
	gameArray = [bitboard, player, True, False]
	search(gameArray)
