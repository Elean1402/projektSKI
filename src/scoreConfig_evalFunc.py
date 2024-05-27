import numpy as np  
from src.model import*  
"""All Versions have to return a Dictionary
"""
class ScoreConfig:
    __REVERSEROW = {1:"8",2:"7",3:"6",4:"5",5:"4",6:"3",7:"2",8:"1"}
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
        
        newDictionary = {}
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
    def Version0(self):
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
        
        
        config =    {Config.MOBILITY : 0,
                     Config.TURN_OPTIONS: 2,
                     Config.PROTECTION_PAWNS : 0,
                     Config.PROTECTION_KNIGHTS : 0,
                     Config.UNPROTECTED_PAWNS : 0,
                     Config.UNPROTECTED_KNIGHTS : 0,
                     Config.UPGRADE_TO_KNIGHT : 0,
                     Config.BLOCKED_FIGURES : 0,
                     Config.MAT_PAWN : 0,
                     Config.MAT_KNIGHT : 0,
                     Config.ENDGAME_MAT_PAWN : 0,
                     Config.ENDGAME_MAT_KNIGHT : 0,
                     Config.PIECESQUARE_TABLE_PAWN_Blue: psqTPawnBlue,
                     Config.PIECESQUARE_TABLE_KNIGHT_Blue: psqTKnightBlue,
                     Config.PIECESQUARE_TABLE_PAWN_Red: psqTPawnRed,
                     Config.PIECESQUARE_TABLE_KNIGHT_Red: psqTKnightRed}
        return config
    
    @classmethod
    def Version1(self):
        """Like Version0 but now with Materials
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
        
        
        config =    {Config.MOBILITY : 0,
                     Config.TURN_OPTIONS: 2,
                     Config.PROTECTION_PAWNS : 0,
                     Config.PROTECTION_KNIGHTS : 0,
                     Config.UNPROTECTED_PAWNS : 0,
                     Config.UNPROTECTED_KNIGHTS : 0,
                     Config.UPGRADE_TO_KNIGHT : 0,
                     Config.BLOCKED_FIGURES : 0,
                     Config.MAT_PAWN : 10,
                     Config.MAT_KNIGHT : 20,
                     Config.ENDGAME_MAT_PAWN : 0,
                     Config.ENDGAME_MAT_KNIGHT : 0,
                     Config.PIECESQUARE_TABLE_PAWN_Blue: psqTPawnBlue,
                     Config.PIECESQUARE_TABLE_KNIGHT_Blue: psqTKnightBlue,
                     Config.PIECESQUARE_TABLE_PAWN_Red: psqTPawnRed,
                     Config.PIECESQUARE_TABLE_KNIGHT_Red: psqTKnightRed}
        return config