import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.gamestate import *
from src.gui import *
from src.benchmark import *
from src.moveGenerator import MoveGenerator
from src.moveLib import *
from src.model import *
from src.scoreConfig_evalFunc import *
from src.evalFunction import *
import time

GET_PLAYER_INDEX = 1
GET_BOARD_INDEX = 0

class TimeExceeded(Exception):
    pass
class AlphaBetaSearch:
    def __init__(self, game):
        self.moveLib = MoveLib()
        self.game = game
        self.player = self.game[GET_PLAYER_INDEX]
        self.opponent = Player.Red if self.player == Player.Blue else Player.Blue
        self.eval = EvalFunction(ScoreConfig.Version2(self.player, self.player))
        self.evalo = EvalFunction(ScoreConfig.Version2(self.player, self.player))
        self.gameover =   [DictMoveEntry.CONTINUE_GAME]
        self.total_gameover = False
        self.bitboards = self.game[GET_BOARD_INDEX]  # Set this to the initial bitboards
        self.moveGen = MoveGenerator(self.bitboards)
        self.best_move = None
        self.time_limit = 100000 
        self.start_time = time.time()
        self.bestMoves = []
        self.alpha = -float('inf')
        self.beta = float('inf')
        self.counter = 0
    def search(self, iterative_deepening=True, time_limit=100000):
        self.start_time = time.time()
        self.time_limit = time_limit 
        try:
            if iterative_deepening:
                
                depth = 2
                while True:
                    print("Iterative Deepening", depth)
                    result, temp_move = self.alphaBetaMax(self.alpha, self.beta, depth, self.bitboards)
                    if temp_move is not None:
                        self.best_move = temp_move
                    self.moveGen.checkBoardIfGameOver(self.gameover,self.bitboards)
                    if self.total_gameover or time.time() - self.start_time > self.time_limit:
                        break
                    depth += 2
            else:
                self.alpha = -float('inf')
                self.beta = float('inf')
                result, temp_move = self.alphaBetaMax(self.alpha, self.beta, 3, self.bitboards)
                if temp_move is not None:
                    self.best_move = temp_move
        except TimeExceeded:
            pass
        
        print(self.counter, "iterations")
        print(self.best_move)
        return self.best_move


    def alphaBetaMax(self, alpha, beta, depthleft, bitboard_copy):
        bitboard = bitboard_copy.copy()
        moves = self.moveGen.genMoves(self.player, self.gameover, bitboard)
        self.moveGen.checkBoardIfGameOver(self.gameover,bitboard)
        if self.gameover[0] != DictMoveEntry.CONTINUE_GAME or  depthleft == 0 or len(moves) == 0:
            if self.gameover[0] != DictMoveEntry.CONTINUE_GAME:
                self.total_gameover = True
            points = self.eval.computeOverallScore(moves, bitboard)[0][3]
            return points, None
            
        scorelist = self.eval.computeOverallScore(moves, bitboard, False)
        best_move = None
        for move in scorelist:
            self.counter += 1
            if time.time() - self.start_time > self.time_limit:
                raise TimeExceeded()
            
            newBoard = self.moveGen.execSingleMove(move, self.player, self.gameover,bitboard,False)
            score, _ = self.alphaBetaMin(alpha, beta, depthleft - 1, newBoard)

            if score >= beta:
                return beta, best_move
            
            if score > alpha:
                best_move = scorelist[0]
                alpha = score
        return alpha, best_move


    def alphaBetaMin(self, alpha, beta, depthleft, bitboard_copy):
        bitboard = bitboard_copy.copy()
        moves = self.moveGen.genMoves(self.opponent, self.gameover, bitboard)
        self.moveGen.checkBoardIfGameOver(self.gameover,bitboard)
        if self.gameover[0] != DictMoveEntry.CONTINUE_GAME or  depthleft == 0 or len(moves) == 0:
            if self.gameover[0] != DictMoveEntry.CONTINUE_GAME:
                self.total_gameover = True

            points = self.evalo.computeOverallScore(moves, bitboard)[0][3]
            return points, None
        scorelist = self.evalo.computeOverallScore(moves, bitboard, False)
        best_move = None
        for move in scorelist:
            self.counter += 1
            if time.time() - self.start_time > self.time_limit:
                raise TimeExceeded()
            
            newBoard = self.moveGen.execSingleMove(move, self.opponent, self.gameover,bitboard, False)
            score, _ = self.alphaBetaMax(alpha, beta, depthleft - 1, newBoard)

            if score <= alpha:
                
                return alpha, best_move
            if score < beta:
                best_move = scorelist[0] 
                beta = score
        return beta, best_move
    
    def play(self, iterative_deepening=False):
        self.time_limit = 1000000000
        moves = []
        origin_bitboard = self.bitboards.copy()
        for i in range(100):
            bitboard = self.bitboards.copy()
            self.moveGen.checkBoardIfGameOver(self.gameover,self.bitboards,True)
            if self.gameover[0] != DictMoveEntry.CONTINUE_GAME:
                break
            next_move = self.search(iterative_deepening)
            out = [MoveLib.BitsToPosition(next_move[0]), MoveLib.BitsToPosition(next_move[1])]
            moves.append(out)
            print("Next Move:", out)
            self.bitboards = self.moveGen.execSingleMove(next_move, self.player, self.gameover,bitboard,False)
            self.player, self.opponent = self.opponent, self.player
            print("not Over")
            #input("Press Enter to continue...")
        print("is Over")
        return bitboard, moves 
        

def call(input_dict):
    m = MoveLib()
    
    fen, player = input_dict["board"].split(" ")
    player = Player.Blue if player == "b" else Player.Red
    bitboard = GameState.createBitBoardFrom(Gui.fenToMatrix(fen), True)
    state = [bitboard, player, True, False]
    search_instance = AlphaBetaSearch(state)
    


    result = Benchmark.benchmark(lambda:search_instance.search(False), repetitions=1)
    #if result is None:
    #    result = [0, 0]
    #result = [m.BitsToPosition(result[0]), m.BitsToPosition(result[1])]
    #result = "-".join(result)

    print(result)
    return result


if __name__ == '__main__':
    input_dict = {"board": "2b03/1b0b05/6b01/3b02r01/1b01r02r01/2b05/2r03r01/3r02 b"}
    #input_dict = {"board": "b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 r"}

    #input_dict = {"board": "2b03/1b0b05/6b01/3b02r01/1b01r02r01/2b05/2r03r01/3r02 b"}
    call(input_dict)
