import numpy as np

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
    def __init__(self,*args):
        """Specific list type for scoring

        Type: List[(np.uint64, np.uint64,int,int)]
            ->List[(FromPos, TargetPos,MoveScore, TotalscoreAfterMove)]
        """
        for item in args:
            self.append(item)
        