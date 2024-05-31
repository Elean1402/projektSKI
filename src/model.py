import numpy as np
from enum import Enum
from collections import Counter
class ScoredMoveList(list):
    
    def append(self, item):
        if (isinstance(item, tuple) and
            isinstance(item[0],np.uint64) and
            isinstance(item[1], np.uint64) and
            isinstance(item[2],int) and
            isinstance(item[3],int) and
            isinstance(item[4], list)):
            super().append(item)
        elif(isinstance(item,list) and 
            isinstance(item[0], tuple) and
            isinstance(item[0][0],np.uint64) and
            isinstance(item[0][1], np.uint64) and
            isinstance(item[0][2],int) and
            isinstance(item[0][3],int) and
            isinstance(item[0][4], list)):
            super().extend(item)
        else:
            raise TypeError("item is not from type ScoredMoveList: List[(np.uint64, np.uint64,int,int)]:\n item:", 
                            item, "\nitem type:", type(item), type(item[0]), type(item[0][0]),type(item[0][1]), type(item[0][2]),type(item[0][3]), type(item[0][4]))
    
    def sort(self):
        """Sort List in ascending order by total score"""
        super().sort(key=lambda x: x[3])
        return self
    def __init__(self,*args):
        """Specific list type for scoring

        Type: List[(np.uint64, np.uint64,int,int)]
            ->List[(FromPos, TargetPos,MoveScore, TotalscoreAfterMove)]
        """
        if(len(args)>0):
            self.append(args)
        
        

class ScoreListForMerging(list):
    
    def append(self, item):
        """Specific Type for Preprocessing Scores

        Args:
             Type: List( ( np.uint64, dict( { np.uint64: int } ) ) )
            ->List( (startPos, dict( { targetPos: score ... } ) ) )
        """
        if(isinstance(item, list)):
             if(isinstance(item[0], tuple) and
                isinstance(item[0][0], np.uint64) and
                isinstance(item[0][1],dict) ):
                super().extend(item)
                
        
        elif(isinstance(item, tuple) and
                isinstance(item[0], np.uint64) and
                isinstance(item[1],dict)):
                super().append(item)
        
        else:        
            raise TypeError("item is not from type ScoredListForMerge: List( ( np.uint64, dict( { np.uint64: int } ) ) )", "item=",item," type of item=",type(item), " type of item[0]=",type(item[0]), "type of item[1]=", type(item[1]), "counter is instance of dict?=>", isinstance(item[1], Counter), "type(item[2])=Bordcommand?=>",isinstance(item[2], BoardCommand) )
        
    
    
    def __init__(self,*args):
        """Specific List Type for Preprocessing Scores for Eval Func
        Type: List( ( np.uint64, dict( { np.uint64: int } ) ) )
            ->List( (startPos, dict( { targetPos: score } ) ) )
        """
        if(len(args)>0):
           self.append(args)
class Config(Enum):
    MOBILITY = "MOBILITY"
    TURN_OPTIONS ="TURN_OPTIONS"
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
    PIECESQUARE_TABLE_PAWN_Blue ="PIECESQUARE_TABLE_PAWN_Blue"
    PIECESQUARE_TABLE_KNIGHT_Blue ="PIECESQUARE_TABLE_KNIGHT_Blue"
    PIECESQUARE_TABLE_PAWN_Red ="PIECESQUARE_TABLE_PAWN_Red"
    PIECESQUARE_TABLE_KNIGHT_Red ="PIECESQUARE_TABLE_KNIGHT_Red"

class Player(Enum):
    """ Blue (Bottom) = Alpha?? (from Zuggenerator)
        Rot (Top) = Beta?? (from Zuggenerator)
    """
    Red = 0
    Blue = 1
    NoOne = 3

class DictMoveEntry(Enum):
    BLUE_PAWN_TO_TOP           =0
    RED_PAWN_TO_BOTTOM         =1
    PAWN_TO_LEFT               =2
    PAWN_TO_RIGHT              =3

    BLUE_KNIGHT_TO_TOPLEFT     =4
    BLUE_KNIGHT_TO_TOPRIGHT    =5
    BLUE_KNIGHT_LEFT           =6
    BLUE_KNIGHT_RIGHT          =7

    RED_KNIGHT_TO_BOTLEFT      =8
    RED_KNIGHT_TO_BOTRIGHT     =9
    RED_KNIGHT_LEFT            =10
    RED_KNIGHT_RIGHT           =11  
    
    BLUE_PAWN_TO_TOP_RIGHT     =12
    BLUE_PAWN_TO_TOP_LEFT      =13
    RED_PAWN_TO_BOTTOM_LEFT    =14
    RED_PAWN_TO_BOTTOM_RIGHT   =15
    GAME_OVER_BLUE_WINS        =16
    GAME_OVER_RED_WINS         =17
    CONTINUE_GAME              =18

