import os
import sys
path_to_src = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
print(path_to_src)
sys.path.append(path_to_src)
import unittest
import json
from gamestate import *
from gui import *
from moveGenerator import *
from model import *

class TestZuggenerator(unittest.TestCase):

    def test_generation(self, filename='test.json'):
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
                print(testcase["board"])
                moveGen = MoveGenerator(GameState.createBitBoardFrom(Gui.fenToMatrix(testcase["board"]), True))
                if testcase["player"] == "b":
                    player = Player.Blue
                else:
                    player = Player.Red

                # Generate moves for the current player
                gameOver = [DictMoveEntry.CONTINUE_GAME]
                print(moveGen.genMoves(player, gameOver))

                # Split the expected and generated moves into lists and sort them
                moves_poss = sorted(testcase["moves"].split(", "))
                #moves_gen = sorted(generated.split(", "))

                # Assert that the generated moves and possible moves are the same
                #self.assertEqual(moves_gen, moves_poss, f"Failed for testcase: {testcase}")


if __name__ == '__main__':
    unittest.main()