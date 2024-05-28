import unittest
from game import *
from board import *
from gamestate import *
from gui import *


class MyTestCase(unittest.TestCase):
	def test_something(self):
		FEN_board = "6/2r0b0r03/3r0r03/8/8/8/8/6"
		init_board(*GameState.createBitBoardFrom(Gui.fenToMatrix(FEN_board), True))
		print_state()
		#init_board(board.blue_p, board.blue_k, board.red_p, board.red_k)
		  # add assertion here


if __name__ == '__main__':
	unittest.main()
