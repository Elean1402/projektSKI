from src.gamestate import GameState
import numpy as np

class EvalFunc:
    # Score distribution of implemented features
    # _MOBILITY = ?
    # _PROTECTION_PAWNS = ?
    # _PROTECTION_KNIGHTS = ?
    # _UNPROTECTED_PAWNS = ?
    # _UNPROTECTED_KNIGHTS = ?
    # _UPGRADE_TO_KNIGHT = ?
    # _BLOCKED_FIGURES = ?
    # _MATERIALS = ?
    
    #NEEDED: Total Order Featurescores
    #e.g. Materials > Mobility ... and so on
    
    def mobility(self, board: list[np.uint64]):
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
    
    def pieceSquareTable(self, board: list[np.uint64]):
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
    
    def protectedFigures(self, board:list[np.uint64]):
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
    
    def unprotectedFigures(self, board:list[np.uint64]):
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
    
    def upgradeFigure(self, board:list[np.uint64]):
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
    
    def blockedFigures(self, board:list[np.uint64]):
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
    
    def materialPoints(self, board:list[np.uint64]):
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
    
    def computeOverallScore(self, board:list[np.uint64]):
        """Computes the total Score of current State

        Args:
            board (list[np.uint64]): _description_
        Return:
            Score: Int
        """
        #TODO
        return 0
        

    
        