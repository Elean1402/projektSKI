import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from src.mcts_uct import MCTS as mcts
from src.mcts_uct import NodeData
from src.model import Player, DictMoveEntry
from src.gamestate import *
from treelib import Node,Tree
import numpy as np
import sys
from io import StringIO
from graphviz import Source
from pygame import time as pgtime

class MCTS(unittest.TestCase):
    
    def test_mcts_init1(self):
        """initial test: creating mcts class
        """
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
        """on this setting node c2 should be selected
        """
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
        """on this setting node c1 should be selected
        """
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
        """ on this setting node c1 should be selected
        """
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
    
    def test_1chooseNode4(self):
        """ chooseNode should set best move
        """
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
        self.assertEqual(np.allclose(monteC.bestMove, choosedNode.data.move), True)       
    
    def test_1chooseNode5(self):
        """input node is a leaf
        """
        fen = "b05/8/8/8/8/8/8/r05"
        bb = GameState.createBitBoardFromFEN(fen)
        monteC = mcts(bb,Player.Blue)
        root = monteC.tree.get_node(1)
        root.data.score = 10
        root.data.simulations = 3
        choosedNode = monteC._1chooseNode(root)
        
        self.assertEqual(choosedNode.identifier, root.identifier)
        self.assertEqual(np.allclose(monteC.bestMove, choosedNode.data.move), True)  
    
        
    def test_computeUCTValue1(self):
        """ Test of computing uct values
        """
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
        """ input is a leaf which cant be expanded"""
        """ 
        """
        fen = "6/8/8/8/8/8/8/rb5"
        bb = GameState.createBitBoardFromFEN(fen)
        monteC = mcts(bb,Player.Blue)
        root = monteC.tree.get_node(1)
        root.data.score = 10
        root.data.simulations = 3

        self.assertEqual(root.data.gameOver[0], DictMoveEntry.GAME_OVER_BLUE_WINS)

    def test_2generateNodes2(self):
        """ input is a leaf which cant be expanded"""
        """ 
        """
        fen = "6/8/8/8/8/8/7b0/rr5"
        bb = GameState.createBitBoardFromFEN(fen)
        monteC = mcts(bb,Player.Blue)
        root = monteC.tree.get_node(1)
        self.assertEqual(root.data.gameOver[0], DictMoveEntry.CONTINUE_GAME)
        
        fen2 = "6/8/8/8/8/8/8/rb5"
        bb2 = GameState.createBitBoardFromFEN(fen2)
        
        c1 = monteC.tree.create_node("C1","c1",root,NodeData(bb2,[DictMoveEntry.CONTINUE_GAME]))
        
        self.assertEqual(monteC.tree.parent(c1.identifier).identifier, root.identifier)
        
        nodes = monteC._2generateNodes(c1.identifier)
        
        self.assertEqual(nodes, [])
        self.assertEqual(c1.data.gameOver[0], DictMoveEntry.GAME_OVER_BLUE_WINS)
    
    def test_2generateNodes3(self):
        """ input is a leaf which cant be expanded"""
        """ 
        """
        fen = "b05/8/8/8/8/8/7r0/rr5"
        bb = GameState.createBitBoardFromFEN(fen)
        monteC = mcts(bb,Player.Blue)
        root = monteC.tree.get_node(1)
        self.assertEqual(root.data.gameOver[0], DictMoveEntry.CONTINUE_GAME)
        
        fen2 = "6/8/8/8/8/8/8/rb5"
        bb2 = GameState.createBitBoardFromFEN(fen2)
        
        c1 = monteC.tree.create_node("C1","c1",root,NodeData(bb2,[DictMoveEntry.GAME_OVER_BLUE_WINS]))
        
        self.assertEqual(monteC.tree.parent(c1.identifier).identifier, root.identifier)
        
        nodes = monteC._2generateNodes(c1.identifier)
        
        self.assertEqual(nodes, [])
        self.assertEqual(c1.data.gameOver[0], DictMoveEntry.GAME_OVER_BLUE_WINS)
           
    
    def test_2generateNodes4(self):
        """ checking correct expansion"""
        fen = "b05/8/8/8/8/8/8/rr5"
        bb = GameState.createBitBoardFromFEN(fen)
        monteC = mcts(bb,Player.Blue)
        root = monteC.tree.get_node(1)
        self.assertEqual(root.identifier, 1)
        nodesBlue = monteC._2generateNodes(root.identifier)
        self.assertEqual(len(nodesBlue), 2)
        nodesRed = monteC._2generateNodes(nodesBlue[0].identifier)
        self.assertEqual(len(nodesRed), 3)
        self.assertEqual(monteC.tree.depth(),2)
        #monteC.printTree(monteC.tree)
        
    def test_3runSimulation1(self):
        """ checking correct expansion"""
        fen = "b05/8/8/8/8/8/8/r05"
        bb = GameState.createBitBoardFromFEN(fen)
        monteC = mcts(bb,Player.Blue)
        root = monteC.tree.get_node(1)
        clock = pgtime.Clock()
        clock.tick()
        score = monteC._3runSimulation(root.identifier)
        clock.tick()
        print("simulation time: ",clock.get_time()/1000, "s")
        #self.assertEqual(score,-1)
        
    
    def test_4backPropagation1(self):
        """ test if values are correctly propagated
            """
        
        fen = "b05/8/8/8/8/8/8/r05"
        bb = GameState.createBitBoardFromFEN(fen)
        monteC = mcts(bb,Player.Blue)
        root = monteC.tree.get_node(1)
        
        blueNodes = monteC._2generateNodes(root.identifier)
        self.assertEqual(len(blueNodes)!= 0, True)
        redNodes = monteC._2generateNodes(blueNodes[0].identifier)
        self.assertEqual(len(redNodes)!= 0, True)
        score  = monteC._3runSimulation(redNodes[0].identifier)
        root2 = monteC._4backPropagation(redNodes[0],score)
        
        self.assertEqual(monteC.tree.get_node(1).identifier, root2.identifier)
        self.assertEqual(redNodes[0].data.score, score)
        self.assertEqual(redNodes[0].data.simulations, 1)
        
        parentRed = monteC.tree.parent(redNodes[0].identifier)
        self.assertEqual(parentRed.data.score, score)
        self.assertEqual(parentRed.data.simulations, 1)
        grandPRed = monteC.tree.parent(parentRed.identifier)
        
        self.assertEqual(grandPRed.identifier, root.identifier)
        self.assertEqual(grandPRed.data.score, score)
        self.assertEqual(grandPRed.data.simulations, 1)

        monteC.printTree(monteC.tree, "propagationtest1")
    
    def test_4backPropagation2(self):
        """ test if values are correctly propagated
            """
        
        fen = "b05/8/8/8/8/8/8/r05"
        bb = GameState.createBitBoardFromFEN(fen)
        monteC = mcts(bb,Player.Blue)
        root = monteC.tree.get_node(1)
        rootscore,rootn = 0,0
        tmpnode = root
        for _ in range(10):
            tmpnode = monteC._1chooseNode(tmpnode)
            print(tmpnode.identifier)
            if(tmpnode.data.simulations == 0):
                #print("simu:",tmpnode.identifier)
                score = monteC._3runSimulation(tmpnode.identifier)
                if(tmpnode.identifier == 1):
                    rootscore, rootn= score,1
                tmpnode = monteC._4backPropagation(tmpnode,score)
            else:
                #print("expansion:", tmpnode.identifier)
                
                nodeList = monteC._2generateNodes(tmpnode.identifier)
                score = monteC._3runSimulation(nodeList[0].identifier)
                tmpnode = monteC._4backPropagation(nodeList[0],score)
        
        monteC.printTree(monteC.tree, "propagationtest2")
        
        childs = monteC.tree.children(1)
        testvalue = sum([child.data.score for child in childs])
        self.assertEqual(testvalue, root.data.score - rootscore)
        testvalue = sum([child.data.simulations for child in childs])
        self.assertEqual(testvalue, root.data.simulations - rootn)
        
        
        
        
        
        
    def test_runMCTS_Worker1(self):
        pass