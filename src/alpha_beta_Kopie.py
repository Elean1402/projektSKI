import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.scoreConfig_evalFunc import ScoreConfig
from src.alt_eval import EvalFunction
from src.model import *
from src.moveGenerator_sicher import MoveGenerator as mvg
from src.moveLib import MoveLib

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

    def store(self, zobrist_key, depth, score, flag, best_move, age):
        self.table[zobrist_key] = {'depth': depth, 'score': score, 'flag': flag, 'best_move': best_move, 'age': age}

    def lookup(self, zobrist_key, depth, alpha, beta):
        if zobrist_key in self.table:
            entry = self.table[zobrist_key]
            if entry['depth'] >= depth:
                if entry['flag'] == 'EXACT':
                    return entry['score'], entry['best_move'], entry['age']
                elif entry['flag'] == 'LOWERBOUND' and entry['score'] >= beta:
                    return entry['score'], entry['best_move'], entry['age']
                elif entry['flag'] == 'UPPERBOUND' and entry['score'] <= alpha:
                    return entry['score'], entry['best_move'], entry['age']
        return None, None, None


class TimeExceeded(Exception):
    pass

class AlphaBetaSearch:
    def __init__(self, game):
        self.total_move_count = 0
        self.total_time = game["time"]
        self.game = game
        self.player = game["player"]
        self.opponent = Player.Red if self.player == Player.Blue else Player.Blue
        self.turn = True if self.player == Player.Blue else False
        self.eval_func = EvalFunction(ScoreConfig.Version2(self.player, self.player))
        self.eval_func_opponent = EvalFunction(ScoreConfig.Version2(self.player, self.opponent))
        self.bitboards = game["bitboards"]
        self.move_gen = mvg(useTakeback=True)
        #self.move_gen.initBoard(*self.bitboards, self.turn)
        self.best_move = None
        self.time_limit = 100  # Default time limit in seconds
        self.zobrist = ZobristHashing(num_positions=64, num_piece_types=4)

    def random_move(self, opening=False):
        #moves = self.move_gen.generate_moves()
        moves = self.move_gen.genMoves()
        piece = random.choice(moves)
        #move = piece[1][0]
        move = piece
        #self.best_move = piece[0], move
        self.best_move = move
        
    def count_pieces(self, fen_string):
        count_b = 0
        count_r = 0
        
        for char in fen_string:
            if char == 'b':
                count_b += 1
            elif char == 'r':
                count_r += 1
        
        if self.player == Player.Blue:
            return count_b, count_r       
        return count_r, count_b
    
    def set_time(self,board):
        if self.move_gen.isOpening(board):
            self.random_move(opening=True)
            raise TimeExceeded()
        elif self.total_time < 100:
            self.random_move(opening=False)
            raise TimeExceeded()
        pieces, pieces_opponent = self.count_pieces
        if pieces > 9 and pieces_opponent > 9:
            return self.total_time / 100
        if pieces > 9 and pieces_opponent <= 4:
            return self.total_time / 40
        if pieces <= 4 and pieces_opponent > 9:
            return self.total_time / 20
        if pieces <= 4 and pieces_opponent <= 4:
            return self.total_time / 20

    def search(self, iterative_deepening=False, time_limit=100, depth=2):
        
        self.transposition_table = TranspositionTable()  # Reset transposition table
        self.total_move_count = 0
        self.start_time = time.time()*1000
        try:
            if iterative_deepening:
                self.time_limit = self.set_time()
                depth = 1
                while True:
                    print(f"Iterative Deepening: {depth}")
                    result, temp_move = self.alpha_beta_max(-float('inf'), float('inf'), depth, self.bitboards, depth)
                    if temp_move is not None:
                        self.best_move = temp_move
                    if self.is_time_exceeded():
                        break
                    depth += 2
            else:
                result, temp_move = self.alpha_beta_max(-float('inf'), float('inf'), depth, self.bitboards, depth)
                if temp_move is not None:
                    self.best_move = temp_move
        except TimeExceeded:
            pass
        
        print(f"Total moves looked at: {self.total_move_count}")
        if self.best_move is not None:
            #print(self.best_move)
            move_string = f"{MoveLib.BitsToPosition(self.best_move[0][0])}-{MoveLib.BitsToPosition(self.best_move[0][1])}"
            print(move_string)
        else:
            move_string = None
            print("No valid move found.")
        print(f"total time: {self.total_time}")
        current_time = time.time()*1000
        time_taken = current_time - self.start_time
        print(f"Time remaining: {self.total_time - time_taken} milliseconds")
        return move_string, self.total_move_count

    def alpha_beta_max(self, alpha, beta, depth_left, bitboards, age):
        if depth_left == 0:
            points = self.eval_func_opponent.computeEvaluationScore(bitboards)
            return points, None

        zobrist_key = self.zobrist.hash_position(bitboards)
        stored_score, stored_move, stored_age = self.transposition_table.lookup(zobrist_key, depth_left, alpha, beta)
        if stored_score is not None:
            return stored_score, stored_move

        moves = self.move_gen.genMoves(self.player,bitboards, [DictMoveEntry.CONTINUE_GAME])
        #Züge sind nach score abssteigend sortiert
        moves = self.eval_func.sortMoveList(self.player,moves,self.move_gen,bitboards)
        best_score = -float('inf')
        best_move = None

        for piece in moves:
            #for dest in piece[1]:
            self.total_move_count += 1
            if self.is_time_exceeded():
                raise TimeExceeded()
            #new_bitboards = self.move_gen.exec_move(piece[0], dest)
            new_bitboards = self.move_gen.execSingleMove(piece,self.player,bitboards,[DictMoveEntry.CONTINUE_GAME])
            score, _ = self.alpha_beta_min(alpha, beta, depth_left - 1, new_bitboards, age)
            self.move_gen.takeback(bitboards)
            if score > best_score:
                best_score = score
                best_move = [piece]
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        
        flag = 'EXACT'
        if best_score <= alpha:
            flag = 'UPPERBOUND'
        elif best_score >= beta:
            flag = 'LOWERBOUND'

        self.transposition_table.store(zobrist_key, depth_left, best_score, flag, best_move, age)
        return best_score, best_move

    def alpha_beta_min(self, alpha, beta, depth_left, bitboards, age):
        if depth_left == 0:
            points = self.eval_func_opponent.computeEvaluationScore(bitboards)
            return points, None

        zobrist_key = self.zobrist.hash_position(bitboards)
        stored_score, stored_move, stored_age = self.transposition_table.lookup(zobrist_key, depth_left, alpha, beta)
        if stored_score is not None:
            return stored_score, stored_move

        moves = self.move_gen.genMoves(self.opponent,bitboards,[DictMoveEntry.CONTINUE_GAME])
        moves = self.eval_func_opponent.sortMoveList(self.opponent,moves,self.move_gen,bitboards)
        best_score = float('inf')
        best_move = None

        for piece in moves:
            #for dest in piece[1]:
            self.total_move_count += 1
            if self.is_time_exceeded():
                raise TimeExceeded()
            #new_bitboards = self.move_gen.exec_move(piece[0], dest)
            new_bitboards = self.move_gen.execSingleMove(piece,self.opponent,bitboards,[DictMoveEntry.CONTINUE_GAME])
            score, _ = self.alpha_beta_max(alpha, beta, depth_left - 1, new_bitboards, age)
            self.move_gen.takeback(bitboards)
            if score < best_score:
                best_score = score
                best_move = [piece]
            beta = min(beta, best_score)
            if beta <= alpha:
                break

        flag = 'EXACT'
        if best_score <= alpha:
            flag = 'UPPERBOUND'
        elif best_score >= beta:
            flag = 'LOWERBOUND'

        self.transposition_table.store(zobrist_key, depth_left, best_score, flag, best_move, age)
        return best_score, best_move

    def is_time_exceeded(self):
        return time.time() - self.start_time > self.time_limit
