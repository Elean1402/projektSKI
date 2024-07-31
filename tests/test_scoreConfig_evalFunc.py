import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from src.scoreConfig_evalFunc import ScoreConfig
from src.model import *
from src.gamestate import GameState


class ScoreConfig_evalFunc(unittest.TestCase):
    @unittest.skip("skip")   
    def test_reversePsqT(self):
        testcase = {    
                        "A8":5,"B8":5,"C8":5,"D8":5,"E8":5,"F8":5,"G8":5,"H8":5,
                        "A7":2,"B7":2,"C7":2,"D7":2,"E7":2,"F7":2,"G7":2,"H7":2,
                        "A6":3,"B6":3,"C6":3,"D6":3,"E6":3,"F6":3,"G6":3,"H6":3,
                        "A5":4,"B5":4,"C5":4,"D5":4,"E5":4,"F5":4,"G5":4,"H5":4,
                        "A4":1,"B4":1,"C4":1,"D4":1,"E4":1,"F4":1,"G4":1,"H4":1,
                        "A3":1,"B3":1,"C3":1,"D3":1,"E3":1,"F3":1,"G3":1,"H3":1,
                        "A2":1,"B2":1,"C2":1,"D2":1,"E2":1,"F2":1,"G2":1,"H2":1,
                        "A1":1,"B1":1,"C1":1,"D1":1,"E1":1,"F1":1,"G1":1,"H1":1}
        target = {'A8': 1, 'B8': 1, 'C8': 1, 'D8': 1, 'E8': 1, 'F8': 1, 'G8': 1, 'H8': 1, 
                    'A7': 1, 'B7': 1, 'C7': 1, 'D7': 1, 'E7': 1, 'F7': 1, 'G7': 1, 'H7': 1, 
                    'A6': 1, 'B6': 1, 'C6': 1, 'D6': 1, 'E6': 1, 'F6': 1, 'G6': 1, 'H6': 1, 
                    'A5': 1, 'B5': 1, 'C5': 1, 'D5': 1, 'E5': 1, 'F5': 1, 'G5': 1, 'H5': 1, 
                    'A4': 4, 'B4': 4, 'C4': 4, 'D4': 4, 'E4': 4, 'F4': 4, 'G4': 4, 'H4': 4, 
                    'A3': 3, 'B3': 3, 'C3': 3, 'D3': 3, 'E3': 3, 'F3': 3, 'G3': 3, 'H3': 3, 
                    'A2': 2, 'B2': 2, 'C2': 2, 'D2': 2, 'E2': 2, 'F2': 2, 'G2': 2, 'H2': 2, 
                    'A1': 5, 'B1': 5, 'C1': 5, 'D1': 5, 'E1': 5, 'F1': 5, 'G1': 5, 'H1': 5}
        print("testcase:\n", ScoreConfig.reversePsqT(testcase))
        print("targetcase:\n",target)
        self.assertEqual(ScoreConfig.reversePsqT(testcase),target)
    @unittest.skip("skip")   
    def test_reversePsqT2(self):
       config1 = ScoreConfig.Version1(Player.Blue)
     
       #print(ScoreConfig.Version1())
       print(config1[Config.TOTAL_SCORE_RATING_PAWN_BLUE])
       print(config1[Config.TOTAL_SCORE_RATING_KNIGHT_BLUE])
       self.assertEqual(True, False)
    @unittest.skip("skip")   
    def test_FieldArray1(self):
        config1 = ScoreConfig.Version2(Player.Blue)
        print(ScoreConfig._ALL_FIELDS_IN_BOARD)
        self.assertEqual(True,False)
    @unittest.skip("skip")   
    def test_CreateScores(self):
        BB = GameState.createBitBoardFromFEN("6/8/b07/1r06/8/8/8/6")
        M= GameState.fromBitBoardToMatrix(BB,True)
        print(M)
        print("zerodict=\n",ScoreConfig._ZERO_DICT)
        
        p,k =ScoreConfig.createScores(ScoreConfig,Player.Red,BB,10,20)
        print("p=\n",p)
        print("k=\n",k)
        config = ScoreConfig.Version2(Player.Blue,BB)
        
        print(config[Config.TOTAL_SCORE_RATING_PAWN_RED])
        self.assertEqual(True,False)