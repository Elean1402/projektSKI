import threading
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.mcts_uct import MCTS
from src.model import Player
from src.gamestate import GameState
from src.gui import Gui
from queue import Queue
from time import sleep
import pygame
import json
from src.moveLib import MoveLib


def start_mcts(servermsg:dict):
    clock = pygame.time.Clock()
    clock.tick()
    
    
    
    fen, color = servermsg["board"].split(" ")
    
    player = Player.Blue if color == "b" else Player.Red
    
    bb = GameState.createBitBoardFrom(Gui.fenToMatrix(fen), True)
    
    myRemainingtime = servermsg["time"]
    
    #mctsO = MCTS(bb,player)
    
    timeOver = threading.Event() # calling instance -> thread
    solutionFoundEvent = threading.Event() # Thread -> calling instance
    request = Queue()
    reply = []
    lock = threading.Lock()
    mcts_thread = threading.Thread(target= runMCTS_Worker, args=(request,reply,timeOver,solutionFoundEvent, lock,bb,player),daemon=True)
    clock.tick()
    myRemainingtime -= clock.get_time()
    #to be fixed
    
    maxTimeFrame = myRemainingtime*0.30
    mcts_thread.start()
    clock.tick()
    while maxTimeFrame > 0.05:
        sleep(maxTimeFrame-0.05)
        clock.tick()
        maxTimeFrame -= clock.get_time()

    timeOver.set()
    result = {}
    with lock:
        if(solutionFoundEvent.is_set()):
            result = reply[0]
        
    if(not result):
        solutionFoundEvent.wait()
        with lock:
            result = reply[0]
    
    return result

def runMCTS_Worker(reqMsg, replMsg, timeOver: threading.Event, solutionFound:threading.Event, lock: threading.Lock ,board,player,maxiter=10000,testmode=False)->None:
    """ Startet die Suche und soll als Thread aufgerufen werden.
        Das Ergebnis soll in replMsg gespeichert werden.
        
        reqMsg:  Aufrufende Instanz -> runMCTS_Worker
        replMsg: Aufrufende Instanz <- runMCTS_Worker
        timeOver: threading Event
        solutionFound: threading Event
        """
    mcts = MCTS(board,player)
    currentNode = mcts.tree.get_node(mcts.tree.root)
    #currentNodeId = currentNode.identifier
    while not timeOver.is_set():
        currentNode = mcts._1chooseNode(currentNode)
        if(mcts.tree.parent(currentNode.identifier).identifier == 1):
            with lock:
                replMsg[0] = json.dumps({"move": MoveLib.move(mcts.bestMove,3)})
                solutionFound.set()
        #mcts.printTree(mcts.tree, str(currentNode.identifier))
        
        if(currentNode.data.simulations == 0):
            #rollout
            score = mcts._3runSimulation(currentNode.identifier)
            currentNode = mcts._4backPropagation(currentNode,score)
        else:
            childIdList= mcts._2generateNodes(currentNode.identifier)
            
            score = mcts._3runSimulation(childIdList[0])
            currentNode = mcts._4backPropagation(mcts.tree.get_node(childIdList[0]),score)
            #if no children jump to root again
            #could lead to endless loop -> but limited to timeOver Event
            # else:
            #     currentNode = mcts.tree.get_node(mcts.root)
            
    # best_move = mcts.tree.bestmove
    # if(best_move[0] == 0 or best_move[1] == 0):
    #     raise Exception("mcts search: something went wrong, no move found")
    # with lock:
    #     replMsg[0] = json.dumps({"move": MoveLib.move(best_move,3)})
    #     solutionFound.set()
    
    return


