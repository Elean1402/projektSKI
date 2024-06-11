import os
import sys
import time

import benchmark

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.gui import *
from src.benchmark import *
from src.scoreConfig_evalFunc import *
from src.evalFunction import *

GET_PLAYER_INDEX = 1
GET_BOARD_INDEX = 0


class TimeExceeded(Exception):
    pass


class AlphaBetaSearch:
    def __init__(self, game):
        self.transposition_table = {}
        self.move_count2 = 0
        self.move_count = 0
        self.moveLib = MoveLib()
        self.game = game
        self.player = self.game[GET_PLAYER_INDEX]
        self.opponent = Player.Red if self.player == Player.Blue else Player.Blue
        self.eval = EvalFunction(ScoreConfig.Version2(self.player, self.player))
        self.evalo = EvalFunction(ScoreConfig.Version2(self.player, self.opponent))
        self.gameover = [DictMoveEntry.CONTINUE_GAME]
        self.total_gameover = False
        self.bitboards = self.game[GET_BOARD_INDEX]
        self.moveGen = MoveGenerator(self.bitboards)
        self.best_move = None
        self.time_limit = 100000
        self.start_time = time.time()
        self.bestMoves = []
        self.alpha = -float('inf')
        self.beta = float('inf')

    def search(self, iterative_deepening=False, time_limit=100, depth=2):
        self.move_count = 0
        self.start_time = time.time()
        self.time_limit = time_limit
        try:
            if iterative_deepening:
                depth = 1
                while True:
                    print("Iterative Deepening", depth)
                    result, temp_move = self.alphaBetaMax(self.alpha, self.beta, depth, self.bitboards)
                    if temp_move is not None:
                        self.best_move = temp_move
                    self.moveGen.checkBoardIfGameOver(self.gameover, self.bitboards)
                    if self.total_gameover or time.time() - self.start_time > self.time_limit:
                        break
                    depth += 2
            else:
                self.alpha = -float('inf')
                self.beta = float('inf')
                depth = depth
                result, temp_move = self.alphaBetaMax(self.alpha, self.beta, depth, self.bitboards)
                if temp_move is not None:
                    self.best_move = temp_move
        except TimeExceeded:
            pass
        print(f"Total scoresmoves looked at: {self.move_count}")
        print(f"Total moves looked at: {self.move_count2}")
        return self.best_move

    def alphaBetaMax(self, alpha, beta, depthleft, bitboard_copy):
        board_hash = hash(bitboard_copy.tobytes())
        if board_hash in self.transposition_table:
            return self.transposition_table[board_hash], None

        gameover_status = self.gameover[0] != DictMoveEntry.CONTINUE_GAME
        self.moveGen.checkBoardIfGameOver(self.gameover, bitboard_copy)
        if gameover_status:
            self.total_gameover = True
        if gameover_status or depthleft == 0:
            return self.evalo.computeOverallScore([], bitboard_copy)[0][3], None

        moves = self.moveGen.genMoves(self.player, self.gameover, bitboard_copy)
        if len(moves) == 0:
            points = self.eval.computeOverallScore(moves, bitboard_copy)[0][3]
            return points, None
        best_score = -float('inf')
        best_move = None
        for move in moves:
            self.move_count += 1
            if time.time() - self.start_time > self.time_limit:
                raise TimeExceeded()
            newBoard = self.moveGen.execSingleMove(move, self.player, self.gameover, bitboard_copy, False)
            score, unused_move = self.alphaBetaMin(alpha, beta, depthleft - 1, newBoard)
            if score >= beta:
                return score, move
            if score > alpha:
                alpha = score
                best_move = move
        self.transposition_table[hash(bitboard_copy.tobytes())] = alpha
        return alpha, best_move

    def alphaBetaMin(self, alpha, beta, depthleft, bitboard_copy):
        board_hash = hash(bitboard_copy.tobytes())
        if board_hash in self.transposition_table:
            return self.transposition_table[board_hash], None

        gameover_status = self.gameover[0] != DictMoveEntry.CONTINUE_GAME
        self.moveGen.checkBoardIfGameOver(self.gameover, bitboard_copy)
        if gameover_status:
            self.total_gameover = True
        if gameover_status or depthleft == 0:
            return self.evalo.computeOverallScore([], bitboard_copy)[0][3], None

        moves = self.moveGen.genMoves(self.opponent, self.gameover, bitboard_copy)
        if len(moves) == 0:
            points = self.evalo.computeOverallScore(moves, bitboard_copy)[0][3]
            return points, None
        best_score = float('inf')
        best_move = None
        for move in moves:
            self.move_count += 1
            if time.time() - self.start_time > self.time_limit:
                raise TimeExceeded()
            newBoard = self.moveGen.execSingleMove(move, self.opponent, self.gameover, bitboard_copy, False)
            score, unused_move = self.alphaBetaMax(alpha, beta, depthleft - 1, newBoard)
            if score <= alpha:
                return score, move
            if score < beta:
                beta = score
                best_move = move
        self.transposition_table[hash(bitboard_copy.tobytes())] = beta
        return beta, best_move

    def play(self, iterative_deepening=False):
        self.time_limit = 1000000000
        moves = []
        for i in range(100):
            bitboard = self.bitboards.copy()
            self.moveGen.checkBoardIfGameOver(self.gameover, self.bitboards, True)
            if self.gameover[0] != DictMoveEntry.CONTINUE_GAME:
                break
            next_move = self.search(iterative_deepening)
            out = [MoveLib.BitsToPosition(next_move[0]), MoveLib.BitsToPosition(next_move[1])]
            moves.append(out)
            self.bitboards = self.moveGen.execSingleMove(next_move, self.player, self.gameover, bitboard, False)
            self.player, self.opponent = self.opponent, self.player
        return bitboard, moves


def call(input_dict):
    fen, player = input_dict["board"].split(" ")
    player = Player.Blue if player == "b" else Player.Red
    bitboard = GameState.createBitBoardFrom(Gui.fenToMatrix(fen), True)
    state = [bitboard, player, True, False]
    search_instance = AlphaBetaSearch(state)
    depth = 2
    next_move = search_instance.search(iterative_deepening=True, time_limit=2, depth=depth)
    out = [MoveLib.BitsToPosition(next_move[0]), MoveLib.BitsToPosition(next_move[1])]
    print(out)
    # print(search_instance.play(iterative_deepening=True))
    # Benchmark.profile(lambda: search_instance.search(iterative_deepening=True, time_limit=2, depth=depth), 'alphaBetaMax')
    # Benchmark.profile(lambda: moveGen.genMoves(player, [DictMoveEntry.CONTINUE_GAME], bitboard), 'genMoves')
    # Benchmark.benchmark(lambda: moveGen.genMoves(player, [DictMoveEntry.CONTINUE_GAME], bitboard), 'genMoves', repetitions=10000)


if __name__ == '__main__':
    input_dict = {"board": "2b01b01/2bb5/3b02b01/3r0brb0r01/1b06/8/2r0rr4/2r01r0r0 r"}
    call(input_dict)
