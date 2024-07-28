import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np

from src.Benchmarktest2_func import *

class TestOptimierung_MoveList():
    
    #def test1_LRU_CACHE_Fakultätsfkt(self):
        #True
    
    
        
    @Benchmarktest2_Func.profile()
    def mapfunc(alist):
        flatList = []
        for x in range(100000):
            flatList= list( map(lambda x: (alist[0][0], x), alist[0][1]) )
        return flatList
    @Benchmarktest2_Func.profile()
    def listcompr_flatt(alist):
        for x in range(100000):
            flatlist = [(alist[0][0], dest) for dest in alist[0][1] ]
        return flatlist
    @Benchmarktest2_Func.profile()
    def nested_listcompr_flatt(alist):
        for x in range(100000):
            flatlist = [[(alist[0][0], dest) for dest in destL[1]] for destL in alist]
        return flatlist                          

if __name__ == '__main__':
    testList1 = [("a", [x for x in range(100)])]
    testList2 = [("a", [x for x in range(100)]), ("b", [x for x in range(100)])]
    
    l1 = TestOptimierung_MoveList.mapfunc(testList1)
    l2 = TestOptimierung_MoveList.listcompr_flatt(testList1)
    l3 = TestOptimierung_MoveList.nested_listcompr_flatt(testList2)
    Benchmarktest2_Func.benchPrint("test")
    