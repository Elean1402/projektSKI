import numpy as np
from typing import overload
class ScoredMoveList(list):
    
    def append(self, item):
        if (isinstance(item, tuple) and
            isinstance(item[0],np.uint64) and
            isinstance(item[1], np.uint64) and
            isinstance(item[2],int) and
            isinstance(item[3],int)):
            super().append(item)
        else:
            raise TypeError("item is not from type ScoredMoveList: List[(np.uint64, np.uint64,int,int)]")
    
    def sort(self):
        """Sort List in ascending order by total score"""
        super().sort(key=lambda x: x[3])
        return self
    def __init__(self,args):
        """Specific list type for scoring

        Type: List[(np.uint64, np.uint64,int,int)]
            ->List[(FromPos, TargetPos,MoveScore, TotalscoreAfterMove)]
        """
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
                super().append(item)
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
        