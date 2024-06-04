import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest

from src.gamestate import *
from src.gui import *


class MyTestCase(unittest.TestCase):
	def test_something(self):
		FEN_board = "6/2r0b0r03/3r0r03/8/8/8/8/6"
		
		#init_board(board.blue_p, board.blue_k, board.red_p, board.red_k)
		  # add assertion here


if __name__ == '__main__':
	unittest.main()
