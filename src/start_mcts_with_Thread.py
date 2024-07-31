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

timeOver = threading.Event() # calling instance -> thread
foundEvent = threading.Event() # Thread -> calling instance
request = Queue()
reply = {}
lock = threading.Lock()
    
def start_mcts_with_Thread(servermsg:dict):
    clock = pygame.time.Clock()
    dt = 0.0
    dt += clock.tick()
    
    if not servermsg:
        raise ValueError("servermsg empty")
    
    fen, color = servermsg["board"].split(" ")
    
    player = Player.Blue if color == "b" else Player.Red
    
    bb = GameState.createBitBoardFrom(Gui.fenToMatrix(fen), True)
    
    myRemainingtime = servermsg["time"]
    
    #mctsO = MCTS(bb,player)
    
    
    mcts_thread = threading.Thread(target= runMCTS_Worker, args=(bb,player,),daemon=True)
    dt += clock.tick()
    myRemainingtime -= dt
    #to be fixed
    
    maxTimeFrame = myRemainingtime*0.05
    mcts_thread.start()

    while maxTimeFrame > 0.05:
        
        maxTimeFrame -= clock.tick(60)

    timeOver.set()
    result = {}
    while not foundEvent.is_set():
        True
    with lock:
        result["move"] = reply["result"]
        
    if(not result):
        raise Exception("No move found")
    
    return result


# Es gibt hier Probleme:
# Es scheint so, als ob durch das Threading
# Der Code in mcts_uct noch strenger überprüft wird
# und ständig type check durchgeführt wird
# als Folge dessen werden ständig Fehlermeldung von NoneType Objects 
#zurückgegeben
def runMCTS_Worker(board,player)->None:
    """ Startet die Suche und soll als Thread aufgerufen werden.
        Das Ergebnis soll in reply gespeichert werden.
        
        request:  Aufrufende Instanz -> runMCTS_Worker
        reply: Aufrufende Instanz <- runMCTS_Worker
        timeOver: threading Event
        foundEvent: threading Event
        """
    reply["result"]= "test"
    mcts = MCTS(board,player)
    
    currentNode = mcts.tree.get_node(mcts.tree.root)
    #currentNodeId = currentNode.identifier
    while not timeOver.is_set():
        currentNode = mcts._1chooseNode(currentNode)
        # if(mcts.tree.parent(currentNode.identifier).identifier == 1):
        #     with lock:
        #         reply[0] = json.dumps({"move": MoveLib.move(mcts.bestMove,3)})
        #         foundEvent.set()
        #mcts.printTree(mcts.tree, str(currentNode.identifier))
        
        if(currentNode.data.simulations == 0):
            #rollout
            score = mcts._3runSimulation(currentNode.identifier)
            currentNode = mcts._4backPropagation(currentNode,score)
        else:
            childIdList= mcts._2generateNodes(currentNode.identifier)
            if(childIdList):
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
    #     reply[0] = json.dumps({"move": MoveLib.move(best_move,3)})
    #     foundEvent.set()
    
    return


