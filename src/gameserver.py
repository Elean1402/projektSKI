from zuggenerator import *


def init():
    fen_string = "6/8/8/8/8/4b03/4r0b02/6 r"
    fen_string, player = fen_string.split(" ")
    bitboard = GameState.createBitBoardFrom(Gui.fenToMatrix(fen_string), True)
    return bitboard, fen_string, player
