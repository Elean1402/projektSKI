import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from treelib import Node, Tree
import numpy as np
import threading
from src.moveGenerator_sicher import MoveGenerator
from src.model import DictMoveEntry,MaxHeapMCTS,Player
from pygame import time as pgtime
from src.moveLib import MoveLib
from graphviz import Source
import json

class NodeData:
    def __init__(self, board:list[np.uint64],gameOver:list[DictMoveEntry] ,move: tuple[np.uint64,np.int64] = (np.uint64(0),np.uint64(0))):
        #initializing the variables this way, gives usually a small speed up, during frequently creating nodes
        self.board, self.score, self.simulations, self.move, self.gameOver = board.copy(), 0, 0, move, gameOver
    

class MCTS:
    
    def __init__(self,board: list[np.uint64],player: Player, C = np.sqrt(2)):
        self.player1 = player # me
        self.player2 = Player.Blue if self.player1 == Player.Red else Player.Red
        self.tree = Tree()
        self.root = 1 # Id for root
        self.currentNode = self.root #used for navigation on tree
        self.C = C # exploration constant
        self._mv = MoveGenerator()
        
        data = NodeData(board,[DictMoveEntry.CONTINUE_GAME])
        self._mv.checkBoardIfGameOver(data.gameOver,board) #root could be already in a end state of the game
        self.tree.create_node("root",1,data=data)
        self.bestMove = (np.uint64(0),np.uint64(0))
        
        
    def _1chooseNode(self,currNode:Node)-> Node:
        """ Diese Funktion soll die UCT-Werte berechnen
            und den ausgewählten Blattknoten wiedergeben"""
        tempNode = currNode
        maxheap = MaxHeapMCTS()
        while not tempNode.is_leaf():
            tmpID = tempNode.identifier
            childlist = self.tree.children(tmpID)
            #[maxheap.push((self._computeUCTValue(child),child)) for child in childlist]
            tempNode= self._getMaxUCTNode(childlist,maxheap)
            
        #state: tempNode is a leaf
        if(self.tree.parent(tempNode.identifier) == self.tree.root):
            self.bestMove = (tempNode.data.move[0],tempNode.data.move[1])
        return tempNode
    
    def _getMaxUCTNode(self,nodes:list[Node],maxheap: MaxHeapMCTS):
        """returns Generator"""
        maxheap.clear()
        for node in nodes:
            if not node.data.simulations:
                return node
            maxheap.push((self._computeUCTValue(node),node))
        maxNode = maxheap.pop()
        maxheap.clear()
        return maxNode
            
        
        
    def _computeUCTValue(self,node:Node)->float:
        """Berechnet den UCT-Wert"""
        nodeId = node.identifier
        N = self.tree.parent(nodeId).data.simulations
        nodedata = self.tree.get_node(nodeId).data
        score = nodedata.score
        n = nodedata.simulations
        x =  np.divide(score, n)
        return np.add(x ,  np.multiply(self.C, np.sqrt(np.divide(np.log(N),n))))
    
    def _2generateNodes(self,nodeId:any)-> list:
        """ Generiert alle Folgezustände ausgehend von nodeId
            Returns list: list[Node] | []"""
        currentNode = self.tree.get_node(nodeId)
        
        depth = self.tree.depth(currentNode)
        player =  self.player1 if np.mod(depth,2,dtype=np.uint64) == 0 else self.player2
        if(currentNode.data.gameOver[0] == DictMoveEntry.GAME_OVER_BLUE_WINS and player == Player.Blue or
           currentNode.data.gameOver[0] == DictMoveEntry.GAME_OVER_RED_WINS and player == Player.Red):
            return []

        board = currentNode.data.board
        
        gameOver = [DictMoveEntry.CONTINUE_GAME]
        movelist = self._mv.genMoves(player,board,gameOver)
        if gameOver[0] != DictMoveEntry.CONTINUE_GAME:
            currentNode.data.gameOver = gameOver
            return []
        movelistGameOvers = zip(movelist, [[DictMoveEntry.CONTINUE_GAME] for _ in movelist])
        
        resBoards = [(self._mv.execSingleMove(move,player,board,gameOver),gameOver) for move,gameOver in movelistGameOvers]
        mvBoardTuple = zip(movelist,resBoards)
        [self.tree.create_node(parent=currentNode,data=NodeData(item[1][0],item[1][1],item[0])) for item in mvBoardTuple]
        
        return self.tree.children(nodeId)
        
    
    def _3runSimulation(self,nodeId:any)-> int:
        """ Führt die randomisierte Simulation durch ausgehend von node von nodeId"""

        player = self.player1 if np.mod(self.tree.depth(nodeId),2,dtype=np.uint64) ==0 else self.player2
        gameOver = [DictMoveEntry.CONTINUE_GAME]
        randG = np.random.default_rng()
        
        currentNode = self.tree.get_node(nodeId)
        currentBoard = currentNode.data.board
        while gameOver[0] == DictMoveEntry.CONTINUE_GAME:
            moves = self._mv.genMoves(player,currentBoard,gameOver)
            if(not moves):
                break
            randmv = randG.choice(np.asarray(moves, dtype="object"))
            currentBoard = self._mv.execSingleMove(randmv,player,currentBoard,gameOver)
            #führe Züge alternierend aus
            player = self.player1 if player == self.player2 else self.player1 # switch players
        
        if(gameOver[0]== DictMoveEntry.GAME_OVER_RED_WINS):
            if(self.player1 == Player.Red):
                return 1
            else:
                return -1
        
        if(self.player1 == Player.Blue):
            return 1
        return -1
    
    def _4backPropagation(self, currentNode:Node, score:float)-> Node:
        """ Führt die Propagation durch ausgehend von currentNode
            Returns treelib.Node: root of tree"""
        data = currentNode.data
        data.simulations += 1
        data.score += score
        tmpNode = currentNode
        tree = self.tree
        while tree.parent(tmpNode.identifier) != None:
            tmpNode = tree.parent(tmpNode.identifier)
            data = tmpNode.data
            data.simulations += 1
            data.score += score

        return tmpNode
    
    def _doMCTS(self):
        pass
    
    def runMCTS_Worker(self, reqMsg, replMsg, timeOver: threading.Event, solutionFound:threading.Event, lock: threading.Lock ,testmode=False)->None:
        """ Startet die Suche und soll als Thread aufgerufen werden.
            Das Ergebnis soll in replMsg gespeichert werden.
            
            reqMsg:  Aufrufende Instanz -> runMCTS_Worker
            replMsg: Aufrufende Instanz <- runMCTS_Worker
            timeOver: threading Event
            solutionFound: threading Event
            """
        currentNode = self.tree.get_node(self.tree.root)
        currentNodeId = currentNode.identifier
        while not timeOver.isSet():
            currentNode = self._1chooseNode(currentNode)
            currentNodeId = currentNode.identifier
            if(currentNode.data.simulations == 0):
                #rollout
                score = self._3runSimulation(currentNodeId)
                currentNode = self._4backPropagation(currentNode,score)
            else:
                childIdList= self._2generateNodes(currentNodeId)
                if(childIdList):
                    score = self._3runSimulation(childIdList[0])
                    currentNode = self._4backPropagation(self.tree.get_node(childIdList[0]),score)
                #if no children jump to root again
                #could lead to endless loop -> but limited to timeOver Event
                else:
                    currentNode = self.tree.get_node(self.root)
                
        best_move = self.tree.bestmove
        if(best_move[0] == 0 or best_move[1] == 0):
            raise Exception("mcts search: something went wrong, no move found")
        with lock:
            replMsg.append(json.dumps({"move": MoveLib.move(best_move,3)}))
            solutionFound.set()
        
        return
    
    def printTree(self,tree:Tree, filename:str, showBoard:bool = False):
        
        dot_lines = ['digraph tree {']
        for node in tree.all_nodes():
            label = f"id:{node.identifier}\n {self.player1  if np.mod(self.tree.depth(node.identifier),2,dtype=np.uint64) ==0 else self.player2} \n{self._mv.prettyPrintBoard2(node.data.board,node.data.gameOver) if showBoard else ""} \n {self._mv.prettyPrintMove(node.data.move) if node.data.move[0] != 0 else "no move applied"} \n score={node.data.score}, n={node.data.simulations}" if node.data else node.tag
            dot_lines.append(f'    "{node.identifier}" [label="{label}"];')
            if node.is_leaf():
                continue
            for child in tree.children(node.identifier):
                dot_lines.append(f'    "{node.identifier}" -> "{child.identifier}";')
        
        dot_lines.append('}')
        dot = '\n'.join(dot_lines)
        src = Source(dot)
        src.format = 'png'
        path = '../data/mcts/trees'  # Ersetzen Sie diesen Pfad durch den gewünschten Ordner
        
        src.render( filename=filename,directory=path, format='png', cleanup=False)
    
    
    
    
    
        