import numpy as np    
"""All Versions have to return a Dictionary
"""
class ScoreConfig:
    def reversePsqT(dictToReverse: dict):
        """Reverse the PieceSquareTable for the opponent Player

        Args:
            dictToReverse (dict):
        Returns:
            dict: new Dict in reverse Ordering
        """
        if(len(dictToReverse)!= 64):
            raise ValueError("Dict size not 64")
        orderCol = {"A":"B","B":"C","C":"D","D":"E","E":"F","F":"G","G":"H","H":"A"}
        reverseRow = {1:"8",2:"7",3:"6",4:"5",5:"4",6:"3",7:"2",8:"1"}
        newDictionary = {}
        for row in np.arange(1,9):
            newDictionary["A"+reverseRow[row]]= dictToReverse["A"+str(row)]
            newDictionary["B"+reverseRow[row]]= dictToReverse["B"+str(row)]
            newDictionary["C"+reverseRow[row]]= dictToReverse["C"+str(row)]
            newDictionary["D"+reverseRow[row]]= dictToReverse["D"+str(row)]
            newDictionary["E"+reverseRow[row]]= dictToReverse["E"+str(row)]
            newDictionary["F"+reverseRow[row]]= dictToReverse["F"+str(row)]
            newDictionary["G"+reverseRow[row]]= dictToReverse["G"+str(row)]
            newDictionary["H"+reverseRow[row]]= dictToReverse["H"+str(row)]
        return newDictionary
    
    def Version0(self):
        """Tests for Piece Square Table

        Returns:
            dict: Configuration for evalFunc
        """
        psqTPawnBlue = {    
            "A8":0,     "B8":0,   "C8":0,     "D8":0,     "E8":0,     "F8":0,     "G8":0,     "H8":0,
            "A7":1,     "B7":5,   "C7":5,     "D7":5,     "E7":5,     "F7":5,     "G7":5,     "H7":1,
            "A6":5,     "B6":10,  "C6":10,    "D6":10,    "E6":10,    "F6":10,    "G6":10,    "H6":5,
            "A5":5,     "B5":20,  "C5":20,    "D5":20,    "E5":20,    "F5":20,    "G5":20,    "H5":5,
            "A4":5,     "B4":30,  "C4":30,    "D4":30,    "E4":30,    "F4":30,    "G4":30,    "H4":5,
            "A3":5,     "B3":40,  "C3":40,    "D3":40,    "E3":40,    "F3":40,    "G3":40,    "H3":5,
            "A2":5,     "B2":50,  "C2":50,    "D2":50,    "E2":50,    "F2":50,    "G2":50,    "H2":5,
            "A1":0,     "B1":100, "C1":100,   "D1":100,   "E1":100,   "F1":100,   "G1":100,   "H1":0,
        }
        psqTPawnRed = self.reversePsqT(psqTPawnBlue)
        psqTKnightBlue = {    
            "A8":0,     "B8":3,     "C8":5,     "D8":5,     "E8":5,     "F8":5,     "G8":3,     "H8":0,
            "A7":5,     "B7":10,    "C7":10,    "D7":10,    "E7":10,    "F7":10,    "G7":10,    "H7":5,
            "A6":10,    "B6":15,    "C6":20,    "D6":20,    "E6":20,    "F6":20,    "G6":15,    "H6":10,
            "A5":20,    "B5":25,    "C5":30,    "D5":30,    "E5":30,    "F5":30,    "G5":25,    "H5":20,
            "A4":30,    "B4":35,    "C4":40,    "D4":40,    "E4":40,    "F4":40,    "G4":35,    "H4":30,
            "A3":40,    "B3":40,    "C3":50,    "D3":50,    "E3":50,    "F3":50,    "G3":40,    "H3":40,
            "A2":30,    "B2":30,    "C2":30,    "D2":35,    "E2":35,    "F2":30,    "G2":30,    "H2":30,
            "A1":0,     "B1":100,   "C1":100,   "D1":100,   "E1":100,   "F1":100,   "G1":100,   "H1":0,
        }
        psqTKnightRed =  self.reversePsqT(psqTKnightBlue)
        
        
        config =    {"MOBILITY" : 0,
                     "PROTECTION_PAWNS" : 0,
                     "PROTECTION_KNIGHTS" : 0,
                     "UNPROTECTED_PAWNS" : 0,
                     "UNPROTECTED_KNIGHTS" : 0,
                     "UPGRADE_TO_KNIGHT" : 0,
                     "BLOCKED_FIGURES" : 0,
                     "MAT_PAWN" : 0,
                     "MAT_KNIGHT" : 0,
                     "ENDGAME_MAT_PAWN" : 0,
                     "ENDGAME_MAT_KNIGHT" : 0,
                     "PIECESQUARE_TABLE_PAWN_Blue": psqTPawnBlue,
                     "PIECESQUARE_TABLE_KNIGHT_Blue": psqTKnightBlue,
                     "PIECESQUARE_TABLE_PAWN_Red": psqTPawnRed,
                     "PIECESQUARE_TABLE_KNIGHT_Red": psqTKnightRed}
        return config