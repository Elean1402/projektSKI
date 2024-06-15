import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.gui import Gui
from src.benchmark import Benchmark
from src.scoreConfig_evalFunc import ScoreConfig
from src.alt_eval import EvalFunction  # Importing the simplified EvalFunction
from src.moveGenerator import *
from src.moveLib import MoveLib
from src.gamestate import GameState


class TimeExceeded(Exception):
    pass


class AlphaBetaSearch:
    def __init__(self, game):
        self.transposition_table = {}
        self.move_count2 = 0
        self.move_count = 0
        self.game = game
        self.player = game["player"]
        self.opponent = Player.Red if self.player == Player.Blue else Player.Blue
        self.eval_func = EvalFunction(ScoreConfig.Version2(self.player, self.player))
        self.eval_func_opponent = EvalFunction(ScoreConfig.Version2(self.player, self.opponent))
        self.gameover = [DictMoveEntry.CONTINUE_GAME]
        self.total_gameover = False
        self.bitboards = game["bitboards"]
        self.move_gen = MoveGenerator(self.bitboards)
        self.best_move = None
        self.time_limit = 100  # Default time limit in seconds
        self.start_time = time.time()
        self.alpha = -float('inf')
        self.beta = float('inf')

    def search(self, iterative_deepening=False, time_limit=100, depth=2):
        self.start_time = time.time()
        self.time_limit = time_limit
        try:
            if iterative_deepening:
                depth = 1
                while True:
                    print(f"Iterative Deepening: {depth}")
                    result, temp_move = self.alpha_beta_max(self.alpha, self.beta, depth, self.bitboards)
                    if temp_move is not None:
                        self.best_move = temp_move
                    self.move_gen.checkBoardIfGameOver(self.gameover, self.bitboards)
                    if self.total_gameover or time.time() - self.start_time > self.time_limit:
                        break
                    depth += 1
            else:
                self.alpha = -float('inf')
                self.beta = float('inf')
                result, temp_move = self.alpha_beta_max(self.alpha, self.beta, depth, self.bitboards)
                if temp_move is not None:
                    self.best_move = temp_move
        except TimeExceeded:
            pass
        print(f"Total scoresmoves looked at: {self.move_count}")
        print(f"Total moves looked at: {self.move_count2}")
        return self.best_move

    def alpha_beta_max(self, alpha, beta, depth_left, bitboards):
        self.move_gen.checkBoardIfGameOver(self.gameover, bitboards)
        game_over_status = self.gameover[0] != DictMoveEntry.CONTINUE_GAME

        if game_over_status:
            self.total_gameover = True
        if game_over_status or depth_left == 0:
            points = self.eval_func_opponent.computeEvaluationScore(bitboards)
            return points, None

        bitboards_bytes = bitboards.tobytes()
        if bitboards_bytes in self.transposition_table and self.transposition_table[bitboards_bytes][1] >= depth_left:
            return self.transposition_table[bitboards_bytes][0], None

        moves = self.move_gen.genMoves(self.player, self.gameover, bitboards)
        self.move_count += len(moves)
        if not moves:
            points = self.eval_func.computeEvaluationScore(bitboards)
            return points, None

        best_score = -float('inf')
        best_move = None
        for move in moves:
            self.move_count2 += 1
            if time.time() - self.start_time > self.time_limit:
                raise TimeExceeded()
            new_board = self.move_gen.execSingleMove(move, self.player, self.gameover, bitboards, False)
            score, _ = self.alpha_beta_min(alpha, beta, depth_left - 1, new_board)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            # if alpha >= beta:
            #     break

        self.transposition_table[bitboards_bytes] = (best_score, depth_left)
        return best_score, best_move

    def alpha_beta_min(self, alpha, beta, depth_left, bitboards):
        self.move_gen.checkBoardIfGameOver(self.gameover, bitboards)
        game_over_status = self.gameover[0] != DictMoveEntry.CONTINUE_GAME

        if game_over_status:
            self.total_gameover = True
        if game_over_status or depth_left == 0:
            points = self.eval_func_opponent.computeEvaluationScore(bitboards)
            return points, None

        bitboards_bytes = bitboards.tobytes()
        if bitboards_bytes in self.transposition_table and self.transposition_table[bitboards_bytes][1] >= depth_left:
            return self.transposition_table[bitboards_bytes][0], None

        moves = self.move_gen.genMoves(self.opponent, self.gameover, bitboards)
        self.move_count += len(moves)
        if not moves:
            points = self.eval_func.computeEvaluationScore(bitboards)
            return points, None

        best_score = float('inf')
        best_move = None
        for move in moves:
            self.move_count2 += 1
            if time.time() - self.start_time > self.time_limit:
                raise TimeExceeded()
            new_board = self.move_gen.execSingleMove(move, self.opponent, self.gameover, bitboards, False)
            score, _ = self.alpha_beta_max(alpha, beta, depth_left - 1, new_board)
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, best_score)
            # if beta <= alpha:
            #     break

        self.transposition_table[bitboards_bytes] = (best_score, depth_left)
        return best_score, best_move
