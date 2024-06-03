import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from src.model import *
from src.moveGenerator import MoveGenerator
from src.gui import *
from src.gamestate import *
from src.moveLib import *

class moveGenerator(unittest.TestCase):
    @unittest.skip("not implemented yet")
    def test_updateBoard_1(self):
        self.assertEqual(True,True)
        
    @unittest.skip("not implemented yet")
    def test_genMoves_1(self):
        self.assertEqual(True,True)
    
    
    def test_genValidatedMoves_1(self):
        """At this moment, only for red player functional"""
        BB = GameState.createBitBoardFromFEN("6/8/8/8/8/8/8/r05")
        mvG = MoveGenerator(BB)
        list1 = mvG._genValidatedMoves(Player.Red)
        mvG.prettyPrintBoard()
        
        print(list1)
        self.assertListEqual([MoveLib.move(x,y,3) for x,y,z in list1], ["B8-B7", "B8-A7", "B8-C7", "B8-C8"])
    
    
    
    def test_genValidatedMoves_2(self):
        """At this moment, only for red player functional"""
        BB = GameState.createBitBoardFromFEN("6/r07/8/8/8/8/8/6")
        mvG = MoveGenerator(BB)
        list = mvG._genValidatedMoves(Player.Red)
        mvG.prettyPrintBoard()
        mvG.prettyPrintMoves(list)
        self.assertEqual([MoveLib.move(x,y,3) for x,y,z in list],["A2-B1","A2-B2"])
        
    def test_genValidatedMoves_3(self):
        """At this moment, only for red player functional"""
        BB = GameState.createBitBoardFromFEN("6/br7/8/8/8/8/8/6")
        mvG = MoveGenerator(BB)
        list = mvG._genValidatedMoves(Player.Red)
        mvG.prettyPrintBoard()
        mvG.prettyPrintMoves(list)
        self.assertEqual([MoveLib.move(x,y,3) for x,y,z in list],["A2-C1"])
    
    def test_genValidatedMoves_4(self):
        """At this moment, only for red player functional"""
        BB = GameState.createBitBoardFromFEN("6/2rr5/8/8/8/8/8/6")
        mvG = MoveGenerator(BB)
        list = mvG._genValidatedMoves(Player.Red)
        mvG.prettyPrintBoard()
        mvG.prettyPrintMoves(list)
        self.assertEqual([MoveLib.move(x,y,3) for x,y,z in list],["C2-E1"])
        
    def test_genValidatedMoves_5(self):
        """At this moment, only for red player functional"""
        BB = GameState.createBitBoardFromFEN("6/8/6br1/8/8/8/8/6")
        mvG = MoveGenerator(BB)
        list = mvG._genValidatedMoves(Player.Red)
        mvG.prettyPrintBoard()
        mvG.prettyPrintMoves(list)
        self.assertEqual([MoveLib.move(x,y,3) for x,y,z in list],["G3-F1","G3-E2"])
    
    def test_genValidatedMoves_6(self):
        
        BB = GameState.createBitBoardFromFEN("6/8/6br1/8/8/8/8/6")
        mvG = MoveGenerator(BB)
        list = mvG._genValidatedMoves(Player.Blue)
        mvG.prettyPrintBoard()
        mvG.prettyPrintMoves(list)
        self.assertEqual([MoveLib.move(x,y,3) for x,y,z in list],[])
    
    def test_genValidatedMoves_7(self):
        
        BB = GameState.createBitBoardFromFEN("6/8/1bb6/8/8/8/8/6")
        mvG = MoveGenerator(BB)
        list = mvG._genValidatedMoves(Player.Blue)
        mvG.prettyPrintBoard()
        mvG.prettyPrintMoves(list)
        
        self.assertEqual([MoveLib.move(x,y,3) for x,y,z in list],["B3-A5","B3-C5", "B3-D4"])
        
    def test_genValidatedMoves_8(self):
        
        BB = GameState.createBitBoardFromFEN("6/8/1bb6/8/8/8/8/6")
        mvG = MoveGenerator(BB)
        list = mvG._genValidatedMoves(Player.Blue)
        mvG.prettyPrintBoard()
        mvG.prettyPrintMoves(list)
        
        self.assertEqual([MoveLib.move(x,y,3) for x,y,z in list],["B3-A5","B3-C5","B3-D4"])
    
    @unittest.skip("not implemented yet")
    def test_getBitPositions_1(self):
        self.assertEqual(True,True)
        
    
    def test_getTarget_1(self):
        BB = GameState.createBitBoardFromFEN("b05/8/8/8/8/8/8/6")
        mvG = MoveGenerator(BB)
        bp = mvG._getAllPawns(Player.Blue)
        move = mvG._getTarget(bp, BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP])
        print(MoveLib.move(*move,3))
        self.assertEqual("B1-B2",MoveLib.move(*move,3))
    
    def test_getTarget_2(self):
        BB = GameState.createBitBoardFromFEN("b05/8/8/8/8/8/8/6")
        mvG = MoveGenerator(BB)
        bp = mvG._getAllPawns(Player.Blue)
        move = mvG._getTarget(bp, BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_LEFT])
        print(MoveLib.move(*move,3))
        self.assertEqual("B1-A2",MoveLib.move(*move,3))   
    
    def test_getTarget_2(self):
        BB = GameState.createBitBoardFromFEN("b05/8/8/8/8/8/8/6")
        mvG = MoveGenerator(BB)
        bp = mvG._getAllPawns(Player.Blue)
        move = mvG._getTarget(bp, BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_RIGHT])
        print(MoveLib.move(*move,3))
        self.assertEqual("B1-C2",MoveLib.move(*move,3))   
    
    def test_getTarget_2(self):
        BB = GameState.createBitBoardFromFEN("b05/8/8/8/8/8/8/6")
        mvG = MoveGenerator(BB)
        bp = mvG._getAllPawns(Player.Blue)
        move = mvG._getTarget(bp, BitMaskDict[DictMoveEntry.PAWN_TO_RIGHT])
        print(MoveLib.move(*move,3))
        self.assertEqual("B1-C1",MoveLib.move(*move,3))   
    
    def test_getTarget_2(self):
        BB = GameState.createBitBoardFromFEN("b05/8/8/8/8/8/8/6")
        mvG = MoveGenerator(BB)
        bp = mvG._getAllPawns(Player.Blue)
        bp = mvG._filterPositions(Player.Blue,bp, BitMaskDict[DictMoveEntry.PAWN_TO_LEFT])
        print("filteredpos:", bp)
        move = mvG._getTarget(bp, BitMaskDict[DictMoveEntry.PAWN_TO_LEFT])
        print(MoveLib.move(*move,3))
        self.assertEqual("H1-H1",MoveLib.move(*move,3))
    
    def test_getTarget_3(self):
        """Edge Case Test - all not possible
            "6/bb7/8/8/8/8/1rbbb3bb1/6" """
        BB = GameState.createBitBoardFromFEN("6/bb7/8/8/8/8/8/6")
        mvG = MoveGenerator(BB)
        bp = mvG._getAllKnights(Player.Blue)
        bp2 = mvG._filterPositions(Player.Blue, bp, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_LEFT])
        move = mvG._getTarget(bp2, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_LEFT])
        
        bp2 = mvG._filterPositions(Player.Blue, bp, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPLEFT])
        move2 = mvG._getTarget(bp2, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPLEFT])
        bp2 = mvG._filterPositions(Player.Blue, bp, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPRIGHT])
        move3 = mvG._getTarget(bp2, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPRIGHT])
        bp2 = mvG._filterPositions(Player.Blue, bp, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_RIGHT])
        move4 = mvG._getTarget(bp2, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_RIGHT])
        print(MoveLib.move(*move,3))
        print(MoveLib.move(*move2,3))
        print(MoveLib.move(*move3,3))
        print(MoveLib.move(*move4,3))
        
        self.assertEqual("H1-H1",MoveLib.move(*move,3))
        self.assertEqual("H1-H1",MoveLib.move(*move2,3))
        self.assertEqual("A2-B4",MoveLib.move(*move3,3))
        self.assertEqual("A2-C3",MoveLib.move(*move4,3))
        
    def test_getTarget_4(self):
        """Edge Case Test - all not possible
            "6/8/8/8/8/8/1rb6/6" """
        BB = GameState.createBitBoardFromFEN("6/8/8/8/8/8/1rb6/6")
        mvG = MoveGenerator(BB)
        bp = mvG._getAllKnights(Player.Blue)
        bp2 = mvG._filterPositions(Player.Blue, bp, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_LEFT])
        move = mvG._getTarget(bp2, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_LEFT])
        
        bp2 = mvG._filterPositions(Player.Blue, bp, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPLEFT])
        move2 = mvG._getTarget(bp2, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPLEFT])
        bp2 = mvG._filterPositions(Player.Blue, bp, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPRIGHT])
        move3 = mvG._getTarget(bp2, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPRIGHT])
        bp2 = mvG._filterPositions(Player.Blue, bp, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_RIGHT])
        move4 = mvG._getTarget(bp2, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_RIGHT])
        print(MoveLib.move(*move,3))
        print(MoveLib.move(*move2,3))
        print(MoveLib.move(*move3,3))
        print(MoveLib.move(*move4,3))
        
        self.assertEqual("H1-H1",MoveLib.move(*move,3))
        self.assertEqual("H1-H1",MoveLib.move(*move2,3))
        self.assertEqual("H1-H1",MoveLib.move(*move3,3))
        self.assertEqual("B7-D8",MoveLib.move(*move4,3))
    
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
    
    def test_checkTargetPos_11(self):
        """At this moment only for blue player implemented
            Test for Pawns"""
        
        BB = GameState.createBitBoardFromFEN("b05/8/8/8/8/8/8/6")    
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard()
       
        moves= mvg._genValidatedMoves(Player.Blue)
        print(moves)
        mvg.prettyPrintMoves(moves)
        #boardcommands = [mvg._checkTargetPos(Player.Blue, move) for move in moves]
        l = [ (MoveLib.move(start,target,3),bc)  for start,target,bc in moves]
        
        self.assertListEqual(l, [("B1-B2",[BoardCommand.Move_Blue_Pawn_no_Change]),("B1-C1",[BoardCommand.Move_Blue_Pawn_no_Change])])
    
    def test_checkTargetPos_12(self):
        """At this moment only for blue player implemented
            Test for Pawns"""
        
        BB = GameState.createBitBoardFromFEN("b05/1r0r07/8/8/8/8/8/6")    
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard()
       
        moves= mvg._genValidatedMoves(Player.Blue)
        print(moves)
        mvg.prettyPrintMoves(moves)
        #boardcommands = [mvg._checkTargetPos(Player.Blue, move) for move in moves]
        l = [ (MoveLib.move(start,target,3),bc)  for start,target,bc in moves]
        
        self.assertListEqual(l, [("B1-C2",[BoardCommand.Hit_Red_PawnOnTarget,BoardCommand.Move_Blue_Pawn_no_Change]),("B1-C1",[BoardCommand.Move_Blue_Pawn_no_Change])])
    
    def test_checkTargetPos_13(self):
        """At this moment only for blue player implemented
            Test for Pawns"""
        
        BB = GameState.createBitBoardFromFEN("b05/r0r0r07/8/8/8/8/8/6")    
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard()
       
        moves= mvg._genValidatedMoves(Player.Blue)
        print(moves)
        mvg.prettyPrintMoves(moves)
        #boardcommands = [mvg._checkTargetPos(Player.Blue, move) for move in moves]
        l = [ (MoveLib.move(start,target,3),bc)  for start,target,bc in moves]
        t = [("B1-C2",[BoardCommand.Hit_Red_PawnOnTarget,BoardCommand.Move_Blue_Pawn_no_Change]),("B1-C1",[BoardCommand.Move_Blue_Pawn_no_Change]),("B1-A2",[BoardCommand.Hit_Red_PawnOnTarget,BoardCommand.Move_Blue_Pawn_no_Change])]
        
        l.sort(key=lambda x: x[0])
        t.sort(key=lambda x: x[0])
        
        self.assertListEqual(l,t)
    
    def test_checkTargetPos_14(self):
        """At this moment only for blue player implemented
            Test for Pawns"""
        
        BB = GameState.createBitBoardFromFEN("bb5/8/8/8/8/8/8/6")    
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard()
       
        moves= mvg._genValidatedMoves(Player.Blue)
        print(moves)
        mvg.prettyPrintMoves(moves)
        #boardcommands = [mvg._checkTargetPos(Player.Blue, move) for move in moves]
        l = [ (MoveLib.move(start,target,3),bc)  for start,target,bc in moves]
        t = [("B1-A3",[BoardCommand.Degrade_Blue_KnightOnTarget]),("B1-C3",[BoardCommand.Degrade_Blue_KnightOnTarget]),("B1-D2",[BoardCommand.Degrade_Blue_KnightOnTarget])]
        
        l.sort(key=lambda x: x[0])
        t.sort(key=lambda x: x[0])
        
        self.assertListEqual(l,t)
    
    def test_checkTargetPos_15(self):
        """At this moment only for blue player implemented
            Test for Pawns"""
        
        BB = GameState.createBitBoardFromFEN("bb5/8/r07/8/8/8/8/6")    
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard()
       
        moves= mvg._genValidatedMoves(Player.Blue)
        print(moves)
        mvg.prettyPrintMoves(moves)
        #boardcommands = [mvg._checkTargetPos(Player.Blue, move) for move in moves]
        l = [ (MoveLib.move(start,target,3),bc)  for start,target,bc in moves]
        t = [("B1-A3",[BoardCommand.Hit_Red_PawnOnTarget,BoardCommand.Degrade_Blue_KnightOnTarget]),("B1-C3",[BoardCommand.Degrade_Blue_KnightOnTarget]),("B1-D2",[BoardCommand.Degrade_Blue_KnightOnTarget])]
        
        l.sort(key=lambda x: x[0])
        t.sort(key=lambda x: x[0])
        
        self.assertListEqual(l,t)
    
    def test_checkTargetPos_16(self):
        """At this moment only for blue player implemented
            Test for Pawns"""
        
        BB = GameState.createBitBoardFromFEN("bb5/8/rr7/8/8/8/8/6")    
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard()
       
        moves= mvg._genValidatedMoves(Player.Blue)
        print(moves)
        mvg.prettyPrintMoves(moves)
        #boardcommands = [mvg._checkTargetPos(Player.Blue, move) for move in moves]
        l = [ (MoveLib.move(start,target,3),bc)  for start,target,bc in moves]
        t = [("B1-A3",[BoardCommand.Hit_Red_KnightOnTarget,BoardCommand.Move_Blue_Knight_no_Change]),("B1-C3",[BoardCommand.Degrade_Blue_KnightOnTarget]),("B1-D2",[BoardCommand.Degrade_Blue_KnightOnTarget])]
        
        l.sort(key=lambda x: x[0])
        t.sort(key=lambda x: x[0])
        
        self.assertListEqual(l,t)
    
    def test_checkTargetPos_17(self):
        """At this moment only for blue player implemented
            Test for Pawns"""
        
        BB = GameState.createBitBoardFromFEN("bb5/8/rb7/8/8/8/8/6")    
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard()
       
        moves= mvg._genValidatedMoves(Player.Blue)
        print(moves)
        mvg.prettyPrintMoves(moves)
        #boardcommands = [mvg._checkTargetPos(Player.Blue, move) for move in moves]
        l = [ (MoveLib.move(start,target,3),bc)  for start,target,bc in moves]
        t = [("B1-C3",[BoardCommand.Degrade_Blue_KnightOnTarget]),("B1-D2",[BoardCommand.Degrade_Blue_KnightOnTarget]),
             ("A3-B5",[BoardCommand.Degrade_Blue_KnightOnTarget]),("A3-C4",[BoardCommand.Degrade_Blue_KnightOnTarget])]
        
        l.sort(key=lambda x: x[0])
        t.sort(key=lambda x: x[0])
        
        self.assertListEqual(l,t)
    
    def test_checkTargetPos_18(self):
        """At this moment only for blue player implemented
            Test for Pawns"""
        
        BB = GameState.createBitBoardFromFEN("b0b04/8/8/8/8/8/8/6")    
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard()
       
        moves= mvg._genValidatedMoves(Player.Blue)
        print(moves)
        mvg.prettyPrintMoves(moves)
        #boardcommands = [mvg._checkTargetPos(Player.Blue, move) for move in moves]
        l = [ (MoveLib.move(start,target,3),bc)  for start,target,bc in moves]
        t = [("B1-B2",[BoardCommand.Move_Blue_Pawn_no_Change]),("B1-C1",[BoardCommand.Upgrade_Blue_KnightOnTarget]),
             ("C1-B1",[BoardCommand.Upgrade_Blue_KnightOnTarget]), ("C1-C2",[BoardCommand.Move_Blue_Pawn_no_Change]),("C1-D1",[BoardCommand.Move_Blue_Pawn_no_Change])]
        
        l.sort(key=lambda x: x[0])
        t.sort(key=lambda x: x[0])
        
        self.assertListEqual(l,t)  
    
    @unittest.skip("not implemented yet")
    def test_validateMoves_1(self):
        self.assertEqual(True,True)
    
    @unittest.skip("not implemented yet")
    def test_gameover_1(self):
        self.assertEqual(True,True)
        
    @unittest.skip("not implemented yet")
    def test_execSingleMove_1(self):
        self.assertEqual(True,True)
    