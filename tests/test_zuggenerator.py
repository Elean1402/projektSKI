import unittest
import json
from src.scoreConfig_evalFunc import ScoreConfig
from src.evalFunction import EvalFunction

from src.gui import Gui
from src.gamestate import GameState
from src.model import *
from src.moveLib import*
from src.moveGenerator import MoveGenerator

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
        FEN_b_pawns_hit = ["6/2r0b0r03/3r0r03/8/8/8/8/6 b", "6/2r0b0r03/2r0r04/8/8/8/8/6 b",
                           "6/2r0b0r03/3r0rr3/8/8/8/8/6 b", "6/2r0b0r03/2rrr04/8/8/8/8/6 b",
                           "6/2r0b0r03/2brr04/8/8/8/8/6 b", "6/2r0b0r03/3r0br3/8/8/8/8/6 b"]
        poss_b_pawns_hit = ["D2-E3", "D2-C3", "D2-E3", "D2-C3", "D2-C3", "D2-E3"]
            
        # Open the JSON file and load the test data


        # Iterate over each test case in the data
        for i in range(len(FEN_b_pawns_hit)):
            testcase = FEN_b_pawns_hit[i]
            poss = poss_b_pawns_hit[i]
            board, player = testcase.split(" ")
            # Initialize the game state with the board from the test case
            testcase = GameState.createBitBoardFromFEN(board)
            print(testcase)
            gameOver = [DictMoveEntry.CONTINUE_GAME]
            if player == "b":
                player = Player.Blue
            else:
                player = Player.Red
            moveGen = MoveGenerator(testcase)
            #moveGen.updateBoard(GameState.createBitBoardFromFEN(testcase["board"]),player, gameOver)


            # Generate moves for the current player

            list = moveGen.genMoves(player, gameOver)

            # Split the expected and generated moves into lists and sort them
            moves_poss = sorted(poss.split(", "))
            moves_gen = sorted([MoveLib.move(x,y,3) for x,y,z in list])
            print(moves_gen)
            print(moves_poss)

            # Assert that the generated moves and possible moves are the same
            self.assertEqual(moves_gen, moves_poss, f"Failed for testcase: {testcase}")


if __name__ == '__main__':
    unittest.main()
