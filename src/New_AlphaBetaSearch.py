import copy
import time

from src.evalFunction import *
from src.gamestate import *
from src.gui import *
from src.scoreConfig_evalFunc import *
from src.moveGenerator import MoveGenerator
from src.moveLib import *
from src.model import *

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
    
    _eval = EvalFunction
    _moveGen = MoveGenerator
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

        self._eval = EvalFunction(ScoreConfig.Version1(), self.player)
        self._moveGen = MoveGenerator(GameState.createBitBoardFromFEN(gameDict[GameServerModel.FEN_BOARD]))
        self._board= GameState.createBitBoardFromFEN(gameDict[GameServerModel.FEN_BOARD])
        
        
    def startGame(self, gameDict: dict, depth: int):
        """
        The function to start the Alpha-Beta Search.
        """
        
        while(self._totalGameOver[0] == DictMoveEntry.CONTINUE_GAME):
            ###################
            #TODO Wait for legal user move
            #Server needs to wait until its our turn
            
            #waiting...
            
            #TODO update Board (opponents move)
            #self._board = xxxx
            
            #TODO CHECK if GAME OVER
            self._moveGen.checkBoardIfGameOver(self._totalGameOver,self._board)
            if(self._totalGameOver[0] != DictMoveEntry.CONTINUE_GAME ):
                break
            
            
            if(self._testmodus):
                _, best_move = self._alpha_beta(self._ALPHA_INIT, self._BETA_INIT, depth,self._max_player, self._board )
            ##TODO exec Best Move
            
            
            ## Send Info To Server
        
        return self._gameover[0]

     
    

   
    def _alpha_beta(self, alpha:int, beta:int, depth: int | float,maxPlayer: Player, board: list[np.uint64], move: tuple = (np.uint64(0),np.uint64(0),[])):
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
        
        if (depth <= 0 or self._gameover[0] != DictMoveEntry.CONTINUE_GAME):
            # no time left or game_over
            # return score, move ?
            True
        
        if(self._max_player == self._my_color_is):
            maxScore = self._ALPHA_INIT
            
            #best move at the beginning at the list
            moveList = self._moveGen.genMoves(self._my_color_is,self._gameover, board)
            
            if(self._testmodus):
                if(len(moveList) ==0):
                    return (maxScore,None)
                scoredMoveList = self._eval.computeOverallScore(moveList, board)
                for moveItem in scoredMoveList:
                    
                    newBoard = self._moveGen.execSingleMove(moveItem, self._max_player, self._gameover,board)
                    
                    self._moveGen.checkBoardIfGameOver(self._gameover,board)
                    if(self._gameover[0] != DictMoveEntry.CONTINUE_GAME):
                       self._gameover[0] = DictMoveEntry.CONTINUE_GAME
                       return moveItem
                        
                    retVal = self._alpha_beta(alpha,beta, depth-1,maxPlayer, newBoard)
                    
                    maxScore = max(maxScore,retVal[3])
                    alpha = max(alpha, retVal[3])
                    
                    if( beta <= alpha):
                        break
        
            return maxScore
        else:
            minScore = self._BETA_INIT
            
            #best move at the beginning at the list
            moveList = self._moveGen.genMoves(self._my_color_is,self._gameover, board)
            
            if(self._testmodus):
                if(len(moveList) ==0):
                    return (minScore,None)
                scoredMoveList = self._eval.computeOverallScore(moveList, board)
                for moveItem in scoredMoveList:
                    
                    newBoard = self._moveGen.execSingleMove(moveItem, self._max_player, self._gameover,board)
                    
                    self._moveGen.checkBoardIfGameOver(self._gameover,board)
                    if(self._gameover[0] != DictMoveEntry.CONTINUE_GAME):
                       self._gameover[0] = DictMoveEntry.CONTINUE_GAME
                       return moveItem
                        
                    retVal = self._alpha_beta(alpha,beta, depth-1,maxPlayer, newBoard)
                    
                    maxScore = max(maxScore,retVal[3])
                    alpha = max(alpha, retVal[3])
                    
                    if( beta <= alpha):
                        break
            
                
            
        

    

    def change_player(self, player):
        self.player = Player.Blue if player == Player.Red else Player.Red
        
    def _convertPlayerString(self,pstr: str):
        return Player.Red if pstr == "r" else Player.Blue