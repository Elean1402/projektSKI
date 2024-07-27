from collections import Counter
from enum import Enum
import heapq
import numpy as np
import os
import sys
import heapq
import fastenum
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.gamestate import GameState

class ScoredMoveList(list):
    def append(self, item):
        if isinstance(item, list):
            super().extend(item)
        elif isinstance(item, tuple):
            super().append(item)
        else:
            raise TypeError("item is not from type ScoredMoveList: List[(np.uint64, np.uint64,int,int, list)]")

    def sort(self):
        """Sort List in descending order by total score"""
        super().sort(key=lambda x: x[3], reverse=True)
        return self

    def __init__(self, *args):
        """Specific list type for scoring

        Type: List[(np.uint64, np.uint64,int,int,list)]
            ->List[(FromPos, TargetPos,MoveScore, TotalscoreAfterMove,BoardCommands)]
        """
        if (len(args) > 0):
            self.append(args)


class ScoreListForMerging(list):

    def append(self, item):
        """Specific Type for Preprocessing Scores

        Args:
             Type: List( ( np.uint64, dict( { np.uint64: int } ) ) )
            ->List( (startPos, dict( { targetPos: score ... } ) ) )
        """
        if (isinstance(item, list)):
            if (isinstance(item[0], tuple) and
                    isinstance(item[0,0], np.uint64) and
                    isinstance(item[0,1], dict)):
                super().extend(item)


        elif (isinstance(item, tuple) and
              isinstance(item[0], np.uint64) and
              isinstance(item[1], dict)):
            super().append(item)

        else:
            raise TypeError(
                "item is not from type ScoredListForMerge: List( ( np.uint64, dict( { np.uint64: int } ) ) )", "item=",
                item, " type of item=", type(item), " type of item[0]=", type(item[0]), "type of item[1]=",
                type(item[1]), "counter is instance of dict?=>", isinstance(item[1], Counter),
                "type(item[2])=Bordcommand?=>", isinstance(item[2], BoardCommand))

    def __init__(self, *args):
        """Specific List Type for Preprocessing Scores for Eval Func
        Type: List( ( np.uint64, dict( { np.uint64: int } ) ) )
            ->List( (startPos, dict( { targetPos: score } ) ) )
        """
        if (len(args) > 0):
            self.append(args)


# class Config(Enum):
#     MOBILITY = "MOBILITY"
#     TURN_OPTIONS = "TURN_OPTIONS"
#     PROTECTION_PAWNS = "PROTECTION_PAWNS"
#     PROTECTION_KNIGHTS = "PROTECTION_KNIGHTS"
#     UNPROTECTED_PAWNS = "UNPROTECTED_PAWNS"
#     UNPROTECTED_KNIGHTS = "UNPROTECTED_KNIGHTS"
#     UPGRADE_TO_KNIGHT = "UPGRADE_TO_KNIGHT"
#     BLOCKED_FIGURES = "BLOCKED_FIGURES"
#     MAT_PAWN = "MAT_PAWN"
#     MAT_KNIGHT = "MAT_KNIGHT"
#     ENDGAME_MAT_PAWN = "ENDGAME_MAT_PAWN"
#     ENDGAME_MAT_KNIGHT = "ENDGAME_MAT_KNIGHT"
#     PIECESQUARE_TABLE_PAWN_Blue = "PIECESQUARE_TABLE_PAWN_Blue"
#     PIECESQUARE_TABLE_KNIGHT_Blue = "PIECESQUARE_TABLE_KNIGHT_Blue"
#     PIECESQUARE_TABLE_PAWN_Red = "PIECESQUARE_TABLE_PAWN_Red"
#     PIECESQUARE_TABLE_KNIGHT_Red = "PIECESQUARE_TABLE_KNIGHT_Red"
#     TOTAL_SCORE_RATING_PAWN_BLUE = "TOTAL_SCORE_RATING_BLUE"
#     TOTAL_SCORE_RATING_KNIGHT_BLUE = "TOTAL_SCORE_RATING_KNIGHT_BLUE"
#     TOTAL_SCORE_RATING_PAWN_RED = "TOTAL_SCORE_RATING_PAWN_RED"
#     TOTAL_SCORE_RATING_KNIGHT_RED = "TOTAL_SCORE_RATING_KNIGHT_RED"
#     MaxPlayer = "MaxPlayer"
#     Player = "Player"
#     CONFIGVERSION = "CONFIGVERSION"
class Config(fastenum.Enum):
    MOBILITY = "MOBILITY"
    TURN_OPTIONS = "TURN_OPTIONS"
    PROTECTION_PAWNS = "PROTECTION_PAWNS"
    PROTECTION_KNIGHTS = "PROTECTION_KNIGHTS"
    UNPROTECTED_PAWNS = "UNPROTECTED_PAWNS"
    UNPROTECTED_KNIGHTS = "UNPROTECTED_KNIGHTS"
    UPGRADE_TO_KNIGHT = "UPGRADE_TO_KNIGHT"
    BLOCKED_FIGURES = "BLOCKED_FIGURES"
    MAT_PAWN = "MAT_PAWN"
    MAT_KNIGHT = "MAT_KNIGHT"
    ENDGAME_MAT_PAWN = "ENDGAME_MAT_PAWN"
    ENDGAME_MAT_KNIGHT = "ENDGAME_MAT_KNIGHT"
    PIECESQUARE_TABLE_PAWN_Blue = "PIECESQUARE_TABLE_PAWN_Blue"
    PIECESQUARE_TABLE_KNIGHT_Blue = "PIECESQUARE_TABLE_KNIGHT_Blue"
    PIECESQUARE_TABLE_PAWN_Red = "PIECESQUARE_TABLE_PAWN_Red"
    PIECESQUARE_TABLE_KNIGHT_Red = "PIECESQUARE_TABLE_KNIGHT_Red"
    TOTAL_SCORE_RATING_PAWN_BLUE = "TOTAL_SCORE_RATING_BLUE"
    TOTAL_SCORE_RATING_KNIGHT_BLUE = "TOTAL_SCORE_RATING_KNIGHT_BLUE"
    TOTAL_SCORE_RATING_PAWN_RED = "TOTAL_SCORE_RATING_PAWN_RED"
    TOTAL_SCORE_RATING_KNIGHT_RED = "TOTAL_SCORE_RATING_KNIGHT_RED"
    MaxPlayer = "MaxPlayer"
    Player = "Player"
    CONFIGVERSION = "CONFIGVERSION"

