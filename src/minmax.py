import os
import sys
import time

import benchmark

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.gui import *
from src.benchmark import *
from src.scoreConfig_evalFunc import *
from src.evalFunction import *


class TimeExceeded(Exception):
    pass


class AlphaBetaSearch:
    def __init__(self, game):
        self.transposition_table = {}
        self.move_count2 = 0
        self.move_count = 0
        self.moveLib = MoveLib()
        self.game = game
        self.player = self.game["player"]
        self.opponent = Player.Red if self.player == Player.Blue else Player.Blue
        self.eval = EvalFunction(ScoreConfig.Version2(self.player, self.player))
        self.evalo = EvalFunction(ScoreConfig.Version2(self.player, self.opponent))
        self.gameover = [DictMoveEntry.CONTINUE_GAME]
        self.total_gameover = False
        self.bitboards = self.game["bitboards"]
        self.moveGen = MoveGenerator(self.bitboards)
        self.best_move = None
        self.time_limit = 100000
        self.start_time = time.time()
        self.bestMoves = []
        self.alpha = -float('inf')
        self.beta = float('inf')

    def search(self, iterative_deepening=False, time_limit=100, minimax=False, depth=2):
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
                    depth += 1
            else:
                self.alpha = -float('inf')
                self.beta = float('inf')
                depth = depth
                if minimax:
                    result, temp_move = self.minimaxMax(depth, self.bitboards)
                else:
                    result, temp_move = self.alphaBetaMax(self.alpha, self.beta, depth, self.bitboards)
                if temp_move is not None:
                    self.best_move = temp_move
        except TimeExceeded:
            pass
        print(f"Total scoresmoves looked at: {self.move_count}")
        print(f"Total moves looked at: {self.move_count2}")
        return self.best_move

    def alphaBetaMax(self, alpha, beta, depthleft, bitboards):
        self.moveGen.checkBoardIfGameOver(self.gameover, bitboards)
        gameover_status = self.gameover[0] != DictMoveEntry.CONTINUE_GAME

        if gameover_status:
            self.total_gameover = True
        if gameover_status or depthleft == 0:
            return self.evalo.computeOverallScore([], bitboards)[0][3], None

        bitboards_bytes = bitboards.tobytes()
        if bitboards_bytes in self.transposition_table and self.transposition_table[bitboards_bytes][1] >= depthleft:
            return self.transposition_table[bitboards_bytes][0], None

        moves = self.moveGen.genMoves(self.player, self.gameover, bitboards)
        self.move_count += len(moves)
        if len(moves) == 0:
            points = self.eval.computeOverallScore(moves, bitboards)[0][3]
            return points, None

        best_score = -float('inf')
        best_move = None
        for move in moves:
            self.move_count2 += 1
            if time.time() - self.start_time > self.time_limit:
                raise TimeExceeded()
            newBoard = self.moveGen.execSingleMove(move, self.player, self.gameover, bitboards, False)
            score, _ = self.alphaBetaMin(alpha, beta, depthleft - 1, newBoard)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break

        self.transposition_table[bitboards_bytes] = (best_score, depthleft)

        return best_score, best_move

    def alphaBetaMin(self, alpha, beta, depthleft, bitboards):
        self.moveGen.checkBoardIfGameOver(self.gameover, bitboards)
        gameover_status = self.gameover[0] != DictMoveEntry.CONTINUE_GAME
        if gameover_status:
            self.total_gameover = True
        if gameover_status or depthleft == 0:
            return self.evalo.computeOverallScore([], bitboards)[0][3], None

        bitboards_bytes = bitboards.tobytes()
        if bitboards_bytes in self.transposition_table and self.transposition_table[bitboards_bytes][1] >= depthleft:
            return self.transposition_table[bitboards_bytes][0], None

        moves = self.moveGen.genMoves(self.opponent, self.gameover, bitboards)
        self.move_count += len(moves)
        if len(moves) == 0:
            points = self.evalo.computeOverallScore(moves, bitboards)[0][3]
            return points, None

        best_score = float('inf')
        best_move = None
        for move in moves:
            self.move_count2 += 1
            if time.time() - self.start_time > self.time_limit:
                raise TimeExceeded()
            newBoard = self.moveGen.execSingleMove(move, self.opponent, self.gameover, bitboards, False)
            score, _ = self.alphaBetaMax(alpha, beta, depthleft - 1, newBoard)
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, best_score)
            if beta <= alpha:
                break

        self.transposition_table[bitboards_bytes] = (best_score, depthleft)

        return best_score, best_move

    def heuristic(self, bitboards):
        # Count the number of pieces each player has
        red_pawns = np.count_nonzero(bitboards[0])
        red_knights = np.count_nonzero(bitboards[1])
        blue_pawns = np.count_nonzero(bitboards[2])
        blue_knights = np.count_nonzero(bitboards[3])

        # The heuristic value is the difference in the number of pieces
        # Here we assume that knights are more valuable than pawns, so we weight them higher
        red_score = red_pawns + 2 * red_knights
        blue_score = blue_pawns + 2 * blue_knights

        # If the current player is red, we want a high score to be good, so we return red_score - blue_score
        # If the current player is blue, we want a low score to be good, so we return blue_score - red_score
        return red_score - blue_score if self.player == Player.Red else blue_score - red_score

    def minimaxMax(self, depthleft, bitboards):
        bitboard = bitboards.copy()
        moves = self.moveGen.genMoves(self.player, self.gameover, bitboard)
        self.moveGen.checkBoardIfGameOver(self.gameover, bitboard)
        if self.gameover[0] != DictMoveEntry.CONTINUE_GAME or depthleft == 0 or len(moves) == 0:
            if self.gameover[0] != DictMoveEntry.CONTINUE_GAME:
                self.total_gameover = True
            points = self.eval.computeOverallScore(moves, bitboard)[0][3]
            return points, None
        scorelist = self.evalo.computeOverallScore(moves, bitboard, False)
        best_score = -float('inf')
        best_move = None
        for move in scorelist:
            self.move_count += 1
            if time.time() - self.start_time > self.time_limit:
                raise TimeExceeded()
            newBoard = self.moveGen.execSingleMove(move, self.player, self.gameover, bitboard, False)
            score, _ = self.minimaxMin(depthleft - 1, newBoard)
            if score > best_score:
                best_move = scorelist[0]
                best_score = score
        return best_score, best_move

    def minimaxMin(self, depthleft, bitboards):
        bitboard = bitboards.copy()
        moves = self.moveGen.genMoves(self.opponent, self.gameover, bitboard)
        self.moveGen.checkBoardIfGameOver(self.gameover, bitboard)
        if self.gameover[0] != DictMoveEntry.CONTINUE_GAME or depthleft == 0 or len(moves) == 0:
            if self.gameover[0] != DictMoveEntry.CONTINUE_GAME:
                self.total_gameover = True
            points = self.evalo.computeOverallScore(moves, bitboard)[0][3]
            return points, None
        scorelist = self.evalo.computeOverallScore(moves, bitboard, False)
        best_score = float('inf')
        best_move = None
        for move in scorelist:
            self.move_count += 1
            if time.time() - self.start_time > self.time_limit:
                raise TimeExceeded()
            newBoard = self.moveGen.execSingleMove(move, self.opponent, self.gameover, bitboard, False)
            score, _ = self.minimaxMax(depthleft - 1, newBoard)
            if score < best_score:
                best_move = scorelist[0]
                best_score = score
        return score, best_move

    def play(self, iterative_deepening=False):
        self.time_limit = 1000000000
        moves = []
        for i in range(100):
            bitboard = self.bitboards.copy()
            self.moveGen.checkBoardIfGameOver(self.gameover, self.bitboards, True)
            if self.gameover[0] != DictMoveEntry.CONTINUE_GAME:
                break
            next_move = self.search(iterative_deepening, depth=5)
            out = [MoveLib.BitsToPosition(next_move[0]), MoveLib.BitsToPosition(next_move[1])]
            moves.append(out)
            self.bitboards = self.moveGen.execSingleMove(next_move, self.player, self.gameover, bitboard, False)
            self.player, self.opponent = self.opponent, self.player
        return bitboard, moves


def call(state):
    moveGen = MoveGenerator(state["bitboards"])
    search_instance = AlphaBetaSearch(state)
    depth = 6
    # next_move = search_instance.search(iterative_deepening=False, time_limit=20, minimax=False, depth=depth)
    # out = [MoveLib.BitsToPosition(next_move[0]), MoveLib.BitsToPosition(next_move[1])]
    # print(out)
    #
    Benchmark.profile(lambda: search_instance.search(iterative_deepening=False, time_limit=20, minimax=False, depth=depth), 'alphaBetaMax')
    # Benchmark.profile(lambda: moveGen.genMoves(player, [DictMoveEntry.CONTINUE_GAME], bitboard), 'genMoves')
    # Benchmark.benchmark(lambda: moveGen.genMoves(player, [DictMoveEntry.CONTINUE_GAME], bitboard), 'genMoves', repetitions=10000)


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
    call(state)
