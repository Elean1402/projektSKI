import os
import sys

import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Füge das Verzeichnis src zum Python-Pfad hinzu
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from gamestate import GameState


class MoveLib:
    _coldict = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8}
    _bitColDict = {7: "A", 6: "B", 5: "C", 4: "D", 3: "E", 2: "F", 1: "G", 0: "H"}

    @classmethod
    def move(self, start, target, mode=1):
        """
        defines a move from position xy to zv

        Args:
            start (str or uint64): start Position e.g. "A4"
            target (str or uint64): target Position e.g. "A5"
            mode (int, optional):  
                0: str -> tupel(str,str), 
                1: str -> tupel(uint64,uint64)
                3: uint64 -> str 

        Returns:
            mode=0: (str,str): string tupel of start and target (for Tests & internal usage)
            mode=1: (uint64,uint64): Bitboard tupel of start and target
            mode=3: str: for communication with game server
        """
        if mode == 0:
            if (type(start) == str and type(target) == str):
                return start, target
            else:
                raise ValueError("start and target are not of type str")
        if mode == 1:
            if (type(start) == str and type(target) == str):
                # TODO convert string to bits
                return self.extractValueFromString(start) | GameState.BITBOARD, self.extractValueFromString(
                    target) | GameState.BITBOARD
            else:
                raise ValueError("start and target are not of type str")
        if mode == 3:
            if (type(start) == np.uint64 and type(target) == np.uint64):
                # TODO convert uint64 position to str value
                return self.BitsToPosition(start) + "-" + self.BitsToPosition(target)
            else:
                raise ValueError("start and target are not of type np.uint64")

    @classmethod
    def extractValueFromString(self, pos: str):
        """
        This function is used to convert a string to a bit value.
        Assuming msb bit order -> Position A0: last "row" in bit order

        Args:
            pos (str): A Position from the Board

        Returns:
            np.uint64: on failure 0, on success bit value
        """
        # todo
        emptyFields = {"A1", "H1", "A8", "H8"}
        if pos in emptyFields:
            return np.uint64(0)

        powValue = self.mapRowToPowValue(pos[1])
        addX = self.mapLetterToNumber(pos[0])

        if powValue == None or addX == None:
            return np.uint64(0)

        rowValue = 0

        if pos[1] == "1":
            rowValue = 8 - int(addX)
        else:
            rowValue = 8 - int(addX) + 1
        # runtime of Pow is garbage
        # completeValue = pow(2, powValue+ rowValue)
        completeValue = 1 << (powValue + rowValue)
        return np.uint64(completeValue)

    def mapRowToPowValue(rowNumber: str):
        """
        Abstraction of the Bitboard and containing only exponent values.
            3 | .. .. .. .. ... ... 
        e.g. 2 |15 14 13 12 11 10 9 8 
            1 | 7  6  5  4  3  2 1 0
            | ____________________
                A  B  C  D  E  F G H
        
        computation goal: "A2" has the value 2**15, so A2 =  7   + (8-1)+1 = 15 
                                                            "2"     "A"        
        Args:
            rowNumber (str): rowNumber of a Position

        Returns:
            int: value for a row, which needs to be added to compute the complete exponent. e.g. "2" -> 7
        """
        match rowNumber:
            case "1":
                return 0
            case "2":
                return 7
            case "3":
                return 15
            case "4":
                return 23
            case "5":
                return 31
            case "6":
                return 39
            case "7":
                return 47
            case "8":
                return 55
            case _:
                return None

    @classmethod
    def mapLetterToNumber(self, letter: str):
        """
        map the letters to column numbers

        Args:
            letter (str): from A to H

        Returns:
            int: column number
        """
        retVal = 0
        try:
            retVal = self._coldict[letter]
        except Exception as error:
            print("Error: ", type(error).__name__)
            return None

        # match letter:
        #     case "A": return 1
        #     case "B": return 2
        #     case "C": return 3
        #     case "D": return 4
        #     case "E": return 5
        #     case "F": return 6
        #     case "G": return 7
        #     case "H": return 8
        #     case _: return None 
        return retVal


    # @classmethod
    # def BitsToPosition(self, value: np.uint64):
    # # Convert np.uint64 to Python int and compute the position of the set bit
    #     pos = int(value).bit_length() - 1

    #     # Compute the row and column using bitwise operations
    #     row = (pos >> 3) + 1
    #     col = pos & 7

    #     # Convert the column to a letter
    #     retCol = self._bitColDict[col]

    #     return retCol + str(row)
    @classmethod
    def BitsToPosition(self, value: np.uint64):
        return self.bitPosDict[value]
    
    bitPosDict = {
        np.uint64(1):  "H1",
        np.uint64(2):  "G1",
        np.uint64(4):  "F1",
        np.uint64(8):  "E1",
        np.uint64(16): "D1",
        np.uint64(32): "C1",
        np.uint64(64): "B1",
        np.uint64(128):"A1",
        
        np.uint64(256):    "H2",
        np.uint64(512):    "G2",
        np.uint64(1024):   "F2",
        np.uint64(2048):   "E2",
        np.uint64(4096):   "D2",
        np.uint64(8192):   "C2",
        np.uint64(16384):  "B2",
        np.uint64(32768):  "A2",
        
        np.uint64(65536):      "H3",
        np.uint64(131072):     "G3",
        np.uint64(262144):     "F3",
        np.uint64(524288):     "E3",
        np.uint64(1048576):    "D3",
        np.uint64(2097152):    "C3",
        np.uint64(4194304):    "B3",
        np.uint64(8388608):    "A3",
        
        np.uint64(16777216):   "H4",
        np.uint64(33554432):   "G4",
        np.uint64(67108864):   "F4",
        np.uint64(134217728):  "E4",
        np.uint64(268435456):  "D4",
        np.uint64(536870912):  "C4",
        np.uint64(1073741824): "B4",
        np.uint64(2147483648): "A4",
        
        np.uint64(4294967296):     "H5",
        np.uint64(8589934592):     "G5",
        np.uint64(17179869184):    "F5",
        np.uint64(34359738368):    "E5",
        np.uint64(68719476736):    "D5",
        np.uint64(137438953472):   "C5",
        np.uint64(274877906944):   "B5",
        np.uint64(549755813888):   "A5",
        
        np.uint64(1099511627776):      "H6",
        np.uint64(2199023255552):      "G6",
        np.uint64(4398046511104):      "F6",
        np.uint64(8796093022208):      "E6",
        np.uint64(17592186044416):     "D6",
        np.uint64(35184372088832):     "C6",
        np.uint64(70368744177664):     "B6",
        np.uint64(140737488355328):    "A6",
        
        np.uint64(281474976710656):    "H7",
        np.uint64(562949953421312):    "G7",
        np.uint64(1125899906842624):   "F7",
        np.uint64(2251799813685248):   "E7",
        np.uint64(4503599627370496):   "D7",
        np.uint64(9007199254740992):   "C7",
        np.uint64(18014398509481984):  "B7",
        np.uint64(36028797018963968):  "A7",
        
        np.uint64(72057594037927936):      "H8",
        np.uint64(144115188075855872):     "G8",
        np.uint64(288230376151711744):     "F8",
        np.uint64(576460752303423488):     "E8",
        np.uint64(1152921504606846976):    "D8",
        np.uint64(2305843009213693952):    "C8",
        np.uint64(4611686018427387904):    "B8",
        np.uint64(9223372036854775808):    "A8",
    }