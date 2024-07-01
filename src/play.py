import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.moveGenerator import MoveGenerator1
from src.moveLib import MoveLib
from src.gui import Gui
from src.alpha_beta import AlphaBetaSearch as AlphaBetaSearch1
from src.alpha_beta_Kopie import AlphaBetaSearch
from src.benchmark import *
from src.gamestate import GameState
from src.model import Player, DictMoveEntry
from src.board_final import Board

def call(state, output=False):

    search_instance = AlphaBetaSearch(state)
    # search_instance1 = AlphaBetaSearch1(state)

    depth = 5
    benchmark(lambda: search_instance.search(iterative_deepening=False, time_limit=5, depth=depth), 'alpha_beta',fen=state['board'], repetitions=1, depth=depth, move_output=True, include_move_count=True)
    

def board_test(state, output=False):
    # game_over = [DictMoveEntry.CONTINUE_GAME]
    move_generator = Board()
    move_generator.initBoard(red_pawns=state["red_pawns"], red_knights=state["red_knights"], blue_pawns=state["blue_pawns"], blue_knights=state["blue_knights"], blue_turn=False)
    # move_generator1 = MoveGenerator1(state["bitboards"])
    # benchmark(lambda: move_generator.generate_moves(), 'genMoves', repetitions=1000, fen=state["board"], include_output=False)
    # benchmark(lambda: move_generator1.genMoves(state["player"],game_over,state["bitboards"]), 'genMoves1', repetitions=1000, fen=state["board"], include_output=False)

    if output:
        test = move_generator.generate_moves()
        for i in test:
            for j in i[1]:
                print(f'{MoveLib.BitsToPosition(i[0])} -> {MoveLib.BitsToPosition(j)}')


if __name__ == '__main__':
    input_dict = {"board": "2b03/1b0b05/6b01/3b02r01/1b01r02r01/2b05/2r03r01/3r02 b"}
    fen, player = input_dict["board"].split(" ")
    player = Player.Blue if player == "b" else Player.Red
    bitboard = GameState.createBitBoardFrom(Gui.fenToMatrix(fen), True)
    red_pawns, red_knights, blue_pawns, blue_knights = bitboard[0], bitboard[1], bitboard[2], bitboard[3]
    state = {
        "board": input_dict["board"],
        "red_pawns": red_pawns,
        "red_knights": red_knights,
        "blue_pawns": blue_pawns,
        "blue_knights": blue_knights,
        "bitboards": bitboard,
        "player": player,
        "player1": True,
        "player2": False,
        "time": 120_000,
    }
    call(state, True)  # Change to 'minimax' to use MinimaxSearch
