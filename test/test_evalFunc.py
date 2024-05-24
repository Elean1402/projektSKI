import unittest
from src.scoreConfig_evalFunc import ScoreConfig
from src.evalFunction import EvalFunction
from src.zuggenerator import *
from src.gui import Gui
from src.gamestate import GameState
from src.model import *
from src.moveLib import*
class EvalFunc(unittest.TestCase):
    # def version0(self):
    #     evFunc = EvalFunc(ScoreConfig.Version0)
    
    def test_pieceSquareTable(self):
       config = ScoreConfig.Version0()
       self.assertEqual(len(config), 16)
       ef =  EvalFunction(config)
       M = Gui.fenToMatrix("2r3/8/8/8/8/8/8/3b2")
       board = GameState.createBitBoardFrom(M,True)
       boardgui = GameState.createBitBoardFrom(M)
       #self.assertEqual(boardgui[GameState._ARR_INDEX_R], 2**62)
       M2 = GameState.fromBitBoardToMatrix(board, True)
       self.assertEqual(np.allclose(M,M2),True)
    
       moveList = list()
       moveList.append( ( 0,np.uint64(2**4),list([np.uint64(2**12),np.uint64(2**3),np.uint64(2**5)] ) ) )
       print("startpos:", moveList[0][1])
       print("targetlist:", moveList[0][2])
       self.assertEqual(2**4,board[GameState._ZARR_INDEX_R_PAWNS])
       self.assertEqual(2**4, moveList[0][1])
       self.assertEqual(2**4,moveList[0][1] & board[GameState._ZARR_INDEX_R_PAWNS] & (~ board[GameState._ZARR_INDEX_B_KNIGHTS])) 
      
       scorelist = ScoreListForMerging()
       for index in moveList:
          print(index[1], index[2], board)
          print("psT:",ef._pieceSquareTable(index[1], index[2], board))
       print(scorelist)
       self.assertEqual(True,False)
    
    def test_moveIsNeighbourOfStartPos(self):
        ef = EvalFunction(ScoreConfig.Version0())
        self.assertEqual(ef._moveIsNeighbourOfStartPos(np.uint64(2**4),np.uint64(2**12)),True)
        self.assertEqual(ef._moveIsNeighbourOfStartPos(np.uint64(2**4),np.uint64(2**3)),True)
        self.assertEqual(ef._moveIsNeighbourOfStartPos(np.uint64(2**4),np.uint64(2**5)),True)
        self.assertEqual(ef._moveIsNeighbourOfStartPos(np.uint64(2**4),np.uint64(2**16)),False)
        self.assertEqual(ef._moveIsNeighbourOfStartPos(np.uint64(2**4),np.uint64(2**2)),False)