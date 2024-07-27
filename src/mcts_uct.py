import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from treelib import Node, Tree
import numpy as np
import threading
from moveGenerator_sicher import MoveGenerator
from model import DictMoveEntry,MaxHeapMCTS,Player
class NodeData:
    def __init__(self, board:list[np.uint64],gameOver:DictMoveEntry ,move: tuple[np.uint64,np.int64] = (np.uint64(0),np.uint64(0))):
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
        self._mv.checkBoardIfGameOver([DictMoveEntry.CONTINUE_GAME],board) #root could be already in a end state of the game
        self.tree.create_node("root",1,data=NodeData(board,self._mv._gameover))
        
    def _1chooseNode(self,currNode:Node)-> Node:
        """ Diese Funktion soll die UCT-Werte berechnen
            und den ausgewählten Knoten wiedergeben"""
        tempNode = currNode
        maxheap = MaxHeapMCTS()
        while not tempNode.is_leaf():
            tmpID = tempNode.identifier
            childIDlist = self.tree.children(tmpID)
            [maxheap.push(self._computeUCTValue(childId)) for childId in childIDlist]
            tempNode = maxheap.pop()
            maxheap.clear()
        #state: tempNode is a leaf
        return tempNode
    
    def _computeUCTValue(self,nodeId:any)->float:
        """Berechnet den UCT-Wert"""
        N = self.tree.parent(nodeId).data.simulations
        nodedata = self.tree.get_node(nodeId).data
        score = nodedata.score
        n = nodedata.simulations
        x =  np.divide(score, n)
        return np.add(x ,  np.multiply(self.C, np.sqrt(np.divide(np.log(N),n))))
    
    def _2generateNodes(self,nodeId:any)-> list:
        """ Generiert alle Folgezustände ausgehend von currentNode
            Returns list: list[nodeIds]"""
        currentNode = self.tree.get_node(nodeId)
        depth = self.tree.depth(currentNode)
        player =  self.player1 if np.mod(depth,2,dtype=np.uint64) == 0 else self.player2
        board = currentNode.data.board
        
        gameOver = [DictMoveEntry.CONTINUE_GAME]
        movelist = self._mv.genMoves(player,board,gameOver)
        if gameOver[0] != DictMoveEntry.CONTINUE_GAME:
            currentNode.data.gameOver = gameOver[0]
            return movelist
        
        resBoards = [self._mv.execSingleMove(move,player,board,[DictMoveEntry.CONTINUE_GAME]) for move in movelist]
        mvBoardTuple = zip(movelist,resBoards)
        [self.tree.create_node(parent=currentNode,data=NodeData(item[1],DictMoveEntry.CONTINUE_GAME,item[0])) for item in mvBoardTuple]
        
        return self.tree.children(nodeId)
        
    
    def _3runSimulation(self,nodeId:any)-> int:
        """ Führt die randomisierte Simulation durch ausgehend von currentNode"""
        player = self.player1 if np.mod(self.tree.depth(nodeId),2,dtype=np.uint64) ==0 else self.player2
        gameOver = [DictMoveEntry.CONTINUE_GAME]
        randG = np.random.default_rng()
        #führe Züge alternierend aus
        currentNode = self.tree.get_node(nodeId)
        currentBoard = currentNode.data.board
        while gameOver[0] == DictMoveEntry.CONTINUE_GAME:
            moves = self._mv.genMoves(player,currentBoard,gameOver)
            randmv = randG.choice(moves)
            currentBoard = self._mv.execSingleMove(randmv,player,currentBoard,gameOver)
            player = self.player1 if player == self.player2 else self.player1 # switch players
            
        if(gameOver[0]== DictMoveEntry.GAME_OVER_RED_WINS):
            if(self.player1 == Player.Red):
                return 1
            else:
                return -1
        
        if(self.player1 == Player.Blue):
            return 1
            
        return -1
    
    def _4backPropagation(self, currentNode:Node, score:float)-> None:
        """ Führt die Propagation durch ausgehend von currentNode"""
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
        
        while not timeOver.isSet():
            print("waiting")

        with lock:
            replMsg.append("item")
            solutionFound.set()
        
        return 
    
    
    
        