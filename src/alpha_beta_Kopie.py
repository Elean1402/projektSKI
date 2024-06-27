import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.gui import Gui
from src.benchmark import Benchmark
from src.scoreConfig_evalFunc import ScoreConfig
from src.alt_eval import EvalFunction
# from src.moveGenerator import MoveGenerator
from src.moveLib import MoveLib
from src.gamestate import GameState
from src.model import *
from board_final import MoveGenerator 

class TimeExceeded(Exception):
    pass

class AlphaBetaSearch:
    def __init__(self, game):
        self.transposition_table = {}
        self.move_count = 0
        self.total_move_count = 0
        self.game = game
        self.player = game["player"]
        self.opponent = Player.Red if self.player == Player.Blue else Player.Blue
        self.turn = True if self.player == Player.Blue else False
        self.eval_func = EvalFunction(ScoreConfig.Version2(self.player, self.player))
        self.eval_func_opponent = EvalFunction(ScoreConfig.Version2(self.player, self.opponent))
        self.gameover = [DictMoveEntry.CONTINUE_GAME]
        self.total_gameover = False
        self.bitboards = game["bitboards"]
        self.move_gen = MoveGenerator(*self.bitboards, self.turn)
        self.best_move = None
        self.time_limit = 100  # Default time limit in seconds
        self.start_time = time.time()
        self.alpha = -float('inf')
        self.beta = float('inf')

    def search(self, iterative_deepening=False, time_limit=100, depth=2):
        """Search for the best move using Alpha-Beta pruning with optional iterative deepening."""
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
                    if self.is_time_exceeded() or self.total_gameover:
                        break
                    depth += 1
            else:
                result, temp_move = self.alpha_beta_max(self.alpha, self.beta, depth, self.bitboards)
                if temp_move is not None:
                    self.best_move = temp_move
        except TimeExceeded:
            pass

        print(f"Total scores moves looked at: {self.move_count}")
        print(f"Total moves looked at: {self.total_move_count}")
        return self.best_move

    def alpha_beta_max(self, alpha, beta, depth_left, bitboards):
        if depth_left == 0:
            return self.eval_func_opponent.computeEvaluationScore(bitboards), None

        moves = self.generate_moves(self.player, bitboards)
        best_score = -float('inf')
        best_move = None

        for move in moves:
            for dest in move[1]:
                if self.is_time_exceeded():
                    raise TimeExceeded()
                self.move_gen.exec_move(move[0], dest)
                score, _ = self.alpha_beta_min(alpha, beta, depth_left - 1, bitboards)
                #undo move
                self.move_gen.takeback()
                if score > best_score:
                    best_score = score
                    best_move = [move[0], dest]
                alpha = max(alpha, best_score)
                if alpha >= beta:
                   break

        return best_score, best_move

    def alpha_beta_min(self, alpha, beta, depth_left, bitboards):
        if depth_left == 0:
            return self.eval_func_opponent.computeEvaluationScore(bitboards), None

        moves = self.generate_moves(self.opponent, bitboards)
        best_score = float('inf')
        best_move = None

        for move in moves:
            for dest in move[1]:
                if self.is_time_exceeded():
                    raise TimeExceeded()
                self.move_gen.exec_move(move[0], dest)
                score, _ = self.alpha_beta_max(alpha, beta, depth_left - 1, bitboards)
                self.move_gen.takeback()
                if score < best_score:
                    best_score = score
                    best_move = [move[0], dest]
                beta = min(beta, best_score)
                if beta <= alpha:
                   break

        return best_score, best_move

    def generate_moves(self, player, bitboards):
        """Generate all possible moves for the given player."""
        moves = self.move_gen.generate_moves()
        for move in moves:
            for i in move[1]:
                self.total_move_count += 1
        return moves

    def is_game_over(self, bitboards):
        """Check if the game is over."""
        self.move_gen.checkBoardIfGameOver(self.gameover, bitboards)
        if self.gameover[0] != DictMoveEntry.CONTINUE_GAME:
            self.total_gameover = True
            return True
        return False

    def is_time_exceeded(self):
        """Check if the time limit has been exceeded."""
        return time.time() - self.start_time > self.time_limit
