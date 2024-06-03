from src.gamestate import GameState
from src.model import *
from src.moveLib import MoveLib
from collections import Counter
from src.moveGenerator import MoveGenerator
import numpy as np
from itertools import chain
from more_itertools import ilen


class EvalFunction:
    # Score distribution (not final) of implemented features
    _TURNOPTIONS=0
    _player = 0
    _CONFIG_DICT = { Config.MOBILITY : -1,
                     Config.TURN_OPTIONS: -1,
                     Config.PROTECTION_PAWNS : -1,
                     Config.PROTECTION_KNIGHTS : -1,
                     Config.UNPROTECTED_PAWNS : -1,
                     Config.UNPROTECTED_KNIGHTS : -1,
                     Config.UPGRADE_TO_KNIGHT : -1,
                     Config.BLOCKED_FIGURES : -1,
                     Config.MAT_PAWN : -1,
                     Config.MAT_KNIGHT : -1,
                     Config.ENDGAME_MAT_PAWN : -1,
                     Config.ENDGAME_MAT_KNIGHT : -1,
                     Config.PIECESQUARE_TABLE_PAWN_Blue: {},
                     Config.PIECESQUARE_TABLE_KNIGHT_Blue: {},
                     Config.PIECESQUARE_TABLE_PAWN_Red: {},
                     Config.PIECESQUARE_TABLE_KNIGHT_Red: {},
                     Config.MaxPlayer : Player.NoOne}
    
    __RANGE = np.array([1,6,1,1],dtype=np.uint64)
    __ZERO = np.uint64(0)
    
    #NEEDED: Total Order Featurescores
    #e.g. Materials > Mobility ... and so on
    def __init__(self,config: dict):
        """Init Evalfunction with config and set Player

        Args:
            config (dict): from scoreConfig_evalFunc.py please choose config
            player : from model.py use Player enum class. Defaults to Player.Red.
        """
        #TODO
        
        #Bitte config nur aus scoreConfig_evalFunc.py verwenden
        if (len(self._CONFIG_DICT) != len(config)):
            raise ValueError("Configs do not have same size")
        self._CONFIG_DICT = self._CONFIG_DICT | config
        #check __Config if all constants got new values
        vals = self._CONFIG_DICT.values()
        if(len(list(filter(lambda x: x==-1, vals)))>0):
            raise ValueError("Config is not complete, you may forgot a key-value pair, value -1 means not set")
        if(len(self._CONFIG_DICT[Config.PIECESQUARE_TABLE_PAWN_Blue]) == 0 or
           len(self._CONFIG_DICT[Config.PIECESQUARE_TABLE_KNIGHT_Blue]) == 0 or
           len(self._CONFIG_DICT[Config.PIECESQUARE_TABLE_PAWN_Red]) == 0 or
           len(self._CONFIG_DICT[Config.PIECESQUARE_TABLE_KNIGHT_Red]) == 0 ):
            raise ValueError("Config: PIECESQUARE_TABLE_\\{Pawn,Knight\\} Dictionary not set")
        if(self._CONFIG_DICT[Config.MaxPlayer] == Player.NoOne):
            raise ValueError("MaxPlayer not set")
        
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
        self._TURNOPTIONS += size
   
    def _computeTurnOptions(self):
        """Computes the Value of the Turnoptions
            After calling this Function, will reset Turnoptions to 0
        Returns:
            Int:
        """
        val = self._TURNOPTIONS*self._CONFIG_DICT[Config.TURN_OPTIONS]
        self._TURNOPTIONS = 0
        return val
    
    # Muss evtl. später optimiert werden, es könnte sein, dass die Loops (initialisierung) langsam sind
    
    def _moveIsNeighbourOfStartPos(self,startPos: np.uint64, targetPos:np.uint64):
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
    
    def _pieceSquareTable(self,startPos: np.uint64, targetmoves: list[np.uint64], board: list[np.uint64], boardcommands: list[BoardCommand]):
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
        targetmoves = [targetmoves]
        targetScores = Counter({})
        
        if(startPos & board[GameState._ZARR_INDEX_R_PAWNS] & ~( board[GameState._ZARR_INDEX_B_KNIGHTS] | board[GameState._ZARR_INDEX_R_KNIGHTS]) != 0):
            targetScores.update(
                {key: self._CONFIG_DICT[Config.PIECESQUARE_TABLE_PAWN_Red][MoveLib.BitsToPosition(key)] 
                 for key in targetmoves if self._moveIsNeighbourOfStartPos(startPos, key)} )
        elif (startPos & board[GameState._ZARR_INDEX_R_KNIGHTS] != 0):
            targetScores.update(
                {key: self._CONFIG_DICT[Config.PIECESQUARE_TABLE_KNIGHT_Red][MoveLib.BitsToPosition(key)] 
                 for key in targetmoves if not self._moveIsNeighbourOfStartPos(startPos, key)})  
        elif(startPos & board[GameState._ZARR_INDEX_B_PAWNS] & 
             ~( board[GameState._ZARR_INDEX_R_KNIGHTS]|board[GameState._ZARR_INDEX_B_KNIGHTS]) != 0):
            targetScores.update(
                {key: self._CONFIG_DICT[Config.PIECESQUARE_TABLE_PAWN_Blue][MoveLib.BitsToPosition(key)] 
                 for key in targetmoves if self._moveIsNeighbourOfStartPos(startPos, key)})
        elif (startPos & board[GameState._ZARR_INDEX_B_KNIGHTS] != 0):
            targetScores.update(
                {key: self._CONFIG_DICT[Config.PIECESQUARE_TABLE_KNIGHT_Blue][MoveLib.BitsToPosition(key)] 
                 for key in targetmoves if not self._moveIsNeighbourOfStartPos(startPos, key)})
            
        if(len(targetScores) == 0):
            raise ValueError("Error in MoveList, please check Zuggenerator, move=", MoveLib.move(startPos, targetmoves[0],3))
        scoreList.append((startPos, targetScores, boardcommands))
        self.__turnOptions(len(targetmoves))
            
                
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
    
    def _materialPoints(self, board:list[np.uint64]):
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
        #count Blue Pawns
        bp = bin(board[GameState._ZARR_INDEX_B_PAWNS] & (~board[GameState._ZARR_INDEX_R_KNIGHTS]))[2:].count("1")*self._CONFIG_DICT[Config.MAT_PAWN]
        #count Blue Knights
        bk = bin(board[GameState._ZARR_INDEX_B_KNIGHTS])[2:].count("1")*self._CONFIG_DICT[Config.MAT_KNIGHT]
        #count Red Pawns
        rp = bin(board[GameState._ZARR_INDEX_R_PAWNS] & (~board[GameState._ZARR_INDEX_B_KNIGHTS]))[2:].count("1")*self._CONFIG_DICT[Config.MAT_PAWN]
        #count Red Knights
        rk = bin(board[GameState._ZARR_INDEX_R_KNIGHTS])[2:].count("1")*self._CONFIG_DICT[Config.MAT_KNIGHT]
        #print("MaterialPoints:", rp,rk,bp,bk)
        return rp+rk-bp-bk if self._CONFIG_DICT[Config.MaxPlayer] == Player.Red else bp+bk-rp-rk
    
    def computeOverallScore(self, moveList: list, board:list[np.uint64]):
        """Computes the total Score of current State
           MoveList only read once!
        Args:
            moveList: list((np.uint64, np.uint64,list[BoardCommand]))
                    -> list(index, figure, BoardCommandlist)
                    The list from alpha/beta-generation() from Zuggenerator 
            board (list[np.uint64]): Bitboard
            
        Returns:
            List(tupel()): (fromPos:np.uint64, targetPos:np.uint64, moveScore:int , Total score: int)
            Ordering: Move with highest overall score at the beginning of the list.
               
        """
        
            
        scoredList = ScoredMoveList()
        if( len(moveList) == 0):
            return scoredList
        #ScoreListForMeging can be merged with other Dict -> Count(Dict)
        # so, that values are added on same keys
        # e.g. dictA + dictB 
        tempScore = ScoreListForMerging()
        totalScore = 0
        for index in moveList:
            tempScore.append(self._pieceSquareTable(index[0],index[1], board,index[2]))
            #TODO add some more Features
            
        #TODO
        #totalScore += self._computeTurnOptions()
        totalScore += self._materialPoints(board)
        totalScore += self._computeActualPositionalPoints(board)
        #print("totalscore :", totalScore)
        #print("tempscore:\n", tempScore)
        #TODO Last processing
        for (startpos,adict,bc) in tempScore:
            scoredList.append([(startpos,targetPos, adict[targetPos],totalScore+adict[targetPos],bc) for targetPos in adict])
        scoredList.sort()
        self.prettyPrintScorelist(scoredList)
        return scoredList
    
    def _computeActualPositionalPoints(self, board: list[np.uint64]):
        positionPointsMax = 0
        positionPointsMin = 0
        positionPoints = 0
        
        maxPlayer =self._CONFIG_DICT[Config.MaxPlayer]
        
        maxPawnPos      = board[GameState._ZARR_INDEX_R_PAWNS   if maxPlayer == Player.Red else GameState._ZARR_INDEX_B_PAWNS]
        maxKnightsPos   = board[GameState._ZARR_INDEX_R_KNIGHTS if maxPlayer == Player.Red else GameState._ZARR_INDEX_B_KNIGHTS]
        
        minPawnsPos     = board[GameState._ZARR_INDEX_B_PAWNS   if maxPlayer == Player.Red else GameState._ZARR_INDEX_R_PAWNS]
        minKnightsPos   = board[GameState._ZARR_INDEX_B_KNIGHTS if maxPlayer == Player.Red else GameState._ZARR_INDEX_R_KNIGHTS]
        
        if(maxPawnPos):
            maxPawnsBits   = MoveGenerator.getBitPositions(maxPawnPos)
            FigPosStrings = [MoveLib.BitsToPosition(bits) for bits in maxPawnsBits]
            for figPos in FigPosStrings:
                positionPointsMax += self._CONFIG_DICT[Config.PIECESQUARE_TABLE_PAWN_Red if maxPlayer == Player.Red else Config.PIECESQUARE_TABLE_PAWN_Blue][figPos]
        
        if(maxKnightsPos):
            maxKnightBits  = MoveGenerator.getBitPositions(maxKnightsPos)
            FigPosStrings = [MoveLib.BitsToPosition(bits) for bits in maxKnightBits]
            for figPos in FigPosStrings:
                positionPointsMax += self._CONFIG_DICT[Config.PIECESQUARE_TABLE_KNIGHT_Red if maxPlayer == Player.Red else Config.PIECESQUARE_TABLE_KNIGHT_Blue][figPos]
        
        if(minPawnsPos):
            minPawnsBits   = MoveGenerator.getBitPositions(minPawnsPos)
            FigPosStrings = [MoveLib.BitsToPosition(bits) for bits in minPawnsBits]
            for figPos in FigPosStrings:
                positionPointsMin += self._CONFIG_DICT[Config.PIECESQUARE_TABLE_PAWN_Blue if maxPlayer == Player.Red else Config.PIECESQUARE_TABLE_PAWN_Red][figPos]
        if(minKnightsPos):
            minKnightBits  = MoveGenerator.getBitPositions(minKnightsPos)
            FigPosStrings = [MoveLib.BitsToPosition(bits) for bits in minKnightBits]
            for figPos in FigPosStrings:
                positionPointsMin += self._CONFIG_DICT[Config.PIECESQUARE_TABLE_KNIGHT_Blue if maxPlayer == Player.Red else Config.PIECESQUARE_TABLE_KNIGHT_Red][figPos]
        
        positionPoints = positionPointsMax - positionPointsMin
        
        return positionPoints
    
    def prettyPrintScorelist(self,list:ScoredMoveList):
        if(len(list) != 0):
            print("Scorelist:")
            for s,t,v,u,z in list:
                print((MoveLib.move(s,t,3),"movescore=",v,"totalscore=",u,z))
            #print([(MoveLib.move(s,t,3),"movescore=",v,"totalscore=",u,z)for s,t,v,u,z in list])
            print("")

    
        