# class Player(Enum):
#     """ Blue (Bottom) = Alpha?? (from Zuggenerator)
#         Rot (Top) = Beta?? (from Zuggenerator)
#     """
#     Red = 0
#     Blue = 1
#     NoOne = 3
class Player(fastenum.Enum):
    """ Blue (Bottom) = Alpha?? (from Zuggenerator)
        Rot (Top) = Beta?? (from Zuggenerator)
    """
    Red = 0
    Blue = 1
    NoOne = 3

# class DictMoveEntry(Enum):
#     BLUE_PAWN_TO_TOP = 0
#     RED_PAWN_TO_BOTTOM = 1
#     PAWN_TO_LEFT = 2
#     PAWN_TO_RIGHT = 3

#     BLUE_KNIGHT_TO_TOPLEFT = 4
#     BLUE_KNIGHT_TO_TOPRIGHT = 5
#     BLUE_KNIGHT_LEFT = 6
#     BLUE_KNIGHT_RIGHT = 7

#     RED_KNIGHT_TO_BOTLEFT = 8
#     RED_KNIGHT_TO_BOTRIGHT = 9
#     RED_KNIGHT_LEFT = 10
#     RED_KNIGHT_RIGHT = 11

#     BLUE_PAWN_TO_TOP_RIGHT = 12
#     BLUE_PAWN_TO_TOP_LEFT = 13
#     RED_PAWN_TO_BOTTOM_LEFT = 14
#     RED_PAWN_TO_BOTTOM_RIGHT = 15
#     GAME_OVER_BLUE_WINS = 16
#     GAME_OVER_RED_WINS = 17
#     CONTINUE_GAME = 18
class DictMoveEntry(fastenum.Enum):
    BLUE_PAWN_TO_TOP = 0
    RED_PAWN_TO_BOTTOM = 1
    PAWN_TO_LEFT = 2
    PAWN_TO_RIGHT = 3

    BLUE_KNIGHT_TO_TOPLEFT = 4
    BLUE_KNIGHT_TO_TOPRIGHT = 5
    BLUE_KNIGHT_LEFT = 6
    BLUE_KNIGHT_RIGHT = 7

    RED_KNIGHT_TO_BOTLEFT = 8
    RED_KNIGHT_TO_BOTRIGHT = 9
    RED_KNIGHT_LEFT = 10
    RED_KNIGHT_RIGHT = 11

    BLUE_PAWN_TO_TOP_RIGHT = 12
    BLUE_PAWN_TO_TOP_LEFT = 13
    RED_PAWN_TO_BOTTOM_LEFT = 14
    RED_PAWN_TO_BOTTOM_RIGHT = 15
    GAME_OVER_BLUE_WINS = 16
    GAME_OVER_RED_WINS = 17
    CONTINUE_GAME = 18


