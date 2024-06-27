import os
import sys
from collections import Counter
import numpy as np
from functools import lru_cache

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.gamestate import GameState
from src.model import *
from src.moveLib import MoveLib
from src.moveGenerator import MoveGenerator1 as MoveGenerator

# Precomputed table of bit counts for 16-bit numbers
BIT_COUNTS = [bin(i).count('1') for i in range(2**16)]

def count_bits(mask):
    return BIT_COUNTS[mask & 0xFFFF] + BIT_COUNTS[(mask >> 16) & 0xFFFF] + BIT_COUNTS[(mask >> 32) & 0xFFFF] + BIT_COUNTS[(mask >> 48) & 0xFFFF]

class EvalFunction:
    _CONFIG_DICT = {
        Config.TURN_OPTIONS: -1,
        Config.MAT_PAWN: -1,
        Config.MAT_KNIGHT: -1,
        Config.TOTAL_SCORE_RATING_PAWN_BLUE: {},
        Config.TOTAL_SCORE_RATING_KNIGHT_BLUE: {},
        Config.TOTAL_SCORE_RATING_PAWN_RED: {},
        Config.TOTAL_SCORE_RATING_KNIGHT_RED: {},
        Config.MaxPlayer: Player.NoOne,
        Config.Player: Player.NoOne,
        Config.CONFIGVERSION: None
    }

    def __init__(self, config: dict):
        if len(self._CONFIG_DICT) != len(config):
            raise ValueError("Configs do not have the same size")
        self._CONFIG_DICT.update(config)
        vals = self._CONFIG_DICT.values()
        self._score_cache = {}
        if any(x == -1 for x in vals):
            raise ValueError("Config is not complete, missing key-value pair")
        if any(len(self._CONFIG_DICT[key]) == 0 for key in [
            Config.TOTAL_SCORE_RATING_PAWN_BLUE, Config.TOTAL_SCORE_RATING_KNIGHT_BLUE,
            Config.TOTAL_SCORE_RATING_PAWN_RED, Config.TOTAL_SCORE_RATING_KNIGHT_RED]):
            raise ValueError("Config: PIECESQUARE_TABLE_{Pawn,Knight} Dictionary not set")
        if self._CONFIG_DICT[Config.Player] == Player.NoOne:
            raise ValueError("Player not set")
        if self._CONFIG_DICT[Config.MaxPlayer] == Player.NoOne:
            raise ValueError("MaxPlayer not set")
        if self._CONFIG_DICT[Config.CONFIGVERSION] is None:
            raise ValueError("CONFIGVERSION NOT SET")

    def _computeActualPositionalPoints(self, board: np.ndarray):
        def compute_points(piece_index, score_dict):
            positions = MoveGenerator.getBitPositions(board[piece_index])
            return np.sum(score_dict[MoveLib.BitsToPosition(bits)] for bits in positions)

        max_player = self._CONFIG_DICT[Config.MaxPlayer]
        if max_player == Player.Red:
            max_indices = (GameState._ZARR_INDEX_R_PAWNS, GameState._ZARR_INDEX_R_KNIGHTS)
            min_indices = (GameState._ZARR_INDEX_B_PAWNS, GameState._ZARR_INDEX_B_KNIGHTS)
            max_score_dicts = (self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_PAWN_RED],
                               self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_KNIGHT_RED])
            min_score_dicts = (self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_PAWN_BLUE],
                               self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_KNIGHT_BLUE])
        else:
            max_indices = (GameState._ZARR_INDEX_B_PAWNS, GameState._ZARR_INDEX_B_KNIGHTS)
            min_indices = (GameState._ZARR_INDEX_R_PAWNS, GameState._ZARR_INDEX_R_KNIGHTS)
            max_score_dicts = (self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_PAWN_BLUE],
                               self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_KNIGHT_BLUE])
            min_score_dicts = (self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_PAWN_RED],
                               self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_KNIGHT_RED])

        position_points_max = 0
        for index, score_dict in zip(max_indices, max_score_dicts):
            position_points_max += compute_points(index, score_dict)

        position_points_min = 0
        for index, score_dict in zip(min_indices, min_score_dicts):
            position_points_min += compute_points(index, score_dict)

        return position_points_max - position_points_min

    @lru_cache(maxsize=None)
    def _materialPoints(self, board):
        bp = count_bits(board[GameState._ZARR_INDEX_B_PAWNS] & ~board[GameState._ZARR_INDEX_R_KNIGHTS]) * self._CONFIG_DICT[Config.MAT_PAWN]
        bk = count_bits(board[GameState._ZARR_INDEX_B_KNIGHTS]) * self._CONFIG_DICT[Config.MAT_KNIGHT]
        rp = count_bits(board[GameState._ZARR_INDEX_R_PAWNS] & ~board[GameState._ZARR_INDEX_B_KNIGHTS]) * self._CONFIG_DICT[Config.MAT_PAWN]
        rk = count_bits(board[GameState._ZARR_INDEX_R_KNIGHTS]) * self._CONFIG_DICT[Config.MAT_KNIGHT]
        return rp + rk - bp - bk if self._CONFIG_DICT[Config.MaxPlayer] == Player.Red else bp + bk - rp - rk

    def computeEvaluationScore(self, board: np.ndarray) -> int:
        board_tuple = tuple(board.tolist())  # Convert numpy array to tuple
        if board_tuple in self._score_cache:
            return self._score_cache[board_tuple]

        totalScore = self._materialPoints(board_tuple)  # Pass tuple to _materialPoints
        totalScore += self._computeActualPositionalPoints(board)

        self._score_cache[board_tuple] = totalScore
        return totalScore