BitMaskDict = {
    DictMoveEntry.BLUE_PAWN_TO_TOP           : np.uint64(0b00000000_01111110_11111111_11111111_11111111_11111111_11111111_01111110),
    DictMoveEntry.BLUE_PAWN_TO_TOP_LEFT      : np.uint64(0b00000000_00111111_01111111_01111111_01111111_01111111_01111111_01111110),
    DictMoveEntry.BLUE_PAWN_TO_TOP_RIGHT     : np.uint64(0b00000000_11111100_11111110_11111110_11111110_11111110_11111110_01111110),
    DictMoveEntry.RED_PAWN_TO_BOTTOM         : np.uint64(0b01111110_11111111_11111111_11111111_11111111_11111111_01111110_00000000),
    DictMoveEntry.RED_PAWN_TO_BOTTOM_LEFT    : np.uint64(0b01111110_01111111_01111111_01111111_01111111_01111111_00111111_00000000),
    DictMoveEntry.RED_PAWN_TO_BOTTOM_RIGHT   : np.uint64(0b01111110_11111110_11111110_11111110_11111110_11111110_11111100_00000000),
    DictMoveEntry.PAWN_TO_LEFT               : np.uint64(0b00111110_01111111_01111111_01111111_01111111_01111111_01111111_00111110),
    DictMoveEntry.PAWN_TO_RIGHT              : np.uint64(0b01111100_11111110_11111110_11111110_11111110_11111110_11111110_01111100),
    
    DictMoveEntry.BLUE_KNIGHT_TO_TOPLEFT     : np.uint64(0b00000000_00000000_00111111_01111111_01111111_01111111_01111111_01111110),
    DictMoveEntry.BLUE_KNIGHT_TO_TOPRIGHT    : np.uint64(0b00000000_00000000_11111100_11111110_11111110_11111110_11111110_01111110),
    DictMoveEntry.BLUE_KNIGHT_LEFT           : np.uint64(0b00000000_00011111_00111111_00111111_00111111_00111111_00111111_00111110),
    DictMoveEntry.BLUE_KNIGHT_RIGHT          : np.uint64(0b00000000_11111000_11111100_11111100_11111100_11111100_11111100_01111100),
    
    DictMoveEntry.RED_KNIGHT_TO_BOTLEFT      : np.uint64(0b01111110_01111111_01111111_01111111_01111111_00111111_00000000_00000000),
    DictMoveEntry.RED_KNIGHT_TO_BOTRIGHT     : np.uint64(0b01111110_11111110_11111110_11111110_11111110_11111100_00000000_00000000),
    DictMoveEntry.RED_KNIGHT_LEFT            : np.uint64(0b00111111_00111111_00111111_00111111_00111111_00111111_00011111_00000000),
    DictMoveEntry.RED_KNIGHT_RIGHT           : np.uint64(0b11111100_11111100_11111100_11111100_11111100_11111100_11111000_00000000),
    DictMoveEntry.GAME_OVER_BLUE_WINS        : np.uint64(0b11111111_00000000_00000000_00000000_00000000_00000000_00000000_00000000),
    DictMoveEntry.GAME_OVER_RED_WINS         : np.uint64(0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_11111111),
}
BIT_MASK_ARRAY_PAWN_RED = np.array([BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM] ,BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM_LEFT], BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM_RIGHT], BitMaskDict[DictMoveEntry.PAWN_TO_LEFT] ,BitMaskDict[DictMoveEntry.PAWN_TO_RIGHT]])
BIT_MASK_ARRAY_PAWN_BLUE = np.array([BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP],BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_LEFT],BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_RIGHT],BitMaskDict[DictMoveEntry.PAWN_TO_LEFT],BitMaskDict[DictMoveEntry.PAWN_TO_RIGHT]])
BIT_MASK_ARRAY_KNIGHT_RED = np.array([BitMaskDict[DictMoveEntry.RED_KNIGHT_TO_BOTLEFT],BitMaskDict[DictMoveEntry.RED_KNIGHT_TO_BOTRIGHT],BitMaskDict[DictMoveEntry.RED_KNIGHT_LEFT],BitMaskDict[DictMoveEntry.RED_KNIGHT_RIGHT]])
BIT_MASK_ARRAY_KNIGHT_BLUE = np.array([BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPLEFT],BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPRIGHT],BitMaskDict[DictMoveEntry.BLUE_KNIGHT_LEFT],BitMaskDict[DictMoveEntry.BLUE_KNIGHT_RIGHT]])



