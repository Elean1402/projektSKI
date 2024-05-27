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
    """ Blue (Bottom) = Alpha (from Zuggenerator)
        Rot (Top) = Beta (from Zuggenerator)
    """
    Red = 0
    Blue = 1