import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from src.mcts_uct import MCTS as mcts
from src.mcts_uct import NodeData
from src.model import Player, DictMoveEntry
from src.gamestate import *
from treelib import Node,Tree
import numpy as np

class MCTS(unittest.TestCase):
    
    def test_mcts_init1(self):
        fen = "b05/8/8/8/8/8/8/r05"
        bb = GameState.createBitBoardFromFEN(fen)
        monteC = mcts(bb,Player.Blue)
        self.assertEqual(monteC.player1, Player.Blue)
        self.assertEqual(monteC.player2, Player.Red)
        
        self.assertIsInstance(monteC.tree, Tree)
        self.assertEqual(monteC.root, 1)
        self.assertEqual(monteC.currentNode, 1)
        self.assertEqual(monteC.C, np.sqrt(2))
        self.assertEqual(np.allclose(monteC.tree.get_node(1).data.board,bb),True)
        self.assertEqual(monteC.tree.get_node(1).data.score,0)
        self.assertEqual(monteC.tree.get_node(1).data.simulations,0)
        self.assertEqual(np.allclose(monteC.tree.get_node(1).data.move,(0,0)),True)
        self.assertEqual(monteC.tree.get_node(1).data.gameOver[0],DictMoveEntry.CONTINUE_GAME)
    
    def test_1chooseNode1(self):
        fen = "b05/8/8/8/8/8/8/r05"
        bb = GameState.createBitBoardFromFEN(fen)
        monteC = mcts(bb,Player.Blue)
        root = monteC.tree.get_node(1)
        root.data.score = 10
        root.data.simulations = 3
        print("root:", root, " data:", root.data.score)
        monteC.tree.create_node(tag="C1",identifier="c1",parent=monteC.tree.root,data= NodeData(bb,[DictMoveEntry.CONTINUE_GAME]))
        c1 = monteC.tree.get_node("c1")
        c1.data.score = 2
        c1.data.simulations = 1
        
        monteC.tree.create_node(tag="C2",identifier="c2",parent=monteC.tree.root,data= NodeData(bb,[DictMoveEntry.CONTINUE_GAME]))
        c2 = monteC.tree.get_node("c2")
        c2.data.score = 8
        c2.data.simulations = 1
        self.assertEqual(root.is_leaf(), False)
        self.assertEqual(monteC.tree.parent(c2.identifier),root)
        self.assertEqual(monteC.tree.parent(c1.identifier),root)
        self.assertEqual(monteC.tree.children(root.identifier)[0].identifier, "c1")
        self.assertEqual(monteC.tree.children(root.identifier)[1].identifier, "c2")
        choosedNode = monteC._1chooseNode(root)
        self.assertEqual(choosedNode.identifier, c2.identifier)
    
    def test_1chooseNode2(self):
        fen = "b05/8/8/8/8/8/8/r05"
        bb = GameState.createBitBoardFromFEN(fen)
        monteC = mcts(bb,Player.Blue)
        root = monteC.tree.get_node(1)
        root.data.score = 10
        root.data.simulations = 3
        print("root:", root, " data:", root.data.score)
        monteC.tree.create_node(tag="C1",identifier="c1",parent=monteC.tree.root,data= NodeData(bb,[DictMoveEntry.CONTINUE_GAME]))
        c1 = monteC.tree.get_node("c1")
        c1.data.score = 8
        c1.data.simulations = 1
        
        monteC.tree.create_node(tag="C2",identifier="c2",parent=monteC.tree.root,data= NodeData(bb,[DictMoveEntry.CONTINUE_GAME]))
        c2 = monteC.tree.get_node("c2")
        c2.data.score = 2
        c2.data.simulations = 1
        self.assertEqual(root.is_leaf(), False)
        self.assertEqual(monteC.tree.parent(c2.identifier),root)
        self.assertEqual(monteC.tree.parent(c1.identifier),root)
        self.assertEqual(monteC.tree.children(root.identifier)[0].identifier, "c1")
        self.assertEqual(monteC.tree.children(root.identifier)[1].identifier, "c2")
        choosedNode = monteC._1chooseNode(root)
        self.assertEqual(choosedNode.identifier, c1.identifier)    
    
    def test_1chooseNode3(self):
        fen = "b05/8/8/8/8/8/8/r05"
        bb = GameState.createBitBoardFromFEN(fen)
        monteC = mcts(bb,Player.Blue)
        root = monteC.tree.get_node(1)
        root.data.score = 10
        root.data.simulations = 3
        print("root:", root, " data:", root.data.score)
        monteC.tree.create_node(tag="C1",identifier="c1",parent=monteC.tree.root,data= NodeData(bb,[DictMoveEntry.CONTINUE_GAME]))
        c1 = monteC.tree.get_node("c1")
        c1.data.score = 2
        c1.data.simulations = 1
        
        monteC.tree.create_node(tag="C2",identifier="c2",parent=monteC.tree.root,data= NodeData(bb,[DictMoveEntry.CONTINUE_GAME]))
        c2 = monteC.tree.get_node("c2")
        c2.data.score = 2
        c2.data.simulations = 1
        self.assertEqual(root.is_leaf(), False)
        self.assertEqual(monteC.tree.parent(c2.identifier),root)
        self.assertEqual(monteC.tree.parent(c1.identifier),root)
        self.assertEqual(monteC.tree.children(root.identifier)[0].identifier, "c1")
        self.assertEqual(monteC.tree.children(root.identifier)[1].identifier, "c2")
        choosedNode = monteC._1chooseNode(root)
        self.assertEqual(choosedNode.identifier, c1.identifier)       
        
    def test_computeUCTValue1(self):
        fen = "b05/8/8/8/8/8/8/r05"
        bb = GameState.createBitBoardFromFEN(fen)
        monteC = mcts(bb,Player.Blue)
        root = monteC.tree.get_node(1)
        root.data.score = 10
        root.data.simulations = 3
        print("root:", root, " data:", root.data.score)
        monteC.tree.create_node(tag="C1",identifier="c1",parent=monteC.tree.root,data= NodeData(bb,[DictMoveEntry.CONTINUE_GAME]))
        c1 = monteC.tree.get_node("c1")
        c1.data.score = 2
        c1.data.simulations = 1
        
        monteC.tree.create_node(tag="C2",identifier="c2",parent=monteC.tree.root,data= NodeData(bb,[DictMoveEntry.CONTINUE_GAME]))
        c2 = monteC.tree.get_node("c2")
        c2.data.score = 8
        c2.data.simulations = 1

        score1  = monteC._computeUCTValue(c1)
        self.assertEqual(round(score1,1),round(2+np.sqrt(2)*np.sqrt(np.log(3)/1),1))
        score2  = monteC._computeUCTValue(c2)
        self.assertEqual(round(score2,1),round(8+np.sqrt(2)*np.sqrt(np.log(3)/1),1))
        
        
    
    def test_2generateNodes1(self):
        pass
    
    def test_3runSimulation1(self):
        pass
    
    def test_4backPropagation1(self):
        pass
    
    def test_runMCTS_Worker1(self):
        pass