import numpy as np
from enum import Enum
class ScoredMoveList(list):
    
    def append(self, item):
        if (isinstance(item, tuple) and
            isinstance(item[0],np.uint64) and
            isinstance(item[1], np.uint64) and
            isinstance(item[2],int) and
            isinstance(item[3],int)):
            super().append(item)
        elif(isinstance(item,list) and 
            isinstance(item[0], tuple) and
            isinstance(item[0][0],np.uint64) and
            isinstance(item[0][1], np.uint64) and
            isinstance(item[0][2],int) and
            isinstance(item[0][3],int)):
            super().extend(item)
        else:
            raise TypeError("item is not from type ScoredMoveList: List[(np.uint64, np.uint64,int,int)]:\n item:", item, "\nitem type:", type(item), type(item[0]), type(item[0][0]),type(item[0][1]), type(item[0][2]),type(item[0][3]))
    
    def sort(self):
        """Sort List in ascending order by total score"""
        super().sort(key=lambda x: x[3])
        return self
    def __init__(self,*args):
        """Specific list type for scoring

        Type: List[(np.uint64, np.uint64,int,int)]
            ->List[(FromPos, TargetPos,MoveScore, TotalscoreAfterMove)]
        """
        if(len(args)==0):
            return None
        
        for item in args:
            self.append(item)

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
                isinstance(item[0][1],dict)):
                super().append(*item)
                return None
        else:
            if(isinstance(item, tuple) and
                isinstance(item[0], np.uint64) and
                isinstance(item[1],dict)):
                super().append(item)
                return None
        raise TypeError("item is not from type ScoredListForMerge: List( ( np.uint64, dict( { np.uint64: int } ) ) )")
        
    
    
    def __init__(self,*args):
        """Specific List Type for Preprocessing Scores for Eval Func
        Type: List( ( np.uint64, dict( { np.uint64: int } ) ) )
            ->List( (startPos, dict( { targetPos: score } ) ) )
        """
        if(len(args)>0):
            for item in args:
                self.append(item)

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
    """ Returns list: [(Bitmask, np.uint64)]"""
    def __init__(self,*alist:list):
        if(len(alist)> 0):
            self.append(alist)
        else:
            return self

    def append(self, alist:list):
        if(len(alist)> 0):
            if(isinstance(alist[0][0], BitMask) and
                isinstance(alist[0][1], np.uint64)):
                for item in alist:
                    self.append(item)
            else:
                raise TypeError("Element of this list must be (Bitmask, np.uint64)")
        else:
            return None
        