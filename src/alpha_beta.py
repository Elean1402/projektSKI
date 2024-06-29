import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.gui import Gui

from src.scoreConfig_evalFunc import ScoreConfig
from src.alt_eval import EvalFunction
# from src.moveGenerator import MoveGenerator
from src.moveLib import MoveLib
from src.gamestate import GameState
from src.model import *
from board_final import Board



class TimeExceeded(Exception):
    pass

class AlphaBetaSearch:
    def __init__(self, game):
        self.total_move_count = 0
        self.game = game
        self.player = game["player"]
        self.opponent = Player.Red if self.player == Player.Blue else Player.Blue
        self.turn = True if self.player == Player.Blue else False
        self.eval_func = EvalFunction(ScoreConfig.Version2(self.player, self.player))
        self.eval_func_opponent = EvalFunction(ScoreConfig.Version2(self.player, self.opponent))
        self.bitboards = game["bitboards"]
        self.move_gen = Board()
        self.move_gen.initBoard(*self.bitboards, self.turn)
        self.best_move = None
        self.time_limit = 100  # Default time limit in seconds
        self.start_time = time.time()
        self.alpha = -float('inf')
        self.beta = float('inf')

    def search(self, iterative_deepening=False, time_limit=100, depth=2):
        """Search for the best move using Alpha-Beta pruning with optional iterative deepening."""
        self.total_move_count = 0
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
                    depth += 2
            else:
                result, temp_move = self.alpha_beta_max(self.alpha, self.beta, depth, self.bitboards)
                if temp_move is not None:
                    self.best_move = temp_move
        except TimeExceeded:
            pass
        
        print(f"Total moves looked at: {self.total_move_count}")
        return self.best_move, self.total_move_count

    def alpha_beta_max(self, alpha, beta, depth_left, bitboards):
        if depth_left == 0:
            return self.eval_func_opponent.computeEvaluationScore(bitboards), None

        moves = self.move_gen.generate_moves()
        best_score = -float('inf')
        best_move = None

        for piece in moves:
            for dest in piece[1]:
                self.total_move_count += 1
                if time.time() - self.start_time > self.time_limit:
                    raise TimeExceeded()
                new_bitboards = self.move_gen.exec_move(piece[0], dest)
                score, _ = self.alpha_beta_min(alpha, beta, depth_left - 1, new_bitboards)
                #undo move
                self.move_gen.takeback()
                if score > best_score:
                    best_score = score
                    best_move = [piece[0], dest]
                alpha = max(alpha, best_score)
                if alpha >= beta:
                   break

        return best_score, best_move

    def alpha_beta_min(self, alpha, beta, depth_left, bitboards):
        if depth_left == 0:
            return self.eval_func_opponent.computeEvaluationScore(bitboards), None

        moves = self.move_gen.generate_moves()
                
        
        best_score = float('inf')
        best_move = None

        for piece in moves:
            for dest in piece[1]:
                self.total_move_count += 1
                if time.time() - self.start_time > self.time_limit:
                    raise TimeExceeded()
                new_bitboards = self.move_gen.exec_move(piece[0], dest)
                score, _ = self.alpha_beta_max(alpha, beta, depth_left - 1, new_bitboards)
                self.move_gen.takeback()
                if score < best_score:
                    best_score = score
                    best_move = [piece[0], dest]
                beta = min(beta, best_score)
                if beta <= alpha:
                   break

        return best_score, best_move

   