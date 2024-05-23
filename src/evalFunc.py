from src.gamestate import GameState
from src.model import *
from src.moveLib import MoveLib
import numpy as np



class EvalFunc:
    # Score distribution (not final) of implemented features
    
    __CONFIG_DICT = {"MOBILITY" : -1,
                     "PROTECTION_PAWNS" : -1,
                     "PROTECTION_KNIGHTS" : -1,
                     "UNPROTECTED_PAWNS" : -1,
                     "UNPROTECTED_KNIGHTS" : -1,
                     "UPGRADE_TO_KNIGHT" : -1,
                     "BLOCKED_FIGURES" : -1,
                     "MAT_PAWN" : -1,
                     "MAT_KNIGHT" : -1,
                     "ENDGAME_MAT_PAWN" : -1,
                     "ENDGAME_MAT_KNIGHT" : -1,
                     "PIECESQUARE_TABLE_PAWN_Blue": {},
                     "PIECESQUARE_TABLE_KNIGHT_Blue": {},
                     "PIECESQUARE_TABLE_PAWN_Red": {},
                     "PIECESQUARE_TABLE_KNIGHT_Red": {},}
    
    #NEEDED: Total Order Featurescores
    #e.g. Materials > Mobility ... and so on
    def __init__(self,config: dict):
        #TODO
        print("Please use only scoreConfig_evalFunc.py for configurating Config!!")
        #Bitte config nur aus scoreConfig_evalFunc.py verwenden
        if len(self.__CONFIG_DICT) != len(config):
            raise ValueError("Configs do not have same size")
        self.__CONFIG_DICT = self.__CONFIG_DICT | config
        #check __Config if all constants got new values
        vals = self.__CONFIG_DICT.values()
        if(len(list(filter(lambda x: x==-1, vals)))>0):
            raise ValueError("Config is not complete, you may forgot a key-value pair, value -1 means not set")
        if(len(self.__CONFIG_DICT["PIECESQUARE_TABLE_PAWN"]) == 0 or
           len(self.__CONFIG_DICT["PIECESQUARE_TABLE_KNIGHT"]) == 0):
            raise ValueError("Config: PIECESQUARE_TABLE_\{Pawn,Knight\} Dictionary not set")
        
    def __mobility(self, board: list[np.uint64]):
        """Score distribution over Board
           Please see Lecture Notes Page 43.
           If necessary: Split up this Function into several subfunctions!!
           -----------------------------------------
           MUST: use the defined Constants!!!!!!
           -----------------------------------------
        Args:
            board (list[np.uint64])
        Returns:
            Score Board:  unknown
        """
        #TODO
        return 0
    
    def __pieceSquareTable(self, TargetPos: np.uint64, board: list[np.uint64]):
        """Score for a Figure
           e.g. Target Fields (ends the game) will have higher Score
           e.g. Good Fields get higher score ...
           See Lecture notes: page 42
           -----------------------------------------
           MUST: use the defined Constants!!!!!!
           -----------------------------------------
        Args:
            board (list[np.uint64])
        Returns:
            Score Board: unknown
        """
        #TODO
        return 0
    
    def __protectedFigures(self, board:list[np.uint64]):
        """Scores for protected figures
           distinguish Score for Protecting pawns and knights
           If necessary: create helper-function for pawns and knights
           -----------------------------------------
           MUST: use the defined Constants!!!!!!
           -----------------------------------------
        Args:
            board (list[np.uint64])
        Return:
            Score Board: unknown
        """
        #TODO
        return 0
    
    def __unprotectedFigures(self, board:list[np.uint64]):
        """Scores for unprotected figures
           distinguish Score between pawns and knights
           if necessary: create helper-function for pawns and knights
           -----------------------------------------
           MUST: use the defined Constants!!!!!!
           ----------------------------------------- 
        Args:
            board (list[np.uint64])
        Return:
            Score Board: unknown
        """
        #TODO
        return 0
    
    def __upgradeFigure(self, board:list[np.uint64]):
        """Score for upgrading figure to Knight
           -----------------------------------------
           MUST: use the defined Constants!!!!!!
           ----------------------------------------- 
        Args:
            board (list[np.uint64])
        Return:
            Score Board: unknown
        """
        #TODO
        return 0
    
    def __blockedFigures(self, board:list[np.uint64]):
        """Score to block movement of figure
           Why? -> if all enemy figures are blocked, game will result into win
           -----------------------------------------
           MUST: use the defined Constants!!!!!!
           ----------------------------------------- 
        Args:
            board (list[np.uint64]): _description_
        Return:
            Score Board: unknown
        """
        #TODO
        return 0
    
    def __materialPoints(self, board:list[np.uint64]):
        """Scores figures
        -----------------------------------------
           MUST: use the defined Constants!!!!!!
        -----------------------------------------
        Args:
            board (list[np.uint64])
        Return:
            Score Board: unknown
        """
        #TODO
        return 0
    
    def computeOverallScore(self, moveList: list[np.uint64], board:list[np.uint64]):
        """Computes the total Score of current State

        Args:
            board (list[np.uint64]): _description_
        Returns:
            TupleList[tuple]: (move:np.uint64 , score: int)
            Ordering: Highest score at the end of the list.   
        """
        scoredList = TupleList()
        #TODO
        
        
        scoredList = sorted(scoredList,key=lambda x: x[1])
        return scoredList
        

    
        