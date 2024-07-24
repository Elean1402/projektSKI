import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from src.model import *
from src.moveGenerator_sicher import MoveGenerator
from src.gui import *
from src.gamestate import *
from src.moveLib import *
from src.model import *
import json
import random
from collections import deque
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
        mvg = MoveGenerator(BB)
        list1 = mvg._genValidatedMoves(Player.Red,[DictMoveEntry.CONTINUE_GAME],BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
        
        print([MoveLib.move(move[0],move[1],3) for move in list1])
        self.assertListEqual([MoveLib.move(x,y,3) for x,y,z in list1], ["B8-B7", "B8-C8"])
    
    
    
    def test_genValidatedMoves_2(self):
        """At this moment, only for red player functional"""
        BB = GameState.createBitBoardFromFEN("6/r07/8/8/8/8/8/6")
        mvg = MoveGenerator(BB)
        list = mvg._genValidatedMoves(Player.Red,[DictMoveEntry.CONTINUE_GAME],BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
        mvg.prettyPrintMoves(list)
        self.assertEqual([MoveLib.move(x,y,3) for x,y,z in list],["A2-B2"])
        
    def test_genValidatedMoves_3(self):
        """At this moment, only for red player functional"""
        BB = GameState.createBitBoardFromFEN("6/br7/8/8/8/8/8/6")
        mvg = MoveGenerator(BB)
        list = mvg._genValidatedMoves(Player.Red,[DictMoveEntry.CONTINUE_GAME],BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
        mvg.prettyPrintMoves(list)
        self.assertEqual([MoveLib.move(x,y,3) for x,y,z in list],["A2-C1"])
    
    def test_genValidatedMoves_4(self):
        """At this moment, only for red player functional"""
        BB = GameState.createBitBoardFromFEN("6/2rr5/8/8/8/8/8/6")
        mvg = MoveGenerator(BB)
        list = mvg._genValidatedMoves(Player.Red,[DictMoveEntry.CONTINUE_GAME],BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
        mvg.prettyPrintMoves(list)
        self.assertEqual([MoveLib.move(x,y,3) for x,y,z in list],["C2-E1"])
        
    def test_genValidatedMoves_5(self):
        """At this moment, only for red player functional"""
        BB = GameState.createBitBoardFromFEN("6/8/6br1/8/8/8/8/6")
        mvg = MoveGenerator(BB)
        list = mvg._genValidatedMoves(Player.Red,[DictMoveEntry.CONTINUE_GAME],BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
        mvg.prettyPrintMoves(list)
        self.assertEqual([MoveLib.move(x,y,3) for x,y,z in list],["G3-F1","G3-E2"])
    
    def test_genValidatedMoves_6(self):
        
        BB = GameState.createBitBoardFromFEN("6/8/6br1/8/8/8/8/6")
        mvg = MoveGenerator(BB)
        list = mvg._genValidatedMoves(Player.Blue,[DictMoveEntry.CONTINUE_GAME],BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
        mvg.prettyPrintMoves(list)
        self.assertEqual([MoveLib.move(x,y,3) for x,y,z in list],[])
    
    def test_genValidatedMoves_7(self):
        
        BB = GameState.createBitBoardFromFEN("6/8/1bb6/8/8/8/8/6")
        mvg = MoveGenerator(BB)
        list = mvg._genValidatedMoves(Player.Blue,[DictMoveEntry.CONTINUE_GAME],BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
        mvg.prettyPrintMoves(list)
        
        self.assertEqual([MoveLib.move(x,y,3) for x,y,z in list],["B3-A5","B3-C5", "B3-D4"])
        
    def test_genValidatedMoves_8(self):
        
        BB = GameState.createBitBoardFromFEN("6/8/1bb6/8/8/8/8/6")
        mvg = MoveGenerator(BB)
        list = mvg._genValidatedMoves(Player.Blue,[DictMoveEntry.CONTINUE_GAME],BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
        mvg.prettyPrintMoves(list)
        
        self.assertEqual([MoveLib.move(x,y,3) for x,y,z in list],["B3-A5","B3-C5","B3-D4"])
    
    @unittest.skip("not implemented yet")
    def test_getBitPositions_1(self):
        self.assertEqual(True,True)
        
    
    def test_getTarget_1(self):
        BB = GameState.createBitBoardFromFEN("b05/8/8/8/8/8/8/6")
        mvg = MoveGenerator(BB)
        bp = mvg._getAllPawns(Player.Blue,BB)
        move = mvg._getTarget(bp, BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP])
        print(MoveLib.move(*move,3))
        self.assertEqual("B1-B2",MoveLib.move(*move,3))
    
    def test_getTarget_2(self):
        BB = GameState.createBitBoardFromFEN("b05/8/8/8/8/8/8/6")
        mvg = MoveGenerator(BB)
        bp = mvg._getAllPawns(Player.Blue,BB)
        move = mvg._getTarget(bp, BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_LEFT])
        print(MoveLib.move(*move,3))
        self.assertEqual("B1-A2",MoveLib.move(*move,3))   
    
    def test_getTarget_3(self):
        BB = GameState.createBitBoardFromFEN("b05/8/8/8/8/8/8/6")
        mvg = MoveGenerator(BB)
        bp = mvg._getAllPawns(Player.Blue,BB)
        move = mvg._getTarget(bp, BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_RIGHT])
        print(MoveLib.move(*move,3))
        self.assertEqual("B1-C2",MoveLib.move(*move,3))   
    
    def test_getTarget_4(self):
        BB = GameState.createBitBoardFromFEN("b05/8/8/8/8/8/8/6")
        mvg = MoveGenerator(BB)
        bp = mvg._getAllPawns(Player.Blue,BB)
        move = mvg._getTarget(bp, BitMaskDict[DictMoveEntry.PAWN_TO_RIGHT])
        print(MoveLib.move(*move,3))
        self.assertEqual("B1-C1",MoveLib.move(*move,3))   
    
    def test_getTarget_5(self):
        BB = GameState.createBitBoardFromFEN("b05/8/8/8/8/8/8/6")
        mvg = MoveGenerator(BB)
        bp = mvg._getAllPawns(Player.Blue,BB)
        bp = mvg._filterPositions(Player.Blue,bp, BitMaskDict[DictMoveEntry.PAWN_TO_LEFT])
        print("filteredpos:", bp)
        move = mvg._getTarget(bp, BitMaskDict[DictMoveEntry.PAWN_TO_LEFT])
        print(MoveLib.move(*move,3))
        self.assertEqual("A0-A0",MoveLib.move(*move,3))
    
    def test_getTarget_6(self):
        """Edge Case Test - all not possible
            "6/bb7/8/8/8/8/1rbbb3bb1/6" """
        BB = GameState.createBitBoardFromFEN("6/bb7/8/8/8/8/8/6")
        mvg = MoveGenerator(BB)
        bp = mvg._getAllKnights(Player.Blue, BB)
        bp2 = mvg._filterPositions(Player.Blue, bp, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_LEFT])
        move = mvg._getTarget(bp2, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_LEFT])
        
        bp2 = mvg._filterPositions(Player.Blue, bp, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPLEFT])
        move2 = mvg._getTarget(bp2, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPLEFT])
        bp2 = mvg._filterPositions(Player.Blue, bp, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPRIGHT])
        move3 = mvg._getTarget(bp2, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPRIGHT])
        bp2 = mvg._filterPositions(Player.Blue, bp, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_RIGHT])
        move4 = mvg._getTarget(bp2, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_RIGHT])
        print(MoveLib.move(*move,3))
        print(MoveLib.move(*move2,3))
        print(MoveLib.move(*move3,3))
        print(MoveLib.move(*move4,3))
        
        self.assertEqual("A0-A0",MoveLib.move(*move,3))
        self.assertEqual("A0-A0",MoveLib.move(*move2,3))
        self.assertEqual("A2-B4",MoveLib.move(*move3,3))
        self.assertEqual("A2-C3",MoveLib.move(*move4,3))
        
    def test_getTarget_7(self):
        """Edge Case Test - all not possible
            "6/8/8/8/8/8/1rb6/6" """
        BB = GameState.createBitBoardFromFEN("6/8/8/8/8/8/1rb6/6")
        mvg = MoveGenerator(BB)
        bp = mvg._getAllKnights(Player.Blue, BB)
        bp2 = mvg._filterPositions(Player.Blue, bp, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_LEFT])
        move = mvg._getTarget(bp2, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_LEFT])
        
        bp2 = mvg._filterPositions(Player.Blue, bp, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPLEFT])
        move2 = mvg._getTarget(bp2, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPLEFT])
        bp2 = mvg._filterPositions(Player.Blue, bp, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPRIGHT])
        move3 = mvg._getTarget(bp2, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPRIGHT])
        bp2 = mvg._filterPositions(Player.Blue, bp, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_RIGHT])
        move4 = mvg._getTarget(bp2, BitMaskDict[DictMoveEntry.BLUE_KNIGHT_RIGHT])
        print(MoveLib.move(*move,3))
        print(MoveLib.move(*move2,3))
        print(MoveLib.move(*move3,3))
        print(MoveLib.move(*move4,3))
        
        self.assertEqual("A0-A0",MoveLib.move(*move,3))
        self.assertEqual("A0-A0",MoveLib.move(*move2,3))
        self.assertEqual("A0-A0",MoveLib.move(*move3,3))
        self.assertEqual("B7-D8",MoveLib.move(*move4,3))
    
    def test_getAllPawns_1(self):
        
        BB = GameState.createBitBoardFromFEN("b05/8/8/8/8/8/8/r05")
        print(BB)
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
        posRedPawns =mvg._getAllPawns(Player.Red,BB)
        posBluePawns = mvg._getAllPawns(Player.Blue,BB)
        
        self.assertEqual(np.log2(posRedPawns),np.log2(2**62))
        self.assertEqual(np.log2(posBluePawns),np.log2(2**6))
    
    def test_getAllPawns_2(self):
        
        BB = GameState.createBitBoardFromFEN("b0b0b0b0b0b0/8/8/8/8/8/8/r0r0r0r0r0r0")
        print(BB)
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
        posRedPawns =mvg._getAllPawns(Player.Red,BB)
        posBluePawns = mvg._getAllPawns(Player.Blue,BB)
        
        self.assertEqual(np.log2(posRedPawns),np.log2(2**62+2**61+2**60+2**59+2**58+2**57))
        self.assertEqual(np.log2(posBluePawns),np.log2(2**6+2**5+2**4+2**3+2**2+2**1))
    
    def test_getAllPawns_3(self):
        
        BB = GameState.createBitBoardFromFEN("6/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/6")
        print(BB)
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
        posRedPawns =mvg._getAllPawns(Player.Red,BB)
        posBluePawns = mvg._getAllPawns(Player.Blue,BB)
        
        self.assertEqual(np.log2(posRedPawns),np.log2(2**54+2**53+2**52+2**51+2**50+2**49))
        self.assertEqual(np.log2(posBluePawns),np.log2(2**14+2**13+2**12+2**11+2**10+2**9))
    
    def test_getAllPawns_4(self):
        
        BB = GameState.createBitBoardFromFEN("6/r0b0r0b0r0b0r01/8/8/8/8/1r0b0r0b0r0b0r0/6")
        print(BB)
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
        posRedPawns =mvg._getAllPawns(Player.Red,BB)
        posBluePawns = mvg._getAllPawns(Player.Blue,BB)
        
        self.assertEqual(np.log2(posRedPawns),np.log2(2**54+2**52+2**50+2**48+2**15+2**13+2**11+2**9))
        self.assertEqual(np.log2(posBluePawns),np.log2(2**53+2**51+2**49+2**14+2**12+2**10))
        
    def test_getAllPawns_5(self):
        
        BB = GameState.createBitBoardFromFEN("6/8/8/8/8/8/8/6")
        print(BB)
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
        posRedPawns =mvg._getAllPawns(Player.Red,BB)
        posBluePawns = mvg._getAllPawns(Player.Blue,BB)
        
        self.assertEqual((posRedPawns),0)
        self.assertEqual((posBluePawns),0)
        
    def test_getAllPawns_6(self):
        
        BB = GameState.createBitBoardFromFEN("bbbbbbbbbbbb/8/8/8/8/8/8/rrrrrrrrrrrr")
        print(BB)
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
        posRedPawns =mvg._getAllPawns(Player.Red,BB)
        posBluePawns = mvg._getAllPawns(Player.Blue,BB)
        
        self.assertEqual((posRedPawns),0)
        self.assertEqual((posBluePawns),0)
        
    def test_getAllPawns_7(self):
        
        BB = GameState.createBitBoardFromFEN("brbrbrbrbrbr/8/8/8/8/8/8/rbrbrbrbrbrb")
        print(BB)
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
        posRedPawns =mvg._getAllPawns(Player.Red,BB)
        posBluePawns = mvg._getAllPawns(Player.Blue,BB)
        
        self.assertEqual((posRedPawns),0)
        self.assertEqual((posBluePawns),0)
    
    def test_getAllPawns_8(self):
        
        BB = GameState.createBitBoardFromFEN("6/r07/8/8/8/8/b07/6")
        print(BB)
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
        posRedPawns =mvg._getAllPawns(Player.Red,BB)
        posBluePawns = mvg._getAllPawns(Player.Blue,BB)
        
        self.assertEqual(np.log2(posRedPawns),np.log2(2**15))
        self.assertEqual(np.log2(posBluePawns),np.log2(2**55))
    
    
    def test_getAllKnights_1(self):
        BB = GameState.createBitBoardFromFEN("bbbbbbbbbbbb/8/8/8/8/8/8/rrrrrrrrrrrr")
        print(BB)
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
        posRedKnights =mvg._getAllKnights(Player.Red,BB)
        posBlueKnights = mvg._getAllKnights(Player.Blue, BB)
        bits = np.uint64(2**6+2**5+2**4+2**3+2**2+2**1)
        self.assertEqual(np.log2(posRedKnights),np.log2(bits << np.uint64(7*8)))
        self.assertEqual(np.log2(posBlueKnights),np.log2(bits))
        
    def test_getAllKnights_2(self):
        BB = GameState.createBitBoardFromFEN("6/8/1rbrbrbrbrbrb1/8/8/1brbrbrbrbrbr1/8/6")
        print(BB)
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
        posRedKnights =mvg._getAllKnights(Player.Red,BB)
        posBlueKnights = mvg._getAllKnights(Player.Blue, BB)
        bits = np.uint64(2**6+2**5+2**4+2**3+2**2+2**1)
        self.assertEqual(np.log2(posRedKnights),np.log2(bits << np.uint64(5*8)))
        self.assertEqual(np.log2(posBlueKnights),np.log2(bits << np.uint64(2*8)))
        
    
    def test_filterPositions_1(self):
        BB = GameState.createBitBoardFromFEN("b05/8/8/8/8/8/8/r05")
        print(BB)
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
        redPawns = mvg._getAllPawns(Player.Red,BB)
        fredpos =mvg._filterPositions(Player.Red,redPawns,BitMaskDict[DictMoveEntry.PAWN_TO_LEFT])
        self.assertEqual(fredpos,0)
        fredpos =mvg._filterPositions(Player.Red,redPawns,BitMaskDict[DictMoveEntry.PAWN_TO_RIGHT])
        self.assertEqual(np.log2(fredpos), np.log2( 2**62))
        fredpos =mvg._filterPositions(Player.Red,redPawns,BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM])
        self.assertEqual(np.log2(fredpos), np.log2( 2**62))
        try:
            fredpos =mvg._filterPositions(Player.Blue,redPawns,BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM])
        except:
            self.assertEqual(True,True)
        try:
            fredpos =mvg._filterPositions(Player.Red,redPawns,BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM_LEFT])
        except:
            self.assertEqual(np.log2(fredpos),np.log2(2**62))
        fredpos =mvg._filterPositions(Player.Red,redPawns,BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM_RIGHT])
        self.assertEqual(fredpos, 2**62)
    
    def test_filterPositions_2(self):
        BB = GameState.createBitBoardFromFEN("b05/8/8/8/8/8/8/r05")
        print(BB)
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
        redPawns = mvg._getAllPawns(Player.Blue,BB)
        fredpos =mvg._filterPositions(Player.Blue,redPawns,BitMaskDict[DictMoveEntry.PAWN_TO_LEFT])
        self.assertEqual(fredpos,0)
        fredpos =mvg._filterPositions(Player.Blue,redPawns,BitMaskDict[DictMoveEntry.PAWN_TO_RIGHT])
        self.assertEqual(np.log2(fredpos), np.log2( 2**6))
        fredpos =mvg._filterPositions(Player.Blue,redPawns,BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP])
        self.assertEqual(np.log2(fredpos), np.log2( 2**6))
        try:
            fredpos =mvg._filterPositions(Player.Blue,redPawns,BitMaskDict[DictMoveEntry.RED_PAWN_TO_BOTTOM])
        except:
            self.assertEqual(True,True)
        try:
            fredpos =mvg._filterPositions(Player.Blue,redPawns,BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_LEFT])
        except:
            self.assertEqual(np.log2(fredpos),np.log2(2**6))
        fredpos =mvg._filterPositions(Player.Blue,redPawns,BitMaskDict[DictMoveEntry.BLUE_PAWN_TO_TOP_RIGHT])
        self.assertEqual(fredpos, 2**6)
    
    def test_filterPositions_3(self):
        BB = GameState.createBitBoardFromFEN("bb5/8/8/8/8/8/8/1r04")
        print(BB)
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
        knights = mvg._getAllKnights(Player.Blue, BB)
        fredpos =mvg._filterPositions(Player.Blue,knights,BitMaskDict[DictMoveEntry.BLUE_KNIGHT_LEFT])
        self.assertEqual(fredpos,0)
        fredpos =mvg._filterPositions(Player.Blue,knights,BitMaskDict[DictMoveEntry.BLUE_KNIGHT_RIGHT])
        self.assertEqual(np.log2(fredpos), np.log2( 2**6))
        fredpos =mvg._filterPositions(Player.Blue,knights,BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPLEFT])
        self.assertEqual(np.log2(fredpos), np.log2( 2**6))
        
        fredpos =mvg._filterPositions(Player.Blue,knights,BitMaskDict[DictMoveEntry.BLUE_KNIGHT_TO_TOPRIGHT])
        self.assertEqual(fredpos,2**6)
    
    def test_filterPositions_4(self):
        BB = GameState.createBitBoardFromFEN("bb5/8/8/8/8/8/8/1rr4")
        print(BB)
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
        knights = mvg._getAllKnights(Player.Red,BB)
        fredpos =mvg._filterPositions(Player.Red,knights,BitMaskDict[DictMoveEntry.RED_KNIGHT_LEFT])
        self.assertEqual(fredpos,2**61)
        fredpos =mvg._filterPositions(Player.Red,knights,BitMaskDict[DictMoveEntry.RED_KNIGHT_RIGHT])
        self.assertEqual(np.log2(fredpos), np.log2( 2**61))
        fredpos =mvg._filterPositions(Player.Red,knights,BitMaskDict[DictMoveEntry.RED_KNIGHT_TO_BOTLEFT])
        self.assertEqual(np.log2(fredpos), np.log2( 2**61))
        
        fredpos =mvg._filterPositions(Player.Red,knights,BitMaskDict[DictMoveEntry.RED_KNIGHT_TO_BOTRIGHT])
        self.assertEqual(fredpos,2**61)
    
    def test_checkTargetPos_11(self):
        """At this moment only for blue player implemented
            Test for Pawns"""
        
        BB = GameState.createBitBoardFromFEN("b05/8/8/8/8/8/8/6")    
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
       
        moves= mvg._genValidatedMoves(Player.Blue,[DictMoveEntry.CONTINUE_GAME],BB)
        
        print(moves)
        mvg.prettyPrintMoves(moves)
        
        #boardcommands = [mvg._checkTargetPos(Player.Blue, move) for move in moves]
        l = [ (MoveLib.move(start,target,3),bc)  for start,target,bc in moves]
        
        self.assertListEqual(l, [("B1-B2",[BoardCommand.Move_Blue_Pawn_no_Change,BoardCommand.Delete_Blue_Pawn_from_StartPos]),("B1-C1",[BoardCommand.Move_Blue_Pawn_no_Change,BoardCommand.Delete_Blue_Pawn_from_StartPos])])
    
    def test_checkTargetPos_12(self):
        """At this moment only for blue player implemented
            Test for Pawns"""
        
        BB = GameState.createBitBoardFromFEN("b05/1r0r07/8/8/8/8/8/6")    
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
       
        moves= mvg._genValidatedMoves(Player.Blue,[DictMoveEntry.CONTINUE_GAME],BB)
        print(moves)
        mvg.prettyPrintMoves(moves)
        #boardcommands = [mvg._checkTargetPos(Player.Blue, move) for move in moves]
        l = [ (MoveLib.move(start,target,3),bc)  for start,target,bc in moves]
        
        self.assertListEqual(l, [("B1-C2",[BoardCommand.Hit_Red_PawnOnTarget,BoardCommand.Move_Blue_Pawn_no_Change, BoardCommand.Delete_Blue_Pawn_from_StartPos]),("B1-C1",[BoardCommand.Move_Blue_Pawn_no_Change,BoardCommand.Delete_Blue_Pawn_from_StartPos])])
    
    def test_checkTargetPos_13(self):
        """At this moment only for blue player implemented
            Test for Pawns"""
        
        BB = GameState.createBitBoardFromFEN("b05/r0r0r07/8/8/8/8/8/6")    
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
       
        moves= mvg._genValidatedMoves(Player.Blue,[DictMoveEntry.CONTINUE_GAME],BB)
        print(moves)
        mvg.prettyPrintMoves(moves)
        #boardcommands = [mvg._checkTargetPos(Player.Blue, move) for move in moves]
        l = [ (MoveLib.move(start,target,3),bc)  for start,target,bc in moves]
        t = [("B1-C2",[BoardCommand.Hit_Red_PawnOnTarget,BoardCommand.Move_Blue_Pawn_no_Change,BoardCommand.Delete_Blue_Pawn_from_StartPos]),("B1-C1",[BoardCommand.Move_Blue_Pawn_no_Change,BoardCommand.Delete_Blue_Pawn_from_StartPos]),("B1-A2",[BoardCommand.Hit_Red_PawnOnTarget,BoardCommand.Move_Blue_Pawn_no_Change,BoardCommand.Delete_Blue_Pawn_from_StartPos])]
        
        l.sort(key=lambda x: x[0])
        t.sort(key=lambda x: x[0])
        
        self.assertListEqual(l,t)
    
    def test_checkTargetPos_14(self):
        """At this moment only for blue player implemented
            Test for Pawns"""
        
        BB = GameState.createBitBoardFromFEN("bb5/8/8/8/8/8/8/6")    
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
       
        moves= mvg._genValidatedMoves(Player.Blue,[DictMoveEntry.CONTINUE_GAME],BB)
        print(moves)
        mvg.prettyPrintMoves(moves)
        #boardcommands = [mvg._checkTargetPos(Player.Blue, move) for move in moves]
        l = [ (MoveLib.move(start,target,3),bc)  for start,target,bc in moves]
        t = [("B1-A3",[BoardCommand.Degrade_Blue_KnightOnTarget,BoardCommand.Delete_Blue_Knight_from_StartPos]),("B1-C3",[BoardCommand.Degrade_Blue_KnightOnTarget,BoardCommand.Delete_Blue_Knight_from_StartPos]),("B1-D2",[BoardCommand.Degrade_Blue_KnightOnTarget,BoardCommand.Delete_Blue_Knight_from_StartPos])]
        
        l.sort(key=lambda x: x[0])
        t.sort(key=lambda x: x[0])
        
        self.assertListEqual(l,t)
    
    def test_checkTargetPos_15(self):
        """At this moment only for blue player implemented
            Test for Pawns"""
        
        BB = GameState.createBitBoardFromFEN("bb5/8/r07/8/8/8/8/6")    
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
       
        moves= mvg._genValidatedMoves(Player.Blue,[DictMoveEntry.CONTINUE_GAME],BB)
        print(moves)
        mvg.prettyPrintMoves(moves)
        #boardcommands = [mvg._checkTargetPos(Player.Blue, move) for move in moves]
        l = [ (MoveLib.move(start,target,3),bc)  for start,target,bc in moves]
        t = [("B1-A3",[BoardCommand.Hit_Red_PawnOnTarget,BoardCommand.Degrade_Blue_KnightOnTarget,BoardCommand.Delete_Blue_Knight_from_StartPos]),("B1-C3",[BoardCommand.Degrade_Blue_KnightOnTarget,BoardCommand.Delete_Blue_Knight_from_StartPos]),("B1-D2",[BoardCommand.Degrade_Blue_KnightOnTarget,BoardCommand.Delete_Blue_Knight_from_StartPos])]
        
        l.sort(key=lambda x: x[0])
        t.sort(key=lambda x: x[0])
        
        self.assertListEqual(l,t)
    
    def test_checkTargetPos_16(self):
        """At this moment only for blue player implemented
            Test for Pawns"""
        
        BB = GameState.createBitBoardFromFEN("bb5/8/rr7/8/8/8/8/6")    
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
       
        moves= mvg._genValidatedMoves(Player.Blue,[DictMoveEntry.CONTINUE_GAME],BB)
        print(moves)
        mvg.prettyPrintMoves(moves)
        #boardcommands = [mvg._checkTargetPos(Player.Blue, move) for move in moves]
        l = [ (MoveLib.move(start,target,3),bc)  for start,target,bc in moves]
        t = [("B1-A3",[BoardCommand.Hit_Red_KnightOnTarget,BoardCommand.Move_Blue_Knight_no_Change,BoardCommand.Delete_Blue_Knight_from_StartPos]),("B1-C3",[BoardCommand.Degrade_Blue_KnightOnTarget,BoardCommand.Delete_Blue_Knight_from_StartPos]),("B1-D2",[BoardCommand.Degrade_Blue_KnightOnTarget,BoardCommand.Delete_Blue_Knight_from_StartPos])]
        
        l.sort(key=lambda x: x[0])
        t.sort(key=lambda x: x[0])
        print("L:", l)
        print("T",t)
        self.assertListEqual(l,t)
    
    def test_checkTargetPos_17(self):
        """At this moment only for blue player implemented
            Test for Pawns"""
        
        BB = GameState.createBitBoardFromFEN("bb5/8/rb7/8/8/8/8/6")    
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
       
        moves= mvg._genValidatedMoves(Player.Blue,[DictMoveEntry.CONTINUE_GAME],BB)
        print(moves)
        mvg.prettyPrintMoves(moves)
        #boardcommands = [mvg._checkTargetPos(Player.Blue, move) for move in moves]
        l = [ (MoveLib.move(start,target,3),bc)  for start,target,bc in moves]
        t = [("B1-C3",[BoardCommand.Degrade_Blue_KnightOnTarget,BoardCommand.Delete_Blue_Knight_from_StartPos]),("B1-D2",[BoardCommand.Degrade_Blue_KnightOnTarget,BoardCommand.Delete_Blue_Knight_from_StartPos]),
             ("A3-B5",[BoardCommand.Degrade_Blue_KnightOnTarget,BoardCommand.Delete_Blue_Knight_from_StartPos]),("A3-C4",[BoardCommand.Degrade_Blue_KnightOnTarget,BoardCommand.Delete_Blue_Knight_from_StartPos])]
        
        l.sort(key=lambda x: x[0])
        t.sort(key=lambda x: x[0])
        
        self.assertListEqual(l,t)
    
    def test_checkTargetPos_18(self):
        """At this moment only for blue player implemented
            Test for Pawns"""
        
        BB = GameState.createBitBoardFromFEN("b0b04/8/8/8/8/8/8/6")    
        mvg = MoveGenerator(BB)
        mvg.prettyPrintBoard(BB,[DictMoveEntry.CONTINUE_GAME])
       
        moves= mvg._genValidatedMoves(Player.Blue,[DictMoveEntry.CONTINUE_GAME],BB)
        print(moves)
        mvg.prettyPrintMoves(moves)
        #boardcommands = [mvg._checkTargetPos(Player.Blue, move) for move in moves]
        l = [ (MoveLib.move(start,target,3),bc)  for start,target,bc in moves]
        t = [("B1-B2",[BoardCommand.Move_Blue_Pawn_no_Change,BoardCommand.Delete_Blue_Pawn_from_StartPos]),("B1-C1",[BoardCommand.Upgrade_Blue_KnightOnTarget, BoardCommand.Delete_Blue_Pawn_from_StartPos]),
             ("C1-B1",[BoardCommand.Upgrade_Blue_KnightOnTarget,BoardCommand.Delete_Blue_Pawn_from_StartPos]), ("C1-C2",[BoardCommand.Move_Blue_Pawn_no_Change,BoardCommand.Delete_Blue_Pawn_from_StartPos]),("C1-D1",[BoardCommand.Move_Blue_Pawn_no_Change,BoardCommand.Delete_Blue_Pawn_from_StartPos])]
        
        l.sort(key=lambda x: x[0])
        t.sort(key=lambda x: x[0])
        
        self.assertListEqual(l,t)  
    
    @unittest.skip("not implemented yet")
    def test_validateMoves_1(self):
        self.assertEqual(True,True)
    
    @unittest.skip("not implemented yet")
    def test_gameover_1(self):
        self.assertEqual(True,True)
        
    def test_Cannot_Move_GameOver(self):
        fen = "6/8/4b03/3b0r0b02/8/8/8/6"
        bb = GameState.createBitBoardFromFEN(fen)
        mvg = MoveGenerator()
        gameOver =[DictMoveEntry.CONTINUE_GAME]
        moves = mvg.genMoves(Player.Red,gameOver,bb)
        self.assertEqual(len(moves), 0)
        self.assertEqual(gameOver[0], DictMoveEntry.GAME_OVER_BLUE_WINS)
        
    def test_TOTAL_ISIS_TEST1(self):
        fdscr = open('test_data.json')
        moves = json.load(fdscr)
        
        testcases = [(move['board'],move['moves']) for move in moves]
        
        for case in testcases:
            fen,player = np.array(case[0].split(" "))
            movelist = np.array([move.replace(" ","") for move in case[1].split(",")])
            print(fen)
            
            print(movelist)
            #movelist =list(map(lambda x: (x[0],x[1]) ,[move.split("-") for move in movelist]))
            bb = GameState.createBitBoardFromFEN(fen)
            mvg = MoveGenerator()
            mvg.prettyPrintBoard(bb,[DictMoveEntry.CONTINUE_GAME])
            genmoves = np.array(list(map(lambda x: MoveLib.move(x[0],x[1],3) ,mvg.genMoves(Player.Blue if player=="b" else Player.Red,[DictMoveEntry.CONTINUE_GAME], bb ))))
            movelist.sort()
            genmoves.sort()
            print("targelist:\n",movelist)
            print("genlist:\n",genmoves)
           
            genmoves = set(genmoves)
            movelist = set(movelist)
            
            
            self.assertEqual(genmoves,movelist)
    
    def test_GameTest_move_exec1(self):
        fen = "b05/8/8/8/8/8/8/r05"
        bb = GameState.createBitBoardFromFEN(fen)
        mv = MoveGenerator(bb)
        gameover = [DictMoveEntry.CONTINUE_GAME]
        RorB = True
        while(gameover[0] is DictMoveEntry.CONTINUE_GAME):
            
            player = Player.Red if RorB else Player.Blue
            moves = mv.genMoves(player,gameover,bb)
            mv.prettyPrintBoard(bb,gameover)
            print("Players turn: ", player)
            mv.prettyPrintMoves(moves)
            a,b = 0, len(moves)
            move = moves[random.randint(a,b-1)]
            bb = mv.execSingleMove(move,player, gameover,bb)
            #mv.prettyPrintBoard(bb,gameover)
            RorB = not RorB
        print("end status:\n")
        mv.prettyPrintBoard(bb,gameover)
        self.assertIsNot(gameover[0],DictMoveEntry.CONTINUE_GAME )
    
    def test_GameTest_move_exec2(self):
        fen = "b0br4/rrbrrr5/8/8/8/8/8/6"
        bb = GameState.createBitBoardFromFEN(fen)
        mv = MoveGenerator(bb)
        gameover = [DictMoveEntry.CONTINUE_GAME]
        RorB = False
        while(gameover[0] is DictMoveEntry.CONTINUE_GAME):
            
            player = Player.Red if RorB else Player.Blue
            moves = mv.genMoves(player,gameover,bb)
            mv.prettyPrintBoard(bb,gameover)
            print("Players turn: ", player)
            mv.prettyPrintMoves(moves)
            a,b = 0, len(moves)
            move = moves[random.randint(a,b-1)]
            bb = mv.execSingleMove(move,player, gameover,bb)
            #mv.prettyPrintBoard(bb,gameover)
            RorB = not RorB
        print("end status:\n")
        mv.prettyPrintBoard(bb,gameover)
        self.assertIsNot(gameover[0],DictMoveEntry.CONTINUE_GAME )
    
    def test_GameTest_move_exec3(self):
        def figureCount(bb: np.ndarray[np.uint64]):
                val1 = bin(bb[GameState._ZARR_INDEX_R_PAWNS])[2:].count("1")+ bin(bb[GameState._ZARR_INDEX_R_KNIGHTS])[2:].count("1")
                val2 = bin(bb[GameState._ZARR_INDEX_B_PAWNS])[2:].count("1")+ bin(bb[GameState._ZARR_INDEX_B_KNIGHTS])[2:].count("1")
                return val1,val2
        def checkCount(before,after):
            return all(list(map(lambda t: t[0] >= t[1], zip(before,after))))
        
        fen = "bb5/8/rr7/8/8/8/8/6"
        bb = GameState.createBitBoardFromFEN(fen)
        mv = MoveGenerator(bb)
        gameover = [DictMoveEntry.CONTINUE_GAME]
        RorB = False
        before = figureCount(bb)
        while(gameover[0] is DictMoveEntry.CONTINUE_GAME):
            
            player = Player.Red if RorB else Player.Blue
            moves = mv.genMoves(player,gameover,bb)
            #print(moves)
            mv.prettyPrintBoard(bb,gameover)
            print("Players turn: ", player)
            #mv.prettyPrintMoves(moves)
            #a,b = 0, len(moves)
            #move = moves[random.randint(a,b-1)]
            move = list(filter(lambda x: MoveLib.move(x[0],x[1],3) == "B1-A3" , moves))
            print(move)
            mv.prettyPrintMoves(move)
            bb = mv.execSingleMove(move[0],player, gameover,bb)
            print("Figure count r and b before move exec:", before)
            after = figureCount(bb)
            print("Figure count r and b after move exec:", after )
            correctness = checkCount(before,after)
            self.assertEqual(True, correctness)
            RorB = not RorB
            gameover=[DictMoveEntry.GAME_OVER_BLUE_WINS]
        print("end status:\n")
        mv.prettyPrintBoard(bb,gameover)
        self.assertIsNot(gameover[0],DictMoveEntry.CONTINUE_GAME )
    
    def test_GameTest_move_exec3(self):
        def figureCount(bb: np.ndarray[np.uint64]):
                val1 = bin(bb[GameState._ZARR_INDEX_R_PAWNS])[2:].count("1")+ bin(bb[GameState._ZARR_INDEX_R_KNIGHTS])[2:].count("1")
                val2 = bin(bb[GameState._ZARR_INDEX_B_PAWNS])[2:].count("1")+ bin(bb[GameState._ZARR_INDEX_B_KNIGHTS])[2:].count("1")
                return val1,val2
        def checkCount(before,after):
            return all(list(map(lambda t: t[0] >= t[1], zip(before,after))))
        
        fen = "bb5/8/br7/8/8/8/8/6"
        bb = GameState.createBitBoardFromFEN(fen)
        mv = MoveGenerator(bb)
        gameover = [DictMoveEntry.CONTINUE_GAME]
        RorB = False
        before = figureCount(bb)
        while(gameover[0] is DictMoveEntry.CONTINUE_GAME):
            
            player = Player.Red if RorB else Player.Blue
            moves = mv.genMoves(player,gameover,bb)
            #print(moves)
            mv.prettyPrintBoard(bb,gameover)
            print("Players turn: ", player)
            #mv.prettyPrintMoves(moves)
            #a,b = 0, len(moves)
            #move = moves[random.randint(a,b-1)]
            move = list(filter(lambda x: MoveLib.move(x[0],x[1],3) == "B1-A3" , moves))
            print(move)
            mv.prettyPrintMoves(move)
            bb = mv.execSingleMove(move[0],player, gameover,bb)
            print("Figure count r and b before move exec:", before)
            after = figureCount(bb)
            print("Figure count r and b after move exec:", after )
            correctness = checkCount(before,after)
            self.assertEqual(True, correctness)
            RorB = not RorB
            gameover=[DictMoveEntry.GAME_OVER_BLUE_WINS]
        print("end status:\n")
        mv.prettyPrintBoard(bb,gameover)
        self.assertIsNot(gameover[0],DictMoveEntry.CONTINUE_GAME )
    
    def test_GameTest_move_exec3(self):
        def figureCount(bb: np.ndarray[np.uint64]):
                val1 = bin(bb[GameState._ZARR_INDEX_R_PAWNS])[2:].count("1")+ bin(bb[GameState._ZARR_INDEX_R_KNIGHTS])[2:].count("1")
                val2 = bin(bb[GameState._ZARR_INDEX_B_PAWNS])[2:].count("1")+ bin(bb[GameState._ZARR_INDEX_B_KNIGHTS])[2:].count("1")
                return val1,val2
        def checkCount(before,after):
            return all(list(map(lambda t: t[0] >= t[1], zip(before,after))))
        
        fen = "bb5/8/r07/8/8/8/8/6"
        bb = GameState.createBitBoardFromFEN(fen)
        mv = MoveGenerator(bb)
        gameover = [DictMoveEntry.CONTINUE_GAME]
        RorB = False
        before = figureCount(bb)
        while(gameover[0] is DictMoveEntry.CONTINUE_GAME):
            
            player = Player.Red if RorB else Player.Blue
            moves = mv.genMoves(player,gameover,bb)
            #print(moves)
            mv.prettyPrintBoard(bb,gameover)
            print("Players turn: ", player)
            #mv.prettyPrintMoves(moves)
            #a,b = 0, len(moves)
            #move = moves[random.randint(a,b-1)]
            move = list(filter(lambda x: MoveLib.move(x[0],x[1],3) == "B1-A3" , moves))
            print(move)
            mv.prettyPrintMoves(move)
            bb = mv.execSingleMove(move[0],player, gameover,bb)
            print("Figure count r and b before move exec:", before)
            after = figureCount(bb)
            print("Figure count r and b after move exec:", after )
            correctness = checkCount(before,after)
            self.assertEqual(True, correctness)
            RorB = not RorB
            gameover=[DictMoveEntry.GAME_OVER_BLUE_WINS]
        print("end status:\n")
        mv.prettyPrintBoard(bb,gameover)
        self.assertIsNot(gameover[0],DictMoveEntry.CONTINUE_GAME )
        
        
    def test_GameTest_move_exec2(self):
        def figureCount(bb: np.ndarray[np.uint64]):
                val1 = bin(bb[GameState._ZARR_INDEX_R_PAWNS])[2:].count("1")+ bin(bb[GameState._ZARR_INDEX_R_KNIGHTS])[2:].count("1")
                val2 = bin(bb[GameState._ZARR_INDEX_B_PAWNS])[2:].count("1")+ bin(bb[GameState._ZARR_INDEX_B_KNIGHTS])[2:].count("1")
                return val1,val2
        def checkCount(before,after):
            return all(list(map(lambda t: t[0] >= t[1], zip(before,after))))
        
        fen = "b0b0b0b0b0b0/8/8/8/8/8/8/r0r0r0r0r0r0"
        bb = GameState.createBitBoardFromFEN(fen)
        mv = MoveGenerator(bb)
        gameover = [DictMoveEntry.CONTINUE_GAME]
        RorB = True
        before = figureCount(bb)
        while(gameover[0] is DictMoveEntry.CONTINUE_GAME):
            
            player = Player.Red if RorB else Player.Blue
            moves = mv.genMoves(player,gameover,bb)
            mv.prettyPrintBoard(bb,gameover)
            print("Players turn: ", player)
            
            a,b = 0, len(moves)
            move = moves[random.randint(a,b-1)]
            mv.prettyPrintMoves([move])
            bb = mv.execSingleMove(move,player, gameover,bb)
            print("Figure count r and b before move exec:", before)
            after = figureCount(bb)
            print("Figure count r and b after move exec:", after )
            correctness = checkCount(before,after)
            self.assertEqual(True, correctness)
            before = after
            #mv.prettyPrintBoard(bb,gameover)
            RorB = not RorB
        print("end status:\n")
        mv.prettyPrintBoard(bb,gameover)
        self.assertIsNot(gameover[0],DictMoveEntry.CONTINUE_GAME )
        #self.assertEqual(True,False)
            
    def test_TOTAL_ISIS_gameplay(self):
        def figureCount(bb: np.ndarray[np.uint64]):
                val1 = bin(bb[GameState._ZARR_INDEX_R_PAWNS])[2:].count("1")+ bin(bb[GameState._ZARR_INDEX_R_KNIGHTS])[2:].count("1")
                val2 = bin(bb[GameState._ZARR_INDEX_B_PAWNS])[2:].count("1")+ bin(bb[GameState._ZARR_INDEX_B_KNIGHTS])[2:].count("1")
                return val1,val2
        def checkCount(before,after):
            return all(list(map(lambda t: t[0] >= t[1], zip(before,after))))
        
        fdscr = open('test_data.json')
        moves = json.load(fdscr)
        
        testcases = [(move['board'],move['moves']) for move in moves]
        
        for case in testcases:
            fen,player = np.array(case[0].split(" "))
            #movelist = np.array([move.replace(" ","") for move in case[1].split(",")])
            print("FEN:", fen)
           
            bb = GameState.createBitBoardFromFEN(fen)
            mv = MoveGenerator(bb)
            gameover = [DictMoveEntry.CONTINUE_GAME]
            RedsTurn = True if player =="r" else False
            before = figureCount(bb)
            while(gameover[0] is DictMoveEntry.CONTINUE_GAME):

                player = Player.Red if RedsTurn else Player.Blue
                moves = mv.genMoves(player,gameover,bb)
                
                print("Players turn: ", player)

                a,b = 0, len(moves)
                move = moves[random.randint(a,b-1)]
                mv.prettyPrintMoves([move])
                bb = mv.execSingleMove(move,player, gameover,bb)
                mv.prettyPrintBoard(bb,gameover)
                print("Figure count r and b before move exec:", before)
                after = figureCount(bb)
                print("Figure count r and b after move exec:", after )
                correctness = checkCount(before,after)
                self.assertEqual(True, correctness)
                before = after
                #mv.prettyPrintBoard(bb,gameover)
                RedsTurn = not RedsTurn
            print("end status:\n")
            mv.prettyPrintBoard(bb,gameover)
            self.assertIsNot(gameover[0],DictMoveEntry.CONTINUE_GAME )
            
    def test_TOTAL_ISIS_gameplay2_unmakeMove(self):
        def figureCount(bb: np.ndarray[np.uint64]):
                val1 = bin(bb[GameState._ZARR_INDEX_R_PAWNS])[2:].count("1")+ bin(bb[GameState._ZARR_INDEX_R_KNIGHTS])[2:].count("1")
                val2 = bin(bb[GameState._ZARR_INDEX_B_PAWNS])[2:].count("1")+ bin(bb[GameState._ZARR_INDEX_B_KNIGHTS])[2:].count("1")
                return val1,val2
        def checkCount(before,after):
            return all(list(map(lambda t: t[0] >= t[1], zip(before,after))))
        
        fdscr = open('test_data.json')
        moves = json.load(fdscr)
        
        testcases = [(move['board'],move['moves']) for move in moves]
        
        for case in testcases:
            fen,player = np.array(case[0].split(" "))
            #movelist = np.array([move.replace(" ","") for move in case[1].split(",")])
            print("FEN:", fen)
           
            bb = GameState.createBitBoardFromFEN(fen)
            initalBoard = bb.copy()
            mv = MoveGenerator(bb,True)
            gameover = [DictMoveEntry.CONTINUE_GAME]
            RedsTurn = True if player =="r" else False
            before = figureCount(bb)
            logstack = deque([])
            logstack.append([initalBoard,list([()])])
            while(gameover[0] is DictMoveEntry.CONTINUE_GAME):

                player = Player.Red if RedsTurn else Player.Blue
                moves = mv.genMoves(player,gameover,bb)
                
                print("Players turn: ", player)

                a,b = 0, len(moves)
                move = moves[random.randint(a,b-1)]
                mv.prettyPrintMoves([move])
                #bb = mv.execSingleMove(move,player, gameover,bb)
                mv.execSingleMove(move,player, gameover,bb)
                logstack.append([bb.copy(), list([move])])
                mv.prettyPrintBoard(bb,gameover)
                print("Figure count r and b before move exec:", before)
                after = figureCount(bb)
                print("Figure count r and b after move exec:", after )
                correctness = checkCount(before,after)
                self.assertEqual(True, correctness)
                before = after
                #mv.prettyPrintBoard(bb,gameover)
                RedsTurn = not RedsTurn
            print("end status:\n")
            mv.prettyPrintBoard(bb,gameover)
            self.assertIsNot(gameover[0],DictMoveEntry.CONTINUE_GAME )

            sizeOfStack = len(mv._stack)
            
            
            for x in range(sizeOfStack):
                correctRes = logstack.pop()
                print("stack item : ", correctRes)
                print("stack[0]:", correctRes[0])
                cplist = list(zip(bb, correctRes[0]))
                print("reconstr. Board and correct Board as (a,b) per item:\n",cplist )
                print("comparing (recB,corrB):\n",list(map(lambda x: x[0] == x[1], cplist)))
                print("reco Board visual\n")
                mv.prettyPrintBoard(bb,[DictMoveEntry.CONTINUE_GAME])
                print("correct Board visual\n")
                mv.prettyPrintBoard(correctRes[0],[DictMoveEntry.CONTINUE_GAME])
                mv.prettyPrintMoves(list((correctRes[1]))) if x != sizeOfStack-1 else print("no moves left")
                
                self.assertEqual((bb==correctRes[0]).all(),True)
                mv.takeback(bb)
                
            
             
        #self.assertEqual(True,False)
            
        
            
            
        
    