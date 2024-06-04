import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.gamestate import *
from src.gui import *
from src.benchmark import *
from src.moveGenerator import MoveGenerator
from src.moveLib import *
from src.model import *
from src.scoreConfig_evalFunc import *
from src.evalFunction import *
import time

GET_PLAYER_INDEX = 1
GET_BOARD_INDEX = 0

class TimeExceeded(Exception):
    pass
class AlphaBetaSearch:
	def __init__(self, game, time_limit=30):
		self.moveLib = MoveLib()
		self.game = game
		self.player = self.game[GET_PLAYER_INDEX]
		self.opponent = Player.Red if self.player == Player.Blue else Player.Blue
		self.eval = EvalFunction(ScoreConfig.Version1(self.player))
		self.gameover =   [DictMoveEntry.CONTINUE_GAME]
		self.total_gameover = False
		self.bitboards = self.game[GET_BOARD_INDEX]  # Set this to the initial bitboards
		self.moveGen = MoveGenerator(self.bitboards)
		self.best_move = None
		self.time_limit = time_limit 
		self.start_time = time.time()
		self.bestMoves = []
		self.alpha = -float('inf')
		self.beta = float('inf')
	
	def search(self, iterative_deepening=True):
		
		try:
			if iterative_deepening:
				
				depth = 2
				while True:
					print("Iterative Deepening", depth)
					result, temp_move = self.alphaBetaMax(self.alpha, self.beta, depth, self.bitboards)
					if temp_move is not None:
						self.best_move = temp_move
					self.moveGen.checkBoardIfGameOver(self.gameover,bitboard)
					if self.total_gameover or time.time() - self.start_time > self.time_limit:
						break
					depth += 2
			else:
				alpha = -float('inf')
				beta = float('inf')
				result, temp_move = self.alphaBetaMax(alpha, beta, 4, self.bitboards)
				if temp_move is not None:
					self.best_move = temp_move
		except TimeExceeded:
			pass
		return self.best_move


	def alphaBetaMax(self, alpha, beta, depthleft, bitboard_copy):
		bitboard = bitboard_copy.copy()
		moves = self.moveGen.genMoves(self.player, self.gameover, bitboard)
		self.moveGen.checkBoardIfGameOver(self.gameover,bitboard)
		if self.gameover[0] != DictMoveEntry.CONTINUE_GAME or  depthleft == 0 or len(moves) == 0:
			if self.gameover[0] != DictMoveEntry.CONTINUE_GAME:
				self.total_gameover = True
			points = self.eval.computeOverallScore(moves, bitboard)[0][3]
			return points, None
			
		scorelist = self.eval.computeOverallScore(moves, bitboard, False)
		best_move = None
		for move in scorelist:
			if time.time() - self.start_time > self.time_limit:
				raise TimeExceeded()
			
			newBoard = self.moveGen.execSingleMove(move, self.player, self.gameover,bitboard,False)
			score, _ = self.alphaBetaMin(alpha, beta, depthleft - 1, newBoard)

			if score >= beta:
				return beta, best_move
			
			if score > alpha:
				best_move = scorelist[0]
				alpha = score
		return alpha, best_move


	def alphaBetaMin(self, alpha, beta, depthleft, bitboard_copy):
		bitboard = bitboard_copy.copy()
		moves = self.moveGen.genMoves(self.opponent, self.gameover, bitboard)
		self.moveGen.checkBoardIfGameOver(self.gameover,bitboard)
		if self.gameover[0] != DictMoveEntry.CONTINUE_GAME or  depthleft == 0 or len(moves) == 0:
			if self.gameover[0] != DictMoveEntry.CONTINUE_GAME:
				self.total_gameover = True

			points = self.eval.computeOverallScore(moves, bitboard)[0][3]
			return points, None
		scorelist = self.eval.computeOverallScore(moves, bitboard, False)
		best_move = None
		for move in scorelist:
			if time.time() - self.start_time > self.time_limit:
				raise TimeExceeded()
			
			newBoard = self.moveGen.execSingleMove(move, self.opponent, self.gameover,bitboard, False)
			score, _ = self.alphaBetaMax(alpha, beta, depthleft - 1, newBoard)

			if score <= alpha:
				
				return alpha, best_move
			if score < beta:
				best_move = scorelist[0] 
				beta = score
		return beta, best_move
	
	def test(self, state):
		self.player = state[1]
		bitboard = state[0]
		moves = self.moveGen.genMoves(self.player, self.gameover, bitboard)
		points = self.eval.computeOverallScore(moves, bitboard)[0][3]
		Benchmark.benchmark(lambda: self.eval.computeOverallScore(moves, bitboard), 'computeOverallScore', '1b01b01b0/1b06/3b04/8/4b0r02/2b03r01/3r0r03/r03r01 b')

def search(state):
	m = MoveLib()
	search_instance = AlphaBetaSearch(state)
	result = search_instance.search()
	if result is not None:
					result = [m.BitsToPosition(result[0]),
							m.BitsToPosition(result[1])]
    
	print(result, "result")
	return result
	
	


if __name__ == '__main__':
	test7 = "3b0b01/8/1b0b01b0b02/2r01b01b01/8/2rr2r02/1r06/2r03 r"
	fen, player = test7.split(" ")
	player = Player.Blue if player == "b" else Player.Red
	bitboard = GameState.createBitBoardFrom(Gui.fenToMatrix(fen), True)
	gameArray = [bitboard, player, True, False]
	search(gameArray)
