import threading
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.start_mcts import *
output = {
    "board": "b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 r",
    "player1": True,
    "player2": False,
    "bothConnected": True,
    "time": 120000
}

res = start_mcts(output)

print(res)