BitMaskDict = {
    DictMoveEntry.BLUE_PAWN_TO_TOP: np.uint64(
        0b00000000_01111110_11111111_11111111_11111111_11111111_11111111_01111110),
    DictMoveEntry.BLUE_PAWN_TO_TOP_LEFT: np.uint64(
        0b00000000_00111111_01111111_01111111_01111111_01111111_01111111_01111110),
    DictMoveEntry.BLUE_PAWN_TO_TOP_RIGHT: np.uint64(
        0b00000000_11111100_11111110_11111110_11111110_11111110_11111110_01111110),
    DictMoveEntry.RED_PAWN_TO_BOTTOM: np.uint64(
        0b01111110_11111111_11111111_11111111_11111111_11111111_01111110_00000000),
    DictMoveEntry.RED_PAWN_TO_BOTTOM_LEFT: np.uint64(
        0b01111110_01111111_01111111_01111111_01111111_01111111_00111111_00000000),
    DictMoveEntry.RED_PAWN_TO_BOTTOM_RIGHT: np.uint64(
        0b01111110_11111110_11111110_11111110_11111110_11111110_11111100_00000000),
    DictMoveEntry.PAWN_TO_LEFT: np.uint64(0b00111110_01111111_01111111_01111111_01111111_01111111_01111111_00111110),
    DictMoveEntry.PAWN_TO_RIGHT: np.uint64(0b01111100_11111110_11111110_11111110_11111110_11111110_11111110_01111100),

    DictMoveEntry.BLUE_KNIGHT_TO_TOPLEFT: np.uint64(
        0b00000000_00000000_00111111_01111111_01111111_01111111_01111111_01111110),
    DictMoveEntry.BLUE_KNIGHT_TO_TOPRIGHT: np.uint64(
        0b00000000_00000000_11111100_11111110_11111110_11111110_11111110_01111110),
    DictMoveEntry.BLUE_KNIGHT_LEFT: np.uint64(
        0b00000000_00011111_00111111_00111111_00111111_00111111_00111111_00111110),
    DictMoveEntry.BLUE_KNIGHT_RIGHT: np.uint64(
        0b00000000_11111000_11111100_11111100_11111100_11111100_11111100_01111100),

    DictMoveEntry.RED_KNIGHT_TO_BOTLEFT: np.uint64(
        0b01111110_01111111_01111111_01111111_01111111_00111111_00000000_00000000),
    DictMoveEntry.RED_KNIGHT_TO_BOTRIGHT: np.uint64(
        0b01111110_11111110_11111110_11111110_11111110_11111100_00000000_00000000),
    DictMoveEntry.RED_KNIGHT_LEFT: np.uint64(0b00111111_00111111_00111111_00111111_00111111_00111111_00011111_00000000),
    DictMoveEntry.RED_KNIGHT_RIGHT: np.uint64(
        0b11111100_11111100_11111100_11111100_11111100_11111100_11111000_00000000),
    DictMoveEntry.GAME_OVER_BLUE_WINS: np.uint64(
        0b11111111_00000000_00000000_00000000_00000000_00000000_00000000_00000000),
    DictMoveEntry.GAME_OVER_RED_WINS: np.uint64(
        0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_11111111),
}
BIT_MASK_ARRAY_PAWN_RED = np.array(
    [BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM], BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM_LEFT],
     BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM_RIGHT], BitMaskDict[DictMoveEntry.PAWN_TO_LEFT],
     BitMaskDict[DictMoveEntry.PAWN_TO_RIGHT]])
BIT_MASK_ARRAY_PAWN_BLUE = np.array(
    [BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP], BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_LEFT],
     BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_RIGHT], BitMaskDict[DictMoveEntry.PAWN_TO_LEFT],
     BitMaskDict[DictMoveEntry.PAWN_TO_RIGHT]])
BIT_MASK_ARRAY_KNIGHT_RED = np.array(
    [BitMaskDict[DictMoveEntry.RED_KNIGHT_TO_BOTLEFT], BitMaskDict[DictMoveEntry.RED_KNIGHT_TO_BOTRIGHT],
     BitMaskDict[DictMoveEntry.RED_KNIGHT_LEFT], BitMaskDict[DictMoveEntry.RED_KNIGHT_RIGHT]])
BIT_MASK_ARRAY_KNIGHT_BLUE = np.array(
    [BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPLEFT], BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPRIGHT],
     BitMaskDict[DictMoveEntry.BLUE_KNIGHT_LEFT], BitMaskDict[DictMoveEntry.BLUE_KNIGHT_RIGHT]])

