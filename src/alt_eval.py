import os
import sys
import numpy as np
from collections import Counter

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.gamestate import GameState
from src.model import *
from src.moveLib import MoveLib
from src.moveGenerator_sicher import MoveGenerator
from collections import deque
from src.board_final import *
#from functools import lru_cache
# Precomputed table of bit counts for 16-bit numbers
BIT_COUNTS = [bin(i).count('1') for i in range(2**16)]

# def count_bits(mask):
#     if not isinstance(mask, int):
#         mask = int(mask)  # Ensure the mask is an integer
#     return BIT_COUNTS[mask & 0xFFFF] + BIT_COUNTS[(mask >> 16) & 0xFFFF] + BIT_COUNTS[(mask >> 32) & 0xFFFF] + BIT_COUNTS[(mask >> 48) & 0xFFFF]


    
    



class EvalFunction_Alt:
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

    def _computeActualPositionalPoints(self, bitboards):
        def compute_points(piece_index, score_dict):
            positions = MoveGenerator.getBitPositions(bitboards[piece_index])
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

    def _materialPoints(self, bitboards):
        bp = count_bits(bitboards[GameState._ZARR_INDEX_B_PAWNS] & ~bitboards[GameState._ZARR_INDEX_R_KNIGHTS]) * self._CONFIG_DICT[Config.MAT_PAWN]
        bk = count_bits(bitboards[GameState._ZARR_INDEX_B_KNIGHTS]) * self._CONFIG_DICT[Config.MAT_KNIGHT]
        rp = count_bits(bitboards[GameState._ZARR_INDEX_R_PAWNS] & ~bitboards[GameState._ZARR_INDEX_B_KNIGHTS]) * self._CONFIG_DICT[Config.MAT_PAWN]
        rk = count_bits(bitboards[GameState._ZARR_INDEX_R_KNIGHTS]) * self._CONFIG_DICT[Config.MAT_KNIGHT]
        return rp + rk - bp - bk if self._CONFIG_DICT[Config.MaxPlayer] == Player.Red else bp + bk - rp - rk

    def computeEvaluationScore(self, bitboards) -> int:
        totalScore = self._materialPoints(bitboards)
        totalScore += self._computeActualPositionalPoints(bitboards)
        return totalScore
    
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
    
   
    def _computeActualPositionalPoints(self, bitboards):
        def compute_points(piece_index, score_dict):
            positions = MoveGenerator.getBitPositions(bitboards[piece_index])
            #return np.sum(score_dict[MoveLib.BitsToPosition(bits)] for bits in positions)
            return np.add.reduce([score_dict[MoveLib.BitsToPosition(bits)] for bits in positions])

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
    def count_bits(self,number: np.uint64)-> int:
        return len(list(MoveGenerator.getBitPositions(number)))
        
    def _materialPoints(self, bitboards):
        bp = self.count_bits(bitboards[GameState._ZARR_INDEX_B_PAWNS] & ~bitboards[GameState._ZARR_INDEX_R_KNIGHTS]) * self._CONFIG_DICT[Config.MAT_PAWN]
        bk = self.count_bits(bitboards[GameState._ZARR_INDEX_B_KNIGHTS]) * self._CONFIG_DICT[Config.MAT_KNIGHT]
        rp = self.count_bits(bitboards[GameState._ZARR_INDEX_R_PAWNS] & ~bitboards[GameState._ZARR_INDEX_B_KNIGHTS]) * self._CONFIG_DICT[Config.MAT_PAWN]
        rk = self.count_bits(bitboards[GameState._ZARR_INDEX_R_KNIGHTS]) * self._CONFIG_DICT[Config.MAT_KNIGHT]
        return rp + rk - bp - bk if self._CONFIG_DICT[Config.MaxPlayer] == Player.Red else bp + bk - rp - rk
    # def _materialPoints(self, bitboards):
    #     bp = count_bits(bitboards[GameState._ZARR_INDEX_B_PAWNS] & ~bitboards[GameState._ZARR_INDEX_R_KNIGHTS]) * self._CONFIG_DICT[Config.MAT_PAWN]
    #     bk = count_bits(bitboards[GameState._ZARR_INDEX_B_KNIGHTS]) * self._CONFIG_DICT[Config.MAT_KNIGHT]
    #     rp = count_bits(bitboards[GameState._ZARR_INDEX_R_PAWNS] & ~bitboards[GameState._ZARR_INDEX_B_KNIGHTS]) * self._CONFIG_DICT[Config.MAT_PAWN]
    #     rk = count_bits(bitboards[GameState._ZARR_INDEX_R_KNIGHTS]) * self._CONFIG_DICT[Config.MAT_KNIGHT]
    #     return rp + rk - bp - bk if self._CONFIG_DICT[Config.MaxPlayer] == Player.Red else bp + bk - rp - rk

    def computeEvaluationScore(self, bitboards) -> int:
        totalScore = self._materialPoints(bitboards)
        totalScore += self._computeActualPositionalPoints(bitboards)
        return totalScore
    
    def sortMoveList(self,player:Player, moveList, moveGen: MoveGenerator, board: list[np.uint64]) -> list[tuple[int,int,BoardCommand,int]]:
        """Sorts the move list in descending order depending on Score

        Args:
            player (Player): _description_
            moveList (_type_): _description_
            moveGen (MoveGenerator): _description_
            board (list[np.uint64]): _description_

        Raises:
            Exception: movegen only with unmake() (useTakeback) configuration

        Returns:
            list[tuple[int,int,BoardCommand,int]]: [(src,dest, bcs, score)]
        """
        maxheap = MaxHeap()
        #[[maxheap.push(itemTuple[0], dest, self._evalSingleMove(boardObjClass, itemTuple[0],dest)) #for dest in itemTuple[1]] 
        #for itemTuple in moveList]
        #return maxheap
        def _evalSingleMove(move) -> int:
            bitboards = moveGen.execSingleMove(move,player,board,[DictMoveEntry.CONTINUE_GAME])
            score  = self.computeEvaluationScore(bitboards)
            moveGen.takeback(board)
            return score
        if(not moveGen._useTakeback):
            raise Exception("sortMoveList: MoveGenerator not for takeback configured")
        maxheap.push([(move[0],move[1],move[2], _evalSingleMove(move)) for move in moveList])
        
        
        return [maxheap.pop() for x in range(len(maxheap._heap))]
    
    
