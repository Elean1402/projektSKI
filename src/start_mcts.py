#import threading
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
    dt = 0.0
    dt += clock.tick()
    
    if not servermsg:
        raise ValueError("servermsg empty")
    
    fen, color = servermsg["board"].split(" ")
    player = Player.Blue if color == "b" else Player.Red
    bb = GameState.createBitBoardFrom(Gui.fenToMatrix(fen), True)
    myRemainingtime = servermsg["time"]
    mcts=MCTS(bb,player=player)
    
    dt += clock.tick()
    myRemainingtime -= dt
    maxTimeFrame = round(myRemainingtime*0.05,2)
    print("timeframe for move: ", maxTimeFrame)
    result = mcts.doMCTS_v1(maxTimeFrame)
    
    result = json.dumps({"move": MoveLib.move(result[0], result[1],3)})
    mcts.printTree("totaltesting")
    return result

if __name__ == '__main__':
    output = {
        "board": "b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 r",
        "player1": True,
        "player2": False,
        "bothConnected": True,
        "time": 120000
    }

    res = start_mcts(output)

    print("result",res)   