DICT_MOVE = {
    DictMoveEntry.RED_PAWN_TO_BOTTOM: np.uint64(8),
    DictMoveEntry.RED_KNIGHT_LEFT: np.uint64(6),
    DictMoveEntry.RED_KNIGHT_RIGHT: np.uint64(10),
    DictMoveEntry.RED_KNIGHT_TO_BOTLEFT: np.uint64(15),
    DictMoveEntry.RED_KNIGHT_TO_BOTRIGHT: np.uint64(17),

    DictMoveEntry.BLUE_PAWN_TO_TOP: np.uint64(8),
    DictMoveEntry.BLUE_KNIGHT_LEFT: np.uint64(10),
    DictMoveEntry.BLUE_KNIGHT_RIGHT: np.uint64(6),
    DictMoveEntry.BLUE_KNIGHT_TO_TOPLEFT: np.uint64(17),
    DictMoveEntry.BLUE_KNIGHT_TO_TOPRIGHT: np.uint64(15),

    DictMoveEntry.PAWN_TO_LEFT: np.uint64(1),
    DictMoveEntry.PAWN_TO_RIGHT: np.uint64(1),
    DictMoveEntry.BLUE_PAWN_TO_TOP_RIGHT: np.uint64(7),
    DictMoveEntry.BLUE_PAWN_TO_TOP_LEFT: np.uint64(9),
    DictMoveEntry.RED_PAWN_TO_BOTTOM_LEFT: np.uint64(7),
    DictMoveEntry.RED_PAWN_TO_BOTTOM_RIGHT: np.uint64(9),
}


class FilteredPositionsArray(list):
    """ list: [(np.uint64, np.uint64)]
                (bitmask, startpos)"""

    def __init__(self, *alist):
        """List[Tuple[bitmask:np.uint64, startpos:np.uint64]]
           or Tuple[np.uint64, np.uint64]
        """
        if (len(alist) > 0):
            self.append(alist)

    def append(self, items):
        if (len(items) > 0):
            if (isinstance(items, list) and
                    isinstance(items[0], tuple) and
                    isinstance(items[0,0], np.uint64) and
                    isinstance(items[0,1], np.uint64)):
                super().extend(items)
            elif (
                    isinstance(items, tuple) and
                    isinstance(items[0], np.uint64) and
                    isinstance(items[1], np.uint64)):
                super().append(items)

            else:
                raise TypeError("Element of this list must be (np.uint64, np.uint64)")


class UnvalidateMovesArray(list):
    def __init__(self, *list):
        """List of (uint64,uint64, uint64): (start,target,bitmask)
        """
        if (len(list) > 0):
            self.append(list)

    def append(self, items):
        if (len(items) > 0):
            if (isinstance(items, list) and
                    isinstance(items[0], tuple) and
                    isinstance(items[0,0], np.uint64) and
                    isinstance(items[0,1], np.uint64) and
                    isinstance(items[0,2], np.uint64)):
                super().extend(items)
            elif (
                    isinstance(items, tuple) and
                    isinstance(items[0], np.uint64) and
                    isinstance(items[1], np.uint64)):
                super().append(items)

            else:
                raise TypeError("Element of this list must be (np.uint64, np.uint64, np.uint64)")


NotAccessiblePos = np.uint64(2 ** 63 + 2 ** 56 + 2 ** 7 + 2 ** 0)


# class BoardCommand(Enum):
#     Hit_Red_PawnOnTarget = 0
#     Hit_Blue_PawnOnTarget = 1
#     Hit_Red_KnightOnTarget = 2
#     Hit_Blue_KnightOnTarget = 3
#     Upgrade_Blue_KnightOnTarget = 4
#     Upgrade_Red_KnightOnTarget = 5
#     Degrade_Blue_KnightOnTarget = 6
#     Degrade_Red_KnightOnTarget = 7
#     Move_Blue_Knight_no_Change = 8
#     Move_Red_Knight_no_Change = 9
#     Move_Blue_Pawn_no_Change = 10
#     Move_Red_Pawn_no_Change = 11
#     Cannot_Move = 12
#     Delete_Red_Pawn_from_StartPos =13
#     Delete_Blue_Pawn_from_StartPos =14
#     Delete_Red_Knight_from_StartPos = 15
#     Delete_Blue_Knight_from_StartPos = 16

