import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from src.scoreConfig_evalFunc import ScoreConfig
from src.alt_eval import EvalFunction

from src.gui import Gui
from src.gamestate import GameState
from src.model import *
from src.moveLib import*
from src.moveGenerator_sicher import MoveGenerator

class EvalFunc(unittest.TestCase):
    # def version0(self):
    #     evFunc = EvalFunc(ScoreConfig.Version0)
    @unittest.skip("depricated")
    def test_pieceSquareTable(self):
       config = ScoreConfig.Version0()
       self.assertEqual(len(config), 16)
       ef =  EvalFunction(config)
       M = Gui.fenToMatrix("2r03/8/8/8/8/8/8/2b03")
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
          print("psT:",ef._pieceSquareTable(index[1],index[2],board))
       print(scorelist)
       self.assertEqual(True,True)
    
    @unittest.skip("depricated")
    def test_turnOptions(self):
        ef = EvalFunction(ScoreConfig.Version0())
        M = Gui.fenToMatrix("2r03/8/8/8/8/8/8/2b03")
        board = GameState.createBitBoardFrom(M,True)
        moveList = list()
        moveList.append( ( 0,np.uint64(2**4),list([np.uint64(2**12),np.uint64(2**3),np.uint64(2**5)] ) ) )
        scorelist = ScoreListForMerging()
        for index in moveList:
            scorelist.append(ef._pieceSquareTable(index[1],index[2],board))
        self.assertEqual(3, ef._TURNOPTIONS)
        self.assertEqual(3*ef._CONFIG_DICT[Config.TURN_OPTIONS], ef._computeTurnOptions())
        self.assertEqual(0, ef._TURNOPTIONS)
    
    @unittest.skip("depricated")
    def test_moveIsNeighbourOfStartPos(self):
        ef = EvalFunction(ScoreConfig.Version0())
        self.assertEqual(ef._moveIsNeighbourOfStartPos(np.uint64(2**4),np.uint64(2**12)),True)
        self.assertEqual(ef._moveIsNeighbourOfStartPos(np.uint64(2**4),np.uint64(2**3)),True)
        self.assertEqual(ef._moveIsNeighbourOfStartPos(np.uint64(2**4),np.uint64(2**5)),True)
        self.assertEqual(ef._moveIsNeighbourOfStartPos(np.uint64(2**4),np.uint64(2**16)),False)
        self.assertEqual(ef._moveIsNeighbourOfStartPos(np.uint64(2**4),np.uint64(2**2)),False)
    
    @unittest.skip("depricated")
    def test_computeOverallScore1(self):
        ef = EvalFunction(ScoreConfig.Version1(),Player.Blue)
        M = Gui.fenToMatrix("2b03/8/8/8/8/8/8/2r03")
        board = GameState.createBitBoardFrom(M,True)
        print("Board blue pawns:",board[GameState._ZARR_INDEX_B_PAWNS])
        init_position(
            board[GameState._ZARR_INDEX_B_PAWNS],
            board[GameState._ZARR_INDEX_B_KNIGHTS],
            board[GameState._ZARR_INDEX_R_PAWNS],
            board[GameState._ZARR_INDEX_R_KNIGHTS]
        )
        moveList = alpha_generation()
        print("moveList:",moveList)
        scorelist = ef.computeOverallScore(moveList,board)
        print("scorelist",scorelist)
        print("startposition:", moveList[0])
        self.assertEqual(True,False)
        #ef.computeOverallScore(movelist, board)
    
    @unittest.skip("not important")
    def test_evalFunc_new(self):
        ef = EvalFunction(ScoreConfig.Version1(),Player.Blue)
        #print(ef._CONFIG_DICT)
        board = GameState.createBitBoardFromFEN("bb5/8/8/8/8/8/8/2r0rr3")
        mvg = MoveGenerator(board)
        
        moves = mvg.genMoves(Player.Blue)
        mvg.prettyPrintMoves(moves)
        scorelist = ef.computeOverallScore(moves, board)
        ef.prettyPrintScorelist(scorelist)
        self.assertEqual(True,True)
    @unittest.skip("depricated")
    def test_evalFunc_FullTest1(self):
        ef = EvalFunction(ScoreConfig.Version1(Player.Red,Player.Blue))
        
        #print(ef._CONFIG_DICT)
        board = GameState.createBitBoardFromFEN("6/8/8/8/2r0b04/8/8/6")
        mvg = MoveGenerator(board)
        gameOver = [DictMoveEntry.CONTINUE_GAME]
        
        
        i = 0
        z= 0
        while(gameOver[0] == DictMoveEntry.CONTINUE_GAME):
        #while(z <= 10):
            if(i == 2):
                i=0
            print("i=",i)
            player = Player.Red if i % 2 == 0 else Player.Blue
            moves = mvg.genMoves(player,board,gameOver)
                
            scorelist = ef.computeOverallScore(moves, board)
            
            newBoard = mvg.execSingleMove(scorelist[0] if len(scorelist)!= 0 else [],player, gameOver, board)
            board = newBoard
            #mvg.up
            i+=1
            z+=1
        
        self.assertEqual(True, False)
    
      
            
        