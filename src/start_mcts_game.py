import threading
import time
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mcts_uct import MCTS, NodeData
from model import Player
from gamestate import GameState
from gui import Gui
import numpy as np
from queue import Queue
from time import sleep
#implementierungsziel -> anbindung an gameclient
timeOver = threading.Event() # calling instance -> thread
solutionFoundEvent = threading.Event() # Thread -> calling instance

#setNewRoot = threading.Event()

request = Queue()
reply = []

#gameconfig = ....load?

input_dict = {"board": "2b03/1b0b05/6b01/3bb2r01/1b01r02r01/2b05/b0b0b0b0b0b0b0b0/3r02 b"}
fen, player = input_dict["board"].split(" ")
player = Player.Blue if player == "b" else Player.Red
board = GameState.createBitBoardFrom(Gui.fenToMatrix(fen), True)

#Zeitkontoverwaltung..?
#TODO
#wie soll man die Zeit für einen Zug einplanen?
#Abhängig von der Simulationszeit wäre gut?


#Starte 1 Thread starte die Zeit
#TODO
tree = MCTS(board)
lock = threading.Lock()
mcts_thread = threading.Thread(target= tree.runMCTS_Worker, args=(request,reply,timeOver,solutionFoundEvent, lock))
#starte Zeit...
#TODO

#starte den Thread
#TODO
mcts_thread.start()
#Func::begib dich in einer Loop und zähle die Zeit ab
#TODO
sleep(2)

#Falls die Zeit vorbei ist, setze EVENT damit der Thread beendet werden kann 
#TODO
timeOver.set()
#checke schonmal ob der Thread eine Antwort geliefert hat, falls nicht warte bis der Thread beendet wird. Setze Lock auf die Message und lese ergebnis aus
#TODO
solutionFoundEvent.wait()
result = 0
with lock:
    result = reply[0]
#Warte bis der Thread beendet, falls noch keine Antwort
#TODO

#return ergebnis im geforderten json format
print(result)

mcts_thread.join()





