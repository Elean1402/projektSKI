import unittest
from src.model import *
from src.moveGenerator import MoveGenerator
from src.gui import *
from src.gamestate import *

class moveGenerator(unittest.TestCase):
    @unittest.skip("not implemented yet")
    def test_updateBoard_1(self):
        self.assertEqual(True,True)
        
    @unittest.skip("not implemented yet")
    def test_genMoves_1(self):
        self.assertEqual(True,True)
    
    @unittest.skip("not implemented yet")
    def test_genUnvalidatedMoves_1(self):
        self.assertEqual(True,True)
    
    @unittest.skip("not implemented yet")
    def test_getBitPositions_1(self):
        self.assertEqual(True,True)
        
    @unittest.skip("not implemented yet")
    def test_getTarget_1(self):
        self.assertEqual(True,True)
    
    
    def test_getAllPawns_1(self):
        
        BB = GameState.createBitBoardFromFEN("b05/8/8/8/8/8/8/r05")
        print(BB)
        mvG = MoveGenerator(BB)
        mvG.prettyPrintBoard()
        posRedPawns =mvG._getAllPawns(Player.Red)
        posBluePawns = mvG._getAllPawns(Player.Blue)
        
        self.assertEqual(np.log2(posRedPawns),np.log2(2**62))
        self.assertEqual(np.log2(posBluePawns),np.log2(2**6))
    
    def test_getAllPawns_2(self):
        
        BB = GameState.createBitBoardFromFEN("b0b0b0b0b0b0/8/8/8/8/8/8/r0r0r0r0r0r0")
        print(BB)
        mvG = MoveGenerator(BB)
        mvG.prettyPrintBoard()
        posRedPawns =mvG._getAllPawns(Player.Red)
        posBluePawns = mvG._getAllPawns(Player.Blue)
        
        self.assertEqual(np.log2(posRedPawns),np.log2(2**62+2**61+2**60+2**59+2**58+2**57))
        self.assertEqual(np.log2(posBluePawns),np.log2(2**6+2**5+2**4+2**3+2**2+2**1))
    
    def test_getAllPawns_3(self):
        
        BB = GameState.createBitBoardFromFEN("6/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/6")
        print(BB)
        mvG = MoveGenerator(BB)
        mvG.prettyPrintBoard()
        posRedPawns =mvG._getAllPawns(Player.Red)
        posBluePawns = mvG._getAllPawns(Player.Blue)
        
        self.assertEqual(np.log2(posRedPawns),np.log2(2**54+2**53+2**52+2**51+2**50+2**49))
        self.assertEqual(np.log2(posBluePawns),np.log2(2**14+2**13+2**12+2**11+2**10+2**9))
    
    def test_getAllPawns_4(self):
        
        BB = GameState.createBitBoardFromFEN("6/r0b0r0b0r0b0r01/8/8/8/8/1r0b0r0b0r0b0r0/6")
        print(BB)
        mvG = MoveGenerator(BB)
        mvG.prettyPrintBoard()
        posRedPawns =mvG._getAllPawns(Player.Red)
        posBluePawns = mvG._getAllPawns(Player.Blue)
        
        self.assertEqual(np.log2(posRedPawns),np.log2(2**54+2**52+2**50+2**48+2**15+2**13+2**11+2**9))
        self.assertEqual(np.log2(posBluePawns),np.log2(2**53+2**51+2**49+2**14+2**12+2**10))
        
    def test_getAllPawns_5(self):
        
        BB = GameState.createBitBoardFromFEN("6/8/8/8/8/8/8/6")
        print(BB)
        mvG = MoveGenerator(BB)
        mvG.prettyPrintBoard()
        posRedPawns =mvG._getAllPawns(Player.Red)
        posBluePawns = mvG._getAllPawns(Player.Blue)
        
        self.assertEqual((posRedPawns),0)
        self.assertEqual((posBluePawns),0)
        
    def test_getAllPawns_6(self):
        
        BB = GameState.createBitBoardFromFEN("bbbbbbbbbbbb/8/8/8/8/8/8/rrrrrrrrrrrr")
        print(BB)
        mvG = MoveGenerator(BB)
        mvG.prettyPrintBoard()
        posRedPawns =mvG._getAllPawns(Player.Red)
        posBluePawns = mvG._getAllPawns(Player.Blue)
        
        self.assertEqual((posRedPawns),0)
        self.assertEqual((posBluePawns),0)
        
    def test_getAllPawns_6(self):
        
        BB = GameState.createBitBoardFromFEN("brbrbrbrbrbr/8/8/8/8/8/8/rbrbrbrbrbrb")
        print(BB)
        mvG = MoveGenerator(BB)
        mvG.prettyPrintBoard()
        posRedPawns =mvG._getAllPawns(Player.Red)
        posBluePawns = mvG._getAllPawns(Player.Blue)
        
        self.assertEqual((posRedPawns),0)
        self.assertEqual((posBluePawns),0)
    
    def test_getAllPawns_6(self):
        
        BB = GameState.createBitBoardFromFEN("6/r07/8/8/8/8/b07/6")
        print(BB)
        mvG = MoveGenerator(BB)
        mvG.prettyPrintBoard()
        posRedPawns =mvG._getAllPawns(Player.Red)
        posBluePawns = mvG._getAllPawns(Player.Blue)
        
        self.assertEqual(np.log2(posRedPawns),np.log2(2**15))
        self.assertEqual(np.log2(posBluePawns),np.log2(2**55))
    
    @unittest.skip("not implemented yet")
    def test_getAllKnights_1(self):
        self.assertEqual(True,True)
        
    @unittest.skip("not implemented yet")
    def test_filterPositions_1(self):
        player = Player.Red
        BB = GameState.createBitBoardFromFEN("b05/8/8/8/8/8/8/r05")
        mvG = MoveGenerator(BB)
        #mvG._filterPositions(player,)
        
        self.assertEqual(True,True)
    
    @unittest.skip("not implemented yet")
    def test_validateMoves_1(self):
        self.assertEqual(True,True)
    
    @unittest.skip("not implemented yet")
    def test_gameover_1(self):
        self.assertEqual(True,True)
        
    @unittest.skip("not implemented yet")
    def test_execSingleMove_1(self):
        self.assertEqual(True,True)
    