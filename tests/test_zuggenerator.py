import unittest
from src.moveGenerator import MoveGenerator
from src.gamestate import GameState
from src.model import *

class TestMoveGenerator(unittest.TestCase):
    def setUp(self):
        self.board = [0]*4  # Initialize with your board setup
        self.move_generator = MoveGenerator(self.board)

    def test_generated_moves(self):
        player = Player.Red  # Change to the player you want to test
        game_over = [DictMoveEntry.CONTINUE]
        generated_moves = self.move_generator.genMoves(player, game_over, self.board)

        # Convert generated moves to strings
        generated_moves_str = [str(move) for move in generated_moves]

        # The expected_moves list should be filled with the expected string representations of the moves
        expected_moves = []  # Fill this with your expected moves

        self.assertCountEqual(generated_moves_str, expected_moves)

if __name__ == '__main__':
    unittest.main()