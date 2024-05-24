from src.gamestate import GameState
from src.model import *
from src.moveLib import MoveLib
from collections import Counter
import numpy as np



class EvalFunc:
    # Score distribution (not final) of implemented features
    _TURNOPTIONS=0
    
    _CONFIG_DICT = {"MOBILITY" : -1,
                     "TURN_OPTIONS": -1,
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
    
    __RANGE = np.array([1,6,1,1],dtype=np.uint64)
    __ZERO = np.uint64(0)
    
    #NEEDED: Total Order Featurescores
    #e.g. Materials > Mobility ... and so on
    def __init__(self,config: dict):
        #TODO
        print("Please use only scoreConfig_evalFunc.py for configurating Config!!")
        #Bitte config nur aus scoreConfig_evalFunc.py verwenden
        if len(self._CONFIG_DICT) != len(config):
            raise ValueError("Configs do not have same size")
        self._CONFIG_DICT = self._CONFIG_DICT | config
        #check __Config if all constants got new values
        vals = self._CONFIG_DICT.values()
        if(len(list(filter(lambda x: x==-1, vals)))>0):
            raise ValueError("Config is not complete, you may forgot a key-value pair, value -1 means not set")
        if(len(self._CONFIG_DICT["PIECESQUARE_TABLE_PAWN"]) == 0 or
           len(self._CONFIG_DICT["PIECESQUARE_TABLE_KNIGHT"]) == 0):
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
    def __turnOptions(self,size:int):
        self._TURNOPTIONS = self._CONFIG_DICT["TURN_OPTIONS"] << np.uint64(size)
    
    
    # Muss evtl. später optimiert werden, es könnte sein, dass die Loops (initialisierung) langsam sind
    def __moveIsNeighbourOfStartPos(self,startPos: np.uint64, targetPos:np.uint64):
        """Checks if targetPos is neighbour of StartPos
           --> the figure is a pawn

        Args:
            startPos (np.uint64) 
            targetPos (np.uint64)

        Returns:
            Boolean: if True, then Figure is pawn
                     else, then Figure is knight
        """
        bool = False
        current = startPos
        for i in self.__RANGE:
            current = current << i
            if(current == targetPos):
                bool = True
                break
            if(current == self.__ZERO):
                break
        current = startPos
        for i in self.__RANGE:
            current = current >> i
            if(current == targetPos):
                bool = True
                break
            if(current == self.__ZERO):
                break
        return bool 
    
    def __pieceSquareTable(self,moveList:list, board: list[np.uint64]):
        """Score for a Figure
           e.g. Target Fields (ends the game) will have higher Score
           e.g. Good Fields get higher score ...
           See Lecture notes: page 42
           -----------------------------------------
           MUST: use the defined Constants!!!!!!
           -----------------------------------------
        Args:
            moveList: list[(int, np.uint64, list[np.uint64])]
                    -> list[index, startPos, moveList]
            board (list[np.uint64])
        Returns:
            list: type ScoreListForMerging
        """
        #TODO
        #determine Figure: Pawn or Knight
        scoreList = ScoreListForMerging()
        for index in moveList:
            targetScores = dict()
            if(index[1] & board[GameState._ZARR_INDEX_R_PAWNS] & (~ board[GameState._ZARR_INDEX_B_KNIGHTS])):
                targetScores.update(dict({key: self._CONFIG_DICT["PIECESQUARE_TABLE_PAWN_Red"][MoveLib.BitsToPosition(key)]} for key in index[2] if self.__moveIsNeighbourOfStartPos(index[1], key)))
            elif (index[1] & board[GameState._ZARR_INDEX_R_KNIGHTS]):
                targetScores.update(dict({key: self._CONFIG_DICT["PIECESQUARE_TABLE_KNIGHT_Red"][MoveLib.BitsToPosition(key)]} for key in index[2] if not self.__moveIsNeighbourOfStartPos(index[1], key)))
            elif(index[1] & board[GameState._ZARR_INDEX_B_PAWNS] & (~ board[GameState._ZARR_INDEX_R_KNIGHTS])):
                targetScores.update(dict({key: self._CONFIG_DICT["PIECESQUARE_TABLE_PAWN_Blue"][MoveLib.BitsToPosition(key)]} for key in index[2] if self.__moveIsNeighbourOfStartPos(index[1], key)))
            elif (index[1] & board[GameState._ZARR_INDEX_B_KNIGHTS]):
                targetScores.update(dict({key: self._CONFIG_DICT["PIECESQUARE_TABLE_KNIGHT_Blue"][MoveLib.BitsToPosition(key)]} for key in index[2] if not self.__moveIsNeighbourOfStartPos(index[1], key)))
            
            scoreList.append((index[1], targetScores))
            self.__turnOptions(len(index[2]))
            
                
        return scoreList
    
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
    @classmethod
    def computeOverallScore(self, moveList: list, board:list[np.uint64]):
        """Computes the total Score of current State
           MoveList only read once!
        Args:
            moveList: list((int, np.uint64,list[np.uint64]))
                    -> list(index, figure, movelist)
            board (list[np.uint64]): _description_
        Returns:
            (TupleList[tuple], int): (move:np.uint64 , Total score: int)
            Ordering: Move with highest score at the end of the list.   
        """
        scoredList = ScoredMoveList()
        tempScore = ScoreListForMerging()
        tempScore.append(self.__pieceSquareTable(moveList, board))
        #TODO
        
        
        scoredList.sort()
        return scoredList
        

    
        