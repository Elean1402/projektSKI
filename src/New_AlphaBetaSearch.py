import copy
import time

from evalFunction import *
from gamestate import *
from gui import *
from scoreConfig_evalFunc import *
from moveGenerator import MoveGenerator
from moveLib import *
from model import *

class AlphaBetaSearch:
    """
    This class implements the Alpha-Beta Search algorithm for a given game.
    """
    
    _gameover =   [DictMoveEntry.CONTINUE_GAME]
    _totalGameOver = [DictMoveEntry.CONTINUE_GAME]
    _ALPHA_INIT     =   -float('inf')
    _BETA_INIT      =   float('inf')
    _board     =   [np.uint64(0),np.uint64(0),np.uint64(0),np.uint64(0)]
    _max_player     =   Player.NoOne
    _who_am_i       :   GameServerModel
    _my_color_is    :   Player.NoOne
    _start_time     =   0
    _max_time       =   0
    _end_time       =   0
    
    _eval = 0
    _moveGen = 0
    _testmodus = False
    _depth_max = -1
    
    def __init__(self, gameDict: dict, iAm: GameServerModel ,myColorIs: Player, depth_max: int, testmodus = False,  max_time: float = 0.5):
        """
        The constructor for AlphaBetaSearch class.
        """
        
        
        #############################################
        """Was soll das bedeuten????"""
        self.start_time = time.time()
        self.max_time = max_time
        self.end_time = time.time() + self.max_time
        ############################################
        
        
        self._max_player = Player.Red if self._convertPlayerString(gameDict[GameServerModel.CURRENT_PLAYER_STRING]) == Player.Red else Player.Blue
        ########################################################
                # WELCHER SPIELER BIN ICH ???????
        #self._who_am_i = ????
        ########################################################
        if(testmodus):
            self._who_am_i = GameServerModel.PLAYER1
            self._my_color_is = Player.Red
            self._testmodus = True
        else:
            self._who_am_i = iAm
            self._my_color_is = myColorIs
        #self._board_init = GameState.createBitBoardFromFEN(game[GameServerModel.FEN_BOARD])

        self._eval = EvalFunction(ScoreConfig.Version1(self._my_color_is))
        self._moveGen = MoveGenerator(GameState.createBitBoardFromFEN(gameDict[GameServerModel.FEN_BOARD]))
        self._board= GameState.createBitBoardFromFEN(gameDict[GameServerModel.FEN_BOARD])
        
        
    def startGame(self, gameDict: dict, depth: int):
        """
        The function to start the Alpha-Beta Search.
        """
        bestMove = []
        newboard = self._board.copy()
        while(self._totalGameOver[0] == DictMoveEntry.CONTINUE_GAME):
            ###################
            #TODO Wait for legal user move
            #Server needs to wait until its our turn
            
            #waiting...
            
            #TODO CHECK if GAME OVER
            self._moveGen.checkBoardIfGameOver(self._totalGameOver,newboard)
            if(self._totalGameOver[0] != DictMoveEntry.CONTINUE_GAME ):
                break
            
            ## Measure Time
            if(self._testmodus):
                self._alpha_beta(self._ALPHA_INIT, self._BETA_INIT, depth+1,self._max_player, newboard, bestMove )
            ## Measure Time ??
            
            ##TODO exec Best Move
            if(len(bestMove) == 0):
                self._totalGameOver[0] == DictMoveEntry.GAME_OVER_RED_WINS if self._my_color_is == Player.Red else DictMoveEntry.GAME_OVER_BLUE_WINS
            
            currentBestMove = bestMove[0]
            newboard = self._moveGen.execSingleMove(bestMove[0],self._my_color_is, self._totalGameOver,newboard,True)
                
            
            ## Send Info To Server
        
        return self._gameover[0]

     
    

   
    def _alpha_beta(self, alpha:int, beta:int, depth: int | float,maxPlayer: Player, board: list[np.uint64], bestMoveStack: list, playersTurn:Player):
        """Alpha Beta Search
            THE BASIS CODE OF THIS FUNCTION IS NOT FROM THE LECTURE,
            SOURCE: https://www.youtube.com/watch?v=l-hh51ncgDI&ab_channel=SebastianLague
            AND HAS BEEN MODYFIED.
        Args:
            alpha (int): score
            beta (int): score
            depth (int | float): for Testing could be depth or time
            board (list[np.uint64]): bitboard array
            maxPlayer (Player): beginning Player
        """
        cboard = board.copy()
        if (depth <= 0 or self._gameover[0] != DictMoveEntry.CONTINUE_GAME):
            # no time left or game_over
            # return score, move ?
            lastMove = bestMoveStack.pop()
            return (lastMove[3],(lastMove[1],lastMove[2]))
        
        if(self._max_player == self._my_color_is):
            maxScore = self._ALPHA_INIT
            
            #best move at the beginning at the list
            # moveList = self._moveGen.genMoves(self._my_color_is,self._gameover, cboard)
            moveList = self._moveGen.genMoves(self._my_color_is,self._gameover, cboard)
            lastMove = 0
            if(self._testmodus):
                if(len(moveList) ==0):
                    return (maxScore,None)
                scoredMoveList = self._eval.computeOverallScore(moveList, cboard,True)
                
                for moveItem in scoredMoveList:
                    bestMoveStack.append(moveItem)
                    newBoard = self._moveGen.execSingleMove(moveItem, self._my_color_is, self._gameover,cboard,True)
                    
                    self._moveGen.checkBoardIfGameOver(self._gameover,newBoard)
                    if(self._gameover[0] != DictMoveEntry.CONTINUE_GAME):
                      
                       return (moveItem[3],(moveItem[0],moveItem[1]))
                    
                    retVal = self._alpha_beta(alpha,beta, depth-1,maxPlayer, newBoard,bestMoveStack)
                    
                    maxScore = max(maxScore,retVal[3])
                    alpha = max(alpha, retVal[3])
                    
                    if( beta <= alpha):
                        break
                    lastMove= bestMoveStack.pop()

            return (maxScore,(lastMove[0],lastMove[1]))
        else:
            minScore = self._BETA_INIT
            
            #best move at the beginning at the list
            moveList = self._moveGen.genMoves(self._my_color_is,self._gameover, cboard)
            lastMove = 0
            if(self._testmodus):
                if(len(moveList) ==0):
                    return (minScore,None)
                scoredMoveList = self._eval.computeOverallScore(moveList, cboard)
                for moveItem in scoredMoveList:
                    bestMoveStack.append(moveItem)
                    newBoard = self._moveGen.execSingleMove(moveItem, self._my_color_is, self._gameover,cboard)
                    
                    self._moveGen.checkBoardIfGameOver(self._gameover,newBoard)
                    if(self._gameover[0] != DictMoveEntry.CONTINUE_GAME):
                       return (moveItem[3], (moveItem[0],moveItem[1]))
                      
                    retVal = self._alpha_beta(alpha,beta, depth-1,maxPlayer, newBoard,bestMoveStack)
                    
                    minScore = min(minScore,retVal[0])
                    alpha = min(beta, retVal[0])
                    
                    if( beta <= alpha):
                        break
                    lastMove =bestMoveStack.pop()
            return (minScore,(lastMove[0],lastMove[1]))
            
                
            
        

    

    def change_player(self, player):
        self.player = Player.Blue if player == Player.Red else Player.Red
        
    def _convertPlayerString(self,pstr: str):
        return Player.Red if pstr == "r" else Player.Blue