DICT_MOVE = {
    DictMoveEntry.RED_PAWN_TO_BOTTOM        :np.uint64(8),
    DictMoveEntry.RED_KNIGHT_LEFT           :np.uint64(6),
    DictMoveEntry.RED_KNIGHT_RIGHT          :np.uint64(10),
    DictMoveEntry.RED_KNIGHT_TO_BOTLEFT     :np.uint64(15),
    DictMoveEntry.RED_KNIGHT_TO_BOTRIGHT    :np.uint64(17),
    
    DictMoveEntry.BLUE_PAWN_TO_TOP          :np.uint64(8),
    DictMoveEntry.BLUE_KNIGHT_LEFT          :np.uint64(10),
    DictMoveEntry.BLUE_KNIGHT_RIGHT         :np.uint64(6),
    DictMoveEntry.BLUE_KNIGHT_TO_TOPLEFT    :np.uint64(17),
    DictMoveEntry.BLUE_KNIGHT_TO_TOPRIGHT   :np.uint64(15),
    
    DictMoveEntry.PAWN_TO_LEFT              :np.uint64(1),
    DictMoveEntry.PAWN_TO_RIGHT             :np.uint64(1),
    DictMoveEntry.BLUE_PAWN_TO_TOP_RIGHT    :np.uint64(7),
    DictMoveEntry.BLUE_PAWN_TO_TOP_LEFT     :np.uint64(9),
    DictMoveEntry.RED_PAWN_TO_BOTTOM_LEFT   :np.uint64(7),
    DictMoveEntry.RED_PAWN_TO_BOTTOM_RIGHT  :np.uint64(9),
}

class FilteredPositionsArray(list): 
    """ list: [(np.uint64, np.uint64)]
                (bitmask, startpos)"""
    def __init__(self,*alist):
        """List[Tuple[bitmask:np.uint64, startpos:np.uint64]]
           or Tuple[np.uint64, np.uint64]
        """
        if(len(alist)> 0):
            self.append(alist)
        

    def append(self, items):
        if(len(items)> 0):
            if( isinstance(items, list) and
                isinstance(items[0], tuple) and
                isinstance(items[0][0], np.uint64) and
                isinstance(items[0][1], np.uint64)):
                super().extend(items)
            elif(
                isinstance(items, tuple) and
                isinstance(items[0], np.uint64) and
                isinstance(items[1], np.uint64)):
                super().append(items)
                
            else:
                raise TypeError("Element of this list must be (np.uint64, np.uint64)")
            
class UnvalidateMovesArray(list):
    def __init__(self,*list):
        """List of (uint64,uint64, uint64): (start,target,bitmask)
        """
        if(len(list)> 0):
            self.append(list)
    
    def append(self, items):
        if(len(items)> 0):
            if( isinstance(items, list) and
                isinstance(items[0], tuple) and
                isinstance(items[0][0], np.uint64) and
                isinstance(items[0][1], np.uint64) and
                isinstance(items[0][2], np.uint64)):
                super().extend(items)
            elif(
                isinstance(items, tuple) and
                isinstance(items[0], np.uint64) and
                isinstance(items[1], np.uint64)):
                super().append(items)
                
            else:
                raise TypeError("Element of this list must be (np.uint64, np.uint64, np.uint64)")
NotAccessiblePos = np.uint64(2**63+2**56+2**7+2**0)

class BoardCommand(Enum):
    Hit_Red_PawnOnTarget            = 0
    Hit_Blue_PawnOnTarget           = 1
    Hit_Red_KnightOnTarget          = 2
    Hit_Blue_KnightOnTarget         = 3
    Upgrade_Blue_KnightOnTarget     = 4
    Upgrade_Red_KnightOnTarget      = 5
    Degrade_Blue_KnightOnTarget     = 6
    Degrade_Red_KnightOnTarget      = 7
    Move_Blue_Knight_no_Change      = 8
    Move_Red_Knight_no_Change       = 9
    Move_Blue_Pawn_no_Change        = 10
    Move_Red_Pawn_no_Change         = 11
    Cannot_Move                     = 12


GET_BOARD_INDEX = 0
GET_PLAYER_INDEX = 1
GET_FIRST_PLAYER_INDEX = 2
GET_SECOND_PLAYER_INDEX = 3

    