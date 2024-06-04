import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.gamestate import *
from src.gui import *
from src.moveGenerator import MoveGenerator
from src.moveLib import *
from src.model import *
from src.scoreConfig_evalFunc import *
from src.evalFunction import *
import time

GET_PLAYER_INDEX = 1
GET_BOARD_INDEX = 0


class AlphaBetaSearch:
	def __init__(self, game, time_limit=5):
		self.moveLib = MoveLib()
		self.game = game
		self.player = self.game[GET_PLAYER_INDEX]
		self.opponent = Player.Red if self.player == Player.Blue else Player.Blue
		self.eval = EvalFunction(ScoreConfig.Version1(self.player))
		self.gameover =   [DictMoveEntry.CONTINUE_GAME]
		self.totalGameOver = [DictMoveEntry.CONTINUE_GAME]
		self.bitboards = self.game[GET_BOARD_INDEX]  # Set this to the initial bitboards
		self.moveGen = MoveGenerator(self.bitboards)
		self.best_move = None
		self.time_limit = time_limit 
		self.bestMoves = []
		self.alpha = -float('inf')
		self.beta = float('inf')
	
	def search(self, iterative_deepening=True):
		start_time = time.time()
		
		if iterative_deepening:
			depth = 1
			while True:
				result, temp_move = self.alphaBetaMax(self.alpha, self.beta, depth, self.bitboards, start_time)
				if temp_move is not None:
					self.best_move = [self.moveLib.BitsToPosition(temp_move[0]),
										self.moveLib.BitsToPosition(temp_move[1])]
					print("Best Move: ", self.best_move)
				self.moveGen.checkBoardIfGameOver(self.gameover,bitboard)
				if self.gameover[0] != DictMoveEntry.CONTINUE_GAME or time.time() - start_time > self.time_limit:
					break
				depth += 1
		else:
			start_time = time.time()
			alpha = -float('inf')
			beta = float('inf')
			print(self.bitboards)
			result, temp_move = self.alphaBetaMax(alpha, beta, 4, self.bitboards, start_time)
			print("Result: ", result)
			if temp_move is not None:
				self.best_move = [self.moveLib.BitsToPosition(temp_move[0]),
									self.moveLib.BitsToPosition(temp_move[1])]
		return self.best_move


	def alphaBetaMax(self, alpha, beta, depthleft, bitboard_copy, start_time):
		self.player = Player.Blue
			
		bitboard = bitboard_copy.copy()
		moves = self.moveGen.genMoves(self.player, self.gameover, bitboard)
		self.moveGen.checkBoardIfGameOver(self.gameover,bitboard)
		if self.gameover[0] != DictMoveEntry.CONTINUE_GAME or  depthleft == 0 or len(moves) == 0:
			points = self.eval.computeOverallScore(moves, bitboard)[0][3]
			return points, None
			
		scorelist = self.eval.computeOverallScore(moves, bitboard, False)
		best_move = None
		for move in scorelist:
			temp_move = move
			if time.time() - start_time > self.time_limit:
				return None, None
			
			newBoard = self.moveGen.execSingleMove(move, self.player, self.gameover,bitboard,False)
			score, _ = self.alphaBetaMin(alpha, beta, depthleft - 1, newBoard, start_time)
			self.player = Player.Blue
			if score >= beta:
				return beta, best_move
			
			if score > alpha:
				best_move = scorelist[0]
				alpha = score
		return alpha, best_move


	def alphaBetaMin(self, alpha, beta, depthleft, bitboard_copy, start_time):
		self.player = Player.Red
		bitboard = bitboard_copy.copy()
		moves = self.moveGen.genMoves(self.opponent, self.gameover, bitboard)
		self.moveGen.checkBoardIfGameOver(self.gameover,bitboard)
		if self.gameover[0] != DictMoveEntry.CONTINUE_GAME or  depthleft == 0 or len(moves) == 0:
			points = self.eval.computeOverallScore(moves, bitboard)[0][3]
			return points, None
		scorelist = self.eval.computeOverallScore(moves, bitboard, False)
		best_move = None
		for move in scorelist:
			temp_move = move
			if time.time() - start_time > self.time_limit:
				return None, None
			
			newBoard = self.moveGen.execSingleMove(move, self.player, self.gameover,bitboard, False)
			score, _ = self.alphaBetaMax(alpha, beta, depthleft - 1, newBoard, start_time)
			
			self.player = Player.Red
			
			if score <= alpha:
				
				return alpha, best_move
			if score < beta:
				best_move = scorelist[0]  # Update the local variable
				beta = score
		return beta, best_move

def search(state):
	search_instance = AlphaBetaSearch(state)
	result = search_instance.search()
	print("result", result)
	return result


if __name__ == '__main__':
	test7 = "6/8/8/8/1r0b0r04/2r05/8/6 b"
	fen, player = test7.split(" ")
	player = Player.Blue if player == "b" else Player.Red
	bitboard = GameState.createBitBoardFrom(Gui.fenToMatrix(fen), True)
	gameArray = [bitboard, player, True, False]
	search(gameArray)