class BoardCommand(fastenum.Enum):
    Hit_Red_PawnOnTarget = 0
    Hit_Blue_PawnOnTarget = 1
    Hit_Red_KnightOnTarget = 2
    Hit_Blue_KnightOnTarget = 3
    Upgrade_Blue_KnightOnTarget = 4
    Upgrade_Red_KnightOnTarget = 5
    Degrade_Blue_KnightOnTarget = 6
    Degrade_Red_KnightOnTarget = 7
    Move_Blue_Knight_no_Change = 8
    Move_Red_Knight_no_Change = 9
    Move_Blue_Pawn_no_Change = 10
    Move_Red_Pawn_no_Change = 11
    Cannot_Move = 12
    Delete_Red_Pawn_from_StartPos =13
    Delete_Blue_Pawn_from_StartPos =14
    Delete_Red_Knight_from_StartPos = 15
    Delete_Blue_Knight_from_StartPos = 16

# class GameServerModel(Enum):
#     FEN_BOARD = 0
#     CURRENT_PLAYER_STRING = 1
#     PLAYER1 = 2
#     PLAYER2 = 3
class GameServerModel(fastenum.Enum):
    FEN_BOARD = 0
    CURRENT_PLAYER_STRING = 1
    PLAYER1 = 2
    PLAYER2 = 3


class MaxHeap:
    _heap =[]
    def __init__(self):
        self._heap = []
    
    def push(self, mvlist):
        [heapq.heappush(self._heap, (-mv[3],mv[0],mv[1],mv[2]) ) for mv in mvlist]    
    def pop(self):
        mv = heapq.heappop(self._heap)
        mv = (mv[1],mv[2],mv[3],-mv[0])
        return mv

class MaxHeapMCTS:
    _heap =[]
    def __init__(self):
        self._heap = []
    
    def push(self, item):
        """ 
        Args:
            item (float,treelib.Node): (score,node)
        """
        score, node = item
        heapq.heappush(self._heap, (-score,node) )     
    def pop(self):
        """returns Tuple[float,treelib.Node]: (score,node)"""
        mv = heapq.heappop(self._heap)
        mv = mv[1]
        return mv
    def clear(self):
        self._heap = []

BC_TO_BOARD_OPS_DICT = {
    BoardCommand.Hit_Red_PawnOnTarget:              [[GameState._ZARR_INDEX_R_PAWNS],True,True],
    BoardCommand.Hit_Blue_PawnOnTarget:             [[GameState._ZARR_INDEX_B_PAWNS],True,True],
    BoardCommand.Hit_Red_KnightOnTarget:            [[GameState._ZARR_INDEX_R_KNIGHTS],True,True],
    BoardCommand.Hit_Blue_KnightOnTarget:           [[GameState._ZARR_INDEX_B_KNIGHTS],True,True], 
    
    BoardCommand.Upgrade_Blue_KnightOnTarget:       [[GameState._ZARR_INDEX_B_KNIGHTS],False,True],  
    BoardCommand.Upgrade_Red_KnightOnTarget:        [[GameState._ZARR_INDEX_R_KNIGHTS],False,True],  
    
    BoardCommand.Degrade_Blue_KnightOnTarget:       [[GameState._ZARR_INDEX_B_PAWNS],False,True],  
    BoardCommand.Degrade_Red_KnightOnTarget:        [[GameState._ZARR_INDEX_R_PAWNS],False,True],  
    
    BoardCommand.Move_Blue_Knight_no_Change:        [[GameState._ZARR_INDEX_B_KNIGHTS],False,True], 
    BoardCommand.Move_Red_Knight_no_Change:         [[GameState._ZARR_INDEX_R_KNIGHTS],False,True], 
    BoardCommand.Move_Blue_Pawn_no_Change:          [[GameState._ZARR_INDEX_B_PAWNS],False,True], 
    BoardCommand.Move_Red_Pawn_no_Change:           [[GameState._ZARR_INDEX_R_PAWNS],False,True], 
    
    BoardCommand.Delete_Red_Pawn_from_StartPos:     [[GameState._ZARR_INDEX_R_PAWNS],True,False], 
    BoardCommand.Delete_Blue_Pawn_from_StartPos:    [[GameState._ZARR_INDEX_B_PAWNS],True,False],
    
    BoardCommand.Delete_Red_Knight_from_StartPos:   [[GameState._ZARR_INDEX_R_KNIGHTS],True,False], 
    BoardCommand.Delete_Blue_Knight_from_StartPos:  [[GameState._ZARR_INDEX_B_KNIGHTS],True,False],     
}

BITMASK_MIDGAME =   np.uint64(0b0000000000000000000000001111111111111111000000000000000000000000)


# class MCTS_GAME_CONFIG:
#     def __init__(self, board:np.uint64, player:Player, C: float= np.sqrt(2)):
#         self.board = board
#         self.player = player
#         self.C = C




