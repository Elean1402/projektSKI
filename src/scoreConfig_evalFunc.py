import numpy as np    
"""All Versions have to return a Dictionary
"""
class ScoreConfig:
    
    def Version1():
        config =    {"MOBILITY" : -1,
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
                     "PIECESQUARE_TABLE_PAWN": np.uint64(0),
                     "PIECESQUARE_TABLE_KNIGHT": np.uint64(0)}
        return config