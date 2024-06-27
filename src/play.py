from moveLib import MoveLib
from src.gui import Gui
from alpha_beta import AlphaBetaSearch

from src.benchmark import Benchmark
from src.moveGenerator import MoveGenerator
from src.gamestate import GameState
from src.model import Player, DictMoveEntry

def call(state, search_type='minmax'):
    if search_type == 'alpha_beta':
        search_instance = AlphaBetaSearch(state)


    depth = 6


    # Initialize the MoveGenerator with the game state's bitboards
    move_generator = MoveGenerator(state["bitboards"])

    # Define the player and game over status
    game_over = [DictMoveEntry.CONTINUE_GAME]
    # Benchmark the genMoves method
    # Benchmark.benchmark(lambda: move_generator.genMoves(state["player"], game_over, state["bitboards"]), 'genMoves')
    # Benchmark.profile(lambda: [move_generator.genMoves(state["player"], game_over, state["bitboards"]) for _ in range(1000)], 'genMoves')
    # Benchmark.benchmark(lambda: move_generator.genMoves(state["player"], gameOver=game_over, board=state["bitboards"]), 'genMoves', func_name='genMoves', repetitions=1000,extra_depth=20,profile=True)
    Benchmark.profile(lambda:search_instance.search(iterative_deepening=False, time_limit=200, depth=depth), 'alpha_beta', mode='text')
    next_move = search_instance.search(iterative_deepening=False, time_limit=200, depth=depth)
    if next_move is not None:
        out = [MoveLib.BitsToPosition(next_move[0]), MoveLib.BitsToPosition(next_move[1])]
        print(out)
    else:
        print("No valid move found.")


if __name__ == '__main__':
    input_dict = {"board": "b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 r"}
    fen, player = input_dict["board"].split(" ")
    player = Player.Blue if player == "b" else Player.Red
    bitboard = GameState.createBitBoardFrom(Gui.fenToMatrix(fen), True)
    state = {
        "bitboards": bitboard,
        "player": player,
        "player1": True,
        "player2": False,
    }
    call(state, search_type='alpha_beta')  # Change to 'minimax' to use MinimaxSearch
