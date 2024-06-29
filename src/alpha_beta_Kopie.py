import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.scoreConfig_evalFunc import ScoreConfig
from src.alt_eval import EvalFunction
from src.model import *
from board_final import Board

import random

class ZobristHashing:
    def __init__(self, num_positions=64, num_piece_types=4):
        # Initialize the Zobrist table with random numbers
        self.zobrist_table = [
            [random.getrandbits(64) for _ in range(num_piece_types)]
            for _ in range(num_positions)
        ]
        self.zobrist_side = random.getrandbits(64)

    def hash_position(self, bitboards):
        red_pawns, red_knights, blue_pawns, blue_knights = bitboards
        h = 0
        
        # Ensure bitboards are integers
        red_pawns = int(red_pawns)
        red_knights = int(red_knights)
        blue_pawns = int(blue_pawns)
        blue_knights = int(blue_knights)
        
        # For red pawns
        for pos in range(64):
            if (red_pawns >> pos) & 1:
                h ^= self.zobrist_table[pos][0]  # Index 0 for red pawns
        
        # For red knights
        for pos in range(64):
            if (red_knights >> pos) & 1:
                h ^= self.zobrist_table[pos][1]  # Index 1 for red knights
        
        # For blue pawns
        for pos in range(64):
            if (blue_pawns >> pos) & 1:
                h ^= self.zobrist_table[pos][2]  # Index 2 for blue pawns
        
        # For blue knights
        for pos in range(64):
            if (blue_knights >> pos) & 1:
                h ^= self.zobrist_table[pos][3]  # Index 3 for blue knights
        
        return h

class TranspositionTable:
    def __init__(self):
        self.table = {}

    def store(self, zobrist_key, depth, score, flag, best_move):
        self.table[zobrist_key] = {'depth': depth, 'score': score, 'flag': flag, 'best_move': best_move}

    def lookup(self, zobrist_key, depth, alpha, beta):
        if zobrist_key in self.table:
            entry = self.table[zobrist_key]
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
        self.zobrist = ZobristHashing(num_positions=64, num_piece_types=4)

    def search(self, iterative_deepening=False, time_limit=100, depth=2):
        self.transposition_table = TranspositionTable()  # Reset transposition table
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
                    if self.is_time_exceeded():
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
            points = self.eval_func_opponent.computeEvaluationScore(bitboards)
            return points, None

        zobrist_key = self.zobrist.hash_position(bitboards)
        stored_score, stored_move = self.transposition_table.lookup(zobrist_key, depth_left, alpha, beta)
        if stored_score is not None:
            return stored_score, stored_move

        moves = self.move_gen.generate_moves()
        best_score = -float('inf')
        best_move = None

        for piece in moves:
            for dest in piece[1]:
                self.total_move_count += 1
                if self.is_time_exceeded():
                    raise TimeExceeded()
                new_bitboards = self.move_gen.exec_move(piece[0], dest)
                score, _ = self.alpha_beta_min(alpha, beta, depth_left - 1, new_bitboards)
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

        self.transposition_table.store(zobrist_key, depth_left, best_score, flag, best_move)
        return best_score, best_move

    def alpha_beta_min(self, alpha, beta, depth_left, bitboards):
        if depth_left == 0:
            points = self.eval_func_opponent.computeEvaluationScore(bitboards)
            return points, None

        zobrist_key = self.zobrist.hash_position(bitboards)
        stored_score, stored_move = self.transposition_table.lookup(zobrist_key, depth_left, alpha, beta)
        if stored_score is not None:
            return stored_score, stored_move

        moves = self.move_gen.generate_moves()
        best_score = float('inf')
        best_move = None

        for piece in moves:
            for dest in piece[1]:
                self.total_move_count += 1
                if self.is_time_exceeded():
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

        flag = 'EXACT'
        if best_score <= alpha:
            flag = 'UPPERBOUND'
        elif best_score >= beta:
            flag = 'LOWERBOUND'

        self.transposition_table.store(zobrist_key, depth_left, best_score, flag, best_move)
        return best_score, best_move

    def is_time_exceeded(self):
        return time.time() - self.start_time > self.time_limit
