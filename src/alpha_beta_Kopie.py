import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.scoreConfig_evalFunc import ScoreConfig
from src.alt_eval import EvalFunction
from src.model import *
from board_final import Board

import hashlib

class TranspositionTable:
    def __init__(self):
        self.table = {}

    def hash_bitboards(self, bitboards):
        # Simple hashing function using hashlib
        return hashlib.md5(str(bitboards).encode('utf-8')).hexdigest()

    def store(self, bitboards, depth, score, flag, best_move):
        key = self.hash_bitboards(bitboards)
        self.table[key] = {'depth': depth, 'score': score, 'flag': flag, 'best_move': best_move}

    def lookup(self, bitboards, depth, alpha, beta):
        key = self.hash_bitboards(bitboards)
        if key in self.table:
            entry = self.table[key]
            if entry['depth'] >= depth:
                if entry['flag'] == 'EXACT':
                    return entry['score'], entry['best_move']
                elif entry['flag'] == 'LOWERBOUND' and entry['score'] >= beta:
                    return entry['score'], entry['best_move']
                elif entry['flag'] == 'UPPERBOUND' and entry['score'] <= alpha:
                    return entry['score'], entry['best_move']
        return None, None


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
        self.transposition_table = TranspositionTable()

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
        return self.best_move

    def alpha_beta_max(self, alpha, beta, depth_left, bitboards):
        if depth_left == 0:
            return self.eval_func_opponent.computeEvaluationScore(bitboards), None

        stored_score, stored_move = self.transposition_table.lookup(bitboards, depth_left, alpha, beta)
        if stored_score is not None:
            return stored_score, stored_move

        moves = self.move_gen.generate_moves()
        best_score = -float('inf')
        best_move = None

        for piece in moves:
            for dest in piece[1]:
                self.total_move_count += 1
                if time.time() - self.start_time > self.time_limit:
                    raise TimeExceeded()
                bitboards = self.move_gen.exec_move(piece[0], dest)
                score, _ = self.alpha_beta_min(alpha, beta, depth_left - 1, bitboards)
                self.move_gen.takeback()
                if score > best_score:
                    best_score = score
                    best_move = [piece[0], dest]
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break

        flag = 'EXACT'
        if best_score <= alpha:
            flag = 'UPPERBOUND'
        elif best_score >= beta:
            flag = 'LOWERBOUND'

        self.transposition_table.store(bitboards, depth_left, best_score, flag, best_move)
        return best_score, best_move

    def alpha_beta_min(self, alpha, beta, depth_left, bitboards):
        if depth_left == 0:
            return self.eval_func_opponent.computeEvaluationScore(bitboards), None

        stored_score, stored_move = self.transposition_table.lookup(bitboards, depth_left, alpha, beta)
        if stored_score is not None:
            return stored_score, stored_move

        moves = self.move_gen.generate_moves()
        best_score = float('inf')
        best_move = None

        for piece in moves:
            for dest in piece[1]:
                self.total_move_count += 1
                if time.time() - self.start_time > self.time_limit:
                    raise TimeExceeded()
                bitboards = self.move_gen.exec_move(piece[0], dest)
                score, _ = self.alpha_beta_max(alpha, beta, depth_left - 1, bitboards)
                self.move_gen.takeback()
                if score < best_score:
                    best_score = score
                    best_move = [piece[0], dest]
                beta = min(beta, best_score)
                if beta <= alpha:
                    break

        flag = 'EXACT'
        if best_score <= alpha:
            flag = 'UPPERBOUND'
        elif best_score >= beta:
            flag = 'LOWERBOUND'

        self.transposition_table.store(bitboards, depth_left, best_score, flag, best_move)
        return best_score, best_move
