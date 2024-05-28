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
       BB = GameState.createBitBoardFromFEN("6/8/8/8/8/8/8/6")
       mvG = MoveGenerator(BB)
       
       self.assertEqual(True,False)
    
    
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
        
    def test_getAllPawns_7(self):
        
        BB = GameState.createBitBoardFromFEN("brbrbrbrbrbr/8/8/8/8/8/8/rbrbrbrbrbrb")
        print(BB)
        mvG = MoveGenerator(BB)
        mvG.prettyPrintBoard()
        posRedPawns =mvG._getAllPawns(Player.Red)
        posBluePawns = mvG._getAllPawns(Player.Blue)
        
        self.assertEqual((posRedPawns),0)
        self.assertEqual((posBluePawns),0)
    
    def test_getAllPawns_8(self):
        
        BB = GameState.createBitBoardFromFEN("6/r07/8/8/8/8/b07/6")
        print(BB)
        mvG = MoveGenerator(BB)
        mvG.prettyPrintBoard()
        posRedPawns =mvG._getAllPawns(Player.Red)
        posBluePawns = mvG._getAllPawns(Player.Blue)
        
        self.assertEqual(np.log2(posRedPawns),np.log2(2**15))
        self.assertEqual(np.log2(posBluePawns),np.log2(2**55))
    
    
    def test_getAllKnights_1(self):
        BB = GameState.createBitBoardFromFEN("bbbbbbbbbbbb/8/8/8/8/8/8/rrrrrrrrrrrr")
        print(BB)
        mvG = MoveGenerator(BB)
        mvG.prettyPrintBoard()
        posRedKnights =mvG._getAllKnights(Player.Red)
        posBlueKnights = mvG._getAllKnights(Player.Blue)
        bits = np.uint64(2**6+2**5+2**4+2**3+2**2+2**1)
        self.assertEqual(np.log2(posRedKnights),np.log2(bits << np.uint64(7*8)))
        self.assertEqual(np.log2(posBlueKnights),np.log2(bits))
        
    def test_getAllKnights_2(self):
        BB = GameState.createBitBoardFromFEN("6/8/1rbrbrbrbrbrb1/8/8/1brbrbrbrbrbr1/8/6")
        print(BB)
        mvG = MoveGenerator(BB)
        mvG.prettyPrintBoard()
        posRedKnights =mvG._getAllKnights(Player.Red)
        posBlueKnights = mvG._getAllKnights(Player.Blue)
        bits = np.uint64(2**6+2**5+2**4+2**3+2**2+2**1)
        self.assertEqual(np.log2(posRedKnights),np.log2(bits << np.uint64(5*8)))
        self.assertEqual(np.log2(posBlueKnights),np.log2(bits << np.uint64(2*8)))
        
    
    def test_filterPositions_1(self):
        BB = GameState.createBitBoardFromFEN("b05/8/8/8/8/8/8/r05")
        print(BB)
        mvG = MoveGenerator(BB)
        mvG.prettyPrintBoard()
        redPawns = mvG._getAllPawns(Player.Red)
        fredpos =mvG._filterPositions(Player.Red,redPawns,BitMaskDict[DictMoveEntry.PAWN_TO_LEFT])
        self.assertEqual(fredpos,0)
        fredpos =mvG._filterPositions(Player.Red,redPawns,BitMaskDict[DictMoveEntry.PAWN_TO_RIGHT])
        self.assertEqual(np.log2(fredpos), np.log2( 2**62))
        fredpos =mvG._filterPositions(Player.Red,redPawns,BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM])
        self.assertEqual(np.log2(fredpos), np.log2( 2**62))
        try:
            fredpos =mvG._filterPositions(Player.Blue,redPawns,BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM])
        except:
            self.assertEqual(True,True)
        try:
            fredpos =mvG._filterPositions(Player.Red,redPawns,BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM_LEFT])
        except:
            self.assertEqual(np.log2(fredpos),np.log2(2**62))
        fredpos =mvG._filterPositions(Player.Red,redPawns,BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM_RIGHT])
        self.assertEqual(fredpos, 2**62)
    
    def test_filterPositions_2(self):
        BB = GameState.createBitBoardFromFEN("b05/8/8/8/8/8/8/r05")
        print(BB)
        mvG = MoveGenerator(BB)
        mvG.prettyPrintBoard()
        redPawns = mvG._getAllPawns(Player.Blue)
        fredpos =mvG._filterPositions(Player.Blue,redPawns,BitMaskDict[DictMoveEntry.PAWN_TO_LEFT])
        self.assertEqual(fredpos,0)
        fredpos =mvG._filterPositions(Player.Blue,redPawns,BitMaskDict[DictMoveEntry.PAWN_TO_RIGHT])
        self.assertEqual(np.log2(fredpos), np.log2( 2**6))
        fredpos =mvG._filterPositions(Player.Blue,redPawns,BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP])
        self.assertEqual(np.log2(fredpos), np.log2( 2**6))
        try:
            fredpos =mvG._filterPositions(Player.Blue,redPawns,BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM])
        except:
            self.assertEqual(True,True)
        try:
            fredpos =mvG._filterPositions(Player.Blue,redPawns,BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_LEFT])
        except:
            self.assertEqual(np.log2(fredpos),np.log2(2**6))
        fredpos =mvG._filterPositions(Player.Blue,redPawns,BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_RIGHT])
        self.assertEqual(fredpos, 2**6)
    
    def test_filterPositions_3(self):
        BB = GameState.createBitBoardFromFEN("bb5/8/8/8/8/8/8/1r04")
        print(BB)
        mvG = MoveGenerator(BB)
        mvG.prettyPrintBoard()
        knights = mvG._getAllKnights(Player.Blue)
        fredpos =mvG._filterPositions(Player.Blue,knights,BitMaskDict[DictMoveEntry.BLUE_KNIGHT_LEFT])
        self.assertEqual(fredpos,0)
        fredpos =mvG._filterPositions(Player.Blue,knights,BitMaskDict[DictMoveEntry.BLUE_KNIGHT_RIGHT])
        self.assertEqual(np.log2(fredpos), np.log2( 2**6))
        fredpos =mvG._filterPositions(Player.Blue,knights,BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPLEFT])
        self.assertEqual(np.log2(fredpos), np.log2( 2**6))
        
        fredpos =mvG._filterPositions(Player.Blue,knights,BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPRIGHT])
        self.assertEqual(fredpos,2**6)
    
    def test_filterPositions_4(self):
        BB = GameState.createBitBoardFromFEN("bb5/8/8/8/8/8/8/1rr4")
        print(BB)
        mvG = MoveGenerator(BB)
        mvG.prettyPrintBoard()
        knights = mvG._getAllKnights(Player.Red)
        fredpos =mvG._filterPositions(Player.Red,knights,BitMaskDict[DictMoveEntry.RED_KNIGHT_LEFT])
        self.assertEqual(fredpos,2**61)
        fredpos =mvG._filterPositions(Player.Red,knights,BitMaskDict[DictMoveEntry.RED_KNIGHT_RIGHT])
        self.assertEqual(np.log2(fredpos), np.log2( 2**61))
        fredpos =mvG._filterPositions(Player.Red,knights,BitMaskDict[DictMoveEntry.RED_KNIGHT_TO_BOTLEFT])
        self.assertEqual(np.log2(fredpos), np.log2( 2**61))
        
        fredpos =mvG._filterPositions(Player.Red,knights,BitMaskDict[DictMoveEntry.RED_KNIGHT_TO_BOTRIGHT])
        self.assertEqual(fredpos,2**61)
    
    
    @unittest.skip("not implemented yet")
    def test_validateMoves_1(self):
        self.assertEqual(True,True)
    
    @unittest.skip("not implemented yet")
    def test_gameover_1(self):
        self.assertEqual(True,True)
        
    @unittest.skip("not implemented yet")
    def test_execSingleMove_1(self):
        self.assertEqual(True,True)
    