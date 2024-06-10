import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
import copy  
from collections import Counter
from src.model import*  
from src.moveLib import*
from src.moveGenerator import MoveGenerator as mg

"""All Versions have to return a Dictionary
"""
class ScoreConfig:
    __REVERSEROW = {1:"8",2:"7",3:"6",4:"5",5:"4",6:"3",7:"2",8:"1"}
    _ALL_FIELDS_IN_BOARD = [MoveLib.BitsToPosition(np.uint64(2**x)) for x in range(64)]
    _ZERO_DICT =Counter({   "A8":0,     "B8":0,   "C8":0,     "D8":0,     "E8":0,       "F8":0,     "G8":0,     "H8":0,
                            "A7":0,     "B7":0,   "C7":0,     "D7":0,     "E7":0,     "F7":0,     "G7":0,     "H7":0,
                            "A6":0,     "B6":0,  "C6":0,     "D6":0,     "E6":0,     "F6":0,     "G6":0,     "H6":0,
                            "A5":0,     "B5":0,  "C5":0,     "D5":0,     "E5":0,     "F5":0,     "G5":0,     "H5":0,
                            "A4":0,     "B4":0,  "C4":0,     "D4":0,     "E4":0,     "F4":0,     "G4":0,     "H4":0,
                            "A3":0,     "B3":0,  "C3":0,     "D3":0,     "E3":0,     "F3":0,     "G3":0,     "H3":0,
                            "A2":0,     "B2":0,  "C2":0,     "D2":0,     "E2":0,     "F2":0,     "G2":0,     "H2":0,
                            "A1":0,     "B1":0,  "C1":0,     "D1":0,     "E1":0,     "F1":0,     "G1":0,     "H1":0})
    
    
    @classmethod
    def reversePsqT(self,dictToReverse: dict):
        """Reverse the PieceSquareTable for the opponent Player

        Args:
            dictToReverse (dict):
        Returns:
            dict: new Dict in reverse Ordering
        """
        if(len(dictToReverse)!= 64):
            raise ValueError("Dict size not 64")
        
        newDictionary = Counter({})
        for row in np.arange(1,9):
            newDictionary["A"+self.__REVERSEROW[row]]= dictToReverse["A"+str(row)]
            newDictionary["B"+self.__REVERSEROW[row]]= dictToReverse["B"+str(row)]
            newDictionary["C"+self.__REVERSEROW[row]]= dictToReverse["C"+str(row)]
            newDictionary["D"+self.__REVERSEROW[row]]= dictToReverse["D"+str(row)]
            newDictionary["E"+self.__REVERSEROW[row]]= dictToReverse["E"+str(row)]
            newDictionary["F"+self.__REVERSEROW[row]]= dictToReverse["F"+str(row)]
            newDictionary["G"+self.__REVERSEROW[row]]= dictToReverse["G"+str(row)]
            newDictionary["H"+self.__REVERSEROW[row]]= dictToReverse["H"+str(row)]
        return newDictionary
    @classmethod
    def PsqTMinus(self, dictFromBetaMinimizer: dict):
        if(len(dictFromBetaMinimizer)!= 64):
            raise ValueError("Dict size not 64")
        newDict = {}
        for row in np.arange(1,9):
            newDict["A"+str(row)]= -dictFromBetaMinimizer["A"+str(row)]
            newDict["B"+str(row)]= -dictFromBetaMinimizer["B"+str(row)]
            newDict["C"+str(row)]= -dictFromBetaMinimizer["C"+str(row)]
            newDict["D"+str(row)]= -dictFromBetaMinimizer["D"+str(row)]
            newDict["E"+str(row)]= -dictFromBetaMinimizer["E"+str(row)]
            newDict["F"+str(row)]= -dictFromBetaMinimizer["F"+str(row)]
            newDict["G"+str(row)]= -dictFromBetaMinimizer["G"+str(row)]
            newDict["H"+str(row)]= -dictFromBetaMinimizer["H"+str(row)]
        return newDict
    
    @classmethod
    def Version0(self, maxPlayer: Player,player:Player, board =[]):
        """Tests for Piece Square Table
           Only for on Red Player the Piece Square Table (Pawn and Knight) is needed, 
        Returns:
            dict: Configuration for evalFunc
        """
        psqTPawnRed = {    
            "A8":0,     "B8":0,   "C8":0,     "D8":0,     "E8":0,     "F8":0,     "G8":0,     "H8":0,
            "A7":1,     "B7":5,   "C7":5,     "D7":5,     "E7":5,     "F7":5,     "G7":5,     "H7":1,
            "A6":5,     "B6":10,  "C6":10,    "D6":10,    "E6":10,    "F6":10,    "G6":10,    "H6":5,
            "A5":5,     "B5":20,  "C5":20,    "D5":20,    "E5":20,    "F5":20,    "G5":20,    "H5":5,
            "A4":5,     "B4":30,  "C4":30,    "D4":30,    "E4":30,    "F4":30,    "G4":30,    "H4":5,
            "A3":5,     "B3":40,  "C3":40,    "D3":40,    "E3":40,    "F3":40,    "G3":40,    "H3":5,
            "A2":5,     "B2":45,  "C2":50,    "D2":50,    "E2":50,    "F2":50,    "G2":45,    "H2":5,
            "A1":0,     "B1":100, "C1":100,   "D1":100,   "E1":100,   "F1":100,   "G1":100,   "H1":0,
        }
        psqTPawnBlue = self.reversePsqT(psqTPawnRed)
        psqTKnightRed = {    
            "A8":0,     "B8":3,     "C8":5,     "D8":5,     "E8":5,     "F8":5,     "G8":3,     "H8":0,
            "A7":5,     "B7":10,    "C7":10,    "D7":10,    "E7":10,    "F7":10,    "G7":10,    "H7":5,
            "A6":10,    "B6":15,    "C6":20,    "D6":20,    "E6":20,    "F6":20,    "G6":15,    "H6":10,
            "A5":20,    "B5":25,    "C5":30,    "D5":30,    "E5":30,    "F5":30,    "G5":25,    "H5":20,
            "A4":30,    "B4":35,    "C4":40,    "D4":40,    "E4":40,    "F4":40,    "G4":35,    "H4":30,
            "A3":40,    "B3":40,    "C3":50,    "D3":50,    "E3":50,    "F3":50,    "G3":40,    "H3":40,
            "A2":30,    "B2":30,    "C2":30,    "D2":35,    "E2":35,    "F2":30,    "G2":30,    "H2":30,
            "A1":0,     "B1":100,   "C1":100,   "D1":100,   "E1":100,   "F1":100,   "G1":100,   "H1":0,
        }
        psqTKnightBlue =  self.reversePsqT(psqTKnightRed)
        
        
        config =    {
                    Config.TURN_OPTIONS: 2,
                    Config.MAT_PAWN : 10,
                    Config.MAT_KNIGHT : 20,
                    Config.TOTAL_SCORE_RATING_PAWN_BLUE: psqTPawnBlue,
                    Config.TOTAL_SCORE_RATING_KNIGHT_BLUE: psqTKnightBlue,
                    Config.TOTAL_SCORE_RATING_PAWN_RED: psqTPawnRed,
                    Config.TOTAL_SCORE_RATING_KNIGHT_RED: psqTKnightRed,
                    Config.MaxPlayer: maxPlayer,
                    Config.Player: player ,
                    Config.CONFIGVERSION: self.Version0,
                    }
        return config
    
    @classmethod
    def Version1(self, maxPlayer: Player, player:Player, board = []):
        """Like Version0 but now with Materials and higher Scores.
           Just define only for Player Red the Piece Square Table (Pawn and Knight), 
        Returns:
            dict: Configuration for evalFunc
        """
        
        psqTPawnRed = {    
            "A8":0,     "B8":0,   "C8":0,     "D8":0,     "E8":0,     "F8":0,     "G8":0,     "H8":0,
            "A7":1,     "B7":5,   "C7":5,     "D7":5,     "E7":5,     "F7":5,     "G7":5,     "H7":1,
            "A6":5,     "B6":10,  "C6":10,    "D6":10,    "E6":10,    "F6":10,    "G6":10,    "H6":5,
            "A5":5,     "B5":20,  "C5":20,    "D5":20,    "E5":20,    "F5":20,    "G5":20,    "H5":5,
            "A4":5,     "B4":30,  "C4":30,    "D4":30,    "E4":30,    "F4":30,    "G4":30,    "H4":5,
            "A3":5,     "B3":40,  "C3":40,    "D3":40,    "E3":40,    "F3":40,    "G3":40,    "H3":5,
            "A2":5,     "B2":45,  "C2":50,    "D2":50,    "E2":50,    "F2":50,    "G2":45,    "H2":5,
            "A1":0,     "B1":10000,"C1":10000,  "D1":10000,  "E1":10000,  "F1":10000,  "G1":10000,  "H1":0,
        }
        psqTPawnBlue = self.reversePsqT(psqTPawnRed)
        psqTKnightRed = {    
            "A8":0,     "B8":3,     "C8":5,     "D8":5,     "E8":5,     "F8":5,     "G8":3,     "H8":0,
            "A7":5,     "B7":10,    "C7":10,    "D7":10,    "E7":10,    "F7":10,    "G7":10,    "H7":5,
            "A6":10,    "B6":15,    "C6":20,    "D6":20,    "E6":20,    "F6":20,    "G6":15,    "H6":10,
            "A5":20,    "B5":25,    "C5":30,    "D5":30,    "E5":30,    "F5":30,    "G5":25,    "H5":20,
            "A4":30,    "B4":35,    "C4":40,    "D4":40,    "E4":40,    "F4":40,    "G4":35,    "H4":30,
            "A3":40,    "B3":40,    "C3":50,    "D3":50,    "E3":50,    "F3":50,    "G3":40,    "H3":40,
            "A2":30,    "B2":30,    "C2":30,    "D2":35,    "E2":35,    "F2":30,    "G2":30,    "H2":30,
            "A1":0,     "B1":10000,  "C1":10000,  "D1":10000,  "E1":10000,  "F1":10000,  "G1":10000,  "H1":0,
        }
        psqTKnightBlue =  self.reversePsqT(psqTKnightRed)
        
        # if(maximizer == Player.Red):
        #     psqTPawnRed = self.PsqTMinus(psqTPawnRed)
        #     psqTKnightRed = self.PsqTMinus(psqTKnightRed)
        # else:
        #     psqTPawnBlue = self.PsqTMinus(psqTPawnBlue)
        #     psqTKnightBlue = self.PsqTMinus(psqTKnightBlue)
        
        
        config =    {
                    Config.TURN_OPTIONS: 2,
                    Config.MAT_PAWN : 10,
                    Config.MAT_KNIGHT : 20,
                    Config.TOTAL_SCORE_RATING_PAWN_BLUE: psqTPawnBlue,
                    Config.TOTAL_SCORE_RATING_KNIGHT_BLUE: psqTKnightBlue,
                    Config.TOTAL_SCORE_RATING_PAWN_RED: psqTPawnRed,
                    Config.TOTAL_SCORE_RATING_KNIGHT_RED: psqTKnightRed,
                    Config.MaxPlayer: maxPlayer,
                    Config.Player: player ,
                    Config.CONFIGVERSION: self.Version1,
                    }
        return config
    
    @classmethod
    def Version2(self,maxPlayer:Player, player: Player, board: list[np.uint64] = []):
        """now with extra scores on Fields with enemies
           and wider spread of points in piece square tables
           To update the Config recall Version2 with new Board
        Args:
            maxPlayer (Player): _description_
            Board (list[np.uint64], optional): _description_. Defaults to [].

        Returns:
            _type_: _description_
        """
        
        psqTPawnRed = Counter({    
            "A8":1,     "B8":1,     "C8":1,     "D8":1,     "E8":1,     "F8":1,     "G8":1,     "H8":1,
            "A7":1,     "B7":15,    "C7":15,    "D7":15,    "E7":15,    "F7":15,    "G7":15,    "H7":1,
            "A6":15,    "B6":30,    "C6":30,    "D6":30,    "E6":30,    "F6":30,    "G6":30,    "H6":15,
            "A5":15,    "B5":45,    "C5":45,    "D5":45,    "E5":45,    "F5":45,    "G5":45,    "H5":15,
            "A4":15,    "B4":60,    "C4":60,    "D4":60,    "E4":60,    "F4":60,    "G4":60,    "H4":15,
            "A3":15,    "B3":75,    "C3":75,    "D3":75,    "E3":75,    "F3":75,    "G3":75,    "H3":15,
            "A2":15,    "B2":90,    "C2":100,   "D2":100,   "E2":100,   "F2":100,   "G2":90,    "H2":15,
            "A1":1,     "B1":10000, "C1":10000, "D1":10000, "E1":10000, "F1":10000, "G1":10000, "H1":1,
        })
        psqTPawnBlue = self.reversePsqT(psqTPawnRed)
        psqTKnightRed = Counter({    
            "A8":1,     "B8":3,     "C8":5,     "D8":5,     "E8":5,     "F8":5,     "G8":3,     "H8":1,
            "A7":5,     "B7":15,    "C7":15,    "D7":15,    "E7":15,    "F7":15,    "G7":15,    "H7":5,
            "A6":20,    "B6":30,    "C6":35,    "D6":35,    "E6":35,    "F6":35,    "G6":30,    "H6":20,
            "A5":20,    "B5":45,    "C5":50,    "D5":50,    "E5":50,    "F5":50,    "G5":45,    "H5":20,
            "A4":30,    "B4":60,    "C4":75,    "D4":75,    "E4":75,    "F4":75,    "G4":60,    "H4":30,
            "A3":40,    "B3":75,    "C3":100,   "D3":100,   "E3":100,   "F3":100,   "G3":75,    "H3":40,
            "A2":20,    "B2":25,    "C2":50,    "D2":50,    "E2":50,    "F2":50,    "G2":25,    "H2":20,
            "A1":1,     "B1":10000, "C1":10000, "D1":10000, "E1":10000, "F1":10000, "G1":10000, "H1":1,
        })
        psqTKnightBlue =  self.reversePsqT(psqTKnightRed)
        
        hitPointsForPawns = 100
        hitPointsForKnights = 200
        
        blueScoreHitPawns   = dict({})
        blueScoreHitKnights = dict({})
        redScoreHitPawns    = dict({})
        redScoreHitKnights  = dict({})
        
        if(len(board)==4):
            blueScoreHitPawns,blueScoreHitKnights = self.createScores(self,Player.Blue,board,hitPointsForPawns,hitPointsForKnights)
            redScoreHitPawns,redScoreHitKnights = self.createScores(self,Player.Red,board,hitPointsForPawns,hitPointsForKnights)
        
        config =    {
                     Config.TURN_OPTIONS: 2,
                     Config.MAT_PAWN : 10,
                     Config.MAT_KNIGHT : 20,
                     Config.TOTAL_SCORE_RATING_PAWN_BLUE: psqTPawnBlue+(blueScoreHitPawns or Counter({"A1":0})),
                     Config.TOTAL_SCORE_RATING_KNIGHT_BLUE: psqTKnightBlue+(blueScoreHitKnights or Counter({"A1":0})),
                     Config.TOTAL_SCORE_RATING_PAWN_RED: psqTPawnRed+(redScoreHitPawns or Counter({"A1":0})),
                     Config.TOTAL_SCORE_RATING_KNIGHT_RED: psqTKnightRed+(redScoreHitKnights or Counter({"A1":0})),
                     Config.MaxPlayer : maxPlayer,
                     Config.Player : player,
                     Config.CONFIGVERSION: self.Version2}
        return config
    
    def createScores(self,player:Player, board: list[np.uint64], scoreP: int,scoreK):
        """ Creates Scores according to enemy Positions

        Args:
            player (Player): use model.py Player
            board (list[np.uint64]): Representing the Boardstate
            scoreP (int):  Score for enemy pawn positions
            scoreK (_type_): Score for enemy knight positions

        Raises:
            ValueError: raised if Player is not Red or Blue

        Returns:
            tuple[dict,dict]: (scoreDictPawns, scoreDictKnights)
        """
        scoreDictPawns = Counter({"A8": 0, "B8": 0, "C8": 0, "D8": 0, "E8": 0, "F8": 0, "G8": 0, "H8": 0,
                                  "A7": 0, "B7": 0, "C7": 0, "D7": 0, "E7": 0, "F7": 0, "G7": 0, "H7": 0,
                                  "A6": 0, "B6": 0, "C6": 0, "D6": 0, "E6": 0, "F6": 0, "G6": 0, "H6": 0,
                                  "A5": 0, "B5": 0, "C5": 0, "D5": 0, "E5": 0, "F5": 0, "G5": 0, "H5": 0,
                                  "A4": 0, "B4": 0, "C4": 0, "D4": 0, "E4": 0, "F4": 0, "G4": 0, "H4": 0,
                                  "A3": 0, "B3": 0, "C3": 0, "D3": 0, "E3": 0, "F3": 0, "G3": 0, "H3": 0,
                                  "A2": 0, "B2": 0, "C2": 0, "D2": 0, "E2": 0, "F2": 0, "G2": 0, "H2": 0,
                                  "A1": 0, "B1": 0, "C1": 0, "D1": 0, "E1": 0, "F1": 0, "G1": 0, "H1": 0})
        scoreDictKnights = Counter({"A8": 0, "B8": 0, "C8": 0, "D8": 0, "E8": 0, "F8": 0, "G8": 0, "H8": 0,
                                    "A7": 0, "B7": 0, "C7": 0, "D7": 0, "E7": 0, "F7": 0, "G7": 0, "H7": 0,
                                    "A6": 0, "B6": 0, "C6": 0, "D6": 0, "E6": 0, "F6": 0, "G6": 0, "H6": 0,
                                    "A5": 0, "B5": 0, "C5": 0, "D5": 0, "E5": 0, "F5": 0, "G5": 0, "H5": 0,
                                    "A4": 0, "B4": 0, "C4": 0, "D4": 0, "E4": 0, "F4": 0, "G4": 0, "H4": 0,
                                    "A3": 0, "B3": 0, "C3": 0, "D3": 0, "E3": 0, "F3": 0, "G3": 0, "H3": 0,
                                    "A2": 0, "B2": 0, "C2": 0, "D2": 0, "E2": 0, "F2": 0, "G2": 0, "H2": 0,
                                    "A1": 0, "B1": 0, "C1": 0, "D1": 0, "E1": 0, "F1": 0, "G1": 0, "H1": 0})
        if(Player.Red == player):
                bluePawnsPos = board[GameState._ZARR_INDEX_B_PAWNS]
                blueKnightsPos = board[GameState._ZARR_INDEX_B_KNIGHTS]
                for pos in mg.getBitPositions(bluePawnsPos):
                    scoreDictPawns[MoveLib.BitsToPosition(pos)] = scoreP
                for pos in mg.getBitPositions(blueKnightsPos):
                    scoreDictKnights[MoveLib.BitsToPosition(pos)] = scoreK
        elif(Player.Blue == player):
                redPawnsPos = board[GameState._ZARR_INDEX_R_PAWNS]
                redKnightsPos = board[GameState._ZARR_INDEX_R_KNIGHTS]
                for pos in mg.getBitPositions(redPawnsPos):
                    #print(pos,MoveLib.BitsToPosition(pos))
                    scoreDictPawns[MoveLib.BitsToPosition(pos)] = scoreP
                for pos in mg.getBitPositions(redKnightsPos):
                    scoreDictKnights[MoveLib.BitsToPosition(pos)] = scoreK
        else:
            raise ValueError("Player is not valid")
        return (scoreDictPawns,scoreDictKnights)
    
  
        