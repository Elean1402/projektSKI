import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.gamestate import GameState
from src.model import *
from src.moveLib import MoveLib
from collections import Counter
from src.moveGenerator import MoveGenerator
from src.scoreConfig_evalFunc import ScoreConfig
import numpy as np




class EvalFunction:
    # Score distribution (not final) of implemented features
    _TURNOPTIONS=0
    _player = 0
    _CONFIG_DICT = { 
                     Config.TURN_OPTIONS: -1,
                     Config.MAT_PAWN : -1,
                     Config.MAT_KNIGHT : -1,
                     Config.TOTAL_SCORE_RATING_PAWN_BLUE: {},
                     Config.TOTAL_SCORE_RATING_KNIGHT_BLUE: {},
                     Config.TOTAL_SCORE_RATING_PAWN_RED: {},
                     Config.TOTAL_SCORE_RATING_KNIGHT_RED: {},
                     Config.MaxPlayer : Player.NoOne,
                     Config.Player : Player.NoOne,
                     Config.CONFIGVERSION: None
                     }

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
        if(len(self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_PAWN_BLUE]) == 0 or
           len(self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_KNIGHT_BLUE]) == 0 or
           len(self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_PAWN_RED]) == 0 or
           len(self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_KNIGHT_RED]) == 0 ):
            raise ValueError("Config: PIECESQUARE_TABLE_\\{Pawn,Knight\\} Dictionary not set")
        if(self._CONFIG_DICT[Config.Player] == Player.NoOne):
            raise ValueError("Player not set")
        if(self._CONFIG_DICT[Config.MaxPlayer] == Player.NoOne):
            raise ValueError("MaxPlayer not set")
        if(self._CONFIG_DICT[Config.CONFIGVERSION] == None):
            raise ValueError("CONFIGVERSION NOT SET")
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
    
    def _scoreRating(self,startPos: np.uint64, targetmoves: list[np.uint64], board: list[np.uint64], boardcommands: list[BoardCommand]):
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
                {key: self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_PAWN_RED][MoveLib.BitsToPosition(key)]
                 for key in targetmoves if self._moveIsNeighbourOfStartPos(startPos, key)} )
        elif (startPos & board[GameState._ZARR_INDEX_R_KNIGHTS] != 0):
            targetScores.update(
                {key: self._CONFIG_DICT[  Config.TOTAL_SCORE_RATING_KNIGHT_RED][MoveLib.BitsToPosition(key)]
                 for key in targetmoves if not self._moveIsNeighbourOfStartPos(startPos, key)})
        elif(startPos & board[GameState._ZARR_INDEX_B_PAWNS] &
             ~( board[GameState._ZARR_INDEX_R_KNIGHTS]|board[GameState._ZARR_INDEX_B_KNIGHTS]) != 0):
            targetScores.update(
                {key: self._CONFIG_DICT[  Config.TOTAL_SCORE_RATING_PAWN_BLUE][MoveLib.BitsToPosition(key)]
                 for key in targetmoves if self._moveIsNeighbourOfStartPos(startPos, key)})
        elif (startPos & board[GameState._ZARR_INDEX_B_KNIGHTS] != 0):
            targetScores.update(
                {key: self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_KNIGHT_BLUE][MoveLib.BitsToPosition(key)]
                 for key in targetmoves if not self._moveIsNeighbourOfStartPos(startPos, key)})

        if(len(targetScores) == 0):
            raise ValueError("Error in MoveList, please check Zuggenerator, move=", MoveLib.move(startPos, targetmoves[0],3))
        scoreList.append((startPos, targetScores, boardcommands))
        self.__turnOptions(len(targetmoves))


        return scoreList

    def _updateConfig(self,player:Player, board:list[np.uint64]):
        updatedConf = self._CONFIG_DICT[Config.CONFIGVERSION](self._CONFIG_DICT[Config.MaxPlayer],player,board)
        self._CONFIG_DICT = updatedConf
    
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
        #print("config MaxPlayer:", self._CONFIG_DICT[Config.MaxPlayer])
        return rp+rk-bp-bk if self._CONFIG_DICT[Config.MaxPlayer] == Player.Red else bp+bk-rp-rk
    
    def computeOverallScore(self, moveList: list, board:list[np.uint64],printList= False, returnSortedList= True )-> ScoredMoveList:
        """Computes the total Score of current State
           MoveList only read once!
        Args:
            moveList: list((np.uint64, np.uint64,list[BoardCommand]))
                    -> list(index, figure, BoardCommandlist)
                    The list from alpha/beta-generation() from Zuggenerator
            board (list[np.uint64]): Bitboard

        Returns:
            List(tupel()): (fromPos:np.uint64, targetPos:np.uint64, moveScore:int , Total score: int, BoardCommandlist: list[BoardCommand])
            Ordering: Move with highest overall score at the beginning of the list.
            If no move is possible, then return [(0,0,0,totalScore,[])]
        """


        scoredList = ScoredMoveList()
        totalScore = 0
        if( len(moveList) == 0):
            totalScore += self._materialPoints(board)
            totalScore += self._computeActualPositionalPoints(board)
            scoredList.append((np.uint64(0),np.uint64(0),int(0),int(totalScore),[]))
            return scoredList

        tempScore = ScoreListForMerging()

        #Update config to get new scores according to board
        self._updateConfig(self._CONFIG_DICT[Config.Player],board)

        for index in moveList:
            tempScore.append(self._scoreRating(index[0],index[1], board,index[2]))
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

        if(returnSortedList):
            scoredList.sort()



        if(printList):
            self.prettyPrintScorelist(scoredList)
            #print(scoredList)
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
                positionPointsMax += self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_PAWN_RED if maxPlayer == Player.Red else   Config.TOTAL_SCORE_RATING_PAWN_BLUE][figPos]
        
        if(maxKnightsPos):
            maxKnightBits  = MoveGenerator.getBitPositions(maxKnightsPos)
            FigPosStrings = [MoveLib.BitsToPosition(bits) for bits in maxKnightBits]
            for figPos in FigPosStrings:
                positionPointsMax += self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_KNIGHT_RED if maxPlayer == Player.Red else Config.TOTAL_SCORE_RATING_KNIGHT_BLUE][figPos]
        
        if(minPawnsPos):
            minPawnsBits   = MoveGenerator.getBitPositions(minPawnsPos)
            FigPosStrings = [MoveLib.BitsToPosition(bits) for bits in minPawnsBits]
            for figPos in FigPosStrings:
                positionPointsMin += self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_PAWN_BLUE if maxPlayer == Player.Red else   Config.TOTAL_SCORE_RATING_PAWN_RED][figPos]
        if(minKnightsPos):
            minKnightBits  = MoveGenerator.getBitPositions(minKnightsPos)
            FigPosStrings = [MoveLib.BitsToPosition(bits) for bits in minKnightBits]
            for figPos in FigPosStrings:
                positionPointsMin += self._CONFIG_DICT[Config.TOTAL_SCORE_RATING_KNIGHT_BLUE if maxPlayer == Player.Red else   Config.TOTAL_SCORE_RATING_KNIGHT_RED][figPos]
        
        positionPoints = positionPointsMax - positionPointsMin
        
        return positionPoints
    
    def prettyPrintScorelist(self,list:ScoredMoveList):
        if(len(list) != 0):
            print("Scorelist:")
            for s,t,v,u,z in list:
                print((MoveLib.move(s,t,3),"movescore=",v,"totalscore=",u,z))
            #print([(MoveLib.move(s,t,3),"movescore=",v,"totalscore=",u,z)for s,t,v,u,z in list])
            print("")
            
    

    
            
        