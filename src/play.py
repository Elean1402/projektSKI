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

def play(FEN_board=False):
	input_dict = {"board": "2b03/1b0b05/6b01/3b02r01/1b01r02r01/2b05/2r03r01/3r02 b"}
	m = MoveLib()
	fen, player = input_dict["board"].split(" ")
	player = Player.Blue if player == "b" else Player.Red
	bitboard = GameState.createBitBoardFrom(Gui.fenToMatrix(fen), True)
	state = [bitboard, player, True, False]
	search_instance = AlphaBetaSearch(state)

	game = []
	print_state("Startpos")
	input()
	while isOver() == "c":
		if alpha_turn:
			source, dest = alpha_random_move_execution(alpha_generation())
		else:
			source, dest = beta_random_move_execution(beta_generation())
		game.append(MoveLib.move(source,dest,mode=3))
		if alpha_turn:
			print_state("Alpha")
		else:
			print_state("Beta")
		alpha_turn = not alpha_turn
		input()
	print(isOver())