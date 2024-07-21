import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import cProfile
import io
import pstats
from pstats import SortKey
import os
import json

class Benchmarktest2_Func:
    """Just put the profile decorator on top of a Function
    e.g. 
    @Benchmarktest2_Func.profile
    aFunc()
    
    after the call of aFunc(), call benchPrint()

    """
    _SAVE_PATH = 'data/profiles/func_Opt'

    if not os.path.exists(_SAVE_PATH):
        os.makedirs(_SAVE_PATH)


    _S = io.StringIO()
    sortby = SortKey.CUMULATIVE  # 'cumulative'

    # Global profiler instance
    global_profiler = cProfile.Profile()

    @classmethod
    def profile(self,func):

        def wrapper(*args, **kwargs):
            if self._S.closed:
                self._S = io.StringIO()
            self.global_profiler.enable()
            retval = func(*args, **kwargs)

            self.global_profiler.disable()
            return retval

        return wrapper
    @classmethod
    def benchPrint(self, filename:str =""):
        ps = pstats.Stats(self.global_profiler, stream=self._S).sort_stats(SortKey.CUMULATIVE)
        ps.strip_dirs()
        ps.print_stats()
        benchContent = self._S.getvalue()
        print(benchContent)
    
        if filename:
            f = open(self._SAVE_PATH + "/" + filename + ".txt", "a")
            f.write(benchContent + "\n==================================================================================================")
            f.close()
        
        self._S.close()
        self.global_profiler.clear()
    
# example
#   N = 1000000
#   seq_list = list(range(N))
#   seq_set = set(range(N))
#   
#   @Benchmarktest2_Func.profile
#   def search_in_list(num_items=N):
#       return num_items - 1 in seq_list
#   
#   @Benchmarktest2_Func.profile
#   def search_in_set(num_items=N):
#       return num_items - 1 in seq_set
#   
#   
#   
#   
#   if __name__ == '__main__':
#       search_in_set()
#       search_in_list()
#       Benchmarktest2_Func.benchPrint("test")