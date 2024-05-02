import numpy as np
from src.gamestate import GameState


class MoveLib:
    @classmethod
    def move(self,start: str, target: str, mode = 1):
        """
        defines a move from position xy to zv

        Args:
            start (str): start Position e.g. "A4"
            target (str): target Position e.g. "A5"
            mode (int, optional):  0 => string representation, 1 => bit (int64) representation.  
                Defaults to 0.

        Returns:
            mode=0: (str,str): string tupel of start and target (for Tests & internal usage)
            mode=1: (uint64,uint64): Bitboard tupel of start and target
            mode=3: str: for communication with game server
        """
        if mode == 0:
            return start,target
        if mode == 1:
            #Todo convert string to bits
            return self.extractValueFromString(start) | GameState.BITBOARD, self.extractValueFromString(target) | GameState.BITBOARD
        if mode == 3:
            return start + "-" + target
    @classmethod
    def extractValueFromString(self,pos: str):
        """
        This function is used to convert a string to a bit value.
        Assuming msb bit order -> Position A0: last "row" in bit order

        Args:
            pos (str): A Position from the Board

        Returns:
            np.uint64: on failure 0, on success bit value
        """
        #todo
        emptyFields = {"A1", "H1" , "A8" , "H8"}
        if pos in emptyFields:
            return np.uint64(0)
        
        powValue = self.mapRowToPowValue(pos[1])
        addX = self.mapLetterToNumber(pos[0])
        
        if powValue == None or addX == None:
            return np.uint64(0)
        
        rowValue = 0
        
        if pos[1] == "1":
            rowValue = 8-int(addX)
        else: 
            rowValue = 8-int(addX)+1
        # runtime of Pow is garbage
        #completeValue = pow(2, powValue+ rowValue)
        completeValue = 1 << (powValue+rowValue)
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
            case "1": return 0
            case "2": return 7
            case "3": return 15
            case "4": return 23
            case "5": return 31
            case "6": return 39
            case "7": return 47
            case "8": return 55
            case _: return None

    def mapLetterToNumber(letter:str):
        """
        map the letters to column numbers

        Args:
            letter (str): from A to H

        Returns:
            int: column number
        """
        match letter:
            case "A": return 1
            case "B": return 2
            case "C": return 3
            case "D": return 4
            case "E": return 5
            case "F": return 6
            case "G": return 7
            case "H": return 8
            case _: return None 
                