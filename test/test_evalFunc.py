import unittest
from src.scoreConfig_evalFunc import ScoreConfig
from src.evalFunc import *
from src.zuggenerator import *

class EvalFunc(unittest.TestCase):
    # def version0(self):
    #     evFunc = EvalFunc(ScoreConfig.Version0)
    def test_version0(self):
        init_position(alpha_p, alpha_k, beta_p, beta_k)
        list = alpha_generation()
        print("type of moveList=",type(list[0][2]))
        print("figure: ",np.log2(list[0][1]))
        print("moves: ", np.log2(list[0][2]))
        print(moves_to_string(list))
        print_bitboards()
        #print_state()
        self.assertEqual(list, ["a"])