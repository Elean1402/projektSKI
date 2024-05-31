import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
import json
from gamestate import GameState
from gui import Gui


class TestZuggenerator(unittest.TestCase):

    def test_generation(self, filename='test_data.json'):
        """
        Test case for move generation. It reads test data from a JSON file, generates moves for each test case,
        and compares the generated moves with the expected moves.

        Args:
            filename (str): The name of the JSON file containing the test data. Defaults to 'test_data.json'.

        Raises:
            AssertionError: If the generated moves do not match the expected moves for any test case.
        """
        # Calculate the absolute path to the JSON file
        data_path = os.path.join(os.path.dirname(__file__), 'testcases', filename)
            
        # Open the JSON file and load the test data
        with open(data_path) as json_file:
            data = json.load(json_file)

            # Iterate over each test case in the data
            for testcase in data:
                # Initialize the game state with the board from the test case
                init_position(*GameState.createBitBoardFrom(Gui.fenToMatrix(testcase["board"]), True))
                GameState.createBitBoardFrom(Gui.fenToMatrix(testcase["board"]), True)

                # Generate moves for the current player
                generated = moves_to_string(move_generation(testcase["player"]))

                # Split the expected and generated moves into lists and sort them
                moves_poss = sorted(testcase["moves"].split(", "))
                moves_gen = sorted(generated.split(", "))

                # Assert that the generated moves and possible moves are the same
                self.assertEqual(moves_gen, moves_poss, f"Failed for testcase: {testcase}")


if __name__ == '__main__':
    unittest.main()